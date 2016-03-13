# -*- coding: utf-8 -*-

# from pprint import pprint,pformat
from git_app_version.helper.process import outputCommand, callCommand
import git_app_version.helper.date as datehelper

class Git(object):
    def isGitRepository(self, cwd=None):
        return callCommand(["git", "rev-parse"], cwd=cwd) == 0

    def getDeployDate(self):
        return datehelper.utcnow()

    def getVersion(self, commit = 'HEAD', cwd=None):
        version = outputCommand(["git", "describe", "--tag", "--always", commit], cwd=cwd).strip()
        if version == '' or version is None:
            version = self.getAbbrevCommit(commit)

        return version

    def getCommitDate(self, commit = 'HEAD', cwd=None):
        isodate = outputCommand(["git", "log", "-1", "--pretty=tformat:%ci", "--no-color", "--date=local", commit], cwd=cwd).strip().replace(' ', 'T', 1).replace(' ', '')
        try:
            return datehelper.dateTimeFromIso8601(isodate, utc=True)
        except Exception as exc:
            return None

    def getFullCommit(self, commit = 'HEAD', cwd=None):
        return outputCommand(["git", "rev-list", "--max-count=1", "--no-abbrev-commit", commit], cwd=cwd).strip()

    def getAbbrevCommit(self, commit = 'HEAD', cwd=None):
        return outputCommand(["git", "rev-list", "--max-count=1", "--abbrev-commit", commit], cwd=cwd).strip()

    def getInfos(self, commit = 'HEAD', cwd=None):
        deployDate = self.getDeployDate()
        commitDate = self.getCommitDate(commit, cwd=cwd)

        return {
            'version': self.getVersion(commit, cwd=cwd),
            'abbrev_commit': self.getAbbrevCommit(commit, cwd=cwd),
            'full_commit': self.getFullCommit(commit, cwd=cwd),
            'commit_date': datehelper.iso8601FromDateTime(commitDate),
            'commit_timestamp': datehelper.timestampFromDateTime(commitDate),
            'deploy_date': datehelper.iso8601FromDateTime(deployDate),
            'deploy_timestamp': datehelper.timestampFromDateTime(deployDate),
        }
