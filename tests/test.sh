#!/bin/bash
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

set -euo pipefail

EXPECTED_CSS='body{color:#fff}'
EXPECTED_JS='function test(){console.log("test");}'
EXPECTED_HTML='<html><head></head><body><div>This is a test ✅</div></body></html>'
EXPECTED_FILTER_MIN='<html><head><style>body{color:#fff}</style></head><body></body></html>'
EXPECTED_FILTER_NO_MIN='<style>
    body{color:#fff}
</style>'

# Detect source directory
# Thanks to http://stackoverflow.com/a/246128/2204144
source="$0"
while [ -h "${source}"  ]; do
    dir="$( cd -P "$( dirname "${source}" )" && pwd )"
    source="$(readlink "${source}")"
done
BASE="$( cd "$( dirname "${source}" )" && pwd )"

TEST_PROJECT="${BASE}/project"
TMP_DIRECTORY="${BASE}/tmp"


build() {
    cd "${TEST_PROJECT}"
    rm -rf "${TMP_DIRECTORY}"
    lektor build -O "${TMP_DIRECTORY}" $@
}

assert() {
    name="$1"
    file="$2"
    expected="$3"
    outcome="$4"

    content="`cat "${TMP_DIRECTORY}/${file}"`"
    if [[ "${content}" == "${expected}" ]]; then
        [[ "${outcome}" = "true" ]] || fail "${name}"
    else
        [[ "${outcome}" = "false" ]] || fail "${name}"
    fi
}

assert_html() { assert html index.html "${EXPECTED_HTML}" "$1"; }
assert_style() { assert css static/style.css "${EXPECTED_CSS}" "$1"; }
assert_script() { assert js static/script.js "${EXPECTED_JS}" "$1"; }
assert_filter_min() { assert filter filter.html "${EXPECTED_FILTER_MIN}" "$1"; }
assert_filter_no_min() { assert filter filter.html "${EXPECTED_FILTER_NO_MIN}" "$1"; }

fail() {
    echo "Failed $@"
    exit 1
}


echo "Testing with no flags..."
build
assert_html false
assert_style false
assert_script false
assert_filter_no_min true

echo "Testing with the minify flag..."
build -f minify
assert_html true
assert_style true
assert_script true
assert_filter_min true

echo "Testing with the minify:css flag..."
build -f minify:css
assert_html false
assert_style true
assert_script false
assert_filter_no_min true

echo "Testing with the minify:js flag..."
build -f minify:js
assert_html false
assert_style false
assert_script true
assert_filter_no_min true

echo "Testing with the minify:html flag..."
build -f minify:html
assert_html true
assert_style false
assert_script false
assert_filter_min true

echo "Testing with the minify:css,js,html flag..."
build -f minify:css,js,html
assert_html true
assert_style true
assert_script true
assert_filter_min true

echo "Test successful!"
rm -rf "${TMP_DIRECTORY}"
