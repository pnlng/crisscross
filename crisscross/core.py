# -*- coding: utf-8 -*-
import shutil
import click
import subprocess
import os
import chevron
import re
import tempfile
from crisscross.util import *


def gen_text(var_dict, ren_path_obj, text_path_obj):
    def sub_include_rec(var_dict, read_file, write_file, asis=False):
        # heavily influenced by the process_file function from include-pandoc: https://github.com/alpianon/include-pandoc/blob/master/include_pandoc/process_includes.py
        wd = os.getcwd()
        read_dir = os.path.dirname(os.path.abspath(read_file.name))
        os.chdir(read_dir)
        lines = read_file.readlines()
        new_line_patt = re.compile('.*\\n$')
        # ensure that there's always a line break at the end of a file
        last_line = lines[-1]
        if not new_line_patt.match(last_line):
            lines[-1] = last_line + '\n'
        for line in lines:
            if asis:
                write_file.write(line)
            else:
                new_line = chevron.render(line, var_dict)
                # has an inclusion tag
                m = inclusion_patt.match(new_line)
                if m:
                    included = m.group('fname').strip()
                    # whether the referenced file should be included as is
                    include_asis = asis_patt.match(new_line)
                    try:
                        with open(included, 'r') as included_file:
                            sub_include_rec(
                                var_dict, included_file, write_file, include_asis)
                    except (FileNotFoundError) as e:
                        echo_warn('In {0}, the file referenced is not found: \n{1}'.format(
                            read_file.name, included))
                        write_file.write(new_line)
                else:
                    write_file.write(new_line)
        os.chdir(wd)
        return write_file.name

    params = get_params()
    templates = params['templates']
    args = params['args']
    render = params['render']
    include_tag = params['include_tag']

    # handle different inclusion tags
    if include_tag == 'include':
        inc_patt_tag = '!INCLUDE'
    elif include_tag == 'import':
        inc_patt_tag = '@import'

    inc_patt_pref = '^\s*'
    inc_patt_suff = '\s.*"(?P<fname>.+)"\s*$'
    inclusion_patt = re.compile(inc_patt_pref + inc_patt_tag + inc_patt_suff)
    asis_patt = re.compile('^[^"]*asis.*')

    out_dir = ren_path_obj.dir
    text_path = text_path_obj.path
    ren_path = ren_path_obj.path

    new_temps = []
    for t in templates:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as write_file:
            with open(t, 'r') as read_file:
                new_t = sub_include_rec(var_dict, read_file, write_file)
        new_temps.append(new_t)

    concat(new_temps, text_path_obj, delete=True)
    return


def gen_ren(render, ren_path_obj, text_path_obj):
    text_path = text_path_obj.path
    ren_path = ren_path_obj.path
    params = get_params()
    args = params['args']
    if render == 'pandoc':
        commands = ['pandoc', text_path, '-o', ren_path] + args
    if render == 'rmarkdown':
        commands = ['Rscript', '-e', 'rmarkdown::render(\'{text_path}\', output_file=\'{ren_basename}\', output_dir=\'{ren_dir}\')'.format(
            text_path=text_path, ren_basename=ren_path_obj.basename, ren_dir=ren_path_obj.dir)]
    try:
        echo('Processing {0}...'.format(text_path_obj.basename))
        p = subprocess.run(
            commands, stderr=subprocess.STDOUT, check=True)
        # if p.returncode == 0:
        echo_success('{0} generated.'.format(ren_path_obj.basename))
    except subprocess.CalledProcessError as e:
        output = e.output
        if not output:
            output_msg = 'exit code ' + str(e.returncode)
        else:
            output_msg = output.decode('ascii')
        raise RuntimeError(output_msg)
    return
