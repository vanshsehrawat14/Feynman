"""algo_12_mst.py — Minimum Spanning Tree"""
from manim import *
from la_utils import *


class MSTScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Minimum Spanning Tree")
        a = Circle(0.2, color=BLUE).shift(LEFT * 1.5)
        b = Circle(0.15, color=GREY).shift(LEFT * 0.5)
        c = Circle(0.15, color=GREY).shift(RIGHT * 0.5)
        d = Circle(0.15, color=GREY).shift(LEFT * 0.5 + UP)
        e1 = Line(a.get_right(), b.get_left())
        e2 = Line(b.get_right(), c.get_left())
        e3 = Line(a.get_top(), d.get_bottom())
        g = VGroup(a, b, c, d, e1, e2, e3)
        self.play(Create(g)); self.wait(0.5)
        txt = Text("Min total weight, all nodes connected.\nKruskal or Prim.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
