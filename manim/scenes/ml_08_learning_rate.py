"""ml_08_learning_rate.py — Learning Rate"""
from manim import *
from la_utils import *
import numpy as np


class LearningRateScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Learning Rate")
        axes = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=6, y_length=4,
                    axis_config={"color": "#555", "include_numbers": False}).shift(LEFT * 1 + DOWN * 0.5)
        curve = axes.plot(lambda x: 2 + 2/(x+0.5), x_range=[0.1, 4], color=BLUE)
        self.play(Create(axes), Create(curve)); self.wait(0.5)
        txt = Text("Too large \u03b1: overshoot.\nToo small: slow.\nJust right: smooth descent.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 3)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
