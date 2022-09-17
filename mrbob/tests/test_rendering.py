# -*- coding: utf-8 -*-

from shutil import rmtree
from tempfile import mkdtemp
import codecs
import os
import stat
import unittest

from unittest import mock
import six


class render_structureTest(unittest.TestCase):

    def setUp(self):
        import mrbob
        self.fs_tempdir = mkdtemp()
        self.fs_templates = os.path.abspath(
            os.path.join(os.path.dirname(mrbob.__file__),
                         'tests', 'templates'))

    def tearDown(self):
        rmtree(self.fs_tempdir)

    def call_FUT(self, template, variables, output_dir=None, verbose=True,
            renderer=None, ignored_files=[], ignored_directories=[]):
        from ..rendering import render_structure
        from ..rendering import jinja2_renderer

        if output_dir is None:
            output_dir = self.fs_tempdir

        if renderer is None:
            renderer = jinja2_renderer

        render_structure(
            template,
            output_dir,
            variables,
            verbose,
            renderer,
            ignored_files,
            ignored_directories,
        )

    def test_subdirectories_created(self):
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'unbound'),
            dict(ip_addr='192.168.0.1',
                 access_control='10.0.1.0/16 allow'),
            renderer=python_formatting_renderer,
        )
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir, '/usr/local/etc')))

    def test_skip_mrbobini_copying(self):
        self.call_FUT(
            os.path.join(self.fs_templates, 'skip_mrbobini'),
            dict(foo='123'),
        )
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir, 'test')))
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, '.mrbob.ini')))

    def test_ds_store(self):
        self.call_FUT(
            os.path.join(self.fs_templates, 'ds_store'),
            dict(),
        )
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, '.mrbob.ini')))
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, '.DS_Store')))

    def test_ignored_files(self):
        self.call_FUT(
            os.path.join(self.fs_templates, 'ignored'),
            dict(),
            ignored_files=['ignored', '*.txt', '.mrbob.ini'],
        )
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, '.mrbob.ini')))
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, 'ignored')))
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir,
            'ignored.txt')))
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir, 'not_ignored')))

    def test_ignored_directories(self):
        self.call_FUT(
            os.path.join(self.fs_templates, 'ignored_dirs'),
            dict(),
            ignored_directories=['ignored', '*_stuff'],
        )
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, 'ignored')))
        self.assertFalse(os.path.exists('%s/%s' % (self.fs_tempdir, 'ignored_stuff')))
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir, 'not_ignored')))

    def test_encoding_is_utf8(self):
        from ..rendering import python_formatting_renderer
        if six.PY3:  # pragma: no cover
            folder_name = 'encodingč'
        else:  # pragma: no cover
            folder_name = 'encodingč'.decode('utf-8')

        self.call_FUT(
            os.path.join(self.fs_templates, folder_name),
            dict(),
            renderer=python_formatting_renderer,
        )

        if six.PY3:  # pragma: no cover
            file_name = 'mapča/ća'
            expected = 'Ćača.\n'
        else:  # pragma: no cover
            file_name = 'mapča/ća'.decode('utf-8')
            expected = 'Ćača.\n'.decode('utf-8')

        with codecs.open(os.path.join(self.fs_tempdir, file_name), 'r', 'utf-8') as f:
            self.assertEquals(f.read(), expected)

    def test_string_replacement(self):
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'unbound'),
            dict(ip_addr='192.168.0.1',
                 access_control='10.0.1.0/16 allow'),
            verbose=False,
            renderer=python_formatting_renderer,
        )
        fs_unbound_conf = os.path.join(self.fs_tempdir, 'usr/local/etc/unbound/unbound.conf')
        self.assertTrue('interface: 192.168.0.1' in open(fs_unbound_conf).read())

    def test_directory_is_renamed(self):
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'renamedir'),
            dict(name='blubber'),
            verbose=False,
            renderer=python_formatting_renderer,
        )
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir, '/partsblubber/part')))

    def test_copied_file_is_renamed(self):
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'renamedfile'),
            dict(name='blubber'),
            verbose=False,
            renderer=python_formatting_renderer,
        )
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir, '/foo.blubber.rst')))

    def test_rendered_file_is_renamed(self):
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'renamedtemplate'),
            dict(name='blubber', module='blather'),
            verbose=False,
            renderer=python_formatting_renderer,
        )
        fs_rendered = '%s/%s' % (self.fs_tempdir, '/blubber_endpoint.py')
        self.assertTrue(os.path.exists(fs_rendered))
        self.assertTrue('from blather import bar' in open(fs_rendered).read())

    def test_rendered_file_is_renamed_dotted_name(self):
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'renamedtemplate2'),
            {'author.name': 'foo'},
            verbose=False,
            renderer=python_formatting_renderer,
        )
        self.assertTrue(os.path.exists('%s/%s' % (self.fs_tempdir,
                                                  '/foo_endpoint.py')))

    def test_compount_renaming(self):
        """ all of the above edgecases in one fixture """
        from ..rendering import python_formatting_renderer
        self.call_FUT(
            os.path.join(self.fs_templates, 'renamed'),
            dict(name='blubber', module='blather'),
            verbose=False,
            renderer=python_formatting_renderer,
        )
        fs_rendered = '%s/%s' % (self.fs_tempdir, '/blatherparts/blubber_etc/blubber.conf')
        self.assertTrue(os.path.exists(fs_rendered))
        self.assertTrue('blather = blubber' in open(fs_rendered).read())


