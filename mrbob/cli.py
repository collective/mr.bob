"""Command line interface to mr.bob"""

import pkg_resources
import sys

import six
import argparse

from .configurator import Configurator
from .configurator import ConfigurationError
from .configurator import TemplateConfigurationError


# http://docs.python.org/library/argparse.html
parser = argparse.ArgumentParser(description='Filesystem template renderer')
parser.add_argument('template',
                    nargs="?",
                    help="""Template to use for rendering
                    """)
parser.add_argument('-O, --target-directory',
                    default=".",
                    dest="target_directory",
                    help='Where to output rendered structure')
parser.add_argument('--verbose',
                    action="store_true",
                    default=False,
                    help='Print more output for debugging')
parser.add_argument('--version',
                    action="store_true",
                    default=False,
                    help='Display version number')
parser.add_argument('--list-questions',
                    action="store_true",
                    default=False,
                    help='List all questions needed for the template')
parser.add_argument('--renderer',
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

    bobconfig = {
        # TODO:    'verbose': options.verbose,
    }
    if options.renderer:
        bobconfig['renderer'] = options.renderer

    try:
        c = Configurator(template=options.template,
            target_directory=options.target_directory,
            bobconfig=bobconfig)
        if options.list_questions:
            return c.print_questions()

        return c.render()
    except TemplateConfigurationError as e:
        parser.error(six.u('TemplateConfigurationError %s') % e.args[0])
    except ConfigurationError as e:
        parser.error(six.u('ConfigurationError %s') % e.args[0])


if __name__ == '__main__':  # pragma: nocover
    print(main())
