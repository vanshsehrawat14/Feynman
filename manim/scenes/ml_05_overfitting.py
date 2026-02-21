"""ml_05_overfitting.py — Overfitting and Underfitting"""
from manim import *
from la_utils import *
import numpy as np


class OverfittingScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Overfitting and Underfitting")
        axes = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=6, y_length=4,
                    axis_config={"color": "#555", "include_numbers": False}).shift(LEFT * 1.5 + DOWN * 0.5)
        pts = [axes.c2p(0.5, 1.2), axes.c2p(1.2, 1.8), axes.c2p(2, 2.2), axes.c2p(2.8, 2)]
        dots = VGroup(*[Dot(p, color=YELL, radius=0.08) for p in pts])
        curve_simple = axes.plot(lambda x: 1.5 + 0.3*x, x_range=[0.2, 3.5], color=BLUE)
        self.play(Create(axes), FadeIn(dots)); self.wait(0.5)
        self.play(Create(curve_simple)); self.wait(0.5)
        txt = Text("Too simple = underfitting.\nToo complex = overfitting.\nSweet spot in between.", font_size=26, color=WHITE)
        txt.move_to(RIGHT * 3)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