class render_templateTest(unittest.TestCase):
    def setUp(self):
        import mrbob
        self.fs_tempdir = mkdtemp()
        self.fs_templates = os.path.abspath(
            os.path.join(os.path.dirname(mrbob.__file__),
                         'tests', 'templates'))

    def tearDown(self):
        rmtree(self.fs_tempdir)

    def call_FUT(self, template, variables, output_dir=None, verbose=False, renderer=None):
        from ..rendering import render_template
        from ..rendering import python_formatting_renderer

        if output_dir is None:
            output_dir = self.fs_tempdir

        if renderer is None:
            renderer = python_formatting_renderer

        return render_template(
            template,
            output_dir,
            variables,
            verbose,
            renderer,
        )

    def test_render_copy(self):
        """if the source is not a template, it is copied."""
        fs_source = os.path.join(self.fs_templates, 'unbound/etc/rc.conf')

        fs_rendered = self.call_FUT(
            fs_source,
            dict(ip_addr='192.168.0.1',
                 access_control='10.0.1.0/16 allow'))
        self.assertTrue(fs_rendered.endswith('rc.conf'))
        with open(fs_source) as f1:
            with open(fs_rendered) as f2:
                self.assertEqual(f1.read(), f2.read())

    def test_render_template(self):
        """if the source is a template, it is rendered and the target file drops
        the `.bob` suffix."""
        fs_source = os.path.join(self.fs_templates,
            'unbound/usr/local/etc/unbound/unbound.conf.bob')
        fs_rendered = self.call_FUT(
            fs_source,
            dict(ip_addr='192.168.0.1',
                 access_control='10.0.1.0/16 allow'))
        self.assertTrue(fs_rendered.endswith('/unbound.conf'))
        self.assertTrue('interface: 192.168.0.1' in open(fs_rendered).read())

    def test_rendered_permissions_preserved(self):
        fs_source = os.path.join(self.fs_templates,
            'unbound/usr/local/etc/unbound/unbound.conf.bob')
        os.chmod(fs_source, 771)
        fs_rendered = self.call_FUT(
            fs_source,
            dict(ip_addr='192.168.0.1',
                 access_control='10.0.1.0/16 allow'))
        self.assertEqual(stat.S_IMODE(os.stat(fs_rendered).st_mode), 771)

    def test_render_missing_key(self):
        t = os.path.join(self.fs_templates,
            'unbound/usr/local/etc/unbound/unbound.conf.bob')

        self.assertRaises(KeyError,
                          self.call_FUT,
                          t,
                          dict())

    def test_render_namespace(self):
        t = os.path.join(self.fs_templates,
            'missing_namespace_key/foo.bob')

        filename = self.call_FUT(t, {'foo.bar': '1'})
        with open(filename) as f:
            self.assertEqual(f.read(), '1\n')

    def test_render_namespace_jinja2(self):
        from ..rendering import jinja2_renderer
        t = os.path.join(self.fs_templates,
            'missing_namespace_key/foo_jinja2.bob')

        filename = self.call_FUT(t,
                                 {'foo.bar': '2'},
                                 renderer=jinja2_renderer)
        with open(filename) as f:
            self.assertEqual(f.read(), '2\n')

    def test_render_newline(self):
        from ..rendering import jinja2_renderer
        t = os.path.join(self.fs_templates,
            'missing_namespace_key/foo_jinja2.bob')

        tfile = open(t, 'r')
        self.assertEqual(tfile.read(), '{{{foo.bar}}}\n')

        filename = self.call_FUT(t,
                                 {'foo.bar': '2'},
                                 renderer=jinja2_renderer)
        with open(filename) as f:
            self.assertEqual(f.read(), '2\n')

    def test_render_namespace_missing_key(self):
        t = os.path.join(self.fs_templates,
            'missing_namespace_key/foo.bob')

        self.assertRaises(KeyError,
                          self.call_FUT,
                          t,
                          {})

    def test_render_namespace_missing_key_jinja2(self):
        from jinja2 import UndefinedError
        from ..rendering import jinja2_renderer
        t = os.path.join(self.fs_templates,
            'missing_namespace_key/foo_jinja2.bob')

        self.assertRaises(UndefinedError,
                          self.call_FUT,
                          t,
                          {},
                          renderer=jinja2_renderer)

    def test_jinja2_strict_undefined(self):
        from jinja2 import UndefinedError
        from ..rendering import jinja2_renderer

        t = os.path.join(self.fs_templates,
            'strict_undefined.bob')

        self.assertRaises(UndefinedError,
                          self.call_FUT,
                          t,
                          {},
                          renderer=jinja2_renderer)


