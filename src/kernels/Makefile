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

JUNIT = ../../../lib/hamcrest-core-1.3.jar:../../../lib/junit-4.13.2.jar

.PHONY: java junit python

java:
	mkdir -p ../../build/kernels/$(KERNEL)
	cd ./$(KERNEL); \
	ls | grep -F ".java" | grep -v "JUTest.java" | xargs javac
	cp ./$(KERNEL)/*.class ../../build/kernels/$(KERNEL)

junit:
	cd ./$(KERNEL); \
	javac -cp .:$(JUNIT) JUTest.java; \
	java -cp .:$(JUNIT) JUTest

python:
	mkdir -p ../../build/kernels/$(KERNEL)
	cp ./$(KERNEL)/*.py ../../build/kernels/$(KERNEL)
