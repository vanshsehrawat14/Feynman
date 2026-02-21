"""algo_07_big_o.py — Big O Notation"""
from manim import *
from la_utils import *
import numpy as np


class BigOScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Big O Notation")
        axes = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=6, y_length=4,
                    axis_config={"color": "#555", "include_numbers": False}).shift(DOWN * 0.5)
        ln = axes.plot(lambda x: x, x_range=[0.1, 4], color=BLUE)
        nlogn = axes.plot(lambda x: x * max(0.01, np.log(max(0.01, x))), x_range=[0.2, 4], color=YELL)
        n2 = axes.plot(lambda x: x**2 * 0.25, x_range=[0.1, 4], color=RED)
        self.play(Create(axes), Create(ln)); self.wait(0.3)
        self.play(Create(nlogn)); self.wait(0.3)
        self.play(Create(n2)); self.wait(0.3)
        txt = Text("O(n), O(n log n), O(n^2).\nWorst-case growth rate.", font_size=28, color=WHITE)
        txt.move_to(UP * 2)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
