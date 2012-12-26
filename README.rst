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
- [medium] write/test/document choice question type and corresponding pre_ask_question, post_ask_question
- [low] Ability to configure what to ignore when copying templates in bobconfig
- [low] better format print questions output (keep order of questions -> use order information like for asking questions)
- [low] document we don't need local commands once answers are remembered (just issue another template on top of current)
- [low] ability to specify variables/defaults to questions from cli
- [maybe] ability to simulate rendering (dry-run)
- [maybe] ability to update/patch templates
