"""econ_02_gdp.py — GDP and Growth"""
from manim import *
from la_utils import *


class GDPScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "GDP and Growth")
        txt = Text(
            "GDP = total output.\n"
            "Growth = change over time.\n"
            "Real vs nominal.",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
