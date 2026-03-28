from pathlib import Path
from manim import *
import numpy as np

from fourier import coeffs
from svg_extractor import get_points

ROOT = Path(__file__).parent.parent
SVG_FILE = str(ROOT / "assets" / "icon-square.svg")
ORPHEUS_IMG = str(ROOT / "assets" / "flag-orpheus-top.png")

# hackclub colors (got them from brand page)
RED = "#ec3750" 
CIRCLE_COLORS = ["#f1c40f", "#ff8c37", "#5bc0de", RED, "#33d6a6"]
STAGES = [(5, 5), (15, 6), (40, 8), (80, 10)]


class FourierOrpheus(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        points = get_points(SVG_FILE)
        max_n = STAGES[-1][0]
        amps, freqs, phases = coeffs(points, max_n)

        def get_centers(t, n):
            contributions = amps[:n] * np.exp(
                1j * (phases[:n] + t * freqs[:n])
            )
            return np.concatenate([[0j], np.cumsum(contributions)])
        
        n= 5
        centers = get_centers(0, n)

        for k in range(n):
            c = np.array([centers[k].real, centers[k].imag, 0.0])
            nx = np.array([centers[k+1].real, centers[k+1].imag, 0.0])

            circle = Circle(radius=max(float(amps[k]), 0.01))
            circle.set_stroke(
                color=CIRCLE_COLORS[k%len(CIRCLE_COLORS)],
                width=1.5, opacity=0.6
            )
            circle.move_to(c)
            self.add(circle)

            if not np.allclose(c, nx):
                arrow = Arrow(
                    c, nx, 
                    buff = 0, color="#ffffff",
                    stroke_width=1, stroke_opacity = 0.35,
                    tip_length= 0.12, max_tip_length_to_length_ratio =0.4,
                )
                self.add(arrow)