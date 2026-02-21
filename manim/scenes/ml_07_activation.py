"""ml_07_activation.py — Activation Functions"""
from manim import *
from la_utils import *
import numpy as np


class ActivationScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Activation Functions")
        axes = Axes(x_range=[-2, 2, 1], y_range=[-0.5, 1.5, 0.5], x_length=6, y_length=3,
                    axis_config={"color": "#555", "include_numbers": False}).shift(DOWN * 0.5)
        relu = axes.plot(lambda x: max(0, x), x_range=[-2, 2], color=BLUE)
        self.play(Create(axes), Create(relu)); self.wait(0.5)
        txt = Text("ReLU, Sigmoid, Tanh.\nEach adds nonlinearity.", font_size=28, color=WHITE)
        txt.move_to(UP * 2)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
