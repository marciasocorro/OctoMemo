# -*- coding: utf-8 -*-
from unittest import TestCase, mock
from unittest.mock import Mock

from pytest import fixture
from github import GithubException

from scripts.user import User


class TestUser(TestCase):
    @fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    def setUp(self):
        TestCase.setUp(self)

    @mock.patch("github.Github.get_user")
    def test_list_all_notes(self, mock_get_user: mock.Mock):
        token = "token"
        expected_file_name = "code_file.txt"
        mock_repo = self.get_mocked_github_repo(expected_file_name)
        mock_github = Mock()
        mock_github.get_repo.return_value = mock_repo
        mock_get_user.return_value = mock_github

        user = User(token)
        user.list_all_notes()

        captured = self.capsys.readouterr()
        self.assertTrue("Available notes:" in captured.out)
        self.assertTrue(expected_file_name in captured.out)
        mock_github.get_repo.assert_called_with("octobook")
        mock_repo.get_dir_contents.assert_called_with("")

    @mock.patch("github.Github.get_user")
    def test_repo_creation(self, mock_get_user: mock.Mock):
        mock_github = Mock()

        mock_github.get_repo.side_effect = GithubException(404, {"message": "Not Found"})
        mock_github.create_repo.return_value = self.get_mocked_github_repo("")
        mock_get_user.return_value = mock_github

        token = "token"
        user = User(token)

        mock_github.get_repo.assert_called_with("octobook")
        mock_github.create_repo.assert_called_once()
        mock_github.create_repo.assert_called_with("octobook", private=True)

        mock_get_user.return_value = mock_github

    def get_mocked_github_repo(self, expected_file_name):
        mock_file = Mock()
        mock_file.name = expected_file_name
        mock_repo = Mock()
        mock_repo.get_dir_contents.return_value = [mock_file]
        return mock_repo
