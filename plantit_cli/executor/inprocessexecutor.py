import traceback

from dagster import execute_pipeline_iterator, DagsterEventType

from plantit_cli.dagster.solids import *
from plantit_cli.exceptions import PlantitException
from plantit_cli.executor.executor import Executor
from plantit_cli.run import Run


class InProcessExecutor(Executor):

    name = "in-process"

    def __run_config(self, run: Run):
        return {
            'storage': {
                'filesystem': {
                    'config': {
                        'base_dir': run.workdir
                    }
                }
            },
            'loggers': {
                'console': {
                    'config': {
                        'log_level': 'INFO'
                    }
                }
            }
        }

    def execute(self, run: Run):
        update_status(run, 3, f"Starting run '{run.identifier}' with '{self.name}' executor.")
        try:
            if run.clone is not None and run.clone is not '':
                Executor.clone(run)

            if run.input:
                dagster_pipeline = Executor.input(run)
            else:
                dagster_pipeline = construct_pipeline_with_no_input(run)

            update_status(run, 3, f"Running '{run.image}' container(s).")
            for event in execute_pipeline_iterator(dagster_pipeline, run_config=self.__run_config(run)):
                if event.event_type is DagsterEventType.PIPELINE_INIT_FAILURE or event.is_pipeline_failure:
                    raise PlantitException(event.message)

            if run.output:
                Executor.output(run)
        except Exception:
            update_status(run, 2, f"Run '{run.identifier}' failed: {traceback.format_exc()}")
            return
