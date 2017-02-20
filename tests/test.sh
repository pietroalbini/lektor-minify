#!/bin/bash
set -euo pipefail

EXPECTED_CSS='body{color:#fff}'
EXPECTED_JS='function test(){console.log("test");}'

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
    echo lektor build -O "${TMP_DIRECTORY}" $@
    lektor build -O "${TMP_DIRECTORY}" $@
}

assert_style() {
    outcome="$1"

    content="`cat "${TMP_DIRECTORY}/static/style.css"`"
    if [[ "${content}" = "${EXPECTED_CSS}" ]]; then
        [[ "${outcome}" = "true" ]] || fail css
    else
        [[ "${outcome}" = "false" ]] || fail css
    fi
}

assert_script() {
    outcome="$1"

    content="`cat "${TMP_DIRECTORY}/static/script.js"`"
    if [[ "${content}" = "${EXPECTED_JS}" ]]; then
        [[ "${outcome}" = "true" ]] || fail js
    else
        [[ "${outcome}" = "false" ]] || fail js
    fi
}

fail() {
    echo "Failed $@"
    exit 1
}


echo "Testing with no flags..."
build
assert_style false
assert_script false

echo "Testing with the minify-assets flag..."
build -f minify-assets
assert_style true
assert_script true

echo "Testing with the minify-css flag..."
build -f minify-css
assert_style true
assert_script false

echo "Testing with the minify-js flag..."
build -f minify-js
assert_style false
assert_script true

rm -rf "${TMP_DIRECTORY}"
