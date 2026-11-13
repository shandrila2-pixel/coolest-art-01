# make.fun entry: coolest-art-01 - "Nebula Silk"
#
# Nebula Silk is a De Jong strange attractor drawn as a luminous
# log-density point cloud and colored through a deep-space palette
# (black -> indigo -> violet -> magenta -> ember -> white), with a
# vertical heat tint, bloom and a subtle chromatic glow, a faint star
# field, a soft vignette and fine grain. Every random step uses fixed
# seeds, so the rendering is fully deterministic.
#
# This file only ships the artwork: it creates /output if missing and
# copies the bundled entry.png (kept next to this script) to
# /output/entry.png. The full generator is generate.py.

import os
import shutil

source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
target_dir = "/output"
target = os.path.join(target_dir, "entry.png")

os.makedirs(target_dir, exist_ok=True)
shutil.copyfile(source, target)
print("wrote", target)
