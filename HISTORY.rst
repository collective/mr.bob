Changelog
=========
    

0.1a7 (2013-01-23)
------------------

- Don't depend on argparse in python 2.7 and higher, since it's already
  in stdlib
  [Domen Kožar]

- #22: Prevent users from specifying target directory inside template dir
  [Domen Kožar]


0.1a6 (2013-01-02)
------------------

- Use ``StrictUndefined`` with jinja2 renderer so that any missing key is
  reported as an error
  [Domen Kožar]

- If a key in a namespace was missing while rendering, no error was raised
  [Domen Kožar]

- Added hook ``mrbob.hooks.show_message``
  [Domen Kožar]

- ``mrbob.validators.boolean`` renamed to ``mrbob.hooks.to_boolean``
  [Domen Kožar]

- Renamed ``validators.py`` to ``hooks.py``
  [Domen Kožar]

- Removed ``validators`` and ``action`` settings from ``[questions]`` as it is
  superseded by hooks
  [Domen Kožar]

- Added ``pre_ask_question`` and ``post_ask_question`` to ``[questions]`` section
  [Domen Kožar]
  
- Added ``pre_render``, ``post_render`` and  ``post_render_msg`` options
  [Domen Kožar]

- Added ``[defaults]`` section that will override template defaults. The only
  difference to ``[variables]`` is that variables provide default answers
  [Domen Kožar]

- Moved ``renderer`` parameter to ``[template]`` section
  [Domen Kožar]

- Added ``[template]`` section that is parsed only from ``.mrbob.ini`` inside a
  template directory.
  [Domen Kožar]

- Correctly evaluate boolean of ``quiet`` and ``verbose`` settings
  [Domen Kožar]

- Added ``non_interactive`` setting that will not prompt for any input and fail
  if any of required questions are not answered
  [Domen Kožar]

- Added ``remember_answers`` setting that will create ``.mrbob.ini`` file inside
  rendered directory with all the answers written to ``[variables]`` section
  [Domen Kožar]

- Include changelog in documentation
  [Domen Kožar]

- ``Question`` does no longer raise error if unknown parameter is passed from a
  config file. Instead those parameters are saved to ``question.extra`` that can
  be later inspected and validated. This is first step to have advanced question
  types such as question with a set of predefined answers
  [Domen Kožar]

- Rewrite all py.test stuff to nosetests, so we have unified testing now. This
  also fixes flake8 segfaults on pypy
  [Domen Kožar]


0.1a5 (2012-12-12)
------------------

- #26: Variables were not correctly parsed from config files
  [Domen Kožar]


0.1a4 (2012-12-11)
------------------

- Fix MANIFEST.in so that template examples are also included with distribution
  [Domen Kožar]

- Add -q/--quiet option to suppress output which isn't strictly necessary
  [Sasha Hart]

- Suppress the interactive-mode welcome banner if there are no questions to ask
  [Sasha Hart]

- Don't raise KeyError: 'questions_order' if [questions] is missing in an ini
  [Sasha Hart]


0.1a3 (2012-11-30)
------------------

- #13: Read user config from ~/.mrbob (as stated in docs and inline comments).
  [Andreas Kaiser]


0.1a2 (2012-11-29)
------------------

- #12: Fix unicode errors when using non-ASCII in questions or defaults
  [Domen Kožar]

- Ask questions in same order they were
  defined in template configuration file
  [Domen Kožar]


0.1a1 (2012-10-19)
------------------

- Initial release.
  [Domen Kožar, Tom Lazar]
