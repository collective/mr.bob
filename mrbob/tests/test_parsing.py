# -*- coding: utf-8 -*-
import os
import unittest
import tempfile
import codecs
from collections import OrderedDict  # NOQA

import six

from unittest import mock


class parse_configTest(unittest.TestCase):

    def call_FUT(self, configname='example.ini'):
        import mrbob
        from ..parsing import parse_config

        if not configname.startswith('http'):
            f = os.path.abspath(
                os.path.join(
                    os.path.dirname(mrbob.__file__), 'tests', configname)
            )
        else:
            f = configname
        return parse_config(f)

    def test_parse_variable(self):
        c = self.call_FUT()
        self.assertEqual(c['variables']['name'], 'Bob')

    def test_parse_nested_variable(self):
        c = self.call_FUT()
        self.assertEqual(c['variables']['host.ip_addr'], '10.0.10.120')

    def test_parse_2nd_level_nested_variable(self):
        c = self.call_FUT()
        self.assertEqual(c['variables']['webserver.foo.bar'], 'barf')

    def test_parse_nested_variable_out_of_order(self):
        c = self.call_FUT('example2.ini')
        self.assertEqual(c['variables']['webserver.foo.bar'], 'barf2')
        self.assertEqual(c['variables']['webserver.ip_addr'], '127.0.0.3')

    def test_ignored_files(self):
        c = self.call_FUT('ignored.ini')
        self.assertTrue('ignored' in c['mr.bob']['ignored_files'])
        self.assertTrue('*.txt' in c['mr.bob']['ignored_files'])

    def test_ignored_directories(self):
        c = self.call_FUT('ignored_dirs.ini')
        self.assertTrue('ignored' in c['mr.bob']['ignored_directories'])
        self.assertTrue('*_stuff' in c['mr.bob']['ignored_directories'])

    def test_parse_deeply_nested_variables(self):
        c = self.call_FUT('example5.ini')
        expected_config = {
            'mr.bob': {},
            'variables': {'a.b.c.d': 'foo', 'a.b.c.f': 'bar', 'name': 'Bob'},
            'questions': {'a': {'b': {'c': {'d': 'foo', 'f': 'bar'}}}, 'name': 'Bob'},
            'template': {},
            'defaults': {},
            'questions_order': [],
        }
        self.assertEqual(c, expected_config)

    def test_parse_config_utf8(self):
        from ..parsing import pretty_format_config
        c = self.call_FUT('example6.ini')
        output_variables = pretty_format_config(c['variables'])
        output_questions = pretty_format_config(c['questions'])
        if six.PY3:  # pragma: no cover
            expected_output = [
                'name = Čebula',
            ]
        else:  # pragma: no cover
            expected_output = [
                'name = Čebula'.decode('utf-8'),
            ]

        self.assertEqual(output_variables, expected_output)
        self.assertEqual(output_questions, expected_output)

    def test_parse_config(self):
        from ..parsing import pretty_format_config
        c = self.call_FUT()
        output = pretty_format_config(c['variables'])
        expected_output = [
            'host.ip_addr = 10.0.10.120',
            'name = Bob',
            'webserver.foo.bar = barf',
            'webserver.fqdn = mrbob.10.0.10.120.xip.io',
            'webserver.ip_addr = 127.0.0.2',
        ]
        self.assertEqual(output, expected_output)

    def test_question_order(self):
        c = self.call_FUT('question_order.ini')
        self.assertEqual(c['questions_order'], ['foo'])

    @mock.patch('mrbob.parsing.urlretrieve')
    def test_parse_remote_config(self, urlretrieve):

        def write(url, filename):
            f = open(filename, 'w')
            f.write(
                "[variables]\n"
                "foo = bar\n"
            )
            f.close()

        urlretrieve.side_effect = write

        c = self.call_FUT(configname='http://nohost/mrbob.ini')
        self.assertEqual(c['variables']['foo'], 'bar')


