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


def render_structure(fs_source_root, fs_target_root, context, renderer):
    """Recursively copies the given filesystem path to a target directory.

    Any files ending in `.tmpl` are rendered as templates using the given
    renderer using the context dictionary, thereby losing the `.tmpl` suffix.

    strings wrapped in `+` signs in file- or directory names will be replaced
    with values from the context, i.e. a file named `+name+.py.tmpl` given a
    dictionary {'name': 'bar'} would be rendered as `bar.py`.
    """
    # TODO: optionally move mrbob.ini to rendered structure
    for fs_source_dir, local_directories, local_files in os.walk(fs_source_root):
        fs_target_dir = path.abspath(path.join(fs_target_root, path.relpath(fs_source_dir, fs_source_root)))
        for local_file in local_files:
            render_template(
                path.join(fs_source_dir, local_file),
                render_filename(fs_target_dir, context),
                context,
                renderer,
            )
        for local_directory in local_directories:
            abs_dir = render_filename(path.join(fs_target_dir, local_directory), context)
            if not path.exists(abs_dir):
                os.mkdir(abs_dir)


def render_template(fs_source, fs_target_dir, context, renderer):
    filename = path.split(fs_source)[1]
    if filename.endswith('.tmpl'):
        filename = filename.split('.tmpl')[0]
        fs_target_path = path.join(fs_target_dir, render_filename(filename, context))
        fs_source_mode = stat.S_IMODE(os.stat(fs_source).st_mode)
        with open(fs_source) as f:
            source_output = f.read()
            output = renderer(source_output, context)
        with open(fs_target_path, 'w') as fs_target:
            fs_target.write(output)
        os.chmod(fs_target_path, fs_source_mode)
    else:
        copy2(fs_source, path.join(fs_target_dir, render_filename(filename, context)))
    return path.join(fs_target_dir, filename)


variables_regex = re.compile("\+[^+]+\+")


def render_filename(filename, context):
    variables = variables_regex.findall(filename)
    rendered = filename
    for variable in variables:
        rendered = str.replace(rendered, variable, context[str.replace(variable, '+', '')])
    return rendered
