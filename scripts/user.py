from github import Github
import base64
import os


class User:
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self.auth = Github(login, password)

    def create_repo(self):
        """Method to create a repository for notes."""
        self.auth.get_user().create_repo("octomemo_" + self._login, private=True)

    def list_all_notes(self):
        """Method to list all notes in a github repository."""
        repo = self.auth.get_user().get_repo("octomemo_" + self._login)
        print("Available notes:")
        for file in repo.get_dir_contents(""):
            print(file.name)

    def create_note(self, name, message="none", content=""):
        """Method to create a note in a github repository.

        :param str name: Note name
        :param str message: Commit message
        :param str content: Note content
        """
        repo = self.auth.get_user().get_repo("octomemo_" + self._login)
        repo.create_file(name, message, content)

    def delete_note(self, name, message="deleting file"):
        """Method to delete a note in a github repository.

        :param str name: Name of note to be deleted
        :param str message: Commit message
        """
        repo = self.auth.get_user().get_repo("octomemo_" + self._login)
        sha = repo.get_contents(name).sha
        repo.delete_file(name, message, sha)

    def edit_note(self, name):
        """Method to edit a note in a github repository.

        :param str name: Name of note to be deleted
        """
        repo = self.auth.get_user().get_repo("octomemo_" + self._login)
        file = repo.get_contents(name)
        text = base64.b64decode(file.content).decode("utf-8")
        f = open(name, "w+")
        f.write(text)
        f.close()
        myCmd = "nano " + name
        os.system(myCmd)
        sha = repo.get_contents(name).sha
        f = open(name, "r")
        contents = f.read()
        repo.update_file(name, "none", contents, sha)
