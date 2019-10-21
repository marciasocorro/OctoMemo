import click
from user import User


@click.group()
def cli():
    context = click.get_current_context()
    context.obj = {}
    login = ""
    password = ""
    memouser = User(login, password)
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
    user.create_note(filename, text)


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
