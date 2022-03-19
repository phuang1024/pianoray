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

import setuptools


with open("../README.md", "r") as fp:
    long_description = fp.read()

with open("../requirements.txt", "r") as fp:
    requirements = fp.read().strip().split("\n")

setuptools.setup(
    name="pianoray",
    version="0.0.1",
    author="PianoRay Authors",
    author_email="phuang1024@gmail.com",
    description="Video rendering pipeline with piano visualization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/pianoray",
    py_modules=["pianoray"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pianoray = pianoray.__main__:main",
        ]
    },
)
