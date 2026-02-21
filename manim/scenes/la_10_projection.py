"""Feynman – Projection (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class ProjectionScene(Scene):
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
        t = Text("Projection", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("Finding the shadow", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Sunlight shining straight down.\nA stick casts a shadow on the ground.\nThe shadow is the projection.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Projection = the closest point on a line (or plane)\nto a given vector. The mathematical shadow.", font_size=24, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("proj_u(v) = (v.u / u.u) * u\n\nProject v onto direction u:\n  Scale u by the dot product fraction.\nResult = component of v along u.", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Geometric Projection")
        ax = self._axes()
        self.play(Create(ax), run_time=2.0); self.wait(0.8)
        u = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=5, buff=0)
        v = Arrow(ax.c2p(0,0), ax.c2p(2,2.5), color=RED, stroke_width=5, buff=0)
        ul = Text("u=(3,0)", font_size=20, color=BLUE).next_to(ax.c2p(1.5,0), DOWN, buff=0.15)
        vl = Text("v=(2,2.5)", font_size=20, color=RED).next_to(ax.c2p(1,1.25), LEFT, buff=0.1)
        self.play(Create(u), Create(v), Write(ul), Write(vl), run_time=2.5); self.wait(0.8)
        proj_x = 2.0
        proj = Arrow(ax.c2p(0,0), ax.c2p(proj_x, 0), color=GREEN, stroke_width=5, buff=0)
        drop = DashedLine(ax.c2p(2,2.5), ax.c2p(2,0), color=YELL)
        self.play(Create(drop), Create(proj), run_time=2.0); self.wait(0.8)
        r1 = Text("proj = (v.u/|u|^2) * u\n= (6/9)*(3,0) = (2,0)", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.3)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Error (rejection):\nv - proj = (0, 2.5)\nPerpendicular to u!", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Projection Formula")
        eq = Text("proj_u(v) = (v . u) / (u . u)  *  u", font_size=30, color=YELL).move_to(UP*2.5)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(1.8)
        matrix_form = Text("Projection matrix onto unit vector u:\n\n  P = u * u^T\n\n  (outer product of u with itself)\n  P^2 = P  (idempotent: projecting twice = projecting once)\n  P is symmetric: P^T = P", font_size=24, color=WHITE).move_to(UP*0.2)
        mb = self._box(matrix_form, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(matrix_form), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(mb), FadeOut(matrix_form), FadeOut(eb), FadeOut(eq), run_time=0.5)
        subspace = Text("Projection onto subspace (column space of A):\n\n  P = A(A^T A)^{-1} A^T\n\n  The projection that minimizes |v - Pv|^2\n  Key in least squares regression:\n  b_hat = (A^T A)^{-1} A^T b  = pseudo-inverse * b", font_size=23, color=GREEN).move_to(ORIGIN)
        sb = self._box(subspace, border=GREEN, buff=0.38)
        self.play(FadeIn(sb), Write(subspace), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Example: proj of v=(3,4) onto u=(1,0)")
        steps = [
            ("v = (3, 4)   u = (1, 0)  (x-axis)", WHITE, 2.5),
            ("v . u = 3*1 + 4*0 = 3", BLUE, 1.7),
            ("u . u = 1^2 + 0^2 = 1", WHITE, 0.9),
            ("proj = (3/1) * (1,0) = (3, 0)", GREEN, 0.1),
            ("rejection = v - proj = (3,4)-(3,0) = (0,4)", YELL, -0.7),
            ("Check: (0,4).(1,0) = 0 (perpendicular!)", GREEN, -1.5),
            ("v = proj + rejection  (decomposition!)", WHITE, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Projection is the core of least squares:\n\n  Given overdetermined system Ax = b (no exact solution)\n  Find x that minimizes |Ax - b|^2\n\n  Solution: project b onto column space of A\n  b_hat = A(A^T A)^{-1} A^T b\n\n  This is linear regression!\n  Fitting a line = projecting data onto\n  the subspace spanned by [1, x]", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        gram = Text("Gram-Schmidt orthogonalization:\n\n  Turn any basis into orthogonal basis\n  using repeated projections:\n\n  u1 = v1\n  u2 = v2 - proj_{u1}(v2)\n  u3 = v3 - proj_{u1}(v3) - proj_{u2}(v3)\n  ...\n\n  Foundation of QR decomposition", font_size=22, color=YELL).move_to(ORIGIN)
        gb = self._box(gram, border=YELL, buff=0.38)
        self.play(FadeIn(gb), Write(gram), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes()
        u = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=4, buff=0)
        v = Arrow(ax.c2p(0,0), ax.c2p(2,2.5), color=RED, stroke_width=4, buff=0)
        proj = Arrow(ax.c2p(0,0), ax.c2p(2,0), color=GREEN, stroke_width=4, buff=0)
        drop = DashedLine(ax.c2p(2,2.5), ax.c2p(2,0), color=YELL)
        self.play(Create(ax), Create(u), Create(v), Create(proj), Create(drop), run_time=2.5); self.wait(0.8)
        sm = Text("Projection\n\n  proj_u(v) = (v.u/u.u) * u\n\n  Component of v along u\n  Minimizes distance (least squares)\n\n  P = u*u^T  (projection matrix)\n  P^2 = P  (idempotent)\n\n  Powers: linear regression, QR,\n  Gram-Schmidt, PCA", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
