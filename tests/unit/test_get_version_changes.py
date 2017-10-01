#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from unittest import mock

from gitlab_changelog import get_version_changes


class TestGetVersionChanges(unittest.TestCase):
    """This class tests the get_version_changes method"""

    @mock.patch('gitlab_changelog.get_merge_request_changes', return_value=['changes'])
    @mock.patch('gitlab_changelog.get_commit_changes')
    def test_has_merge_request_changes_must_not_call_get_commit_changes(self, mock_get_merge_request_changes, mock_get_commit_changes):
        self.assertFalse(mock_get_commit_changes.called, get_version_changes('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha'))

    @mock.patch('gitlab_changelog.get_merge_request_changes', return_value=['changes'])
    def test_has_merge_request_changes_must_call_get_merge_request_changes(self, mock_get_merge_request_changes):
        actual = get_version_changes('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')
        mock_get_merge_request_changes.assert_called_once_with('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')

    @mock.patch('gitlab_changelog.get_merge_request_changes', return_value=['changes'])
    def test_has_merge_request_changes_must_return_merge_request_changes(self, mock_get_merge_request_changes):
        actual = get_version_changes('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')
        self.assertEqual(actual, ['changes'])

    @mock.patch('gitlab_changelog.get_merge_request_changes', return_value=[])
    @mock.patch('gitlab_changelog.get_commit_changes', return_value=['changes'])
    def test_does_not_have_merge_request_changes_must_call_get_commit_changes(self, mock_get_merge_request_changes, mock_get_commit_changes):
        actual = get_version_changes('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')
        mock_get_commit_changes.assert_called_once_with('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')

    @mock.patch('gitlab_changelog.get_merge_request_changes', return_value=[])
    @mock.patch('gitlab_changelog.get_commit_changes', return_value=['changes'])
    def test_does_not_have_merge_request_changes_must_return_commit_changes(self, mock_get_merge_request_changes, mock_get_commit_changes):
        actual = get_version_changes('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')
        self.assertEqual(actual, ['changes'])

    @mock.patch('gitlab_changelog.get_merge_request_changes', return_value=[])
    @mock.patch('gitlab_changelog.get_commit_changes', return_value=[])
    def test_does_not_have_commit_changes_must_return_empty_list(self, mock_get_merge_request_changes, mock_get_commit_changes):
        actual = get_version_changes('https://gitlab.com/api/v4', 'gitlab_token', 'project_id', 'commit_sha')
        self.assertEqual(actual, [])


if __name__ == '__main__':
    unittest.main()
