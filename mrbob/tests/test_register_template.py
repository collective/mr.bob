# -*- coding: utf-8 -*-
"""Testing registration of project templates"""

import unittest
import os

from mrbob import register_template

class RegisterTemplateTest(unittest.TestCase):
    """The register_template function
    """
    def test_no_such_folder(self):
        """This template folder does not exist
        """
        self.assertRaises(ValueError, register_template, 'not-existing-directory')
        return

    def test_not_bob_template(self):
        """This folder exists but is not a mr.bob template
        """
        self.assertRaises(ValueError, register_template, 'templates')
        return

    def test_bob_template_wo_description(self):
        """This is a mr.bob template folder but its config has no description
        """
        reg = register_template('templates/empty')
        self.assertTrue("No description available" in reg.description)
        return

    def test_forced_description(self):
        """The description of the template is provided as parameter
        """
        # With a template which config file has no description
        descr = "This template is wonderful"
        reg = register_template('templates/empty', description=descr)
        self.assertTrue(descr in reg.description)

        # With a config file that has another description
        reg = register_template('templates/config_description', description=descr)
        self.assertTrue(descr in reg.description)
        return

    def test_config_description(self):
        """The description of the template is in the config file
        """
        reg = register_template('templates/config_description')
        self.assertTrue("The description is in the config file" in reg.description)
        return

    def test_registered_path(self):
        """The registered template path is OK
        """
        this_directory = os.path.dirname(__file__)
        expect = os.path.join(this_directory, 'templates/empty')
        reg = register_template('templates/empty')
        self.assertEqual(reg.directory, expect)
        return


