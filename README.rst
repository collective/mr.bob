Mister Bob the Builder renders directory skeleton to a target directory.

More: http://mrbob.readthedocs.org/

TODO
====

- [medium] Consider http://www.stat.washington.edu/~hoytak/code/treedict/overview.html#overview for variables storage
- [medium] Ability to configure what to ignore when copying templates in bobconfig
- [medium] validate questions being answered through config files
- [medium] better format print questions output
- [medium] non-interactive support (disable last phase of configuration)
- [medium] figure out how templates can depend on each other (bobconfig setting with a list of template names?)
- [medium] ability to use multiple templates at the same time and depend on them (similar templer structures, but doesnt separate structures and templates)
- [low] ability to have localcommands (maybe we dont need that because of multiple templates?)
- [low] ability to specify pre/post functions when rendering templates
- [low] ability to specify actions to answers, for example if one question was answered, another template may be triggered
- [low] ability to specify answers to questions from cli
- [low] ability to simulate rendering (dry-run)
- [low] ability to rewrite templates
- [low] ability to remember answers for the rendered template (goes together with updating/overriding templates)
