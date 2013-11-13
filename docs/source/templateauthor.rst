Writing your own template
=========================


Starting
--------

Writing your own template is as easy as creating a `.mrbob.ini` that may contain questions.
Everything else is extra. To start quickly, use the template starter that ships with `mr.bob`::

  $ mrbob mrbob:template_sample
  Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

  Answer with a question mark to display help.
  Value in square brackets at the end of the questions present default value if there is no answer.


  --> What is your name?: 

  --> How old are you? [24]:

  --> Enter password:

  --> Render optionnal folder structure [y/n] [y]:


  Generated file structure at /home/ielectric/code/mr.bob

See `.mrbob.ini` for sample questions and `sample.txt.bob` for sample rendering.


How it works
------------

Files inside the structure can be just copied to destination, or they can be suffixed with `.bob` and the templating engine
will be used to render them.

By default a slightly customized `Jinja2` templating is used. The big differences are that variables are referenced with `{{{ variable }}}` instead of `{{ variable }}` and blocks are `{{% if variable %}}` instead of `{% if variable %}`. To read more about templating see `Jinja2 documentation <http://jinja.pocoo.org/docs/templates/#variables>`_.

Variables can also be used on folder and file names. Surround variables with plus signs. For example `foo/+author+/+age+.bob` given variables *author* being `Foo` and *age* being `12`, `foo/Foo/12` will be rendered.

Variables can also influence rendering. Surround variables with plus signs. For example `foo/+__if_render.me__++author+/+age+.bob` given variables *author* being `Foo` and *age* being `12`, `foo/Foo/12` will be rendered if `render.me` is True.  Else only `foo/` will be rendered. Please notice that only ('y', 'yes', 'true', 'True', 1) are True, anything else will be considred as False.


Templating engine can be changed by specifying `renderer` in mr.bob config section in :term:`dotted notation`. It must be a callable that expects a text source as the first parameter and a dictionary of variables as the second.

When rendering the structure, permissions will be preserved for files.


Writing Questions
-----------------

`[question]` section in `.mrbob.ini` specifies a *schema* for how `[variables]` are validated.
Example speaks for itself:

.. code-block:: ini

  [questions]
  author.name.question = What is your name?
  author.name.required = True

  author.age.question = How old are you?
  author.age.help = We need your age information to render the template
  author.age.default = 24

  author.password.question = Enter password
  author.password.command_prompt = getpass:getpass

Questions will be asked in the order written in `.mrbob.ini`.


``questions`` section reference
*******************************


================= ================= =================================================================================================
  Parameter         Default          Explanation
================= ================= =================================================================================================
name                                Required. Unique identifier for the question
question                            Required. Question given interactively to a user when generating structure
default           None              Default value when no answer is given. Can be a `dotted notation`
required          False             Specify if question must be answered
command_prompt    :func:`raw_input` Function that accepts a question and asks user for the answer
help              ""                Extra help returned when user inputs a question mark
pre_ask_question  None              :term:`dotted notation` function to run before asking the question
post_ask_question None              :term:`dotted notation` function to run after asking the question (also does validation)
================= ================= =================================================================================================

Common needs for templating
---------------------------

Default value of the question is dynamic
****************************************

Use something like:

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.pre_ask_question = bobtemplates.mytemplate.hooks:pre_author

Where `pre_author` function will modify the question and provide new :attr:`mrbob.configurator.Question.default`.

Conditionally render a file
***************************

Use something like:

.. code-block:: ini

    [template]
    post_render = bobtemplates.mytemplate.hooks:delete_readme

And based on `mrbob.Configurator.variables` answers, delete a file or add one.

or use `+__if_var.me__+` on foldername or filneame, they will be rendered only if `var.me` is True.

Based on the answer of the question do something
************************************************

Use something like:

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.post_ask_question = bobtemplates.mytemplate.hooks:post_author

Where `post_author` function will take :class:`mrbob.configurator.Configurator`, question and it's answer. 

Ask a question based on answer of previous question
***************************************************

use post_ask_question and add another question (is that possible if we are looping through questions? -> While questions: questions.pop())


Hooks
-----

A list of places where you can hook into the process flow and provide your
custom code. All hooks can have multiple entries limited by whitespace.

.. _post-render-hook:

Post render hook
****************

If you would like to execute a custom Python script after rendering
is complete, you can use `post_render` hook in your ``.mrbob.ini``.

.. code-block:: ini

    [template]
    post_render = bobtemplates.mytemplate.hooks:my_post_render_function

This assumes you have a `bobtemplate.mytemplate` egg with a ``hooks.py``
module. This module contains a ``my_post_render_hook`` function, which gets
called after mr.bob has finished rendering your template.

The function expects one argument (:class:`mrbob.configurator.Configurator`)
and looks something like this:

.. code-block:: python

    def my_post_render_function(configurator):
        if configurator.variables['author.email']:
            # do something here

.. _pre-render-hook:

Pre render hook
***************

Much like the :ref:`post-render-hook` example above, you can use ``pre_render``
variable in your ``.mrbob.ini`` to specify a function to call before rendering
starts.

.. code-block:: ini

    [template]
    pre_render = bobtemplates.mytemplate.hooks:my_pre_render_function


.. _pre-question-hook:

Pre question hook
*****************

For maximum flexibility, `mr.bob` allows you to set hooks to questions. Using
``pre_ask_question`` in your ``.mrbob.ini`` allows you to run custom
code before a certain question.

The function expects two arguments:
 * :class:`mrbob.configurator.Question`
 * :class:`mrbob.configurator.Configurator`

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.pre_ask_question = bobtemplates.mytemplate.hooks:pre_author

.. code-block:: python

    def set_fullname(configurator, question):
        question.default = 'foobar'

If you want question to be skipped, simply raise :exc:`mrbob.exceptions.SkipQuestion` inside
your hook.

.. _post-question-hook:

Post question hook
******************

Similar to :ref:`pre-question-hook` example above, you can use
``post_ask_question`` variable in your ``.mrbob.ini`` to specify a function to
call after a question has been asked. :ref:`post-question-hook` **must** return
the answer of the question.

The function expects three arguments:
 * :class:`mrbob.configurator.Question`
 * :class:`mrbob.configurator.Configurator`
 * answer from the question

.. code-block:: ini

    [questions]
    author.firstname.question = What's your name?
    author.lastname.question = What's your surname?
    author.lastname.post_ask_question = bobtemplates.mytemplate.hooks:set_fullname

.. code-block:: python

    def set_fullname(configurator, question, answer):
        configurator.variables['author.fullname'] =
            configurator.variables['author.firstname'] + ' ' +
            answer
        return answer

Raise :exc:`mrbob.exceptions.ValidationError` to re-ask the question.


Hooks shipped with `mr.bob`
***************************

See :mod:`mrbob.hooks`.


``template`` section reference
------------------------------

===================== =============================== ======================================================================================
Parameter             Default                         Explanation
===================== =============================== ======================================================================================
renderer              mrbob.rendering:jinja2_renderer Function for rendering templates in :term:`dotted notation`
pre_render            None                            :term:`dotted notation` function to run before rendering the templates
post_render           None                            :term:`dotted notation` function to run after rendering the templates
===================== =============================== ======================================================================================
