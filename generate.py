# coolest-art-01 entry — "Nebula Silk": De Jong strange attractor, log-density,
# auto-centered, vertical heat tint, bloom with chromatic glow, vignette, grain.
# Deterministic (fixed seeds), runs offline, writes entry.png next to this file.
import math, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

W = H = 1024
SEED = 20261113
a, b, c, d = -2.24, 0.43, -0.65, -2.43

# ---------- pre-pass: find stable bounds ----------
rp = np.random.RandomState(SEED)
N0 = 20000
x0 = rp.uniform(-2, 2, N0); y0 = rp.uniform(-2, 2, N0)
for _ in range(120):
    x0, y0 = np.sin(a * y0) - np.cos(b * x0), np.sin(c * x0) - np.cos(d * y0)
ang = math.radians(-8)
ca, sa = math.cos(ang), math.sin(ang)
xr = x0 * ca - y0 * sa; yr = x0 * sa + y0 * ca
xr_lo, xr_hi = np.percentile(xr, [0.5, 99.5])
yr_lo, yr_hi = np.percentile(yr, [0.5, 99.5])
cxr, cyr = (xr_lo + xr_hi) / 2, (yr_lo + yr_hi) / 2
scale = max(xr_hi - xr_lo, yr_hi - yr_lo) / 2 * 1.04

def to_px(x, y):
    xr = x * ca - y * sa - cxr
    yr = x * sa + y * ca - cyr
    px = (xr / scale * 0.5 + 0.5) * (W - 1)
    py = (1.0 - (yr / scale * 0.5 + 0.5)) * (H - 1)
    return px, py

# ---------- accumulate ----------
rs = np.random.RandomState(SEED)
N = 1_600_000
IT = 9
x = rs.uniform(-2, 2, N); y = rs.uniform(-2, 2, N)
acc = np.zeros((H, W), dtype=np.float64)
ynorm = None
for it in range(IT):
    px, py = to_px(x, y)
    ix = np.clip(px.astype(np.int64), 0, W - 1)
    iy = np.clip(py.astype(np.int64), 0, H - 1)
    fx = px - np.floor(px); fy = py - np.floor(py)
    for ox in (0, 1):
        for oy in (0, 1):
            wgt = (fx if ox else 1 - fx) * (fy if oy else 1 - fy)
            np.add.at(acc, (np.clip(iy + oy, 0, H - 1), np.clip(ix + ox, 0, W - 1)), wgt)
    xn = np.sin(a * y) - np.cos(b * x)
    yn = np.sin(c * x) - np.cos(d * y)
    x, y = xn, yn

hmax = acc.max()
# light smoothing kills bilinear-splat speckle
acc_img = Image.fromarray((np.log1p(acc) / np.log1p(hmax) * 255).astype(np.uint8))
acc_img = acc_img.filter(ImageFilter.GaussianBlur(0.9))
v = np.asarray(acc_img, dtype=np.float64) / 255
v = np.clip(v, 0, 1) ** 0.85
# kill the uniform noise floor so empty space stays deep black
v = np.clip((v - 0.22) / 0.78, 0, 1)

# ---------- palette with vertical heat: top cool indigo, bottom ember ----------
stops = [
    (0.00, (2, 4, 12)),
    (0.20, (22, 20, 70)),
    (0.38, (72, 34, 146)),
    (0.54, (162, 40, 150)),
    (0.68, (232, 66, 116)),
    (0.80, (255, 124, 66)),
    (0.90, (255, 190, 110)),
    (1.00, (255, 246, 226)),
]
def palette(t):
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,))
    for k in range(len(stops) - 1):
        t0, c0 = stops[k]
        t1, c1 = stops[k + 1]
        m = (t >= t0) & (t <= t1)
        f = np.where(t1 > t0, (t - t0) / (t1 - t0), 0)
        for ch in range(3):
            out[:, :, ch] = np.where(m, c0[ch] + (c1[ch] - c0[ch]) * f, out[:, :, ch])
    return out

# vertical heat: bottom hotter (multiplicative keeps background uniform)
ys_g, xs_g = np.mgrid[0:H, 0:W]
img = palette(np.clip(v * (0.80 + 0.55 * (1 - ys_g / H)), 0, 1))

# ---------- bloom ----------
bright = np.clip((v - 0.50) / 0.50, 0, 1) ** 1.5
bl = Image.fromarray((bright * 255).astype(np.uint8))
b1 = np.asarray(bl.filter(ImageFilter.GaussianBlur(5)), dtype=np.float64) / 255
b2 = np.asarray(bl.filter(ImageFilter.GaussianBlur(28)), dtype=np.float64) / 255
glow = (b1 * 0.55 + b2 * 0.45)[:, :, None]
glow = np.repeat(glow, 3, axis=2)
# chromatic aberration without wrap artifacts
r_g = glow[:, :, 0].copy(); b_g = glow[:, :, 2].copy()
r_g[:, :-3] = r_g[:, 3:];  r_g[:, -3:] = r_g[:, -4:-3]
b_g[:, 3:] = b_g[:, :-3];  b_g[:, :3] = b_g[:, 3:4]
glow2 = np.stack([r_g, glow[:, :, 1], b_g], axis=2)
img = 255 - (255 - img) * (255 - np.clip(glow2 * 255 * 1.25, 0, 255)) / 255

# ---------- stars ----------
rs2 = np.random.RandomState(SEED + 1)
starm = Image.fromarray(img.astype(np.uint8))
sd = ImageDraw.Draw(starm, 'RGBA')
for _ in range(150):
    sx = rs2.randint(0, W); sy = rs2.randint(0, H)
    if v[sy, sx] < 0.08:
        continue
    r = rs2.uniform(0.4, 1.3)
    al = int(rs2.uniform(50, 170))
    sd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 244, 230, al))
img = np.asarray(starm, dtype=np.float64)

# ---------- vignette + light grain ----------
rv = np.sqrt(((xs_g - 0.5 * W) / (0.72 * W)) ** 2 + ((ys_g - 0.5 * H) / (0.72 * H)) ** 2)
img *= np.clip(1 - np.clip(rv - 0.62, 0, 1) * 0.6, 0, 1)[:, :, None]
rng = np.random.RandomState(SEED + 2)
img += rng.normal(0, 1.0, (H, W, 1))

out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')
out.save(outp, optimize=True, compress_level=9)
print('saved', outp)
