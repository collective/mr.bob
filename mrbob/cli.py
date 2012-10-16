"""Command line interface to mr.bob"""

import pkg_resources
import sys
import os

import six
import argparse

from .configurator import Configurator
from .configurator import ConfigurationError
from .configurator import TemplateConfigurationError
from .parsing import parse_config, update_config


# http://docs.python.org/library/argparse.html
# TODO: split into sections for global and template related?
parser = argparse.ArgumentParser(description='Filesystem template renderer')
# TODO: write more about specifying templates
parser.add_argument('template',
                    nargs="?",
                    help="""Template to use for rendering
                    """)
parser.add_argument('-O', '--target-directory',
                    default=".",
                    dest="target_directory",
                    help='Where to output rendered structure. Defaults to current directory.')
# TODO: implement verbose mode
#parser.add_argument('-v', '--verbose',
#                    action="store_true",
#                    default=False,
#                    help='Print more output for debugging')
parser.add_argument('-c', '--config',
                    action="store",
                    help='Configuration file to specify either [mr.bob] or [variables] sections.')
parser.add_argument('-V', '--version',
                    action="store_true",
                    default=False,
                    help='Display version number')
parser.add_argument('-l', '--list-questions',
                    action="store_true",
                    default=False,
                    help='List all questions needed for the template')
parser.add_argument('-r', '--renderer',
                    action="store",
                    help='Dotted notation to a renderer function. Defaults to mrbob.rendering:jinja2_renderer')
#parser.add_option('--simulate',
                  #dest='simulate',
                  #action='store_true',
                  #help='Simulate but do no work')
#parser.add_option('--overwrite',
                  #dest='overwrite',
                  #action='store_true',
                  #help='Always overwrite')
#parser.add_option('--interactive',
                  #dest='interactive',
                  #action='store_true',
                  #help='When a file would be overwritten, interrogate')


def main(args=sys.argv[1:], quiet=False):
    options = parser.parse_args(args=args)

    if options.version:
        version = pkg_resources.get_distribution('mr.bob').version
        return version

    if not options.template:
        parser.error('You must specify what template to use.')

    userconfig = os.path.expanduser('~/.mrbob.ini')
    if os.path.exists(userconfig):
        global_config = parse_config(userconfig)
        global_bobconfig = global_config['mr.bob']
        global_variables = global_config['variables']
    else:
        global_bobconfig = {}
        global_variables = {}

    if options.config:
        if not os.path.exists(options.config):
            parser.error(six.u('ConfigurationError: config file does not exist: %s') % options.config)
        file_config = parse_config(options.config)
        file_bobconfig = file_config['mr.bob']
        file_variables = file_config['variables']
    else:
        file_bobconfig = {}
        file_variables = {}

    cli_variables = {}  # TODO: implement variables on cli
    cli_bobconfig = {
        # TODO:    'verbose': options.verbose,
    }
    if options.renderer:
        cli_bobconfig['renderer'] = options.renderer

    bobconfig = update_config(update_config(global_bobconfig, file_bobconfig), cli_bobconfig)
    variables = update_config(update_config(global_variables, file_variables), cli_variables)

    try:
        c = Configurator(template=options.template,
            target_directory=options.target_directory,
            bobconfig=bobconfig,
            variables=variables)

        if options.list_questions:
            return c.print_questions()

        print("Welcome to mr.bob interactive mode. Before we generate file structure, some questions need to be answered.")
        print("")
        print("Answer with a question mark to display help.")
        print("Value in square brackets at the end of the questions present default value if there is no answer.")
        print("\n")
        c.ask_questions()
        c.render()
        print("Generated file structure at %s" % os.path.realpath(options.target_directory))
        return
    except TemplateConfigurationError as e:
        parser.error(six.u('TemplateConfigurationError: %s') % e.args[0])
    except ConfigurationError as e:
        parser.error(six.u('ConfigurationError: %s') % e.args[0])


if __name__ == '__main__':  # pragma: nocover
    print(main())
