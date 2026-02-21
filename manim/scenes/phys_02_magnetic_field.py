"""phys_02_magnetic_field.py — Magnetic Fields"""
from manim import *
from la_utils import *


class MagneticFieldScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Magnetic Fields")
        bar = Rectangle(width=1.2, height=0.3, color=GREY)
        circles = VGroup(*[
            Circle(radius=0.4 + i * 0.15, color=BLUE, stroke_width=2).move_to(bar.get_center() + UP * (0.5 + i * 0.4))
            for i in range(3)
        ])
        self.play(Create(bar), Create(circles)); self.wait(0.5)
        txt = Text("Current produces B.\nRight-hand rule.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 3)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
