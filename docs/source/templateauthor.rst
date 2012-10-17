Writing your own template
=========================


Starting
--------

Writing your own template is as easy as creating a `.mrbob.ini` that may contain questions. Everything else is extra.

Templating
----------

TODO: document that jinja templating has extra configuration

Writing Questions
-----------------

``questions`` section reference
*******************************

=============== ================= ===========================================================================
  Parameter         Default          Explanation
=============== ================= ===========================================================================
name                              Required. Unique identifier for the question.
question                          Required. Question given interactively to a user when generating structure
default         None              Default value when no answer is given. Can be a `dotted notation`.
required        False
action          lambda x: x
validator       None
command_prompt  :func:`raw_input`
help            ""
=============== ================= ===========================================================================
