from github import Github, GithubException
import base64
import os

class User:
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self.auth = Github(login, password)
        self.repo = self.get_repo()

    def create_repo(self):
        """Method to create a repository for notes."""
        return self.auth.get_user().create_repo("octomemo_" + self._login, private=True)

    def get_repo(self):
        """ Gets the repo if exists, create it if not """
        repo_name = self._login

        if '@' in repo_name:
            repo_name = repo_name.replace('@', '-')

        try:
            repo = self.auth.get_user().get_repo("octomemo_" + repo_name)
            return repo
        except GithubException as error:
            if error.data.get('message') == 'Not Found':
                return self.create_repo()
            raise

    def list_all_notes(self):
        """Method to list all notes in a github repository."""
        print("Available notes:")
        try:
            for file in self.repo.get_dir_contents(""):
                print(file.name)
        except GithubException as error:
           print(error.data.get('message'))

    def create_note(self, name, message="none", content=""):
        """Method to create a note in a github repository.

        :param str name: Note name
        :param str message: Commit message
        :param str content: Note content
        """
        self.repo.create_file(name, message, content)

    def delete_note(self, name, message="deleting file"):
        """Method to delete a note in a github repository.

        :param str name: Name of note to be deleted
        :param str message: Commit message
        """
        sha = self.repo.get_contents(name).sha
        repo.delete_file(name, message, sha)

    def edit_note(self, name):
        """Method to edit a note in a github repository.

        :param str name: Name of note to be deleted
        """
        file = self.repo.get_contents(name)
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
