"""Feynman – Null Space (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class NullSpaceScene(Scene):
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
        t = Text("Null Space", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("What gets sent to zero?", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("A transformation crushes some information.\nThe vectors it sends to zero —\nthose are the ones it destroys.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("The null space (kernel) is the collection\nof all vectors that A maps to zero: Av=0.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("null(A) = ker(A) = {x : Ax = 0}\n\nAlways a subspace (contains 0, closed under + and *)\nDimension = nullity(A)\n\nRank-Nullity theorem: rank + nullity = n\n(columns + null space = full input space)", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Null Space as Lost Information")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(-2,-1), color=RED, stroke_width=4, buff=0)
        line = Line(plane.c2p(-3,-1.5), plane.c2p(3,1.5), color=YELL, stroke_width=2)
        self.play(Create(line), Create(v1), Create(v2), run_time=2.0); self.wait(0.8)
        r1 = Text("A projection onto x-axis:\nAll vectors on this line map to 0\n(That line IS the null space)", font_size=22, color=YELL)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Null space of projection:\n  All vectors perpendicular to x-axis\n  = the y-axis\nnullity = 1,  rank = 1,  1+1 = 2", font_size=22, color=GREEN)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=GREEN)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Finding the Null Space")
        method = Text("Algorithm: row reduce [A] -> RREF, set free variables\n\nExample: A = [[1,2,3],[2,4,6]]\nRow reduce: [[1,2,3],[0,0,0]]\nFree vars: x2, x3\nx1 = -2*x2 - 3*x3\n\nnull(A) = span{(-2,1,0), (-3,0,1)}\nnullity = 2", font_size=24, color=WHITE).move_to(UP*0.5)
        mb = self._box(method, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(method), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(mb), FadeOut(method), run_time=0.5)
        rank_null = Text("Rank-Nullity Theorem:\n\n  rank(A) + nullity(A) = n   (number of columns)\n\n  rank = dim(column space) = pivot columns\n  nullity = dim(null space) = free variables\n\n  Full column rank -> nullity=0 -> Ax=0 has only x=0\n  -> A is injective (one-to-one)", font_size=23, color=YELL).move_to(ORIGIN)
        rb = self._box(rank_null, border=YELL, buff=0.38)
        self.play(FadeIn(rb), Write(rank_null), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Null Space of [[2,4],[1,2]]")
        steps = [
            ("A = [[2,4],[1,2]]", WHITE, 2.5),
            ("Row reduce: R1/2 -> [[1,2],[1,2]]", BLUE, 1.7),
            ("R2 = R2-R1: -> [[1,2],[0,0]]", GREEN, 0.9),
            ("Pivot: x1. Free: x2 = t (parameter)", WHITE, 0.1),
            ("x1 + 2*x2 = 0  ->  x1 = -2t", YELL, -0.7),
            ("null(A) = span{(-2, 1)}", GREEN, -1.5),
            ("rank=1, nullity=1, 1+1=2=cols ✓", BLUE, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("The null space reveals invertibility:\n\n  null(A) = {0} only  <->  A is invertible\n  (no information is destroyed)\n\n  Null space tells you solution structure:\n  If Ax=b has one solution x0,\n  ALL solutions are: x0 + null(A)\n  (particular + homogeneous solutions)\n\n  Dimensions: null(A) = n - rank(A)\n  Every dimension in null space = a 'destroyed' direction", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications:\n\n  Signal processing: null space of sensing matrix\n  = signals that cannot be detected\n  (blind spots of the system)\n\n  Control theory: null space of control matrix\n  = motions that the controller cannot affect\n\n  Neural networks: null space of weight matrix\n  = directions that produce zero activation", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Null Space  null(A) = {x : Ax = 0}\n\n  Always a subspace\n  nullity = number of free variables\n\n  Rank-Nullity: rank + nullity = n\n\n  null={0}  <->  A invertible\n  null={0}  <->  unique solution to Ax=b\n\n  Solution structure:\n  Ax=b solutions = x_particular + null(A)\n\n  Reveals destroyed information", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
