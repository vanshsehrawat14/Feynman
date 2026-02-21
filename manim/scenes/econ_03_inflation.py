"""econ_03_inflation.py — Inflation"""
from manim import *
from la_utils import *


class InflationScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Inflation")
        txt = Text(
            "Rising prices over time.\n"
            "Reduces purchasing power.\n"
            "Central banks target low inflation.",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=RED)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
