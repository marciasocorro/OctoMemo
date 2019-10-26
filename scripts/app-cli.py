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
@click.option("--content", default="", help="text content")
@click.pass_context
@click.argument("file_name")
def cnote(context, file_name, content):
    user = context.obj[u"memouser"]
    file_name = file_name
    text_content = content
    user.create_note(file_name, content=text_content)


@cli.command()
@click.pass_context
@click.argument("file_name")
def dnote(context, file_name):
    user = context.obj[u"memouser"]
    file_name = file_name
    user.delete_note(file_name)


@cli.command()
@click.pass_context
def enote(context):
    user = context.obj[u"memouser"]
    filename = input("filename:")
    user.edit_note(filename)


if __name__ == "__main__":
    cli()
