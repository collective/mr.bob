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
  author.name.required = True

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
action          lambda x: x       Extra action to be taken except returning value to be used stored in variables
validator       None              Validator can raise :exc:`mrbob.configurator.ValidationError` and question will be asked again
command_prompt  :func:`raw_input` Function that accepts a question and asks user for the answer
help            ""                Extra help returned when user inputs a question mark
=============== ================= =================================================================================================


Validators
----------

Validators are functions with an answer as the only parameter. They may return a value to be used as
an answer and may raise :exc:`ValidationError` for the question to be asked again.

See :mod:`mrbob.validators` for validators that ship with `mr.bob`.
