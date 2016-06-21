# -*- coding: utf-8 -*-

from git_app_version.helper.process import outputCommand, callCommand
import git_app_version.helper.date as datehelper
import re

class Git(object):
    def isGitRepository(self, cwd=None):
        return callCommand(["git", "rev-parse"], cwd=cwd) == 0

    def getDeployDate(self):
        return datehelper.utcnow()

    def getVersion(self, commit = 'HEAD', default=None, cwd=None):
        version = outputCommand(["git", "describe", "--tag", "--always", commit], cwd=cwd).strip()
        if version == '' or version is None:
            if not default:
                 default = self.getAbbrevCommit(commit, cwd=cwd)

            version = default

        return version

    def getBranches(self, commit = 'HEAD', cwd=None):
        rawBranches = outputCommand(["git", "branch", "--no-color", "--remote","--contains="+commit], cwd=cwd).splitlines()

        regexPoint = re.compile(r'->') # remove git reference pointing

        branches = []
        for rawBranch in rawBranches:
            branch = rawBranch.strip()
            match = regexPoint.search(branch)
            if not match :
                branches.append(branch)

        return branches

    def getTopBranches(self, branches = [], abbrevCommit = None, cwd=None):
        topBranches = []
        for branch in branches :
            if abbrevCommit == self.getAbbrevCommit(branch, cwd=cwd):
                topBranches.append(branch)

        return topBranches

    def removeRemotePrefix(self, branches):
        regexRemote = re.compile(r'^[^/]+/') # remove git remote prefix

        cleanBranches = []
        for branch in branches :
            cleanBranches.append(regexRemote.sub('', branch))

        return cleanBranches

    def getCommitterName(self, commit = 'HEAD', cwd=None):
        return self._getLogField(field='cn', commit=commit, cwd=cwd)

    def getCommitterEmail(self, commit = 'HEAD', cwd=None):
        return self._getLogField(field='ce', commit=commit, cwd=cwd)

    def getAuthorName(self, commit = 'HEAD', cwd=None):
        return self._getLogField(field='an', commit=commit, cwd=cwd)

    def getAuthorEmail(self, commit = 'HEAD', cwd=None):
        return self._getLogField(field='ae', commit=commit, cwd=cwd)

    def _getLogField(self, field, commit = 'HEAD', cwd=None):
        return outputCommand(["git", "log", "-1", "--pretty=tformat:%"+field, "--no-color", commit], cwd=cwd).strip()

    def getCommitDate(self, commit = 'HEAD', cwd=None):
        return self._getDate(field='ci', commit=commit, cwd=cwd)

    def getAuthorDate(self, commit = 'HEAD', cwd=None):
        return self._getDate(field='ai', commit=commit, cwd=cwd)

    def _getDate(self, field, commit = 'HEAD', cwd=None):
        isodate = outputCommand(["git", "log", "-1", "--pretty=tformat:%"+field, "--no-color", "--date=local", commit], cwd=cwd).strip().replace(' ', 'T', 1).replace(' ', '')
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
        abbrevCommit = self.getAbbrevCommit(commit, cwd=cwd)
        commitDate = self.getCommitDate(commit, cwd=cwd)
        authorDate = self.getAuthorDate(commit, cwd=cwd)

        branches = self.getBranches(commit, cwd=cwd)
        topBranches = self.getTopBranches(branches=branches, abbrevCommit=abbrevCommit, cwd=cwd)

        return {
            'branches': self.removeRemotePrefix(branches),
            'top_branches': self.removeRemotePrefix(topBranches),
            'version': self.getVersion(commit, default=abbrevCommit, cwd=cwd),
            'abbrev_commit': abbrevCommit,
            'full_commit': self.getFullCommit(commit, cwd=cwd),
            'author_name': self.getAuthorName(commit, cwd=cwd),
            'author_email': self.getAuthorEmail(commit, cwd=cwd),
            'committer_name': self.getCommitterName(commit, cwd=cwd),
            'committer_email': self.getCommitterEmail(commit, cwd=cwd),
            'commit_date': datehelper.iso8601FromDateTime(commitDate),
            'commit_timestamp': datehelper.timestampFromDateTime(commitDate),
            'author_date': datehelper.iso8601FromDateTime(authorDate),
            'author_timestamp': datehelper.timestampFromDateTime(authorDate),
            'deploy_date': datehelper.iso8601FromDateTime(deployDate),
            'deploy_timestamp': datehelper.timestampFromDateTime(deployDate),
        }
