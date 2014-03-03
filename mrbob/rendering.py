from os import path
from shutil import copy2
import codecs
import fnmatch
import os
import re
import six
import stat

from jinja2 import Environment, StrictUndefined


jinja2_env = Environment(
    block_start_string="{{%",
    block_end_string="%}}",
    variable_start_string="{{{",
    variable_end_string="}}}",
    trim_blocks=True,
    undefined=StrictUndefined,
)

jinja2_renderer = lambda s, v: jinja2_env.from_string(s).render(parse_variables(v))
python_formatting_renderer = lambda s, v: s % v

DEFAULT_IGNORED_FILES = ['.mrbob.ini', '.DS_Store']
DEFAULT_IGNORED_DIRECTORIES = []


def parse_variables(variables):
    d = dict()

    for key, value in variables.items():
        keys = key.split('.')
        new_d = None
        for k in keys[:-1]:
            if new_d is None:
                if k not in d:
                    d[k] = dict()
                new_d = d[k]
            else:
                if k not in new_d:
                    new_d[k] = dict()
                new_d = new_d[k]
        if new_d is None:
            d[keys[-1]] = value
        else:
            new_d[keys[-1]] = value
    return dict(d)


def matches_any(filename, patterns):
    result = any(fnmatch.fnmatch(filename, pat) for pat in patterns)
    return result


def render_structure(
    fs_source_root, fs_target_root, variables, verbose, renderer,
    ignored_files, ignored_directories
):
    """Recursively copies the given filesystem path `fs_source_root_ to a
    target directory `fs_target_root`.

    Any files ending in `.bob` are rendered as templates using the given
    renderer using the variables dictionary, thereby losing the `.bob` suffix.

    Strings wrapped in `+` signs in file or directory names will be replaced
    with values from the variables, i.e. a file named `+name+.py.bob` given a
    dictionary {'name': 'bar'} would be rendered as `bar.py`.

    Any symbolic links will be replicated as per the source, as such is best
    that templates use relative symbolic links.
    """
    ignored_files.extend(DEFAULT_IGNORED_FILES)
    ignored_directories.extend(DEFAULT_IGNORED_DIRECTORIES)
    if not isinstance(fs_source_root, six.text_type):  # pragma: no cover
        fs_source_root = six.u(fs_source_root)

    # Iterate through all files and directories from the source directory
    for current_directory, sub_directories, local_files in os.walk(
        fs_source_root, topdown=True
    ):
        # Remove any ignored directories from our list of sub-directories
        sub_directories[:] = [d for d in sub_directories
                              if not matches_any(d, ignored_directories)]

        fs_target_dir = path.abspath(path.join(
            fs_target_root, path.relpath(current_directory, fs_source_root)))

        # Iterate through all files
        for local_file in local_files:

            # If the file is to be ignored, skip it
            if matches_any(local_file, ignored_files):
                continue

            fs_source_file = path.join(current_directory, local_file)
            fs_target_dir_rendered = render_filename(
                fs_target_dir, variables)

            # Source file is a symbolic link
            if path.islink(fs_source_file):
                fs_source_symlink = os.readlink(fs_source_file)
                filename = path.split(fs_source_file)[1]
                if filename.endswith('.bob'):
                    filename = filename.split('.bob')[0]
                fs_target_file = path.join(
                    fs_target_dir_rendered,
                    render_filename(filename, variables))

                # If the target exists, we need to clean it up first.
                # We assume it's not a directory since performing a recursive
                # delete would simply be too risky.
                if path.islink(fs_target_file) or path.exists(fs_target_file):
                    os.remove(fs_target_file)

                # Create the symlink
                if verbose:
                    print(
                        six.u("Symlinking file %s to %s") %
                        (fs_target_file, fs_source_symlink))
                os.symlink(fs_source_symlink, fs_target_file)

            # Source file is a regular file
            else:
                render_template(
                    fs_source_file, fs_target_dir_rendered, variables,
                    verbose, renderer)

        # Iterate through all sub-directories
        for sub_directory in sub_directories:

            fs_source_subdir = path.join(current_directory, sub_directory)
            fs_target_subdir = path.join(fs_target_dir, sub_directory)
            fs_target_subdir_rendered = render_filename(
                fs_target_subdir, variables)

            # If the target sub-directory doesn't exist, we create it.
            # We assume that an existing directory symlink points to the right
            # place since a recursive delete would be too risky.
            if not path.exists(fs_target_subdir_rendered):

                # Source sub-directory is a symbolic link
                if path.islink(fs_source_subdir):
                    fs_source_symlink = os.readlink(fs_source_subdir)
                    if verbose:
                        print(
                            six.u("Symlinking directory %s to %s") %
                            (fs_target_subdir_rendered, fs_source_symlink))
                    os.symlink(fs_source_symlink, fs_target_subdir_rendered)

                # Source sub-directory is a regular directory
                else:
                    if verbose:
                        print(
                            six.u("Making directory %s") %
                            fs_target_subdir_rendered)
                    os.mkdir(fs_target_subdir_rendered)


def render_template(fs_source, fs_target_dir, variables, verbose, renderer):
    filename = path.split(fs_source)[1]
    if filename.endswith('.bob'):
        filename = filename.split('.bob')[0]
        fs_target_path = path.join(fs_target_dir, render_filename(filename, variables))
        if verbose:
            print(six.u("Rendering %s to %s") % (fs_source, fs_target_path))
        fs_source_mode = stat.S_IMODE(os.stat(fs_source).st_mode)
        with codecs.open(fs_source, 'r', 'utf-8') as f:
            source_output = f.read()
            output = renderer(source_output, variables)
            # append newline due to jinja2 bug, see https://github.com/iElectric/mr.bob/issues/30
            if source_output.endswith('\n') and not output.endswith('\n'):
                output += '\n'
        with codecs.open(fs_target_path, 'w', 'utf-8') as fs_target:
            fs_target.write(output)
        os.chmod(fs_target_path, fs_source_mode)
    else:
        fs_target_path = path.join(fs_target_dir, render_filename(filename, variables))
        if verbose:
            print(six.u("Copying %s to %s") % (fs_source, fs_target_path))
        copy2(fs_source, fs_target_path)
    return path.join(fs_target_dir, filename)


def render_filename(filename, variables):
    variables_regex = re.compile(r"\+[^+%s]+\+" % re.escape(os.sep))

    replaceables = variables_regex.findall(filename)
    for replaceable in replaceables:
        actual_replaceable = replaceable.replace('+', '')
        if actual_replaceable in variables:
            filename = filename.replace(replaceable, variables[actual_replaceable])
        else:
            raise KeyError('%s key part of filename %s was not found in variables %s' % (actual_replaceable, filename, variables))
    return filename
