Mister Bob the Builder renders directory skeleton to a target directory.

More: http://mrbob.readthedocs.org/

TODO
====

- [high] rename .tmpl to .mrbob?
- [high] better format print questions output
- [high] Support http zip files and extract template https://github.com/iElectric/bobtemplates.ielectric/downloads/zip:pyramid_template/
- [high] Write template for quickstarter to write new templates
- [high] write a sample template to start with (foobar template)
- [high] ability to configure what to ignore when copying templates in bobconfig
- [high] write usermanual/developermanual (diagram how it works)
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
