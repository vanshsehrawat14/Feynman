"""algo_08_recursion.py — Recursion"""
from manim import *
from la_utils import *


class RecursionScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Recursion")
        txt = Text(
            "Solve a problem by solving smaller versions.\n"
            "Base case stops the recursion.\n"
            "Factorial, Fibonacci, tree traversal.",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
