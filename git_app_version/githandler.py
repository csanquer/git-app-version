# -*- coding: utf-8 -*-
"""
    Git manipulation
"""
import re

from git import GitCommandError, Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError

import git_app_version.helper.date as dthelper


class GitHandler(object):

    def __init__(self, path):
        try:
            self.repo = Repo(path)
        except (InvalidGitRepositoryError, NoSuchPathError):
            raise ValueError(
                'The directory \'{}\' is not a git repository.'.format(path))

    def get_deploy_date(self):
        return dthelper.utcnow()

    def get_version(self, commit='HEAD', default=''):
        try:
            version = self.repo.git.describe(
                '--tag', '--always', commit).strip()
        except GitCommandError:
            version = ''

        if not version:
            version = default

        return version

    def get_branches(self, commit='HEAD'):
        raw = self.repo.git.branch("--no-color",
                                   "--remote",
                                   "--contains=" + commit)
        raw_branches = raw.splitlines()

        regex_point = re.compile(r'->')  # remove git reference pointing

        branches = []
        for raw_branch in raw_branches:
            branch = raw_branch.strip()
            match = regex_point.search(branch)
            if not match:
                branches.append(branch)

        return branches

    def get_top_branches(self, branches, abbrev_commit=None):
        top_branch = []

        for branch in branches:
            if abbrev_commit == self.get_abbrev_commit(branch):
                top_branch.append(branch)

        return top_branch

    def remove_remote_prefix(self, branches):
        regex_remote = re.compile(r'^[^/]+/')  # remove git remote prefix

        clean_branches = []
        for branch in branches:
            clean_branches.append(regex_remote.sub('', branch))

        return clean_branches

    def get_committer_name(self, commit='HEAD'):
        return self.repo.commit(commit).committer.name

    def get_committer_email(self, commit='HEAD'):
        return self.repo.commit(commit).committer.email

    def get_author_name(self, commit='HEAD'):
        return self.repo.commit(commit).author.name

    def get_author_email(self, commit='HEAD'):
        return self.repo.commit(commit).author.email

    def get_commit_date(self, commit='HEAD'):
        return self.repo.commit(commit).committed_datetime

    def get_author_date(self, commit='HEAD'):
        return self.repo.commit(commit).authored_datetime

    def get_full_commit(self, commit='HEAD'):
        return self.repo.commit(commit).hexsha

    def get_abbrev_commit(self, commit='HEAD'):
        return self.repo.commit(commit).hexsha[0:7]

    def get_infos(self, commit='HEAD'):
        deploy_date = self.get_deploy_date()
        abbrev_commit = self.get_abbrev_commit(commit)
        commit_date = self.get_commit_date(commit)
        author_date = self.get_author_date(commit)

        branches = self.get_branches(commit)
        top_branch = self.get_top_branches(
            branches=branches, abbrev_commit=abbrev_commit)

        return {
            'branches': self.remove_remote_prefix(branches),
            'top_branches': self.remove_remote_prefix(top_branch),
            'version': self.get_version(commit, default=abbrev_commit),
            'abbrev_commit': abbrev_commit,
            'full_commit': self.get_full_commit(commit),
            'author_name': self.get_author_name(commit),
            'author_email': self.get_author_email(commit),
            'committer_name': self.get_committer_name(commit),
            'committer_email': self.get_committer_email(commit),
            'commit_date': dthelper.iso8601_from_datetime(commit_date),
            'commit_timestamp': dthelper.timestamp_from_datetime(commit_date),
            'author_date': dthelper.iso8601_from_datetime(author_date),
            'author_timestamp': dthelper.timestamp_from_datetime(author_date),
            'deploy_date': dthelper.iso8601_from_datetime(deploy_date),
            'deploy_timestamp': dthelper.timestamp_from_datetime(deploy_date),
        }
