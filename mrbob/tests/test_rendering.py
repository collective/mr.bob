from os import path
from filecmp import cmp
from tempfile import mkdtemp
from shutil import rmtree
from pytest import raises

from mrbob.rendering import (render_structure,
        render_template,
        python_formatting_renderer)


def pytest_funcarg__examples(request):
    def setup():
        import mrbob
        fs_tempdir = mkdtemp()
        return (fs_tempdir,
            path.abspath(path.join(path.dirname(mrbob.__file__),
                'tests', 'templates')))

    def teardown(examples):
        fs_tempdir, fs_examples = examples
        rmtree(fs_tempdir)

    return request.cached_setup(setup=setup,
        teardown=teardown, scope='function')


def test_subdirectories_created(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'unbound'),
        target_dir,
        dict(ip_addr='192.168.0.1',
             access_control='10.0.1.0/16 allow'),
        python_formatting_renderer,
    )
    assert path.exists('%s/%s' % (target_dir, '/usr/local/etc'))


def test_string_replacement(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'unbound'),
        target_dir,
        dict(ip_addr='192.168.0.1',
             access_control='10.0.1.0/16 allow'),
        python_formatting_renderer,
    )
    fs_unbound_conf = path.join(target_dir, 'usr/local/etc/unbound/unbound.conf')
    assert ('interface: 192.168.0.1' in open(fs_unbound_conf).read())


def test_render_copy(examples):
    """if the source is not a template, it is copied."""
    target_dir, fs_examples = examples
    fs_source = path.join(fs_examples, 'unbound/etc/rc.conf')
    fs_rendered = render_template(fs_source,
        target_dir,
        dict(ip_addr='192.168.0.1', access_control='10.0.1.0/16 allow'),
        python_formatting_renderer)
    assert fs_rendered.endswith('/rc.conf')
    assert (cmp(fs_source, fs_rendered))


def test_render_template(examples):
    """if the source is a template, it is rendered and the target file drops
    the `.tmpl` suffix."""
    target_dir, fs_examples = examples
    fs_rendered = render_template(path.join(fs_examples,
            'unbound/usr/local/etc/unbound/unbound.conf.tmpl'),
        target_dir,
        dict(ip_addr='192.168.0.1', access_control='10.0.1.0/16 allow'),
        python_formatting_renderer)
    assert fs_rendered.endswith('/unbound.conf')
    assert ('interface: 192.168.0.1' in open(fs_rendered).read())


def test_render_missing_key(examples):
    target_dir, fs_examples = examples
    with raises(KeyError):
        render_template(path.join(fs_examples,
                'unbound/usr/local/etc/unbound/unbound.conf.tmpl'),
            target_dir,
            dict(),
            python_formatting_renderer)
