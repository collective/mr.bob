Mister Bob the Builder renders directory structure templates.

More: http://mrbob.readthedocs.org/

TODO
====

- [high] write usermanual/developermanual (diagram how it works)
- [high] non-interactive support (disable last phase of configuration)
- [high] ability to configure what to ignore when copying templates in bobconfig
- [high] write a sample template to start with (foobar template)
- [high] figure out how templates can depend on each other (bobconfig setting with a list of template names?)
- [high] ability to use multiple templates at the same time and depend on them (similar templer structures, but doesnt separate structures and templates)
- [high] Support http zip files and extract template https://github.com/iElectric/bobtemplates.ielectric/downloads/zip:pyramid_template/
- [low] ability to have localcommands (maybe we dont need that because of multiple templates?)
- [low] ability to specify pre/post functions when rendering templates
- [low] ability to specify actions to answers, for example if one question was answered, another template may be triggered
- [low] ability to specify answers to questions from cli
- [low] ability to simulate rendering (dry-run)
- [low] ability to rewrite templates
- [low] ability to remember answers for the rendered template (goes together with updating/overriding templates)
