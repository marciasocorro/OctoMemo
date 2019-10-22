import os

AUTH_FILE = ".octo"


def auth_path():
    return os.path.join(os.environ.get("HOME"), AUTH_FILE)


def store_github_token(token):
    """Store Github token."""
    try:
        with os.fdopen(os.open(auth_path(), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as file:
            file.write(token)
        print("Sucess!.")
    except OSError:
        print("Unable to create token file.\n")


def get_github_token():
    """Return Github Token."""
    token = None
    try:
        with open(auth_path()) as file:
            token = file.read().strip()
    except IOError as e:
        print("Unable to read token file.\n")

    if not token:
        print("Unable to find github token.")
        raise SystemExit
    else:
        return token
