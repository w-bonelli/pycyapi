"""
    Communication with the server
"""
import time
import json
import requests

class Comms:
    '''
        Base class for communications.

        Comms classes handle passing information about the job progress back
        to the web server.
    '''
    #Possible Status States
    OK = 3
    WARN = 4
    FAILED = 2

    def update_status(self,status,description):
        """
            Update job status.

            Args:
                status (int): Status State. Must be one of (Comms.OK,
                Comms.WARN, or COMMS.FAIL)
                url (str): url for server REST API
                description (str): Status description string. Descriptions
                    greater than 150 characters are truncated to
                    last 150 characters
        """
        pass

    def update_job(self,props):
        """
            Update job properties

            Args:
                props (dict): properties to update
        """
        pass

    def task_complete(self, task_pk):
        """
            Mark job task as complete.

            Args:
                task_pk (int): pk of task to mark as complete
        """
        pass

    def update_task(self, task_pk):
        """
            Update task properties

            Args:
                task_pk (int): pk of task to mark as complete
                props (dict): properties to update
        """
        pass

class STDOUTComms(Comms):
    '''
        Prints all server communication to the command line.

        Does not actually connect to a server for communication, used for
        testing, see tests/test.py for an example.
    '''
    def status_str(self,status):
        if status == self.OK:
            return "OK"
        elif status == self.WARN:
            return "WARNING"
        elif status == self.FAILED:
            return "FAILED"

    def update_status(self,status,description):
        print("Status (%s): %s"%(self.status_str(status),description))

    def update_job(self,props):
        print("Job updated with: %s"%(props,))

    def task_complete(self, task_pk):
        print("Task %s complete"%(task_pk))

    def update_task(self,task_pk,props):
        print("Task %s updated with: %s"%(task_pk,props))

class RESTComms(Comms):
    """
        Handles communication with the web server via calls to the REST API
    """

    def __init__(self, url, job_pk, headers=None):
        '''
            Args:
                url (str): The base url for the plant it REST API
                    (<hostname>/apis/v1/ in the default Plant IT configuration)
                job_pk (int): pk of the Plant IT job that started clusterside.
                headers (dict): Headers to include in communction with REST API.
                    see `[headers]<https://2.python-requests.org/en/master/user/quickstart/#custom-headers>`_
                    for details.
        '''
        self.url = url + "jobs/%d/"%(job_pk,)

        if headers is None:
            self.headers = {}
        else:
            self.headers = headers
        self.headers["Content-Type"] = "application/json"

    def update_job(self,props):
        patch = json.dumps(props)

        response = requests.patch(self.url,
                                  patch,
                                  headers=self.headers)

        response.raise_for_status()

    def update_status(self, status, description):
        if len(description) > 150:
            description = description[-150:] + "..."

        msg ={
                "status_set": [
                    {
                        "state": status,
                        "date": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "description": description
                    }
                ]
            }

        self.update_job(msg)

    def update_task(self, task_pk, props):
        msg = { "task_set": [
                        {
                            "pk": task_pk,
                        }
                    ]
               }

        for prop,value in props.items():
            msg['task_set'][0][prop] = value

        patch = json.dumps(msg)

        response = requests.patch(self.url,
                                  patch,
                                  headers=self.headers)

        response.raise_for_status()

    def task_complete(self, task_pk):
        self.update_task(task_pk,{"complete": "true"})
