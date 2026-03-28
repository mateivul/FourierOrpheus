import numpy as np
from svgpathtools import svg2paths

def get_points(svg_file):
    paths, _ = svg2paths(svg_file)
    paths = [p for p in paths if len(p) > 5]

    chunks = []
    for path in paths: 
        lengths = [max(seg.length(), 1e-6) for seg in path]
        total = sum(lengths)
        chunks.append(np.concatenate([
            seg.points(np.linspace(0, 1, max(2, round(1000 * seg_len / total))))
            for seg, seg_len in zip(path, lengths)
        ]))

    ordered = [chunks.pop(0)]
    while chunks:
        tail = ordered[-1][-1]
        pick, flip, best_d = 0, False, np.inf
        for i, chunk in enumerate(chunks):
            d_fwd = abs(chunk[0] - tail)
            d_rev = abs(chunk[-1] - tail)
            if d_fwd < best_d:
                pick, flip, best_d = i, False, d_fwd
            if d_rev < best_d:
                pick, flip, best_d = i, True, d_rev
        chunk = chunks.pop(pick)
        ordered.append(chunk[::-1] if flip else chunk)

    points = np.concatenate(ordered)
    points = points.conjugate()

    # default mamin frame (canvas)
    scale = max(
        (points.real.max() - points.real.min()) / 12.6,
        (points.imag.max() - points.imag.min()) / 7.2,
    )
    if scale > 0:
        points /= scale 
    cx = (points.real.max() + points.real.min()) / 2
    cy = (points.imag.max() + points.imag.min()) / 2
    points -= (cx + 1j * cy)

    return np.append(points, points[:1])