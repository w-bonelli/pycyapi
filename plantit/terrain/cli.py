import click

from plantit.cli import cli
import plantit.terrain.commands as commands


@cli.group()
def terrain():
    pass


@terrain.command()
@click.option("--username", required=True, type=str)
@click.option("--password", required=True, type=str)
def token(username, password):
    click.echo(commands.cas_token(username=username, password=password))


@terrain.command()
@click.argument("username")
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def user(username, token, timeout):
    click.echo(commands.user_info(username=username, token=token, timeout=timeout))


@terrain.command()
@click.argument("remote_path")
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def list(remote_path, token, timeout):
    click.echo(commands.paged_directory(path=remote_path, token=token, timeout=timeout))


@terrain.command()
@click.argument("remote_path")
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def stat(remote_path, token, timeout):
    click.echo(commands.stat(path=remote_path, token=token, timeout=timeout))


@terrain.command()
@click.argument("remote_path")
@click.option("--type", required=False, type=str)
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def exists(remote_path, type, token, timeout):
    click.echo(
        commands.exists(path=remote_path, type=type, token=token, timeout=timeout)
    )


@terrain.command()
@click.argument("remote_path")
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def create(remote_path, token, timeout):
    click.echo(commands.create(path=remote_path, token=token, timeout=timeout))


@terrain.command()
@click.argument("remote_path")
@click.option("--local_path", "-p", required=False, type=str)
@click.option("--include_pattern", "-ip", required=False, type=str, multiple=True)
@click.option("--force", "-f", required=False, type=str, multiple=True)
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def download(remote_path, local_path, include_pattern, force, token, timeout):
    commands.download(
        remote_path=remote_path,
        local_path=local_path,
        patterns=include_pattern,
        force=force,
        token=token,
        timeout=timeout,
    )
    click.echo(f"Downloaded {remote_path} to {local_path}")


@terrain.command()
@click.argument("remote_path")
@click.option("--local_path", "-p", required=False, type=str)
@click.option("--include_pattern", "-ip", required=False, type=str, multiple=True)
@click.option("--include_name", "-in", required=False, type=str, multiple=True)
@click.option("--exclude_pattern", "-ep", required=False, type=str, multiple=True)
@click.option("--exclude_name", "-en", required=False, type=str, multiple=True)
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def upload(
    remote_path,
    local_path,
    include_pattern,
    include_name,
    exclude_pattern,
    exclude_name,
    token,
    timeout,
):
    commands.upload(
        local_path=local_path,
        remote_path=remote_path,
        include_patterns=include_pattern,
        include_names=include_name,
        exclude_patterns=exclude_pattern,
        exclude_names=exclude_name,
        token=token,
        timeout=timeout,
    )
    click.echo(f"Uploaded {local_path} to {remote_path}")


@terrain.command()
@click.argument("remote_path")
@click.option("--username", "-u", required=True, type=str)
@click.option("--permission", "-p", required=True, type=str)
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def share(remote_path, username, permission, token, timeout):
    commands.share(
        username=username,
        path=remote_path,
        permission=permission,
        token=token,
        timeout=timeout,
    )
    click.echo(f"Shared {remote_path} with {username}")


@terrain.command()
@click.argument("remote_path")
@click.option("--username", "-u", required=True, type=str, multiple=True)
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def unshare(remote_path, username, token, timeout):
    commands.unshare(username=username, path=remote_path, token=token, timeout=timeout)
    click.echo(f"Unshared {remote_path} with {username}")


@terrain.command()
@click.argument("id")
@click.option("--attribute", "-a", required=False, type=str, multiple=True)
@click.option("--irods_attribute", "-ia", required=False, type=str, multiple=True)
@click.option("--token", "-t", required=False, type=str)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def tag(id, attribute, irods_attribute, token, timeout):
    commands.tag(
        id=id,
        attributes=attribute,
        irods_attributes=irods_attribute,
        token=token,
        timeout=timeout,
    )
    newline = "\n"
    click.echo(
        f"Tagged data object with ID {id}:\nRegular:\n{newline.join(attribute)}\niRODS:\n{newline.join(irods_attribute)}"
    )


@terrain.command()
@click.argument("id")
@click.option("--token", "-t", required=False, type=str)
@click.option("--irods", "-i", required=False, default=False, type=bool)
@click.option("--timeout", "-to", required=False, type=int, default=15)
def tags(id, irods, token, timeout):
    attributes = commands.tags(id=id, irods=irods, token=token, timeout=timeout)
    newline = "\n"
    click.echo(newline.join(attributes))
