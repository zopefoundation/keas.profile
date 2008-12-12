##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
# Portions copyright (c) 2005 Ian Bicking and contributors; written for Paste
# (http://pythonpaste.org) and licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php
#
###############################################################################
"""WSGI Profiler Middleware.

$Id$
"""

import cgi
import threading
import cProfile
import pstats
from cStringIO import StringIO

from paste import response


class ProfileMiddleware(object):
    """Middleware that profiles all requests.

    This is a fork of paste.debug.profile.ProfileMiddleware.  It uses
    cProfile instead of hotshot (which is buggy).  It doesn't cause the
    truncate the profiler output to be truncated in the browser.  It sorts
    the stats by cumulative time rather than internal time.

    If the following bugs were fixed upstream, we could switch to paste.debug
    again:

        http://trac.pythonpaste.org/pythonpaste/ticket/204
        http://trac.pythonpaste.org/pythonpaste/ticket/311
        http://trac.pythonpaste.org/pythonpaste/ticket/312

    However upstream says at leas one of those won't be fixed, and suggests
    we look into better-maintained WSGI profiler middleware products such as
    repoze.profile or Dozer.
    """

    style = ('clear: both; background-color: #ff9; color: #000; '
             'border: 2px solid #000; padding: 5px;')

    def __init__(self, app, global_conf=None,
                 log_filename='profile.log.tmp',
                 limit=40):
        self.app = app
        self.lock = threading.Lock()
        self.log_filename = log_filename
        self.limit = limit

    def __call__(self, environ, start_response):
        catch_response = []
        body = []
        def replace_start_response(status, headers, exc_info=None):
            catch_response.extend([status, headers])
            start_response(status, headers, exc_info)
            return body.append
        def run_app():
            app_iter = self.app(environ, replace_start_response)
            try:
                body.extend(app_iter)
            finally:
                if hasattr(app_iter, 'close'):
                    app_iter.close()
        self.lock.acquire()
        try:
            profiler = cProfile.Profile()
            profiler.runctx("run_app()", globals(), locals())
            body = ''.join(body)
            headers = catch_response[1]
            content_type = response.header_value(headers, 'content-type')
            if content_type is None or not content_type.startswith('text/html'):
                # We can't add info to non-HTML output
                return [body]
            stream = StringIO()
            stats = pstats.Stats(profiler, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('cumulative', 'calls')
            stats.print_stats(self.limit)
            output = stream.getvalue()
            stream.reset()
            stream.truncate()
            stats.print_callers(self.limit)
            output_callers = stream.getvalue()
            stream.close()
            body += '<pre style="%s">%s\n%s</pre>' % (
                self.style, cgi.escape(output), cgi.escape(output_callers))
            response.replace_header(headers, 'Content-Length', str(len(body)))
            try:
                import pyprof2calltree
            except ImportError:
                pass
            else:
                # Use kcachegrind to view the profile interactively.
                pyprof2calltree.convert(profiler.getstats(),
                                        self.log_filename + '.kgrind')
            return [body]
        finally:
            self.lock.release()


def make_profiler(app, global_conf, **local_conf):
    """Create the Profiler app."""
    return ProfileMiddleware(app, global_conf)

