Writing your own template
=========================


Starting
--------

Writing your own template is as easy as creating a `.mrbob.ini` that may contain questions.
Everything else is extra. To start quickly, use template starter that ships with `mr.bob`::

  $ mr.bob mrbob:template_starter/
  ...

See `.mrbob.ini` for sample questions and `sample.bob` for sample rendering.


Templating
----------

Files inside structure can be just copied to destiantion or they can be suffixed with `.bob` and templating engine
will be used to render them.

By default a little bit customized `Jinja2` templating is used. The big difference is that variables are referenced with `{{{ variable }}}` instead of `{{ variable }}` and blocks are `{{% if variable %}}` instead of `{% if variable %}`. To read more about templating see `Jinja2 documentation <http://jinja.pocoo.org/docs/templates/#variables>`_.

Variables can also be used on folder and file names. Surround variables with plus signs. For example `foo/+author+/+age+.bob` given variables *author* being `Foo` and *age* being `12`, `foo/Foo/12` will be rendered.

Templating engine can be changed by specifying `renderer` in mr.bob config section in :term:`dotted notation`. It must be a callable that expects text source as first parameter and dictionary of variables as second.

When rendering structure, permissions will be preserved for files.


Writing Questions
-----------------

`[question]` section in `.mrbob.ini` specifies schema how `[variables]` are validated.
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


``questions`` section reference
*******************************

=============== ================= =================================================================================================
  Parameter         Default          Explanation
=============== ================= =================================================================================================
name                              Required. Unique identifier for the question
question                          Required. Question given interactively to a user when generating structure
default         None              Default value when no answer is given. Can be a `dotted notation`
required        False             Specify if question must be answered
action          lambda x: x       Extra action to be taken except returning value to be used stored in variables
validator       None              Validator can raise :exc:`mrbob.configurator.ValidationError` and question will be asked again
command_prompt  :func:`raw_input` Function that accepts question and asks user for the answer
help            ""                Extra help returned when user inputs a question mark
=============== ================= =================================================================================================
