# -*- coding: utf-8 -*-
'''
    Main module
'''
# from __future__ import unicode_literals

import os
import re

import click
from tabulate import tabulate

import git_app_version.version
from git_app_version.dumper import FileDumper
from git_app_version.githandler import RESERVED_KEYS, GitHandler

__version__ = git_app_version.version.__version__


def print_version(ctx, param, value):
    '''
    display application version
    '''
    if not value or ctx.resilient_parsing:
        return
    click.echo('git-app-version ' + __version__)
    ctx.exit()


CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


class MetadataParamType(click.ParamType):
    '''
    Click paramerer Type to parse <key>=<value> option
    '''
    name = 'metadata'

    def convert(self, value, param, ctx):
        '''
        convert row option value to dict
        '''
        try:
            match = re.match(r'^([^=]+)=(.*)$', value)
            if not match:
                raise ValueError(
                    '%s is not a valid meta data string e.g. : <key>=<value>' %
                    value)

            if match.group(1) in RESERVED_KEYS:
                raise ValueError('%s is a reserved key' % match.group(1))

            return {match.group(1): match.group(2).strip('"\'')}

        except ValueError as exc:
            self.fail(str(exc), param, ctx)


METADATA = MetadataParamType()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-V', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
# @click.option('--verbose', '-v', count=True)
@click.option('--quiet', '-q', is_flag=True, help='silent mode')
@click.option('--output', '-o', default='version',
              help='output file path (without extension).'
              ' Default is \'<repository-path>/version\'.')
@click.option('--format', '-f', 'output_formats',
              type=click.Choice([
                  'all',
                  'json',
                  'yml',
                  'xml',
                  'ini',
                  'csv',
                  'sh'
              ]),
              multiple=True, default=['json'],
              help='output file format and extension,'
              ' use \'all\' to output all format , Default is json.')
@click.option('--namespace', '-n', default='',
              help='namespace like notation in version file, use dot separator'
              ' to segment namespaces e.g.: \'foo.bar.git\'.'
              ' Default is \'app_version\' for XML and INI'
              ' and no namespace for JSON and YAML.'
              ' Never used for CSV or Shell file.')
@click.option('--meta', '-m', type=METADATA, multiple=True,
              help='meta data to add, format = "<key>=<value>"')
@click.option('--csv-delimiter', '-d', 'csv_delimiter', default=u',',
              help='CSV delimiter, default=","')
@click.option('--csv-eol', '-e', 'csv_eol', type=click.Choice(['lf', 'crlf']),
              default="lf",
              help='CSV end of line,'
              ' lf = Unix new line, crlf = windows new line, default=lf')
@click.option('--csv-quote', '-u', 'csv_quote', default=u'"',
              help='CSV quoting character, default=\'"\'')
@click.argument('repository',
                type=click.Path(exists=True, resolve_path=True,
                                file_okay=False, readable=True),
                default=os.getcwd())
@click.argument('commit', default='HEAD')
@click.pass_context
def dump(ctx, repository, commit, output, output_formats,
         namespace, meta, quiet, csv_delimiter, csv_quote, csv_eol):
    '''
    Get Git commit informations and store them in a config file

    \b
    REPOSITORY git repository path, Default is the current directory.
    COMMIT     git commit to check, Default is HEAD.
    '''

    try:
        vcs = GitHandler(repository)

        data = vcs.get_infos(commit=commit)

        # add metadatas
        for item in meta:
            for key, val in item.items():
                data[key] = val

        if not quiet:
            print_commit_table(data)

        dumper = FileDumper()
        if not quiet and len(output_formats):
            click.echo("written to :")

        if 'all' in output_formats:
            output_formats = ['json', 'yml', 'xml', 'ini', 'csv', 'sh']

        for output_format in output_formats:
            dest = dumper.dump(
                data=data,
                fileformat=output_format,
                target=output,
                cwd=repository,
                namespace=namespace,
                csv_delimiter=csv_delimiter,
                csv_quote=csv_quote,
                csv_eol=csv_eol)
            if not quiet:
                click.echo(dest)

        ctx.exit(0)

    except (RuntimeError, ValueError, TypeError) as exc:
        click.echo("Error Writing version config file : " + str(exc))
        ctx.exit(1)


def print_commit_table(data):
    '''
    display a dict as a Table in standard output
    '''
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

if __name__ == '__main__':
    dump()
