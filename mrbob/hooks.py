"""Use any of hooks below or write your own. You are welcome to contribute them!"""

import re
import time

from .bobexceptions import ValidationError


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


def to_integer(configurator, question, answer):
    """
    If you want to convert an answer to Python integer, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        owner.question = What's your age?
        owner.post_ask_question = mrbob.hooks:to_integer

    """
    try:
        return int(answer)
    except ValueError:
        raise ValidationError('Value must be an integer')


def to_decimal(configurator, question, answer):
    """
    If you want to convert an answer to Python float, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        daemon.question = What interval should the daemon poll for data?
        daemon.post_ask_question = mrbob.hooks:to_decimal

    """
    try:
        return float(answer)
    except ValueError:
        raise ValidationError('Value must be a decimal')


def validate_choices(configurator, question, answer):
    """
    If you want to validate an answer using a limited set of choices, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        license.question = What license would you like to use?
        license.post_ask_question = mrbob.hooks:validate_choices
        license.choices = MIT|BSD|Apache 2.0|Other
        license.choices_case_sensitive = yes
        license.choices_delimiter = |

    Currently choices are split using whitespace by default. If you wish to
    have whitespace within each choice, you may specify a custom delimiter
    which will be used to split the choices.

    This hook may be set to validate the choices in a case sensitive manner.
    However, this behaviour is disabled by default.
    """
    delimiter = question.extra.get('choices_delimiter')
    choices = question.extra.get('choices', '').split(delimiter)

    # If no choices are defined, then we assume the provided answer is correct
    if not choices:
        return answer

    # Determine case sensitivity
    case_sensitive_config = question.extra.get('choices_case_sensitive')
    case_sensitive = False
    if case_sensitive_config:
        try:
            case_sensitive = to_boolean(None, None, case_sensitive_config)
        except ValidationError:
            pass

    if case_sensitive:
        valid = answer in choices
    else:
        valid = answer.lower() in [c.lower() for c in choices]

    if valid:
        return answer
    else:
        raise ValidationError(
            'Value must be ' + ', '.join(choices[:-1]) + ' or ' + choices[-1])


def validate_regex(configurator, question, answer):
    """
    If you want to validate an answer using a regular expression, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        project.question = Please specify a name (only lowercase characters)?
        project.post_ask_question = mrbob.hooks:validate_regex
        project.regex = ^[a-z]+$

    """
    regex = question.extra.get('regex')

    # If no regex is defined, then we assume the provided answer is correct
    if not regex:
        return answer

    if re.match(regex, answer):
        return answer
    else:
        raise ValidationError(
            'Value was not of the expected format (%s)' % regex)


def set_current_datetime(configurator, question):
    """
    If you want to set the default answer of a question to the current
    date and time, use this function as :ref:`pre-question-hook`:

    .. code-block:: ini

        [questions]
        project.question = What year was the project started?
        project.pre_ask_question = mrbob.hooks:set_current_datetime
        project.datetime_format = %%Y

    The datetime_format property should be of the standard Python strftime
    format.  It defaults to YYYY-MM-DD if not specified.

    Please note that you'll have to escape the % character (by using %%)
    due to the fact it's a special character in INI files.

    See the following URL for more information:
    http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    """
    datetime_format = question.extra.get('datetime_format', '%Y-%m-%d')
    question.default = time.strftime(datetime_format)


def validate_datetime(configurator, question, answer):
    """
    If you want to validate a date using a chosen date format, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        project.question = What year was the project started?
        project.post_ask_question = mrbob.hooks:validate_datetime
        project.datetime_format = %%Y

    The datetime_format property should be of the standard Python strftime
    format.  It defaults to YYYY-MM-DD if not specified.

    Please note that you'll have to escape the % character (by using %%)
    due to the fact it's a special character in INI files.

    See the following URL for more information:
    http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    """
    datetime_format = question.extra.get('datetime_format', '%Y-%m-%d')
    try:
        time.strptime(answer, datetime_format)
        return answer
    except ValueError:
        raise ValidationError(
            'Value was not a date in the format ' + datetime_format)


def show_message(configurator):
    """
    If you want to display a message to the user when rendering is complete, you
    can use this function as :ref:`post-render-hook`:

    .. code-block:: ini

        [template]
        post_render = mrbob.hooks:show_message
        message = Well done, %%(author.name)s, your code is ready!

    As shown above, you can use standard Python formatting in ``post_render_msg``.
    """
    message = configurator.templateconfig.get('message', '')
    if not configurator.quiet and message:
        print(message % configurator.variables)
