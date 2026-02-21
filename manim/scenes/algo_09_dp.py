"""algo_09_dp.py — Dynamic Programming"""
from manim import *
from la_utils import *


class DynamicProgrammingScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Dynamic Programming")
        txt = Text(
            "Store subproblem results.\n"
            "Avoid redundant computation.\n"
            "Fibonacci, shortest path, knapsack.",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
