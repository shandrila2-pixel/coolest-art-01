# coolest-art-01 entry v4: density-colored strange attractor
import math, os
import numpy as np
from PIL import Image, ImageFilter, ImageChops

W = H = 2048
a, b, c, d = 1.641, 1.902, 0.316, 1.525

WALKERS = 4000
STEPS = 6000  # 24M points
xs = np.random.uniform(-2, 2, WALKERS)
ys = np.random.uniform(-2, 2, WALKERS)

dens = np.zeros((H, W), dtype=np.float32)
cx, cy = W * 0.5, H * 0.52
scale = W * 0.30

for s in range(STEPS):
    nx = np.sin(a * ys) - np.cos(b * xs)
    ny = np.sin(c * xs) - np.cos(d * ys)
    xs, ys = nx, ny
    if s < 20:
        continue
    px = (cx + xs * scale).astype(np.int64)
    py = (cy + ys * scale * 0.9).astype(np.int64)
    ok = (px >= 0) & (px < W) & (py >= 0) & (py < H)
    np.add.at(dens, (py[ok], px[ok]), 1.0)

# --- density -> color: multi-stop gradient (near-black -> deep blue -> violet -> magenta -> orange -> white)
dmax = np.log1p(dens)
dmax /= (dmax.max() + 1e-9)
t = np.clip(dmax, 0, 1) ** 0.62

stops_t = [0.00, 0.18, 0.38, 0.55, 0.75, 0.90, 1.00]
stops_r = [3, 10, 70, 190, 255, 255, 255]
stops_g = [5, 25, 30, 40, 110, 210, 255]
stops_b = [20, 110, 160, 200, 60, 160, 255]
r = np.interp(t, stops_t, stops_r)
g = np.interp(t, stops_t, stops_g)
bch = np.interp(t, stops_t, stops_b)

img = np.dstack([r, g, bch]).astype(np.uint8)
out = Image.fromarray(img, 'RGB')

# background stars
st = Image.new('RGB', out.size, (1, 2, 8))
sd = ImageDraw = None
import random
from PIL import ImageDraw
sd = ImageDraw.Draw(st)
random.seed(5)
for _ in range(700):
    x, y = random.randint(0, W - 1), random.randint(0, H - 1)
    rr = random.choice([1, 1, 2])
    aa = random.randint(30, 130)
    sd.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(int(aa * 0.8), int(aa * 0.85), aa))
mask = out.convert('L').point(lambda p: min(255, int((p / 255) ** 0.5 * 255)))
final = Image.composite(out, st, mask)

# bloom
bloom = final.filter(ImageFilter.GaussianBlur(5))
final = ImageChops.add(final, bloom.point(lambda p: int(p * 0.35)))
final = final.resize((1024, 1024), Image.LANCZOS)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')
final.save(p)
print('saved v4', p)
