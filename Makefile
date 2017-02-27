# Copyright (c) 2016-2017  Pietro Albini <pietro@pietroalbini.org>
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

# Configuration
SOURCE = lektor_minify
PACKAGES_OUT = build/packages

# Uploading configuration
RELEASES_SERVER = files@winter.net.pietroalbini.org
RELEASES_DIR = public/releases/$(NAME)/$(shell $(PYTHON) setup.py --version)

# Executables
PYTHON = python3
GPG = gpg
TWINE = twine

.PHONY: build sign _pre-sign upload test clean


# Basic packages building

build: $(PACKAGES_OUT)/*.tar.gz $(PACKAGES_OUT)/*.whl

$(PACKAGES_OUT):
	@mkdir -p $(PACKAGES_OUT)

$(PACKAGES_OUT)/*.tar.gz: $(PACKAGES_OUT) setup.py $(wildcard $(SOURCE)/*)
	@$(PYTHON) setup.py sdist -d $(PACKAGES_OUT)

build/packages/*.whl: $(PACKAGES_OUT) setup.py $(wildcard $(SOURCE)/*)
	@$(PYTHON) setup.py bdist_wheel -d $(PACKAGES_OUT)


# Packages signing

sign: _pre-sign $(addsuffix .asc,$(filter-out $(wildcard $(PACKAGES_OUT)/*.asc),$(wildcard $(PACKAGES_OUT)/*)))

_pre-sign:
	@rm -f $(PACKAGES_OUT)/*.asc

$(PACKAGES_OUT)/%.asc:
	@$(GPG) --detach --armor --sign $(PACKAGES_OUT)/$*


# Packages uploading

upload: build sign
	@ssh $(RELEASES_SERVER) -- mkdir -p $(RELEASES_DIR)
	@scp $(PACKAGES_DIR)/* $(RELEASES_SERVER):$(RELEASES_DIR)
	@$(TWINE) upload --config-file .pypirc -r upload --skip-existing $(PACKAGES_OUT)/*


# Testing

test:
	@tests/test.sh


# Cleanup

clean:
	@rm -rf build
	@rm -rf tests/tmp
	@find -name "*.pyc" -delete
	@rm -rf $(SOURCE).egg-info
