"""Use any of hooks below or write your own. You are welcome to contribute them!"""

from .configurator import ValidationError


def to_boolean(configurator, question, answer):
    """
    If you want to convert an answer to Python boolean, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        idiot.question = Are you young?
        idiot.post_ask_question = mrbob.hooks:to_boolean

    Following variables can be converted to a boolean: **y, n, yes, no, true, false, 1, 0**
    """
    value = answer.lower()
    if value in ['y', 'yes', 'true', '1']:
        return True
    elif value in ['n', 'no', 'false', '0']:
        return False
    else:
        raise ValidationError('Value must be a boolean (y/n)')


def show_message(configurator):
    """
    If you want to display a message to the user when rendering is complete, you
    can use this function as :ref:`post-render-hook`:

    .. code-block:: ini

        [template]
        post_render = mrbob.hooks:show_message
        message = Well done, %(author.name)s, your code is ready!

    As shown above, you can use standard Python formatting in ``post_render_msg``.
    """
    message = configurator.templateconfig.get('message', '')
    if not configurator.quiet and message:
        print(message % configurator.variables)
