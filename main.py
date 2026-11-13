import os
import shutil

# make.fun entry — coolest-art-01 ("Make the coolest art")
# Writes the competition's entry image to /output/entry.png.
# The image is bundled in this repository (entry.png): "Nebula Silk",
# a De Jong strange attractor rendered as log-density point clouds
# (14.4M points), auto-centered, colored through a deep-space palette
# (black → indigo → violet → magenta → ember → white) with a vertical
# heat tint, bloom with chromatic glow, star field, vignette and fine
# grain. numpy + PIL, fully deterministic (fixed seeds), no network.
# generate.py holds the full generator for reference.

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")

os.makedirs("/output", exist_ok=True)
shutil.copyfile(src, "/output/entry.png")
print("wrote /output/entry.png")
# deterministic: same input image → same output bytes every run
# Entry for make.fun coolest-art-01 bounty ($250 USDC on Solana)

