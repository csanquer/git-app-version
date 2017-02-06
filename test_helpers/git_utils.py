# -*- coding: utf-8 -*-
"""
    Git fixtures helpers
"""

import os

from git import Repo

def commit(repo, message, author=None, date=None):
    cwd = os.getcwd()

    os.chdir(repo.working_dir)

    # need to do a manual commit to allow empty message and set committer date
    cmd = 'git commit --allow-empty -m "{}"'.format(message)
    if author:
        cmd = cmd+' --author="{}"'.format(author)

    if date:
        cmd = 'GIT_COMMITTER_DATE="{}" '.format(date)+cmd+' --date="{}"'.format(date)

    os.system(cmd)
    os.chdir(cwd)

    return repo.commit('HEAD')

def tag(repo, version, author=None, date=None):
    commit_obj = commit(repo=repo, message="release: {}".format(version), author=author, date=date)
    repo.create_tag(path=version, message=version)

    return commit_obj

def branch(repo, name, start='HEAD'):
    return repo.create_head(name, commit=start)

def clone(remote_repo, path):
    return remote_repo.clone(path)

def init(email='user@example.com', username='User Test', repo_dir=None):
    cwd = os.getcwd()
    if not repo_dir or not os.path.exists(repo_dir):
        repo_dir = cwd

    os.chdir(repo_dir)

    repo = Repo.init(repo_dir)

    # git config
    with repo.config_writer() as cfg:
        cfg.add_section('user')
        cfg.set('user', 'email', email)
        cfg.set('user', 'name', username)

        cfg.release()

    os.chdir(cwd)

    return repo

def default_init(version='0.1.2',
                 email='user@example.com', username='User Test',
                 author='User Test <user@example.com>',
                 date='2016-11-20T12:41:30+0000',
                 tag_date='2016-11-20T12:42:30+0000', repo_dir=None):
    repo = init(email=email, username=username, repo_dir=repo_dir)
    commit(repo=repo, message='initial commit', author=author, date=date)
    tag(repo=repo, version=version, author=author, date=tag_date)

    return repo
