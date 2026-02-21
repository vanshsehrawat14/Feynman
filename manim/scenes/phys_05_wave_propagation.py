"""phys_05_wave_propagation.py — Wave Propagation"""
from manim import *
from la_utils import *
import numpy as np


class WavePropagationScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Wave Propagation")
        axes = Axes(x_range=[0, 6, 1], y_range=[-1.5, 1.5, 0.5], x_length=7, y_length=3,
                    axis_config={"color": "#555", "include_numbers": False})
        wave = axes.plot(lambda x: np.sin(x), x_range=[0, 6], color=BLUE)
        self.play(Create(axes), Create(wave)); self.wait(0.5)
        txt = Text("E and B oscillate.\nWave travels at c.", font_size=28, color=WHITE)
        txt.move_to(UP * 2)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
