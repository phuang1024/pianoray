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

import sys
import json

from blocks import compute_blocks
from filter import filter_midi
from length import length


def main():
    print("STARTED", file=sys.stderr)
    inp = json.loads(sys.stdin.readline())["midi"]

    if inp["type"] == "length":
        out = length(inp)
    elif inp["type"] == "filter":
        out = filter_midi(inp)
    elif inp["type"] == "blocks":
        out = compute_blocks(inp)
    else:
        raise TypeError("Type {} not allowed.".format(inp["type"]))

    out = {"midi": out}
    json.dump(out, sys.stdout)
    print(flush=True)
    sys.stdout.close()


if __name__ == "__main__":
    while True:
        main()
