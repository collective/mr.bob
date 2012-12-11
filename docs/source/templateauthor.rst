Writing your own template
=========================


Starting
--------

Writing your own template is as easy as creating a `.mrbob.ini` that may contain questions.
Everything else is extra. To start quickly, use the template starter that ships with `mr.bob`::

  $ mr.bob mrbob:template_starter/
  Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

  Answer with a question mark to display help.
  Value in square brackets at the end of the questions present default value if there is no answer.


  --> How old are you? [24]:

  --> What is your name?: Foobar

  --> Enter password:


  Generated file structure at /home/ielectric/code/mr.bob

See `.mrbob.ini` for sample questions and `sample.txt.bob` for sample rendering.


Templating
----------

Files inside the structure can be just copied to destination, or they can be suffixed with `.bob` and the templating engine
will be used to render them.

By default a slightly customized `Jinja2` templating is used. The big differences are that variables are referenced with `{{{ variable }}}` instead of `{{ variable }}` and blocks are `{{% if variable %}}` instead of `{% if variable %}`. To read more about templating see `Jinja2 documentation <http://jinja.pocoo.org/docs/templates/#variables>`_.

Variables can also be used on folder and file names. Surround variables with plus signs. For example `foo/+author+/+age+.bob` given variables *author* being `Foo` and *age* being `12`, `foo/Foo/12` will be rendered.

Templating engine can be changed by specifying `renderer` in mr.bob config section in :term:`dotted notation`. It must be a callable that expects a text source as the first parameter and a dictionary of variables as the second.

When rendering the structure, permissions will be preserved for files.


Writing Questions
-----------------

`[question]` section in `.mrbob.ini` specifies a *schema* for how `[variables]` are validated.
Example speaks for itself:

.. code-block:: ini

  [questions]
  author.name.question = What is your name?
  author.required = True

  author.age.question = How old are you?
  author.age.help = We need your age information to render the template
  author.age.default = 24

  author.password.question = Enter password
  author.password.command_prompt = getpass:getpass

Questions will be asked in the order written in `.mrbob.ini`.


``questions`` section reference
*******************************


=============== ================= =================================================================================================
  Parameter         Default          Explanation
=============== ================= =================================================================================================
name                              Required. Unique identifier for the question
question                          Required. Question given interactively to a user when generating structure
default         None              Default value when no answer is given. Can be a `dotted notation`
required        False             Specify if question must be answered
validator       None              Validator can raise :exc:`mrbob.configurator.ValidationError` and question will be asked again
command_prompt  :func:`raw_input` Function that accepts a question and asks user for the answer
help            ""                Extra help returned when user inputs a question mark
=============== ================= =================================================================================================


Validators
----------

Validators are functions with an answer as the only parameter. They may return a value to be used as
an answer and may raise :exc:`ValidationError` for the question to be asked again.

See :mod:`mrbob.validators` for validators that ship with `mr.bob`.

Common needs for templating
---------------------------

Default value of the question is dynamic
****************************************

(for example url of documentation may propose package.rtfd.org link for docs) -> use pre_ask_question to set default value

Conditionally render a file
***************************

use post_render and delete the file if needed


Based on the answer of the question do something
************************************************

if one question was answered, another template may be triggered -> use post_ask_question and use api to do whatever

Ask a question based on answer of previous question
***************************************************

use post_ask_question and add another question (is that possible if we are looping through questions? -> While questions: questions.pop())


- mention mr.bob configures template also
- mr.bob in template override everything or just sets new defaults?

TODO: mention post_render_msg can use python formatting to access variables
TODO: mr.bob additional settings

Preserve ``.mrbob.ini``
***********************

In some cases you want to render the ``.mrbob.ini`` in your result, for example
to keep track of what you answered to bob's questions. You can achive this
by setting ``preserve_mrbob_config`` to True:

.. code-block:: ini

    [mr.bob]
    preserve_mrbob_config = True


Hooks
-----

A list of places where you can hook into the process flow and provide your
custom code.

Post render message
*******************

If you want to display a message to the user when rendering is complete, you
can use `post_render_msg` in your ``.mrbob.ini``:

.. code-block:: ini

    [mr.bob]
    post_render_msg = Well done, %(author.name)s, your code is ready!

As shown above, you can use standard Python formatting in ``post_render_msg``.

.. _post-render-hook:

Post render hook
****************

Similarly if you would like to execute a custom Python script after rendering
is complete, you can use `post_render` hook in your ``.mrbob.ini``.

.. code-block:: ini

    [mr.bob]
    post_render = bobtemplates.mytemplate.hooks:my_post_render_function

This assumes you have a `bobtemplate.mytemplate` egg with a ``hooks.py``
module. This module contains a ``my_post_render_hook`` function, which gets
called after mr.bob has finished rendering your template.

The function expects one argument (:class:`mrbob.configurator.Configurator`)
and looks something like this:

.. code-block:: python

    def my_post_render_function(configurator):
        if configurator.variables['author.email']:
            # do some validation here or something

.. _pre-render-hook:

Pre render hook
***************

Much like the :ref:`post-render-hook` example above, you can use ``pre_render``
variable in your ``.mrbob.ini`` to specify a funtion to call before rendering
starts.

.. code-block:: ini

    [mr.bob]
    pre_render = bobtemplates.mytemplate.hooks:my_pre_render_function


.. _pre-question-hook:

Pre question hook
*****************

To allow for flexibility, mr.bob allows you to set hooks to questions. Using
``pre_ask_question`` variable in your ``.mrbob.ini`` allows you to run custom
code before a certain question.

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.pre_ask_question = bobtemplates.mytemplate.hooks:pre_author.name_question

See below for an example of a hook function.

.. _post-question-hook:

Post question hook
******************

Much like the :ref:`pre-question-hook` example above, you can use
``post_ask_question`` variable in your ``.mrbob.ini`` to specify a funtion to
call after a question has been asked.

.. code-block:: ini

    [questions]
    author.firstname.question = What's your name?
    author.lastname.question = What's your surname?
    author.lastname.post_ask_question = bobtemplates.mytemplate.hooks:set_fullname

.. code-block:: python

    def set_fullname(question, configurator):
        configurator.variables['author.fullname'] =
            configurator.variables['author.firstname'] + ' ' +
            configurator.variables['author.lastname']

The function expects two arguments:
 * :class:`mrbob.configurator.Question`
 * :class:`mrbob.configurator.Configurator`

 Note that `pre_ask_question` and `post_ask_question` are defined for questions
in the ``[questions]`` section of ``.mrbob.ini``.