class update_configTest(unittest.TestCase):

    def call_FUT(self, config, newconfig):
        from ..parsing import update_config
        return update_config(config, newconfig)

    def test_update_config_override_one_option(self):
        config = {
            'foo': 'bar',
            'foo1': 'mar'
        }
        new_config = {
            'foo1': 'bar'
        }
        self.call_FUT(config, new_config)

        expected_config = {
            'foo': 'bar',
            'foo1': 'bar'
        }

        self.assertEqual(config, expected_config)

    def test_update_config_override_nested(self):
        config = {
            'foo': 'bar',
            'bar': {
                'foo': 'bar',
                'foo1': 'foo',
            }
        }
        new_config = {
            'foo1': 'bar',
            'bar': {
                'foo1': 'moo',
                'moo': 'moo',
            }
        }
        self.call_FUT(config, new_config)

        expected_config = {
            'foo': 'bar',
            'foo1': 'bar',
            'bar': {
                'foo': 'bar',
                'foo1': 'moo',
                'moo': 'moo',
            }
        }

        self.assertEqual(config, expected_config)


class write_configTest(unittest.TestCase):

    def setUp(self):
        self.tmpfile = tempfile.mkstemp()[1]

    def tearDown(self):
        os.remove(self.tmpfile)

    def call_FUT(self, section, data):
        from ..parsing import write_config
        return write_config(self.tmpfile, section, data)

    def test_multiple_options(self):
        self.call_FUT(
            'variables',
            {'foo.bar': 'a',
             'foo.bar.moo': 'b'},
        )

        with open(self.tmpfile) as f:
            output = f.read()
            self.assertTrue('\nfoo.bar = a\n' in output)
            self.assertTrue('\nfoo.bar.moo = b\n' in output)

    def test_empty(self):
        self.call_FUT(
            'variables',
            {},
        )

        with open(self.tmpfile) as f:
            self.assertEqual(f.read(), """[variables]\n\n""")

    def test_utf8(self):
        if six.PY3:  # pragma: nocover
            var_ = 'č'
        else:  # pragma: nocover
            var_ = 'č'.decode('utf-8')

        self.call_FUT(
            'variables',
            {'foo.bar': var_},
        )

        with codecs.open(self.tmpfile, 'r', 'utf-8') as f:
            self.assertEqual(f.read(), six.u("[variables]\nfoo.bar = %s\n\n") % var_)

    def test_non_str(self):
        self.call_FUT(
            'variables',
            {'foo': True},
        )

        with open(self.tmpfile) as f:
            output = f.read()
            self.assertTrue('\nfoo = True\n' in output)


class pretty_format_configTest(unittest.TestCase):

    def call_FUT(self, config):
        from ..parsing import pretty_format_config
        return pretty_format_config(config)

    def test_complex(self):
        c = self.call_FUT({
            'foo': 'bar',
            'bar': {'moo': '1', 'ma': '2'},
            'z': 'z',
            'a': 'b',
        })
        self.assertEqual(c, [
            'a = b',
            'bar.ma = 2',
            'bar.moo = 1',
            'foo = bar',
            'z = z'],
        )


class nest_variablesTest(unittest.TestCase):

    def call_FUT(self, d):
        from ..parsing import nest_variables
        return nest_variables(d)

    def test_overwrite_dict_with_value(self):
        """ providing a value for a key that already contains a
        dictionary raises a ConfigurationError """
        from ..bobexceptions import ConfigurationError
        d = OrderedDict([('foo.bar', '1'), ('foo', '2')])
        self.assertRaises(ConfigurationError, self.call_FUT, d)

    def test_overwrite_value_with_dict(self):
        """ providing a dict for a key that already contains a
        string raises a ConfigurationError """
        from ..bobexceptions import ConfigurationError
        d = OrderedDict([('foo', '2'), ('foo.bar', '1')])
        self.assertRaises(ConfigurationError, self.call_FUT, d)
