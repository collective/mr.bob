**Mister Bob the Builder** creates directory skeletons.

Documentation
=============

http://mrbob.readthedocs.org/

TODO
====

- [medium] ability to use multiple templates at the same time and depend on them (similar templer structures, but doesnt separate structures and templates)
- [medium] figure out how templates can depend on each other (bobconfig setting with a list of template names?)
- [medium] gittip
- [medium] add +var+ folder in template_sample
- [medium] Check how one would implement multi-namespace python package with current mr.bob api
- [low] document: Consider http://www.stat.washington.edu/~hoytak/code/treedict/overview.html#overview for "variables" storage (it needs C extensions or Cython - this is a blocker)
- [low] Ability to configure what to ignore when copying templates in bobconfig
- [low] better format print questions output (keep order of questions -> use order information like for asking questions)
- [low] document we don't need local commands once answers are remembered (just issue another template on top of current)
- [low] ability to specify answers to questions from cli
- [maybe] ability to simulate rendering (dry-run)
- [maybe] ability to update/patch templates



new templating options TODO:

- variables provide answers, defaults provide defaults
- don't restrict what options are passed to Question
- should we rename validators module to hooks? so next thing we can add is choice pre_question. How do we specify pre_ask_question? maybe just in template
- tests, docs, changelog
- document non-interactive, remember-answers, defaults
- document Question and Configurator
- update mrbob --help output in docs
