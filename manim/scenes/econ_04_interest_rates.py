"""econ_04_interest_rates.py — Interest Rates"""
from manim import *
from la_utils import *


class InterestRatesScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Interest Rates")
        txt = Text(
            "Cost of borrowing.\n"
            "Higher rate = less spending, more saving.",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
