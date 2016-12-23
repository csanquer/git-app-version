# -*- coding: utf-8 -*-
"""
    Git manipulation
"""
import re
from git_app_version.helper.process import output_command, call_command
import git_app_version.helper.date as datehelper


class Git(object):

    def is_git_repo(self, cwd=None):
        return call_command(["git", "rev-parse"], cwd=cwd) == 0

    def get_deploy_date(self):
        return datehelper.utcnow()

    def get_version(self, commit='HEAD', default=None, cwd=None):
        version = output_command(
            ["git", "describe", "--tag", "--always", commit], cwd=cwd).strip()
        if version == '' or version is None:
            if not default:
                default = self.get_abbrev_commit(commit, cwd=cwd)

            version = default

        return version

    def get_branches(self, commit='HEAD', cwd=None):
        raw_branches = output_command(["git",
                                       "branch",
                                       "--no-color",
                                       "--remote",
                                       "--contains=" + commit],
                                      cwd=cwd).splitlines()

        regex_point = re.compile(r'->')  # remove git reference pointing

        branches = []
        for raw_branch in raw_branches:
            branch = raw_branch.strip()
            match = regex_point.search(branch)
            if not match:
                branches.append(branch)

        return branches

    def get_top_branches(self, branches, abbrev_commit=None, cwd=None):
        top_branch = []

        for branch in branches:
            if abbrev_commit == self.get_abbrev_commit(branch, cwd=cwd):
                top_branch.append(branch)

        return top_branch

    def remove_remote_prefix(self, branches):
        regex_remote = re.compile(r'^[^/]+/')  # remove git remote prefix

        clean_branches = []
        for branch in branches:
            clean_branches.append(regex_remote.sub('', branch))

        return clean_branches

    def get_committer_name(self, commit='HEAD', cwd=None):
        return self._get_log_field(field='cn', commit=commit, cwd=cwd)

    def get_committer_email(self, commit='HEAD', cwd=None):
        return self._get_log_field(field='ce', commit=commit, cwd=cwd)

    def get_author_name(self, commit='HEAD', cwd=None):
        return self._get_log_field(field='an', commit=commit, cwd=cwd)

    def get_author_email(self, commit='HEAD', cwd=None):
        return self._get_log_field(field='ae', commit=commit, cwd=cwd)

    def _get_log_field(self, field, commit='HEAD', cwd=None):
        return output_command(["git",
                               "log",
                               "-1",
                               "--pretty=tformat:%" + field,
                               "--no-color",
                               commit],
                              cwd=cwd).strip()

    def get_commit_date(self, commit='HEAD', cwd=None):
        return self._get_date(field='ci', commit=commit, cwd=cwd)

    def get_author_date(self, commit='HEAD', cwd=None):
        return self._get_date(field='ai', commit=commit, cwd=cwd)

    def _get_date(self, field, commit='HEAD', cwd=None):
        isodate = output_command(["git",
                                  "log",
                                  "-1",
                                  "--pretty=tformat:%" + field,
                                  "--no-color",
                                  "--date=local",
                                  commit],
                                 cwd=cwd).strip().replace(' ',
                                                          'T',
                                                          1).replace(' ',
                                                                     '')

        return datehelper.datetime_from_iso8601(isodate, utc=True)

    def get_full_commit(self, commit='HEAD', cwd=None):
        return output_command(["git",
                               "rev-list",
                               "--max-count=1",
                               "--no-abbrev-commit",
                               commit],
                              cwd=cwd).strip()

    def get_abbrev_commit(self, commit='HEAD', cwd=None):
        return output_command(["git",
                               "rev-list",
                               "--max-count=1",
                               "--abbrev-commit",
                               commit],
                              cwd=cwd).strip()

    def get_infos(self, commit='HEAD', cwd=None):
        deploy_date = self.get_deploy_date()
        abbrev_commit = self.get_abbrev_commit(commit, cwd=cwd)
        commit_date = self.get_commit_date(commit, cwd=cwd)
        author_date = self.get_author_date(commit, cwd=cwd)

        branches = self.get_branches(commit, cwd=cwd)
        top_branch = self.get_top_branches(
            branches=branches, abbrev_commit=abbrev_commit, cwd=cwd)

        return {
            'branches': self.remove_remote_prefix(branches),
            'top_branches': self.remove_remote_prefix(top_branch),
            'version': self.get_version(commit, default=abbrev_commit, cwd=cwd),
            'abbrev_commit': abbrev_commit,
            'full_commit': self.get_full_commit(commit, cwd=cwd),
            'author_name': self.get_author_name(commit, cwd=cwd),
            'author_email': self.get_author_email(commit, cwd=cwd),
            'committer_name': self.get_committer_name(commit, cwd=cwd),
            'committer_email': self.get_committer_email(commit, cwd=cwd),
            'commit_date': datehelper.iso8601_from_datetime(commit_date),
            'commit_timestamp': datehelper.timestamp_from_datetime(commit_date),
            'author_date': datehelper.iso8601_from_datetime(author_date),
            'author_timestamp': datehelper.timestamp_from_datetime(author_date),
            'deploy_date': datehelper.iso8601_from_datetime(deploy_date),
            'deploy_timestamp': datehelper.timestamp_from_datetime(deploy_date),
        }
