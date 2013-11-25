
.. _`writing your plugin`:

Writing your own plugin
=========================


render_filename plugin
-----------------------

With your own plugin you can extend or override ``render_filename`` in a very flexible way.

structure
**********

A render_filename plugin class must have an **order** attribute (optional but fully recommended) and a **get_filename** method.

.. warning:: If it doesn't provide this method an ErrorAttribute is raised.

`get_filename` must return a tuple where the first element is the rended new filename, and the second a boolean 



plugin sample

.. code-block:: python
  
 class NoBarInFilename():
    order = 15

    def __init__(self, filename, variables, will_continue=True):
        self.filename = filename
        self.variables = variables
        self.will_continue = will_continue

    def get_filename(self):
        if 'bar' in self.filename:
            self.filename = None
        else:
            self.filename = 'fake_foo_' + self.filename
        
        return self.filename, self.will_continue
 
code behavior

.. literalinclude:: ../../mrbob/rendering.py
   :lines: 133-143


If filename is None or the boolean is False,  filename is immediatly returned, otherwise new filename will be interpreted  over the mrbob render_filename function.


Register your plugin(s) 
************************

You register your plugin(s) to mrbob with classic setuptools entrypoints within your setup.py egg file.

    .. code-block:: python

        entry_points='''
        # -*- Entry points: -*-
        [mr.bob.plugins]
        render_filename=bobplugins.pkg.module:NoFooInFilename
        render_filename=bobplugins.pkg.module:NoBarInFilename
        render_filename=bobplugins.pkg.module:NeitherBarOrFooInFilename

        ''',

Here we have 3 render_filename plugins, assume that :

 + NoFooInFilename  `order` attribute is 10
 + NoBarInFilename  `order` attribute is 15
 + NeitherBarOrFooInFilename  `order` attribute is 20

If you don't specify a  `-r, --rdr-fname-plugin-target`  NeitherBarOrFooInFilename will be loaded due to its order attribute, higher is prefered.

If you want to load NoBarInFilename, just invoque mr bob with -r 15 . If you target a non registered `order` an ErrorAttribute is raised ::
 
 AttributeError: No plugin target 18 ! Registered are [10, 15, 20]

If you register 2 max order plugins, an alphabetical asc sort based on namespace-pkg-classname will return the last
