import os
from os import path
from shutil import copy2


def render_structure(fs_source_root, fs_target_root, context):
    """Recursively copies the given filesystem path to a target directory.

    Any files ending in `.tmpl` are interpreted as templates using Python
    string formatting and rendered using the context dictionary, thereby losing
    the `.tmpl` suffix.

    Returns the absolute path to the target directory.
    """
    for fs_source_dir, local_directories, local_files in os.walk(fs_source_root):
        fs_target_dir = path.abspath(path.join(fs_target_root, path.relpath(fs_source_dir, fs_source_root)))
        for local_file in local_files:
            render_template(path.join(fs_source_dir, local_file),
                fs_target_dir,
                context)
        for local_directory in local_directories:
            abs_dir = path.join(fs_target_dir, local_directory)
            if not path.exists(abs_dir):
                os.mkdir(abs_dir)
    return fs_target_root


def render_template(fs_source, fs_target_dir, context):
    filename = path.split(fs_source)[1]
    if filename.endswith('.tmpl'):
        filename = filename.split('.tmpl')[0]
        fs_path = path.join(fs_target_dir, filename)
        fs_target = open(fs_path, 'w')
        fs_target.write(open(fs_source).read() % context)
        fs_target.close()
    else:
        copy2(fs_source, path.join(fs_target_dir, filename))
    return path.join(fs_target_dir, filename)
