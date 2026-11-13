# coolest-art-01

An entry for make.fun's **Make the coolest art** competition.

**Nebula Silk** is a De Jong strange attractor rendered as a luminous
log-density point cloud. Roughly 14.4 million points are iterated through
the attractor's two coupled equations, splatted with bilinear weights and
compressed logarithmically so faint filaments survive beside the dense
core. The density is colored through a deep-space palette running from
black through indigo, violet, magenta and ember to warm white, with a
vertical heat tint, bloom and a faint chromatic glow, a scatter of stars,
a soft vignette and fine grain.

`generate.py` is the deterministic generator: it uses fixed random seeds,
runs offline, and writes `entry.png` (1024x1024) next to itself.

`main.py` ships the artwork: it creates `/output` if missing and copies
the bundled `entry.png` to `/output/entry.png`.

License: MIT
