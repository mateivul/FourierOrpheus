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
STAGES = [(5, 6.2), (15, 7.1), (40, 9), (80, 10)]


class FourierOrpheus(ZoomedScene):
    def __init__(self, **kwargs): #zoomed in on animation part 
        super().__init__(
            zoom_factor=0.22,
            zoomed_display_height=3,
            zoomed_display_width=4,
            image_frame_stroke_width=1.5,
            zoomed_camera_config={
                "default_frame_stroke_width": 1.5,
                "default_frame_stroke_color": RED,
                "background_color": "#000000"
            },
            **kwargs
        )

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

        counter = VGroup( #the circle counter on bottom left (each phase)
            Text(str(STAGES[0][0]), font_size=52, color=RED, weight=BOLD),
            Text("circles", font_size=16, color="#ffffff").set_opacity(0.5),
        ).arrange(DOWN, buff=0.15).to_corner(DL, buff=0.5)
        self.add(counter)

        for i, (n, duration) in enumerate(STAGES):
            last = i == len(STAGES)-1

            tracker = ValueTracker(0)

            start_tip = get_centers(0, n)[-1]
            pos = [np.array([start_tip.real, start_tip.imag, 0.0])]

            circles = VGroup(*[
                Circle(radius=max(float(amps[k]), 0.01))
                .set_stroke(color=CIRCLE_COLORS[k % len(CIRCLE_COLORS)], width=1.5, opacity=0.6)
                for k in range(n)
            ])

            radius_lines = VGroup ()
            for k in range(n):
                radius_lines.add(Arrow(
                    ORIGIN, RIGHT * max(float(amps[k]), 0.01),
                    buff=0, color='#ffffff', stroke_width=1, stroke_opacity=0.35,
                    tip_length=0.12, max_tip_length_to_length_ratio=0.4,
                ))
 
            glow_trace = TracedPath(
                lambda tp=pos: tp[0].copy(),
                stroke_color="#ff8c37", stroke_width=6, stroke_opacity=0.3,
            )
            trace = TracedPath (
                lambda tp=pos: tp[0].copy(),
                stroke_color=RED, stroke_width=3, stroke_opacity=1,
            )
            
            def update(mob, t=tracker, nc=n, tp=pos, cl=circles, rl=radius_lines):
                centers = get_centers(t.get_value(), nc)
                for j in range(nc):
                    c = np.array([centers[j].real, centers[j].imag, 0.0])
                    nx = np.array([centers[j+1].real, centers[j+1].imag, 0.0])
                    cl[j].move_to(c)
                    if not np.allclose(c, nx):
                        rl[j].put_start_and_end_on(c, nx)
                tip = centers[-1]
                tp[0] = np.array([tip.real, tip.imag, 0.0])
            circles.add_updater(update)
            self.add(glow_trace, trace, circles, radius_lines)

            if last: # position for zoomed in frame  
                self.zoomed_display.to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
                self.zoomed_camera.frame.move_to(pos[0])
                self.activate_zooming(animate=True)
                self.zoomed_camera.frame.add_updater(
                    lambda m, tp=pos: m.move_to(tp[0])
                )
            
            self.play(
                tracker.animate.set_value(2 * np.pi + 0.05),
                run_time=duration,
                rate_func=linear,
            )

            circles.clear_updaters()
            trace.clear_updaters()
            glow_trace.clear_updaters()
            if last:
                self.zoomed_camera.frame.clear_updaters()

            if not last:
                nn = STAGES[i + 1][0]
                new_counter = VGroup(
                    Text(str(nn), font_size=52, color=RED, weight=BOLD),
                    Text("circles", font_size=16, color="#ffffff").set_opacity(0.5),
                ).arrange(DOWN, buff=0.15).to_corner(DL, buff=0.5)

                self.play(
                    FadeOut(circles), FadeOut(radius_lines),
                    FadeOut(trace), FadeOut(glow_trace),
                    Transform(counter, new_counter),
                    run_time=0.5
                )

            else: # the top falg appearance
                self.wait(2.5)

                final_tip_3d = pos[0].copy()

                self.play(
                    FadeOut(circles), 
                    FadeOut(radius_lines),
                    FadeOut(counter),
                    FadeOut(self.zoomed_display),
                    FadeOut(self.zoomed_camera.frame),
                    run_time=1.5
                )

                self.play(
                    trace.animate.set_stroke(opacity=0.12),
                    glow_trace.animate.set_stroke(opacity=0.06),
                    run_time=0.7,
                )

                orpheus = ImageMobject(ORPHEUS_IMG)
                orpheus.scale_to_fit_height(5)
                orpheus.move_to(ORIGIN)

                self.play(
                    GrowFromPoint(orpheus, final_tip_3d),
                    run_time=1.8,
                    rate_func=smooth,
                )
                self.wait(2.5)