import six
import stat
import os
import re
from os import path
from shutil import copy2
from jinja2 import Environment


jinja2_env = Environment(
    block_start_string="{{%",
    block_end_string="%}}",
    variable_start_string="{{{",
    variable_end_string="}}}",
    trim_blocks=True,
)

jinja2_renderer = lambda s, v: jinja2_env.from_string(s).render(v)
python_formatting_renderer = lambda s, v: s % v


def render_structure(fs_source_root, fs_target_root, context, verbose, renderer):
    """Recursively copies the given filesystem path `fs_source_root_ to a target directory `fs_target_root`.

    Any files ending in `.bob` are rendered as templates using the given
    renderer using the context dictionary, thereby losing the `.bob` suffix.

    strings wrapped in `+` signs in file- or directory names will be replaced
    with values from the context, i.e. a file named `+name+.py.bob` given a
    dictionary {'name': 'bar'} would be rendered as `bar.py`.
    """
    if not isinstance(fs_source_root, six.text_type):
        fs_source_root = six.u(fs_source_root)
    for fs_source_dir, local_directories, local_files in os.walk(fs_source_root):
        fs_target_dir = path.abspath(path.join(fs_target_root, path.relpath(fs_source_dir, fs_source_root)))
        for local_file in local_files:
            render_template(
                path.join(fs_source_dir, local_file),
                render_filename(fs_target_dir, context),
                context,
                verbose,
                renderer,
            )
        for local_directory in local_directories:
            abs_dir = render_filename(path.join(fs_target_dir, local_directory), context)
            if not path.exists(abs_dir):
                if verbose:
                    print(six.u("mkdir %s") % abs_dir)
                os.mkdir(abs_dir)


def render_template(fs_source, fs_target_dir, context, verbose, renderer):
    filename = path.split(fs_source)[1]
    if filename.endswith('.bob'):
        filename = filename.split('.bob')[0]
        fs_target_path = path.join(fs_target_dir, render_filename(filename, context))
        if verbose:
            print(six.u("Rendering %s to %s") % (fs_source, fs_target_path))
        fs_source_mode = stat.S_IMODE(os.stat(fs_source).st_mode)
        with open(fs_source) as f:
            source_output = f.read()
            output = renderer(source_output, context)
        with open(fs_target_path, 'w') as fs_target:
            fs_target.write(output)
        os.chmod(fs_target_path, fs_source_mode)
    else:
        fs_target_path = path.join(fs_target_dir, render_filename(filename, context))
        if verbose:
            print(six.u("Copying %s to %s") % (fs_source, fs_target_path))
        copy2(fs_source, fs_target_path)
    return path.join(fs_target_dir, filename)


variables_regex = re.compile("\+[^+]+\+")


def render_filename(filename, context):
    variables = variables_regex.findall(filename)
    rendered = filename
    for variable in variables:
        rendered = rendered.replace(variable, context[variable.replace('+', '')])
    return rendered
