**Mister Bob the Builder** creates directory skeletons.

Documentation
=============

http://mrbob.readthedocs.org/

TODO
====

- gittip
- add +var+ folder in template_sample
- [medium] Check how one would implement multi-namespace python package with current mr.bob api
- [medium] validate questions being answered through config files
- [medium] ability to use multiple templates at the same time and depend on them (similar templer structures, but doesnt separate structures and templates)
- [medium] figure out how templates can depend on each other (bobconfig setting with a list of template names?)
- [medium] Consider http://www.stat.washington.edu/~hoytak/code/treedict/overview.html#overview for "variables" storage
- [low] Ability to configure what to ignore when copying templates in bobconfig
- [low] better format print questions output (keep order of questions -> use order information like for asking questions)
- [low] non-interactive support (disable last phase of configuration) - what happens on missing variable: if required, it fails
- [low] document we don't need local commands once answers are remembered (just issue another template on top of current)
- [low] ability to specify answers to questions from cli
- [low] ability to remember answers for the rendered template (goes together with updating/overriding templates)
- [maybe] ability to simulate rendering (dry-run)
- [maybe] ability to update/patch templates
