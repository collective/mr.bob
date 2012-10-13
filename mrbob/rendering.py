import os
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

jinja2_renderer = jinja2_env.from_string,
python_formatting_renderer = lambda s, v: s % v


def render_structure(fs_source_root, fs_target_root, context, renderer):
    """Recursively copies the given filesystem path to a target directory.

    Any files ending in `.tmpl` are interpreted as templates using Python
    string formatting and rendered using the context dictionary, thereby losing
    the `.tmpl` suffix.
    """
    for fs_source_dir, local_directories, local_files in os.walk(fs_source_root):
        fs_target_dir = path.abspath(path.join(fs_target_root, path.relpath(fs_source_dir, fs_source_root)))
        for local_file in local_files:
            render_template(
                path.join(fs_source_dir, local_file),
                fs_target_dir,
                context,
                renderer,
            )
        for local_directory in local_directories:
            abs_dir = path.join(fs_target_dir, local_directory)
            if not path.exists(abs_dir):
                os.mkdir(abs_dir)


def render_template(fs_source, fs_target_dir, context, renderer):
    filename = path.split(fs_source)[1]
    if filename.endswith('.tmpl'):
        filename = filename.split('.tmpl')[0]
        fs_path = path.join(fs_target_dir, filename)
        output = renderer(open(fs_source).read(), context)
        with open(fs_path, 'w') as fs_target:
            fs_target.write(output)
    else:
        copy2(fs_source, path.join(fs_target_dir, filename))
    return path.join(fs_target_dir, filename)
