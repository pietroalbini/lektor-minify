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


MINIFY_ALL_FLAG = "minify-assets"
MINIFY_CSS_FLAG = "minify-css"
MINIFY_JS_FLAG = "minify-js"


class MinifyAssetsPlugin(Plugin):
    name = u"minify-assets"
    description = u"Minify your CSS and JS files during the Lektor build"

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)

    def on_before_build_all(self, builder, **extra):
        # Prepare some state
        self.seen_artifacts = set()

        try:  # Lektor 3+
            flags = builder.extra_flags
        except AttributeError:  # Lektor 2
            flags = builder.build_flags

        if MINIFY_ALL_FLAG in flags:
            self.can_minify_css = True
            self.can_minify_js = True
        else:
            self.can_minify_css = MINIFY_CSS_FLAG in flags
            self.can_minify_js = MINIFY_JS_FLAG in flags

    def get_minifier_for(self, file_name):
        """Check if the file should be minified and return the minifier"""
        if file_name.endswith(".css") and self.can_minify_css:
            return rcssmin.cssmin
        elif file_name.endswith(".js") and self.can_minify_js:
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
