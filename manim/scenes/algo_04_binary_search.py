"""algo_04_binary_search.py — Binary Search"""
from manim import *
from la_utils import *


class BinarySearchScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Binary Search")
        arr = VGroup(*[
            Rectangle(width=0.6, height=0.5, color=GREY).shift(LEFT * 2.5 + RIGHT * i * 0.65)
            for i in range(8)
        ])
        mid = Rectangle(width=0.6, height=0.5, color=YELL)
        mid.move_to(arr[4].get_center())
        self.play(FadeIn(arr), FadeIn(mid)); self.wait(0.5)
        txt = Text("Cut search space in half each step.\nO(log n) lookups in sorted array.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
