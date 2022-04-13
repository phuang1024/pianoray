#
#  PianoRay
#  Piano performance visualizer.
#  Copyright  PianoRay Authors  2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

PYTHON = python3

.PHONY: help wheel install docs all

help:
	@echo Makefile help:
	@echo - make wheel: Build wheel in ./build
	@echo - make install: Install wheel file
	@echo - make docs: Documentation.
	@echo - make all: Uninstall, build, install, docs.
	@echo   Useful for developers.

wheel:
	mkdir -p ./build
	rm -rf ./build/pianoray ./build/build ./build/dist ./build/*.egg-info
	cp -r ./src ./build/pianoray
	cp ./setup.py ./MANIFEST.in ./build
	cd ./build; \
	$(PYTHON) setup.py bdist_wheel sdist

install:
	$(PYTHON) -m pip install ./build/dist/*.whl

docs:
	cd ./docs; \
	rm -rf _build; \
	mkdir -p _static _templates; \
	make html SPHINXOPTS="-W --keep-going"

all:
	$(PYTHON) -m pip uninstall -y pianoray
	make wheel
	make install
	make docs
