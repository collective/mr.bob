Mister Bob the Builder renders directory skeleton to a target directory.

More: http://mrbob.readthedocs.org/

TODO
====

- gittip
- add +var+ folder in template_sample
- [medium] validate questions being answered through config files
- [medium] figure out how templates can depend on each other (bobconfig setting with a list of template names?)
- [medium] ability to use multiple templates at the same time and depend on them (similar templer structures, but doesnt separate structures and templates)
- [medium] Ability to configure what to ignore when copying templates in bobconfig
- [medium] better format print questions output
- [medium] Check how one would implement multi-namespace python package with current mr.bob api
- [medium] Consider http://www.stat.washington.edu/~hoytak/code/treedict/overview.html#overview for "variables" storage
- [medium] non-interactive support (disable last phase of configuration) - what happens on missing variable?
- [low] ability to have localcommands (maybe we dont need them because you can just use another template on top of template) - document this
- [low] ability to specify answers to questions from cli
- [low] ability to simulate rendering (dry-run)
- [low] ability to rewrite templates
- [low] ability to remember answers for the rendered template (goes together with updating/overriding templates)


[high] parse mr.bob section in templates (determine how that goes into configuration chain):

::

    [mr.bob]
    post_render_msg = Balblablalba
    pre_render(all stuff passed to render())
    post_render
    pre_ask_question(question, questions, more?)
    post_ask_question

Add **advanced templating** docs section:

- remove action in favor of post_ask_question
- default may require input from previous answers (for example url of documentation may propose package.rtfd.org link for docs) -> use pre_ask_question to set default value
- ability to conditionally render a file -> use post_render and delete the file if needed
- if one question was answered, another template may be triggered -> use post_ask_question and use api to do whatever
- question may be asked if another question is answered in a certain way -> use post_ask_question and add another question (is that possible if we are looping through questions? -> While questions: questions.pop())
