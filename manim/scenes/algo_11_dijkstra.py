"""algo_11_dijkstra.py — Dijkstra's Algorithm"""
from manim import *
from la_utils import *


class DijkstraScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Dijkstra's Algorithm")
        a = Circle(0.2, color=YELL).shift(LEFT * 2)
        b = Circle(0.15, color=GREY).shift(LEFT * 0.5)
        c = Circle(0.15, color=GREY).shift(RIGHT * 1 + UP)
        e1 = Line(a.get_right(), b.get_left())
        e2 = Line(b.get_top(), c.get_bottom())
        g = VGroup(a, b, c, e1, e2)
        self.play(Create(g)); self.wait(0.5)
        txt = Text("Shortest path from source.\nGreedy, weights non-negative.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
