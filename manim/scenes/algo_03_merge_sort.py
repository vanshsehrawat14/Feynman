"""algo_03_merge_sort.py — Merge Sort"""
from manim import *
from la_utils import *


class MergeSortScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Merge Sort")
        txt = Text(
            "Split in half recursively.\n"
            "Merge sorted halves in linear time.\n"
            "Always O(n log n).",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
