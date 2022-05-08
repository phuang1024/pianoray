"""
Automatically generated documentation for properties.
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.realpath(__file__))

# Using list instead of dict because order matters.
PROP_ATTRS = [
    ("name", "Name"),
    ("desc", "Description"),
    ("animatable", "Animatable"),
    ("mods", "Modifiers"),
    ("default", "Default"),
    ("min", "Minimum"),
    ("max", "Maximum"),
    ("min_len", "Min Length"),
    ("max_len", "Max Length"),
    ("isdir", "Is Directory"),
    ("isfile", "Is File"),
]


def write_header(fp):
    fp.write("Properties\n==========\n\n"
        "Automatically generated property docs.\n\n")


def doc_prop(fp, pgroup_idname, idname, prop):
    fp.write(f"- ``scene.{pgroup_idname}.{idname}``: "
        f":class:`~pianoray.{type(prop).__name__}`\n")

    for attr, name in PROP_ATTRS:
        if hasattr(prop, attr):
            v = getattr(prop, attr)
            if v is None:
                continue

            if attr == "mods":
                v = ", ".join(type(x).__name__ for x in v)

            if (
                attr == "isdir" and not v or
                attr == "isfile" and not v or
                attr == "mods" and len(v) == 0
                ):
                continue

            if attr not in ("name", "desc"):
                v = "``" + str(v) + "``"
            fp.write(f"   :{name}: {v}\n")

def doc_pgroup(fp, name, idname, annotations):
    fp.write("{}\n{}\n\n".format(name, "-"*len(name)))

    for prop_id, prop in annotations.items():
        doc_prop(fp, idname, prop_id, prop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output RST file.",
        required=True)
    args = parser.parse_args()

    sys.path.insert(0, os.path.dirname(ROOT))

    import pianoray
    scene = pianoray.api.DefaultScene

    with open(args.output, "w") as fp:
        write_header(fp)

        for key in sorted(scene._pgroups.keys()):
            cls = type(scene._pgroups[key])
            doc_pgroup(fp, cls.__name__, key, cls.__annotations__)
            fp.write("\n")


if __name__ == "__main__":
    main()
