# -*- coding: utf-8 -*-
import stat
import os
import codecs
from os import path, chmod
from filecmp import cmp
from tempfile import mkdtemp
from shutil import rmtree
from pytest import raises
import six

from mrbob.rendering import (render_structure,
    render_template,
    python_formatting_renderer,
    jinja2_renderer,
    render_filename)


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
        True,
        python_formatting_renderer,
    )
    assert path.exists('%s/%s' % (target_dir, '/usr/local/etc'))


def test_skip_mrbobini_copying(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'skip_mrbobini'),
        target_dir,
        dict(foo='123'),
        True,
        jinja2_renderer,
    )
    assert path.exists('%s/%s' % (target_dir, 'test'))
    assert not path.exists('%s/%s' % (target_dir, '.mrbob.ini'))


def test_encoding_is_utf_eight(examples):
    target_dir, fs_examples = examples
    if six.PY3:  # pragma: no cover
        folder_name = 'encodingč'
    else:  # pragma: no cover
        folder_name = 'encodingč'.decode('utf-8')
    render_structure(
        path.join(fs_examples, folder_name),
        target_dir,
        dict(),
        True,
        python_formatting_renderer,
    )
    if six.PY3:  # pragma: no cover
        file_name = '/mapča/ća'
    else:  # pragma: no cover
        file_name = '/mapča/ća'.decode('utf-8')
    if six.PY3:  # pragma: no cover
        expected = 'Ćača.\n'
    else:  # pragma: no cover
        expected = 'Ćača.\n'.decode('utf-8')
    with codecs.open(target_dir + file_name, 'r', 'utf-8') as f:
        assert f.read() == expected


def test_string_replacement(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'unbound'),
        target_dir,
        dict(ip_addr='192.168.0.1',
             access_control='10.0.1.0/16 allow'),
        False,
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
        False,
        python_formatting_renderer)
    assert fs_rendered.endswith('/rc.conf')
    assert (cmp(fs_source, fs_rendered))


def test_render_template(examples):
    """if the source is a template, it is rendered and the target file drops
    the `.bob` suffix."""
    target_dir, fs_examples = examples
    fs_rendered = render_template(path.join(fs_examples,
            'unbound/usr/local/etc/unbound/unbound.conf.bob'),
        target_dir,
        dict(ip_addr='192.168.0.1', access_control='10.0.1.0/16 allow'),
        False,
        python_formatting_renderer)
    assert fs_rendered.endswith('/unbound.conf')
    assert ('interface: 192.168.0.1' in open(fs_rendered).read())


def test_render_missing_key(examples):
    target_dir, fs_examples = examples
    with raises(KeyError):
        t = path.join(
            fs_examples,
            'unbound/usr/local/etc/unbound/unbound.conf.bob')
        render_template(t,
            target_dir,
            dict(),
            False,
            python_formatting_renderer)


def test_rendered_permissions_preserved(examples):
    target_dir, fs_examples = examples
    fs_template = path.join(fs_examples,
        'unbound/usr/local/etc/unbound/unbound.conf.bob')
    chmod(fs_template, 771)
    fs_rendered = render_template(fs_template,
        target_dir,
        dict(ip_addr='192.168.0.1', access_control='10.0.1.0/16 allow'),
        False,
        python_formatting_renderer)
    assert stat.S_IMODE(os.stat(fs_rendered).st_mode) == 771


def test_filename_substitution():
    assert render_filename(
        'em0_+ip_addr+.conf',
        dict(ip_addr='127.0.0.1')) == 'em0_127.0.0.1.conf'


def test_filename_nested():
    assert render_filename(
        'em0_+ip.addr+.conf',
        {'ip.addr': '127.0.0.1'}) == 'em0_127.0.0.1.conf'


def test_multiple_filename_substitution():
    assert render_filename(
        '+device+_+ip_addr+.conf',
        dict(ip_addr='127.0.0.1',
            device='em0')) == 'em0_127.0.0.1.conf'


def test_single_plus_not_substituted():
    assert render_filename('foo+bar',
        dict(foo='127.0.0.1',
            bar='em0')) == 'foo+bar'


def test_no_substitution():
    assert render_filename('foobar',
        dict(foo='127.0.0.1')) == 'foobar'


def test_missing_key():
    with raises(KeyError):
        render_filename('foo+bar+blub', dict())


def test_directory_is_renamed(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'renamedir'),
        target_dir,
        dict(name='blubber'),
        False,
        python_formatting_renderer,
    )
    assert path.exists('%s/%s' % (target_dir, '/partsblubber'))
    assert path.exists('%s/%s' % (target_dir, '/partsblubber/part'))


def test_copied_file_is_renamed(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'renamedfile'),
        target_dir,
        dict(name='blubber'),
        False,
        python_formatting_renderer,
    )
    assert path.exists('%s/%s' % (target_dir, '/foo.blubber.rst'))


def test_rendered_file_is_renamed(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'renamedtemplate'),
        target_dir,
        dict(name='blubber', module='blather'),
        False,
        python_formatting_renderer,
    )
    fs_rendered = '%s/%s' % (target_dir, '/blubber_endpoint.py')
    assert path.exists(fs_rendered)
    assert ('from blather import bar' in open(fs_rendered).read())


def test_rendered_file_is_renamed_dotted_name(examples):
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'renamedtemplate2'),
        target_dir,
        {'author.name': 'foo'},
        False,
        python_formatting_renderer,
    )
    fs_rendered = '%s/%s' % (target_dir, '/foo_endpoint.py')
    assert path.exists(fs_rendered)


def test_compount_renaming(examples):
    """ all of the above edgecases in one fixture """
    target_dir, fs_examples = examples
    render_structure(
        path.join(fs_examples, 'renamed'),
        target_dir,
        dict(name='blubber', module='blather'),
        False,
        python_formatting_renderer,
    )
    fs_rendered = '%s/%s' % (target_dir, '/blatherparts/blubber_etc/blubber.conf')
    assert path.exists(fs_rendered)
    assert ('blather = blubber' in open(fs_rendered).read())


def test_parse_variables():
    from ..rendering import parse_variables
    variables = {'author.name': 'foobar',
                 'author.age': '23',
                 'license': 'BSD',
                 'foo.bar.zar.mar': 'foo'}
    vars_ = parse_variables(variables)
    assert set(vars_.keys()) == set(['foo', 'license', 'author'])
    assert set(vars_['author'].items()) == set([('name', 'foobar'), ('age', '23')])
    assert set(vars_['foo']['bar']['zar'].items()) == set([('mar', 'foo')])
