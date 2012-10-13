"""Command line interface to mr.bob"""

import pkg_resources
import sys
import argparse


# http://docs.python.org/library/argparse.html#argparse.ArgumentParser.add_argument
parser = argparse.ArgumentParser(description='Filesystem template renderer')
parser.add_argument('template',
                    nargs="?",
                    help="""Template to use for rendering
                    """)
parser.add_argument('-O, --target-directory',
                    default=".",
                    help='Where to output rendered structure')
parser.add_argument('--verbose',
                    action="store_true",
                    default=False,
                    help='Print more output for debugging')
parser.add_argument('--version',
                    action="store_true",
                    default=False,
                    help='Display version number')
parser.add_argument('--list-variables',
                    action="store_true",
                    default=False,
                    help='List all variables needed for template')
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
# TODO: ability to specify variables from CLI


def main(args=sys.argv[1:], quiet=False):
    options = parser.parse_args(args=args)

    if options.version:
        version = pkg_resources.get_distribution('mr.bob').version
        return version

    if not options.template:
        parser.error('You must specify what template to use.')

    # Questions(verbose=options.verbose, template=options.template, directory=options.directory)
    # TODO: list variables


if __name__ == '__main__':  # pragma: nocover
    print main()
