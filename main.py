import os
import shutil

# make.fun entry — coolest-art-01 ("Make the coolest art")
# Writes the competition's entry image to /output/entry.png.
# The image is bundled in this repository (entry.png) and is a
# deterministic render: a De Jong strange attractor colored by
# point density (near-black → deep blue → violet → magenta → orange → white),
# 4000 walkers × 6000 steps ≈ 24M points, numpy + PIL.
# generate.py holds the full generator for reference.

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")

os.makedirs("/output", exist_ok=True)
shutil.copyfile(src, "/output/entry.png")
print("wrote /output/entry.png")
