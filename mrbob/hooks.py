"""Use any of hooks below or write your own. You are welcome to contribute them!"""

import os
import re
import time
import subprocess

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
        license.choices = MIT;BSD;Apache 2.0;Other
        license.choices_case_sensitive = yes
        license.choices_delimiter = ;

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


def validate_url(configurator, question, answer):
    """
    If you want to validate whether an answer is a valid HTTP/HTTPS URL, you
    can use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        website.question = Please enter the URL where your website is located
        website.post_ask_question = mrbob.hooks:validate_url

    This code was adapted from Django's core.validators.URLValidator class.
    """
    url_schemes = ['http', 'https']
    url_regex = re.compile(
        r'(?:[a-z0-9\.\-]*)://'  # scheme is validated separately
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if (answer.split('://')[0].lower() in url_schemes and
            re.match(url_regex, answer)):
        return answer
    else:
        raise ValidationError('Value was not a valid URL')


def set_current_datetime(configurator, question):
    """
    If you want to set the default answer of a question to the current
    date and time, use this function as :ref:`pre-question-hook`:

    .. code-block:: ini

        [questions]
        project.question = What year was the project started?
        project.pre_ask_question = mrbob.hooks:set_current_datetime
        project.datetime_format = %Y

    The datetime_format property should be of the standard Python strftime
    format.  It defaults to YYYY-MM-DD if not specified.

    See the following URL for more information:
    http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    """
    datetime_format = question.extra.get('datetime_format', '%Y-%m-%d')
    question.default = time.strftime(datetime_format)


def set_target_dir_basename(configurator, question):
    """
    If you want to set the default answer of a question to the base name of
    the target directory, then use this function as :ref:`pre-question-hook`:

    .. code-block:: ini

        [questions]
        project.question = What is your project module name?
        project.pre_ask_question = mrbob.hooks:set_target_dir_basename

    For example, if your target directory is set to /home/user/project123,
    then this will set the question default to project123.
    """
    question.default = os.path.basename(configurator.target_directory)


def validate_datetime(configurator, question, answer):
    """
    If you want to validate a date using a chosen date format, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        project.question = What year was the project started?
        project.post_ask_question = mrbob.hooks:validate_datetime
        project.datetime_format = %Y

    The datetime_format property should be of the standard Python strftime
    format.  It defaults to YYYY-MM-DD if not specified.

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


def _run_script(configurator, script):
    """
    This helper function builds an environment based on the provided
    configurator and then attempts to run the given script.

    The function will search for scripts with relative paths in the target
    directory first and in the template directory second.

    Scripts are started with the working directory set to the target directory.

    If the script is not found, it is ignored quietly.
    """

    # Prepare the environment variables
    env = os.environ.copy()
    for key, value in configurator.variables.items():
        key_env = 'MRBOB_%s' % key.upper().replace('_', '').replace('.', '_')
        env[key_env] = str(value)

    # Determine the correct script to run first trying the target directory
    # as the root, followed by the template directory next.
    script_to_run = os.path.join(configurator.target_directory, script)
    if not os.path.exists(script_to_run):
        script_to_run = os.path.join(configurator.template_dir, script)

    # Run the script if it exists
    if os.path.exists(script_to_run):
        proc = subprocess.Popen(
            script_to_run, cwd=configurator.target_directory, env=env)
        proc.wait()


def run_pre_script(configurator):
    """
    If you want to run a chosen shell script or similar before rendering, you
    use this function as :ref:`pre-render-hook`:

    .. code-block:: ini

        [template]
        pre_render = mrbob.hooks:run_pre_script
        pre_script = /usr/local/bin/thescript.sh

    If an absolute path is not specified, mr.bob will attempt to run the
    script specified from the template directory.

    The script will be run with the working directory set to the root of the
    target directory.

    A special set of mr.bob environment variables will be made available to
    your script which expose all the variables and their answers.  Variable
    names are transformed as follows to comply with the limitations
    of shell variable names:

    - All underscores will be removed from variable names
    - The dot separators will be transformed into underscores
    - All variable names will have MRBOB_ prepended to their name
    - The variables will be in uppercase

    For example, **author.full_name** will become **MRBOB_AUTHOR_FULLNAME**.

    You may use the following basic shell script to easily see the variables
    your configuration has made available.

    .. code-block:: bash

        #!/bin/bash
        env | grep ^MRBOB

    """
    pre_script = configurator.templateconfig.get('pre_script')

    # If no script location has been provided, then we have nothing to do
    if not pre_script:
        return

    _run_script(configurator, pre_script)


def run_post_script(configurator):
    """
    If you want to run a chosen shell script or similar after rendering, you
    use this function as :ref:`post-render-hook`:

    .. code-block:: ini

        [template]
        post_render = mrbob.hooks:run_post_script
        post_script = ./setup.sh

    The run_post_script hook works exactly like **run_pre_script**.  Please
    refer to its documentation for further information.

    """
    post_script = configurator.templateconfig.get('post_script')

    # If no script location has been provided, then we have nothing to do
    if not post_script:
        return

    _run_script(configurator, post_script)


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
