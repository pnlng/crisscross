# -*- coding: utf-8 -*-
import click
from glob import glob
from crisscross.core import *
from crisscross.util import *
import os
import poyo
import chevron
from itertools import product

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    Please use one of the subcommands below.
    """


@cli.command()
@click.pass_context
@click.option('-y', '--yaml', default=['custom/*.yaml'], help='The YAML file(s) to be used. If wildcard characters are used, then the whole argument must be quoted, e.g., -y \'*.yaml\'. \n(Default: custom/*.yaml)', type=click.Path(), multiple=True)
@click.option('--no-yaml', default=False, help='Use no YAML files. In this case, key-value pairs must be supplied with -k --key-value. \n(Default: disabled)', is_flag=True)
@click.option('-o', '--out', default='docs/{{id}}.pdf', help='Schema for the path to an output file. Variables are accepted. \n(Default: docs/{{id}}.pdf)', type=click.Path(resolve_path=True))
@click.option('--open-ren/--no-open-ren', default=True, help='Whether to open the rendered files automatically. \n(Default: enabled)')
@click.option('--open-text/-no-open-text', default=False, help='Whether to open the generated text files automatically. \n(Default: disabled)')
@click.option('-a', '--args', default='', help='A string of arguments to be passed on to pandoc. Passing arguments to rmarkdown not supported. If there are spaces, the string should be quoted.')
@click.option('-r', '--render', default='pandoc', type=click.Choice(['pandoc', 'rmarkdown']), help='Render using vanilla pandoc or rmarkdown, or do not render at all. \n(Default: pandoc)')
@click.option('--no-render', default=False, help='Do not render the files with pandoc or rmarkdown. Only do variable substitution or file inclusion. \n(Default: disabled)', is_flag=True)
@click.option('--include-tag', default='include', help='Syntax for file inclusion. Either !INCLUDE "filename" or @import "filename". \n(Default: include)', type=click.Choice(['include', 'import']))
@click.option('-V', '--variable', help='A key-value pair separated by ":". No spaces allowed. Can be used in conjunction with or in place of YAML files.', multiple=True, type=click.STRING)
@click.option('-f', '--force', default=False, help='Suppress warnings. \n(Default: disabled)', is_flag=True)
@click.option('-q/-v', '--quiet/--verbose', default=False, help='Suppress messages. \n(Default: disabled)')
@click.argument('templates', nargs=-1, type=click.Path(exists=True, resolve_path=True), required=True)
def process(ctx, yaml, no_yaml, templates, out, open_ren, open_text, args, render, no_render, variable, force, quiet, include_tag):
    """
    Preprocess text files, and render with pandoc or rmarkdown.
    """
    def process_kv(variable):
        kv_dict = {}
        p = re.compile('^(?P<key>.+?):(?P<value>.+)$')
        for kv in variable:
            m = p.match(kv)
            if m:
                key = strip_quotes(m.group('key'))
                value = strip_quotes(m.group('value'))
                kv_dict[key] = value
            else:
                raise ValueError('Invalid key-value pair: {}.'.format(kv))
        return kv_dict

    def add_default_kv(d, identifier='compiled', key='id'):
        return merge_dicts({key: identifier}, d)

    def process_yaml(f):
        identifier = FilePath.get_filename(f)
        with open(f) as yamlfile:
            yaml_vars = poyo.parse_string(yamlfile.read())
            id_vars = add_default_kv(yaml_vars, identifier)
        return id_vars

    def generate(var_dict):
        ren_path = chevron.render(out_path, var_dict)
        ren_path_obj = FilePath(ren_path)
        text_path_obj = FilePath(
            ren_path_obj.dir_ + ren_path_obj.name + in_ext)
        try:
            gen_text(var_dict=var_dict, ren_path_obj=ren_path_obj,
                     text_path_obj=text_path_obj)
            if not no_render:
                gen_ren(render, ren_path_obj=ren_path_obj,
                        text_path_obj=text_path_obj)
            else:
                if text_path_obj.path != ren_path_obj.path:
                    shutil.copy(text_path_obj.path, ren_path_obj.path)
                echo_success(ren_path_obj.basename + ' generated.')
        except (RuntimeError, ValueError) as e:
            raise click.ClickException(e.args)
            click.Abort()
        except (FileNotFoundError) as e:
            raise click.ClickException(e.strerror + ': ' + e.filename)
            click.Abort()
        if open_ren:
            open_file(ren_path_obj.path)
        if open_text:
            open_file(text_path_obj.path)
        return

    params = click.get_current_context().params
    params.update(args=process_args(params['args']))

    # if out is a dir
    if re.fullmatch('.*/', out):
        confirm(
            'You supplied a directory for -o --out. No file name or format is specified. PDF files with default names will be created. \n\nOutput schema: {0}\n\nIs this correct?'.format(out))
        out_path = out+'{{id}}.pdf'
    else:
        out_path = out

    in_ext = validate_exts(templates)
    out_ext = os.path.splitext(out_path)[-1]

    if out_ext == '':
        confirm(
            '\nThe output schema you supplied does not appear to have an extension. \n\nOutput schema: {0}\n\nIs this correct?'.format(out_path))
    if no_render:
        if in_ext != out_ext:
            confirm(
                '\nYou choose to not render the documents, but the input and output files specified seem to have different extensions. \n\n Input: {input}\n Output: {output}\n\nIs this correct? If not, please modify -o --out.'.format(input=' '.join([os.path.basename(t) for t in templates]), output=os.path.basename(out_path)))

    kv_dict = process_kv(variable)

    all_yamls = []

    if not no_yaml:
        yaml_dicts = []
        for y in yaml:
            y_expanded = glob(y)
            all_yamls += y_expanded
            if not y_expanded:
                if not variable:
                    echo_warn('Nothing matching {0}.'.format(y))
            else:
                for f in y_expanded:
                    yaml_dicts.append(process_yaml(f))
        # assume that user forgot to add --no-yaml tag
        if not yaml_dicts:
            yaml_dicts = [add_default_kv({})]

        # add kv pairs
        gen_dicts = [merge_dicts(yd, kv_dict) for yd in yaml_dicts]

    else:
        if not kv_dict:
            m = re.match('\{\{(?!id).+\}\}', out_path)
            # contains anything other than {{id}}
            if m:
                raise click.BadOptionUsage(
                    option_name='-k --variable', message='--no-yaml specified, but no key-value pairs provided.')
                click.Abort()
        gen_dicts = [add_default_kv(kv_dict)]

    # multiple yamls but no variable in outpath
    if len(gen_dicts) > 1 and not re.match('.*\{\{.+\}\}', out_path):
        confirm('You have supplied multiple YAML files, but the output schema does not contain variables. Files generated earlier will be overriden.\n\nYAML files: {all_yamls} \nOutput schema: {out_path} \n\nIs this correct?'.format(
            all_yamls=' '.join(all_yamls), out_path=out_path))
    for kv in gen_dicts:
        generate(kv)


@cli.command()
@click.pass_context
@click.option('-o', '--out', default='./', help='Output directory.', type=click.Path(file_okay=False))
@click.option('-s', '--separator', default='_', help='Character used to join the names of input files.')
@click.option('-q/-v', '--quiet/--verbose', default=False, help='Suppress messages. \n(Default: disabled)')
@click.argument('files', nargs=-1)
def combine(ctx, out, separator, quiet, files):
    """
    Generate the 'Cartesian product' of multiple files.
    """
    try:
        ext = validate_exts(files)
        ll = [fl.split(',') for fl in files]
        ll_iter = product(*ll)
        for flistr in ll_iter:
            fnames = [FilePath.get_filename(f) for f in flistr]
            out_name = separator.join(fnames)
            out_path = out.strip('/') + '/' + out_name + ext
            out_path_obj = FilePath(out_path)
            concat(flistr, out_path_obj)
            echo_success(out_path_obj.basename + ' generated.')
    except (ValueError) as e:
        raise click.ClickException(e.args)
        click.Abort()


if __name__ == '__main__':
    cli()
