import click
from user import User
from file_management import get_github_token


@click.group()
def cli():
    context = click.get_current_context()
    context.obj = {}
    token = get_github_token()
    memouser = User(token)
    context.obj["memouser"] = memouser


@cli.command()
@click.pass_context
def lnote(context):
    user = context.obj[u"memouser"]
    user.list_all_notes()


@cli.command()
@click.pass_context
def cnote(context):
    user = context.obj[u"memouser"]
    filename = input("filename:")
    text = input("text:")
    user.create_note(filename, content=text)


@cli.command()
@click.pass_context
def dnote(context):
    user = context.obj[u"memouser"]
    filename = filename = input("filename:")
    user.delete_note(filename)


@cli.command()
@click.pass_context
def enote(context):
    user = context.obj[u"memouser"]
    filename = input("filename:")
    user.edit_note(filename)


if __name__ == "__main__":
    cli()
