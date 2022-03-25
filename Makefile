#
#  PianoRay
#  Video rendering pipeline with piano visualization.
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

.PHONY: driver kernels test install clean docs

driver:
	rm -rf ./build/driver
	mkdir -p ./build/driver
	rm -rf ./build/pianoray
	cp -r ./src/driver ./build/pianoray
	cd ./build; \
	python ./setup.py bdist_wheel sdist; \
	mv -f ./build ./dist ./*.egg-info ./driver

kernels:
	cd ./src/kernels; \
	make python KERNEL=midi; \
	make java KERNEL=jtest; \
	make python KERNEL=pytest; \
	make cpp KERNEL=ctest; \

test:
	cd ./src/kernels; \
	make junit KERNEL=jtest; \

install:
	pip install ./build/driver/dist/*.whl

clean:
	find -name "*.class" | grep -v build | xargs rm -f
	rm -rf ./build/pianoray
	rm -rf ./build/driver/build ./build/driver/*.egg-info

docs:
	cd ./docs; \
	make html
