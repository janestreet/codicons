# The script can be run as
# $ cd lib/codicons/src
# $ python3 ./generate.py svg.ml LICENSE

from subprocess import run
from os import listdir
from sys import argv
from shutil import copyfile


run(["git", "clone", "https://github.com/microsoft/vscode-codicons.git", "./repo"])

for icon in listdir("../custom"):
    copyfile(f"../custom/{icon}", f"./repo/src/icons/{icon}")

icons = [icon for icon in listdir("./repo/src/icons") if icon.endswith(".svg")]
icons.sort()

svgs_16_16 = []
svgs_24_24 = []
for icon in icons:
    with open(f"./repo/src/icons/{icon}", "r") as f:
        svg = f.read()
        if 'viewBox="0 0 16 16"' in svg:
            svg = svg.replace(
                '<svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" fill="currentColor">',
                "",
            ).replace("</svg>", "")
            svgs_16_16.append((icon[:-4], svg))
        elif 'viewBox="0 0 24 24"' in svg:
            svg = svg.replace(
                '<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor">',
                "",
            ).replace("</svg>", "")
            svgs_24_24.append((icon[:-4], svg))


def varname(name):
    return name.replace("-", "_").capitalize()


def escape(svg):
    return svg.replace('"', '\\"')


type_def = """type t =
"""
type_def += "  (* 16x16 *)\n"
for name, _ in svgs_16_16:
    type_def += f"  | {varname(name)}\n"
type_def += "  (* 24x24 *)\n"
for name, _ in svgs_24_24:
    type_def += f"  | {varname(name)}\n"
type_def += "[@@deriving enumerate, sexp_of]\n"


svg_function = """
let svg = function
"""
svg_function += "  (* 16x16 *)\n"
for name, svg in svgs_16_16:
    svg_function += f'  | {varname(name)} -> "{escape(svg)}"\n'
svg_function += "  (* 24x24 *)\n"
for name, svg in svgs_24_24:
    svg_function += f'  | {varname(name)} -> "{escape(svg)}"\n'


frame_function = """
let frame = function
"""
frame_function += "  (* 16x16 *)\n"
for name, svg in svgs_16_16:
    frame_function += f"  | {varname(name)}\n"
frame_function += "  -> 16\n"
frame_function += "  (* 24x24 *)\n"
for name, svg in svgs_24_24:
    frame_function += f"  | {varname(name)}\n"
frame_function += "  -> 24\n"


with open(argv[1], "w") as f:
    f.write(type_def + svg_function + frame_function)

run(["mv", "./repo/LICENSE", argv[2]])
run(["rm", "-rf", "./repo"])
