# -*- coding: utf-8 -*-
'''
    Git manipulation
'''
from __future__ import unicode_literals

import re

from git import GitCommandError, Repo

import git_app_version.helper.date as dthelper

RESERVED_KEYS = (
    'abbrev_commit',
    'author_date',
    'author_email',
    'author_name',
    'author_timestamp',
    'branches',
    'commit_date',
    'commit_timestamp',
    'committer_email',
    'committer_name',
    'deploy_date',
    'deploy_timestamp',
    'full_commit',
    'message',
    'top_branches',
    'version'
)


class GitHandler(object):
    '''
    Git
    '''

    def __init__(self, path):
        self.repo = Repo(path)

    def get_deploy_date(self):
        '''
        get current date
        '''

        return dthelper.utcnow()

    def get_version(self, commit='HEAD', default=''):
        '''
        get human readable version
        result of `git describe --tag --always`
        '''

        try:
            version = self.repo.git.describe(
                '--tag', '--always', commit).strip()
        except GitCommandError:
            version = ''

        if not version:
            version = default

        return version

    def get_branches(self, commit='HEAD'):
        '''
        get remote branches which commit belong
        result of `git branch --remote --no-color --contains=<commit>`
        '''

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
        '''
        get remote branches which commit belong and is the branch HEAD
        '''

        top_branch = []

        for branch in branches:
            if abbrev_commit == self.get_abbrev_commit(branch):
                top_branch.append(branch)

        return top_branch

    def remove_remote_prefix(self, branches):
        '''
        remove git remote prefix from branch name
        e.g.: origin/master = master
        '''
        regex_remote = re.compile(r'^[^/]+/')  # remove git remote prefix

        clean_branches = []
        for branch in branches:
            clean_branches.append(regex_remote.sub('', branch))

        return clean_branches

    def get_committer_name(self, commit='HEAD'):
        '''
        get git committer name
        '''

        return self.repo.commit(commit).committer.name

    def get_committer_email(self, commit='HEAD'):
        '''
        get git committer email
        '''

        return self.repo.commit(commit).committer.email

    def get_author_name(self, commit='HEAD'):
        '''
        get git author name
        '''

        return self.repo.commit(commit).author.name

    def get_author_email(self, commit='HEAD'):
        '''
        get git author email
        '''

        return self.repo.commit(commit).author.email

    def get_commit_date(self, commit='HEAD'):
        '''
        get git commit date
        '''

        return self.repo.commit(commit).committed_datetime

    def get_author_date(self, commit='HEAD'):
        '''
        get git authoring date
        '''

        return self.repo.commit(commit).authored_datetime

    def get_full_commit(self, commit='HEAD'):
        '''
        get git commit full SHA1 hash
        '''

        return self.repo.commit(commit).hexsha

    def get_abbrev_commit(self, commit='HEAD'):
        '''
        get git commit shorten SHA1 hash
        '''

        return self.repo.commit(commit).hexsha[0:7]

    def get_message(self, commit='HEAD'):
        '''
        get git commit message
        '''

        return self.repo.commit(commit).message.strip()

    def get_infos(self, commit='HEAD'):
        '''
        get all git commit data
        '''

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
            'message': self.get_message(commit),
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
