"""ml_09_cnn.py — Convolutional Neural Networks"""
from manim import *
from la_utils import *


class ConvolutionalScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Convolutional Neural Networks")
        grid = VGroup(*[
            Square(side_length=0.5, color=GREY, stroke_width=1).shift(LEFT*2 + UP*1 + RIGHT*(i%4)*0.55 + DOWN*(i//4)*0.55)
            for i in range(16)
        ])
        self.play(Create(grid)); self.wait(0.5)
        txt = Text("Filter slides over image.\nDetects edges and patterns.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
