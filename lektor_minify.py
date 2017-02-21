# Copyright (c) 2017  Pietro Albini <pietro@pietroalbini.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import rcssmin
import rjsmin
from lektor.pluginsystem import Plugin
from lektor.reporter import reporter


MINIFY_FLAG = "minify"
ALLOWED_KINDS = {"css", "js"}


class MinifyPlugin(Plugin):
    name = u"minify"
    description = u"Minify your build artifacts during the build process"

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)

    def on_before_build_all(self, builder, **extra):
        # Prepare some state
        self.seen_artifacts = set()

        try:  # Lektor 3+
            flags = builder.extra_flags
        except AttributeError:  # Lektor 2
            flags = builder.build_flags

        if MINIFY_FLAG in flags:
            if flags[MINIFY_FLAG] == u"minify":
                self.can_minify = set(ALLOWED_KINDS)
            else:
                kinds = set(flags[MINIFY_FLAG].split(","))

                diff = kinds - ALLOWED_KINDS
                for kind in diff:
                    reporter.report_generic(
                        "\033[33mUnknown param for minify:\033[37m %s" % kind
                    )

                self.can_minify = kinds & ALLOWED_KINDS
        else:
            self.can_minify = set()

    def get_minifier_for(self, file_name):
        """Check if the file should be minified and return the minifier"""
        if file_name.endswith(".css") and "css" in self.can_minify:
            return rcssmin.cssmin
        elif file_name.endswith(".js") and "js" in self.can_minify:
            return rjsmin.jsmin
        else:
            return None

    def on_after_build(self, build_state, **extra):
        # Get a list of the new artifacts updated since last event
        artifacts = set(build_state.updated_artifacts) - self.seen_artifacts
        self.seen_artifacts = artifacts

        # Check if the new artifacts should be minified
        for artifact in artifacts:
            name = artifact.dst_filename

            minifier = self.get_minifier_for(name)
            if minifier is None:
                continue

            with artifact.update():
                with artifact.open("r+") as f:
                    content = minifier(f.read())

                    # Rewrite the file in-place
                    f.seek(0)
                    f.write(content)
                    f.truncate()
