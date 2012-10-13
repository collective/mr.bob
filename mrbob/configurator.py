""""""

import os


def resolve_dotted(name):
    module_name, func_name = name.split(':')
    module = __import__(module_name)
    func = getattr(module, func_name, None)
    if func:
        return func
    else:
        raise ValueError(
            'Module %s does not contain object %s' % (module, func))


def parse_template(template_name):
    if ':' in template_name:
        return resolve_dotted(template_name)
    else:
        return os.path.realpath(template_name)


class Configurator(object):
    """"""

    def __init__(self, template, target_directory, verbose=False):
        self.template = parse_template(template)
        # TODO: get information about the template
        self.target_directory = os.path.realpath(target_directory)
        if not os.path.isdir(self.target_directory):
            os.makedirs(self.target_directory)
        self.verbose = verbose

    def get_variables(self):  # pragma: no cover
        # TODO: return information about questions
        return