class render_filenameTest(unittest.TestCase):

    def call_FUT(self, filename, variables):
        from ..rendering import render_filename
        return render_filename(filename, variables)

    def test_filename_substitution(self):
        t = self.call_FUT('em0_+ip_addr+.conf', dict(ip_addr='127.0.0.1'))
        self.assertEqual(t, 'em0_127.0.0.1.conf')

    def test_filename_nested(self):
        t = self.call_FUT('em0_+ip.addr+.conf', {'ip.addr': '127.0.0.1'})
        self.assertEqual(t, 'em0_127.0.0.1.conf')

    def test_multiple_filename_substitution(self):
        t = self.call_FUT('+device+_+ip_addr+.conf',
                          dict(ip_addr='127.0.0.1', device='em0'))
        self.assertEqual(t, 'em0_127.0.0.1.conf')

    def test_single_plus_not_substituted(self):
        t = self.call_FUT('foo+bar',
                          dict(foo='127.0.0.1', bar='em0'))
        self.assertEqual(t, 'foo+bar')

    def test_no_substitution(self):
        t = self.call_FUT('foobar',
                          dict(foo='127.0.0.1', bar='em0'))
        self.assertEqual(t, 'foobar')

    def test_pluses_in_path(self):
        t = self.call_FUT('+/bla/+/+bar+',
                          dict(bar='em0'))
        self.assertEqual(t, '+/bla/+/em0')

    @mock.patch('mrbob.rendering.os', sep='\\')
    def test_pluses_in_pathwindows(self, mock_sep):
        t = self.call_FUT('+\\bla\\+\\+bar+',
                          dict(bar='em0'))
        self.assertEqual(t, '+\\bla\\+\\em0')

    def test_missing_key(self):
        self.assertRaises(KeyError, self.call_FUT, 'foo+bar+blub', dict())


class parse_variablesTest(unittest.TestCase):

    def test_complex_example(self):
        from ..rendering import parse_variables
        variables = {'author.name': 'foobar',
                     'author.age': '23',
                     'license': 'BSD',
                     'foo.bar.zar.mar': 'foo'}
        vars_ = parse_variables(variables)
        self.assertEqual(
            set(vars_.keys()),
            set(['foo', 'license', 'author']),
        )
        self.assertEqual(
            set(vars_['author'].items()),
            set([('name', 'foobar'), ('age', '23')]),
        )
        self.assertEqual(
            set(vars_['foo']['bar']['zar'].items()),
            set([('mar', 'foo')]),
        )

        # there is no such key in this namespace
        self.assertRaises(KeyError, lambda x: vars_['author'][x], 'foo')
