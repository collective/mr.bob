"""Command line interface to mr.bob"""

import pkg_resources
import sys
import os
import shutil

import six
import argparse

from .configurator import Configurator
from .configurator import maybe_bool
from .bobexceptions import ConfigurationError
from .bobexceptions import TemplateConfigurationError
from .parsing import parse_config, update_config, pretty_format_config


# http://docs.python.org/library/argparse.html
parser = argparse.ArgumentParser(description='Filesystem template renderer')
parser.add_argument('template',
                    nargs="?",
                    help="""Template name to use for rendering. See
                    http://mrbob.readthedocs.org/en/latest/userguide.html#usage
                    for a guide to template syntax

                    """)
parser.add_argument('-O', '--target-directory',
                    default=".",
                    dest="target_directory",
                    help='Where to output rendered structure. Defaults to current directory')
parser.add_argument('-v', '--verbose',
                    action="store_true",
                    default=False,
                    help='Print more output for debugging')
parser.add_argument('-c', '--config',
                    action="store",
                    help='Configuration file to specify either [mr.bob] or [variables] sections')
parser.add_argument('-V', '--version',
                    action="store_true",
                    default=False,
                    help='Display version number')
parser.add_argument('-l', '--list-questions',
                    action="store_true",
                    default=False,
                    help='List all questions needed for the template')
parser.add_argument('-w', '--remember-answers',
                    action="store_true",
                    default=False,
                    help='Remember answers to .mrbob.ini file inside output directory')
parser.add_argument('-n', '--non-interactive',
                  dest='non_interactive',
                  action='store_true',
                  default=False,
                  help="Don't prompt for input. Fail if questions are required but not answered")
parser.add_argument('-q', '--quiet',
                    action="store_true",
                    default=False,
                    help='Suppress all but necessary output')


def main(args=sys.argv[1:]):
    """Main function called by `mrbob` command.
    """
    options = parser.parse_args(args=args)

    if options.version:
        version = pkg_resources.get_distribution('mr.bob').version
        return version

    if not options.template:
        parser.error('You must specify what template to use.')

    userconfig = os.path.expanduser('~/.mrbob')
    if os.path.exists(userconfig):
        global_config = parse_config(userconfig)
        global_bobconfig = global_config['mr.bob']
        global_variables = global_config['variables']
        global_defaults = global_config['defaults']
    else:
        global_bobconfig = {}
        global_variables = {}
        global_defaults = {}

    original_global_bobconfig = dict(global_bobconfig)
    original_global_variables = dict(global_variables)
    original_global_defaults = dict(global_defaults)

    if options.config:
        try:
            file_config = parse_config(options.config)
        except ConfigurationError as e:
            parser.error(e)
        file_bobconfig = file_config['mr.bob']
        file_variables = file_config['variables']
        file_defaults = file_config['defaults']

    else:
        file_bobconfig = {}
        file_variables = {}
        file_defaults = {}

    cli_variables = {}  # TODO: implement variables on cli
    cli_defaults = {}  # TODO: implement defaults on cli
    cli_bobconfig = {
        'verbose': options.verbose,
        'quiet': options.quiet,
        'remember_answers': options.remember_answers,
        'non_interactive': options.non_interactive,
    }

    bobconfig = update_config(update_config(global_bobconfig, file_bobconfig), cli_bobconfig)
    variables = update_config(update_config(global_variables, file_variables), cli_variables)
    defaults = update_config(update_config(global_defaults, file_defaults), cli_defaults)

    c = None
    if bobconfig['verbose']:
        print('')
        print('Configuration provided:')
        print('')
        print('[variables] from ~/.mrbob')
        for line in pretty_format_config(original_global_variables):
            print(line)
        print('[variables] from --config file')
        for line in pretty_format_config(file_variables):
            print(line)
        # TODO: implement variables on cli
        # print('[variables] from command line interface')
        # for line in pretty_format_config(file_variables):
        #     print(line)
        print('[defaults] from ~/.mrbob')
        for line in pretty_format_config(original_global_defaults):
            print(line)
        print('[defaults] from --config file')
        for line in pretty_format_config(file_defaults):
            print(line)
        # TODO: implement defaults on cli
        # print('[defaults] from command line interface')
        # for line in pretty_format_config(file_defaults):
        #     print(line)
        print('[mr.bob] from ~/.mrbob')
        for line in pretty_format_config(original_global_bobconfig):
            print(line)
        print('[mr.bob] from --config file')
        for line in pretty_format_config(file_bobconfig):
            print(line)
        print('[mr.bob] from command line interface')
        for line in pretty_format_config(cli_bobconfig):
            print(line)

    try:
        c = Configurator(template=options.template,
            target_directory=options.target_directory,
            bobconfig=bobconfig,
            variables=variables,
            defaults=defaults)

        if options.list_questions:
            return c.print_questions()

        if c.questions and not maybe_bool(bobconfig['quiet']):
            if options.non_interactive:
                print('')
                print('Welcome to mr.bob non-interactive mode. Questions will be answered by default values or hooks.')
                print('')
            else:
                print('')
                print('Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.')
                print('')
                print('Answer with a question mark to display help.')
                print('Values in square brackets at the end of the questions show the default value if there is no answer.')
                print('\n')
            c.ask_questions()
            if not options.non_interactive:
                print('')
        c.render()
        if not maybe_bool(bobconfig['quiet']):
            print("Generated file structure at %s" % os.path.realpath(options.target_directory))
            print('')
        return
    except TemplateConfigurationError as e:
        parser.error(six.u('TemplateConfigurationError: %s') % e.args[0])
    except ConfigurationError as e:
        parser.error(six.u('ConfigurationError: %s') % e.args[0])
    finally:
        if c and c.is_tempdir:
            shutil.rmtree(c.template_dir)


if __name__ == '__main__':  # pragma: nocover
    print(main())
