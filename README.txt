===================
Profiler middleware
===================

This package provides middleware for profiling of the application.  It's based
on `paste.debug.profile <http://pythonpaste.org/modules/debug.profile.html>`_,
but uses cProfile instead of hotshot.

If you use PasteScript, enabling the profiler is as simple as adding ::

  [filter-app:profile]
  use = egg:keas.profile#profiler
  next = main

to your paster configuration file and passing ``--app-name=profile`` to
``paster``.  When you access your web application, every page will have the
profiler output appended to the end of the document body.


Viewing profiles with KCacheGrind
---------------------------------

KCacheGrind is a GUI application for digging through the profile data and
visualizing call trees.  keas.profile uses pyprof2calltree to convert the
profiler data into KCacheGrind format for your convenience.  To view it,
open the log file (``profile.log.tmp.kgrind`` by default) in KCacheGrind.
