# -*- coding: utf-8 -*-
'''
    Main module
'''
import os

import click
from tabulate import tabulate

import git_app_version.version
from git_app_version.dumper import FileDumper
from git_app_version.githandler import GitHandler

__version__ = git_app_version.version.__version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('git-app-version ' + __version__)
    ctx.exit()


CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-V', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
# @click.option('--verbose', '-v', count=True)
@click.option('--quiet', '-q', is_flag=True, help='silent mode')
@click.option('--output', '-o', default='version',
              help='output file path (without extension).'
              ' Default is \'<repository-path>/version\'.')
@click.option('--format', '-f', 'output_formats',
              type=click.Choice(['json', 'yml', 'xml', 'ini']),
              multiple=True, default=['json'],
              help='output file format and extension, Default is json.')
@click.option('--namespace', '-n', default='',
              help='namespace like notation in version file, use dot separator'
              ' to segment namespaces e.g.: \'foo.bar.git\'.'
              ' Default is \'app_version\' for XML and INI'
              ' and no namespace for JSON and YAML.')
@click.argument('repository', type=click.Path(
    exists=True, resolve_path=True, file_okay=False, readable=True),
    default=os.getcwd())
@click.argument('commit', default='HEAD')
@click.pass_context
def dump(ctx, repository, commit, output, output_formats, namespace, quiet):
    '''
    Get Git commit informations and store them in a INI/XML/YAML/JSON file

    \b
    REPOSITORY git repository path, Default is the current directory.
    COMMIT     git commit to check, Default is HEAD.
    '''

    try:
        vcs = GitHandler(repository)

        data = vcs.get_infos(commit=commit)

        if not quiet:
            print_commit_table(data)

        dumper = FileDumper()
        if not quiet and len(output_formats):
            click.echo("written to :")

        for output_format in output_formats:
            dest = dumper.dump(
                data=data,
                fileformat=output_format,
                target=output,
                cwd=repository,
                namespace=namespace)
            if not quiet:
                click.echo(dest)

        ctx.exit(0)

    except (RuntimeError, ValueError, TypeError) as exc:
        click.echo("Error Writing version config file : " + str(exc))
        ctx.exit(1)


def print_commit_table(data):
    click.echo('Git commit :')
    keys = sorted(data.keys())
    table = []
    for key in keys:
        if isinstance(data[key], list):
            item = ' '.join(data[key])
        else:
            item = data[key]

        table.append([key, item])

    click.echo(tabulate(table, tablefmt='simple'))
