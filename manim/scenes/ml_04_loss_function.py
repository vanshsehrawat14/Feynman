"""ml_04_loss_function.py — What is a Loss Function (Gold Standard)"""
from manim import *
from la_utils import *
import numpy as np


class LossFunctionScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "What is a Loss Function")
        t1 = Text("What is a Loss Function?", font_size=44, color=WHITE)
        t2 = Text("Measuring Prediction Error", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), FadeIn(t2)); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2)); self.wait(0.3)

        axes = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=6, y_length=4,
                    axis_config={"color": "#555", "include_numbers": False}).shift(LEFT * 1.5 + DOWN * 0.5)
        self.play(Create(axes)); self.wait(0.5)
        pred = Dot(axes.c2p(2, 2), color=YELL, radius=0.12)
        actual = Dot(axes.c2p(2.5, 3), color=RED, radius=0.12)
        line = DashedLine(pred.get_center(), actual.get_center(), color=GREY)
        self.play(FadeIn(pred), FadeIn(actual), Create(line)); self.wait(0.5)
        lbl = Text("Prediction vs Reality.\nLoss = distance between them.", font_size=26, color=WHITE)
        lbl.move_to(RIGHT * 3 + UP * 0.5)
        bl = text_box(lbl, border=BLUE)
        self.play(FadeIn(bl), Write(lbl)); self.wait(3)

