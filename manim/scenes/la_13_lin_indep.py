"""Feynman – Linear Independence (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class LinearIndepScene(Scene):
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
        t = Text("Linear Independence", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("No redundancy in directions", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Can any of your vectors be written as a\ncombination of the others?\nIf not: they are linearly independent.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Redundant vectors waste dimensions.\nIndependent vectors give you new directions.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Formally: v1,...,vn are linearly independent if\n\n  c1*v1 + c2*v2 + ... + cn*vn = 0\n  implies c1=c2=...=cn=0\n\nOnly the trivial solution! No vector is\na combination of the others.", font_size=24, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Independent vs Dependent")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=RED, stroke_width=5, buff=0)
        self.play(Create(v1), Create(v2), run_time=2.0); self.wait(0.8)
        r1 = Text("(2,0) and (0,2):\nIndependent! Different directions.\nSpan all of R^2", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b1), FadeOut(r1), FadeOut(v2), run_time=0.3)
        v2dep = Arrow(plane.c2p(0,0), plane.c2p(4,0), color=RED, stroke_width=5, buff=0)
        self.play(Create(v2dep), run_time=1.5); self.wait(0.8)
        r2 = Text("(2,0) and (4,0):\nDependent! (4,0) = 2*(2,0)\nSpan only x-axis, dim=1", font_size=22, color=RED)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b2), FadeOut(r2), FadeOut(v2dep), run_time=0.3)
        v3 = Arrow(plane.c2p(0,0), plane.c2p(1,1), color=GREEN, stroke_width=5, buff=0)
        self.play(Create(v3), run_time=1.5); self.wait(0.6)
        r3 = Text("3 vectors in R^2: always dependent!\n(2 dimensions can only hold 2 independent)", font_size=22, color=YELL)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=YELL)
        self.play(FadeIn(b3), Write(r3), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Testing Independence")
        method = Text("Method: form matrix A = [v1|v2|...|vn]\nThen row reduce.\n\n  Independent iff no free variables\n  (every column has a pivot)\n  <-> rank(A) = number of vectors\n  <-> det(A) != 0  (for square matrices)\n\nNumber of independent vectors = rank", font_size=24, color=WHITE).move_to(UP*0.5)
        mb = self._box(method, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(method), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(mb), FadeOut(method), run_time=0.5)
        rules = Text("Key rules:\n\n  n+1 vectors in R^n are always dependent\n  n vectors in R^n: independent iff det != 0\n  Subset of independent set is independent\n  Span = same if add dependent vector\n  Basis = maximal independent set = minimal spanning set", font_size=23, color=YELL).move_to(ORIGIN)
        rb = self._box(rules, border=YELL, buff=0.38)
        self.play(FadeIn(rb), Write(rules), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Test: (1,2), (3,4), (5,6) in R^2")
        steps = [
            ("Form matrix:  [[1,3,5],[2,4,6]]", WHITE, 2.5),
            ("Row reduce: R2 = R2 - 2*R1", BLUE, 1.7),
            ("-> [[1,3,5],[0,-2,-4]]", GREEN, 0.9),
            ("R2 = R2/(-2): -> [[1,3,5],[0,1,2]]", GREEN, 0.1),
            ("R1 = R1-3*R2: -> [[1,0,-1],[0,1,2]]", GREEN, -0.7),
            ("Free variable in column 3: DEPENDENT", RED, -1.5),
            ("(5,6) = -1*(1,2) + 2*(3,4)  [verify!]", YELL, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Linear independence is THE central concept\nin linear algebra:\n\n  Rank-Nullity theorem: rank + nullity = n\n  (independent cols + dependent cols = total cols)\n\n  Basis = maximal independent set\n  Dimension = size of any basis\n\n  Gram-Schmidt turns dependent set into independent!\n  SVD reveals true independence structure", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        ml = Text("In machine learning:\n\n  Features: independent = carry unique information\n  Dependent = redundant, causes multicollinearity\n\n  PCA: find directions of maximum variance\n  = independent principal components\n\n  Attention heads in transformers:\n  Should attend to independent aspects\n  of the input (diversity is valuable)", font_size=22, color=YELL).move_to(ORIGIN)
        mb = self._box(ml, border=YELL, buff=0.38)
        self.play(FadeIn(mb), Write(ml), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=BLUE, stroke_width=4, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=RED, stroke_width=4, buff=0)
        self.play(Create(plane), Create(v1), Create(v2), run_time=2.0); self.wait(0.8)
        sm = Text("Linear Independence\n\n  c1*v1+...+cn*vn=0 => all ci=0\n  No vector is combo of others\n\n  Test: row reduce, check rank\n  n vectors in R^n: det != 0 <-> indep\n\n  Basis = maximal independent set\n  Rank = count of independent cols\n  Foundation of dimension theory", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
