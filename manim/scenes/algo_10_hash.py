"""algo_10_hash.py — Hash Tables"""
from manim import *
from la_utils import *


class HashTableScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Hash Tables")
        boxes = VGroup(*[
            Rectangle(width=0.8, height=0.5, color=GREY).shift(LEFT * 2 + RIGHT * (i % 4) * 0.9 + DOWN * (i // 4) * 0.6)
            for i in range(8)
        ])
        self.play(FadeIn(boxes)); self.wait(0.5)
        txt = Text("Key -> hash -> bucket. O(1) average lookup.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
