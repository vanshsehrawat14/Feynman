"""algo_06_bfs.py — Breadth-First Search"""
from manim import *
from la_utils import *


class BFSScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Breadth-First Search")
        circ = Circle(radius=0.25, color=BLUE).shift(LEFT * 2)
        c2 = Circle(radius=0.2, color=GREY).shift(LEFT * 0.5 + UP)
        c3 = Circle(radius=0.2, color=GREY).shift(LEFT * 0.5 + DOWN)
        e1 = Line(circ.get_right(), c2.get_left())
        e2 = Line(circ.get_right(), c3.get_left())
        g = VGroup(circ, c2, c3, e1, e2)
        self.play(Create(g)); self.wait(0.5)
        txt = Text("Explore level by level. Use a queue.", font_size=28, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
