# -*- coding: utf-8 -*-
from unittest import TestCase, mock
from unittest.mock import Mock

from pytest import fixture

from scripts.user import User


class TestUser(TestCase):
    @fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    def setUp(self):
        TestCase.setUp(self)

    def test_create_repo(self):
        self.assertTrue(True)

    @mock.patch('github.Github.get_user')
    def test_list_all_notes(self, mock_get_user: mock.Mock):
        user = User("login", "password")
        expected_file_name = "code_file.txt"
        mock_repo = self.get_mocked_github_repo(expected_file_name)
        mock_github = Mock()
        mock_github.get_repo.return_value = mock_repo
        mock_get_user.return_value = mock_github

        user.list_all_notes()

        captured = self.capsys.readouterr()
        self.assertTrue("Available notes:" in captured.out)
        self.assertTrue(expected_file_name in captured.out)

    def get_mocked_github_repo(self, expected_file_name):
        mock_file = Mock()
        mock_file.name = expected_file_name
        mock_repo = Mock()
        mock_repo.get_dir_contents.return_value = [mock_file]
        return mock_repo
