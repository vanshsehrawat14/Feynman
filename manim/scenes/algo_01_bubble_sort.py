"""algo_01_bubble_sort.py — Bubble Sort"""
from manim import *
from la_utils import *


class BubbleSortScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Bubble Sort")
        bars = VGroup(*[
            Rectangle(width=0.4, height=0.5 + i * 0.25, color=BLUE).shift(LEFT * 2 + RIGHT * i * 0.5)
            for i in [2, 4, 1, 3]
        ])
        self.play(FadeIn(bars)); self.wait(0.5)
        txt = Text("Compare neighbors, swap if out of order.\nRepeated passes until sorted.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
