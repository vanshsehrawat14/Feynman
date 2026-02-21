"""phys_01_electric_field.py — Electric Fields"""
from manim import *
from la_utils import *
import numpy as np


class ElectricFieldScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Electric Fields")
        dot = Dot(color=YELL, radius=0.2)
        arrows = VGroup(*[
            Arrow(ORIGIN, 0.7 * np.array(d), color=BLUE, buff=0)
            for d in [(1,0), (-1,0), (0,1), (0,-1), (0.7,0.7), (-0.7,0.7), (0.7,-0.7), (-0.7,-0.7)]
        ])
        arrows.move_to(ORIGIN)
        self.play(FadeIn(dot), Create(arrows)); self.wait(0.5)
        txt = Text("Charge creates field.\nForce on other charges.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 3)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
