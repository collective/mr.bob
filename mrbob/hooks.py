from .configurator import ValidationError


def to_boolean(configurator, question, answer):
    """Converts value to Python boolean given values:
    y, n, yes, no, true, false, 1, 0
    """
    value = answer.lower()
    if value in ['y', 'yes', 'true', '1']:
        return True
    elif value in ['n', 'no', 'false', '0']:
        return False
    else:
        raise ValidationError('Value must be a boolean (y/n)')


def post_render_msg(configurator):
    """TODO:docs"""
    post_render_msg = configurator.templateconfig.get('post_render_msg', '')
    if not configurator.quiet and post_render_msg:
        print(post_render_msg % configurator.variables)
