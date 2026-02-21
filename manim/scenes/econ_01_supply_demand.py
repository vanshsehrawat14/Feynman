"""econ_01_supply_demand.py — Supply and Demand"""
from manim import *
from la_utils import *
import numpy as np


class SupplyDemandScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Supply and Demand")
        axes = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=5, y_length=4,
                    axis_config={"color": "#555", "include_numbers": False})
        dd = axes.plot(lambda x: 3.5 - 0.7*x, x_range=[0.2, 4], color=RED)
        ss = axes.plot(lambda x: 0.5 + 0.5*x, x_range=[0.2, 4], color=BLUE)
        self.play(Create(axes), Create(dd), Create(ss)); self.wait(0.5)
        txt = Text("Intersection = equilibrium.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 3)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
