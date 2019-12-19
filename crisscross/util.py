import os
import click
import platform
import subprocess


class FilePath:
    def __init__(self, path):
        self.path = path
        self.basename = os.path.basename(path)
        self.name, self.ext = os.path.splitext(self.basename)
        self.dir = os.path.dirname(self.path)
        self.dir_ = self.dir + '/'

    @staticmethod
    def get_filename(path, ext=False):
        basename = os.path.basename(path)
        if ext:
            return basename
        else:
            name, ext = os.path.splitext(basename)
            return name


def process_args(args):
    return strip_quotes(args).split()


def get_params():
    return click.get_current_context().params


def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return


def concat(file_list, pathobj, delete=False):
    makedir(pathobj.dir)
    with open(pathobj.path, 'w') as outfile:
        content = ''
        for f in file_list:
            with open(f, 'r') as infile:
                content += infile.read().strip() + '\n'
        outfile.write(content)
    if delete:
        for f in file_list:
            os.remove(f)
    return


def strip_quotes(string):
    return string.strip('\'\"')


def open_file(path):
    # https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os#435669
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', path))
    return


def echo_warn(message):
    params = get_params()
    return echo(message, fg='yellow')


def echo_success(message):
    params = get_params()
    return echo(message, fg='green')


def echo(message, fg='blue'):
    params = get_params()
    if params:
        quiet = params.get('quiet', False)
    else:
        quiet = False
    if not quiet:
        click.secho(message, fg=fg)
    return


def confirm(message):
    params = get_params()
    if not params['force']:
        click.confirm(message, abort=True)
    return


def validate_exts(paths):
    ext_list = [os.path.splitext(p)[-1] for p in paths]
    exts = set(ext_list)
    if len(exts) > 1:
        yaml_exts = set(['.yaml', '.yml'])
        if yaml_exts == exts:
            return '.yml'
        else:
            main_ext = exts - yaml_exts
            if len(main_ext) == 1:
                return main_ext.pop()
            else:
                ext_str = ' '.join(list(main_ext))
                raise ValueError(
                    'Template files have inconsistent extensions: ' + ext_str)
    else:
        return exts.pop()


def merge_dicts(x, y):
    new_dict = x.copy()
    new_dict.update(y)
    return new_dict
