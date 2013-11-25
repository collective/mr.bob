# -*- coding: utf-8 -*-


import pkg_resources
import unittest


foo_src = 'render_filename=mrbob.tests.fake_plugins:FooRenderFilename'
bar_src = 'render_filename=mrbob.tests.fake_plugins:BarRenderFilename'
bad_src = 'render_filename=mrbob.tests.fake_plugins:BadRenderFilename'

foo_ep = pkg_resources.EntryPoint.parse(foo_src)
bar_ep = pkg_resources.EntryPoint.parse(bar_src)
bad_ep = pkg_resources.EntryPoint.parse(bad_src)

unordered_pkg_mock_entries = [bad_ep, bar_ep, foo_ep]
will_continue_mock_ep = [foo_ep]
bad_mock_ep = [bad_ep]


class load_pluginsTest(unittest.TestCase):

    def test_load_plugin_max_order_is_loaded(self):
        import mrbob.plugins
        ep = mrbob.plugins.load_plugin('render_filename',
                                        unordered_pkg_mock_entries)
        self.assertEqual(ep.order, 20)

    def test_load_plugin_target_is_loaded(self):
        import mrbob.plugins
        ep = mrbob.plugins.load_plugin('render_filename',
                                        unordered_pkg_mock_entries,
                                        target=15)

        self.assertEqual(ep.order, 15)

    def test_error_load_plugin_bad_target(self):
        import mrbob.plugins
        self.assertRaises(AttributeError, mrbob.plugins.load_plugin,
                          'render_filename', unordered_pkg_mock_entries,
                          target=19)

# vim:set et sts=4 ts=4 tw=80:
