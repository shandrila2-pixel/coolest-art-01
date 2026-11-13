# Nebula Silk - notes

Nebula Silk is the concept: a strange attractor that reads like a sheet of
interstellar gas. The structure is purely mathematical, but the palette,
bloom and star field are picked so it looks like a nebula, not a plot.

The shape comes from the De Jong strange attractor. Four parameters (a, b, c, d)
define two coupled recurrences, x' = sin(a*y) - cos(b*x) and
y' = sin(c*x) - cos(d*y). Millions of points pass through this map, and because
it is nonlinear and dissipative they collapse onto a bounded, filamentary
structure with no closed form.

A short pre-pass finds where that structure lives, so the image auto-centers
for any parameters: it burns 20,000 points for 120 iterations, rotates them by
the same -8 degrees the final frame uses, and takes the 0.5th and 99.5th
percentiles per axis. Their midpoint becomes the center and their padded span
becomes the scale.

Rendering is a log-density histogram. About 1.6M points are iterated nine times
each, for 14.4M splats, each mapped to pixel space and spread over its four
neighbors with bilinear weights to avoid nearest-pixel hard edges. Counts are
compressed with log1p so faint filaments survive beside the dense core, then a
uniform noise floor is subtracted so empty space stays deep black.

Color passes through an eight-stop deep-space palette (near-black, indigo,
violet, magenta, ember orange, warm white). A vertical heat tint scales density
up toward the bottom, so the top stays cold indigo while the lower half glows
ember; the tint is multiplicative, so the background stays uniformly dark.

Highlights are lifted by synthetic bloom: a bright mask blurred at two radii and
combined, then split into per-channel copies offset a few pixels, red one way
and blue the other, for a subtle chromatic glow at hot edges. A 150-star field,
a soft vignette and fine gaussian grain add texture, and every random step draws
from fixed numpy seeds, so the generator reproduces the same PNG byte for byte.
