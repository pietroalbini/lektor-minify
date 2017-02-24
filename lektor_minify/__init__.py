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

import codecs

import rcssmin
import rjsmin
import htmlmin.minify as htmlmin

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter


MINIFY_FLAG = "minify"

# To add new minifiers, you need to add a new matcher and the corresponding
# minifier -- no other code change is needed
MATCHERS = {
    "html": lambda name: name.endswith(".html"),
    "css": lambda name: name.endswith(".css"),
    "js": lambda name: name.endswith(".js"),
}
MINIFIERS = {
    "html": htmlmin.html_minify,
    "css": rcssmin.cssmin,
    "js": rjsmin.jsmin,
}


class MinifyPlugin(Plugin):
    name = u"minify"
    description = u"Minify your build artifacts during the build process"

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)

    def can_minify(self, builder, type):
        """Check if a file type can be minified"""
        try:
            types = builder.__can_minify
        except AttributeError:
            types = self.parse_flags(builder)

        return type in types

    def parse_flags(self, builder):
        """Parse the flags of the provided builder"""
        try:  # Lektor 3+
            flags = builder.extra_flags
        except AttributeError:  # Lektor 2
            flags = builder.build_flags

        types = set()

        allowed_kinds = set(MATCHERS.keys())
        if MINIFY_FLAG in flags:
            if flags[MINIFY_FLAG] == MINIFY_FLAG:
                types = allowed_kinds
            else:
                kinds = set(flags[MINIFY_FLAG].split(","))

                diff = kinds - allowed_kinds
                for kind in diff:
                    reporter.report_generic(
                        "\033[33mUnknown param for flag %s:\033[37m %s"
                        % (MINIFY_FLAG, kind)
                    )

                types = kinds & allowed_kinds

        builder.__can_minify = types
        return types

    def on_after_build(self, builder, build_state, **extra):
        # Get the new artifacts built in this state
        try:
            seen = build_state.__seen_artifacts
        except AttributeError:
            build_state.__seen_artifacts = set()
            artifacts = set(build_state.updated_artifacts)
        else:
            updated = set(build_state.updated_artifacts)
            artifacts = updated - seen

        # This keeps track of the artifacts already built in this build_state,
        # so those files aren't minified multiple times
        build_state.__seen_artifacts |= artifacts

        for artifact in artifacts:
            name = artifact.dst_filename

            for type, matcher in MATCHERS.items():
                if matcher(name) and self.can_minify(builder, type):
                    minifier = MINIFIERS[type]
                    break
            else:
                continue

            with artifact.update():
                with artifact.open("rb+") as f:
                    content = codecs.decode(f.read(), "utf-8")

                    f.seek(0)
                    f.write(codecs.encode(minifier(content), "utf-8"))
                    f.truncate()
