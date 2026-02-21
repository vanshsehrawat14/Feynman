"""Feynman – Span (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class SpanScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.s1_hook();     self._fade_all()
        self.s2_geometry(); self._fade_all()
        self.s3_notation(); self._fade_all()
        self.s4_example();  self._fade_all()
        self.s5_insight();  self._fade_all()
        self.s6_summary()
    def _fade_all(self):
        mobs = list(self.mobjects)
        if mobs: self.play(*[FadeOut(m) for m in mobs], run_time=0.6)
        self.wait(0.6)
    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)
    def _rp(self, mob, y=0.0, x=4.3):
        mob.move_to(RIGHT * x + UP * y); return mob
    def _axes(self, xr=(-0.3,4.5,1), yr=(-0.3,4.5,1)):
        return Axes(x_range=[*xr], y_range=[*yr], x_length=7.2, y_length=5.0,
            axis_config={"color": AX_COLOR,"stroke_width":2,"include_tip":True,"include_ticks":True}
        ).shift(LEFT*1.5+DOWN*0.5)

    def s1_hook(self):
        t = Text("Span", font_size=56, color=WHITE).move_to(UP*0.5)
        t2 = Text("All reachable destinations", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("You have two vectors.\nBy scaling and adding them in all possible ways,\nwhat destinations can you reach?", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("The SET of all reachable points is the span.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("span{v1, v2, ..., vn} =\n{ c1*v1 + c2*v2 + ... + cn*vn | ci in R }\n\nThe set of ALL linear combinations.\nAlways a subspace (contains 0, closed under + and *).", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Three Cases for Span")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=5, buff=0)
        self.play(Create(v1), Create(v2), run_time=1.5); self.wait(0.8)
        r1 = Text("Case 1: v1=(1,0), v2=(0,1)\nspan = entire R^2 plane", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        v2b = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=RED, stroke_width=5, buff=0)
        line = Line(plane.c2p(-4,0), plane.c2p(4,0), color=YELL, stroke_width=2)
        self.play(Transform(v2, v2b), Create(line), run_time=1.5); self.wait(0.8)
        r2 = Text("Case 2: v1=(1,0), v2=(2,0)\nParallel! span = x-axis only (line)", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b2), FadeOut(r2), FadeOut(line), run_time=0.3)
        dot = Dot(plane.c2p(0,0), color=GREEN, radius=0.15)
        self.play(FadeOut(v1), FadeOut(v2), run_time=0.3)
        self.play(FadeIn(dot), run_time=0.5)
        r3 = Text("Case 3: v=0 only\nspan = just the origin (point)", font_size=22, color=RED)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=RED)
        self.play(FadeIn(b3), Write(r3), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Span and Subspaces")
        defn = Text("A subspace must satisfy:\n  1. Contains the zero vector\n  2. Closed under addition\n  3. Closed under scalar multiplication\n\nspan{v1,...,vn} always satisfies all three.\nTherefore span is always a subspace.", font_size=24, color=WHITE).move_to(UP*0.8)
        db = self._box(defn, border=BLUE, buff=0.38)
        self.play(FadeIn(db), Write(defn), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(db), FadeOut(defn), run_time=0.5)
        dim = Text("Dimension of span:\n\n  span{v1} in R^2: dim 1 (line)\n  span{v1,v2} in R^2: dim 2 if independent, 1 if parallel\n  span{v1,...,vn}: dim = rank (number of independent vectors)\n\n  span fills R^n  iff  rank = n  (vectors span the full space)", font_size=23, color=YELL).move_to(ORIGIN)
        yb = self._box(dim, border=YELL, buff=0.38)
        self.play(FadeIn(yb), Write(dim), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Does v=(3,5) lie in span{(1,2),(2,3)}?")
        steps = [
            ("Find c1, c2 such that c1*(1,2) + c2*(2,3) = (3,5)", WHITE, 2.8),
            ("c1 + 2*c2 = 3   (x-equation)", BLUE, 2.0),
            ("2*c1 + 3*c2 = 5  (y-equation)", BLUE, 1.2),
            ("From eq1: c1 = 3 - 2*c2", WHITE, 0.4),
            ("Sub into eq2: 2(3-2*c2) + 3*c2 = 5", WHITE, -0.4),
            ("6 - 4*c2 + 3*c2 = 5  ->  c2 = 1,  c1 = 1", GREEN, -1.2),
            ("YES! v = 1*(1,2) + 1*(2,3) = (3,5) in span.", YELL, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "Span is Everywhere")
        ins = Text("Column space of a matrix = span of its columns\n\nAx = b  has a solution iff  b is in span(cols of A)\n\nThis is why span determines solvability!\n\n  Rank of matrix = dim of column space\n  = dim of span of columns\n\nFull column rank -> can solve Ax=b for any b\nRank deficient -> some b unreachable (no solution)", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Real applications of span:\n\n  Graphics: span{right, up, forward} = 3D space\n  Signals: Fourier basis spans all periodic functions\n  ML: span of training data = what model can represent\n  Control: reachable states = span of control inputs\n  Quantum: superposition = span of basis states", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        self.play(Create(plane), run_time=1.5)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=4, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=4, buff=0)
        self.play(Create(v1), Create(v2), run_time=1.5); self.wait(0.8)
        sm = Text("Span\n\n  span{v1,...,vn} = all linear combinations\n  c1*v1 + ... + cn*vn  (ci in R)\n\n  Always a subspace\n  dim = number of independent vectors\n\n  2 independent vectors in R^2 -> spans R^2\n  Parallel vectors -> span is a line only\n\n  Column space = span of columns", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
