"""Feynman – Determinant = 0 (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class DetZeroScene(Scene):
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
        t = Text("When det = 0", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Singular matrices and collapsed dimensions", font_size=24, color=RED).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("A transformation flattens 3D space into a plane.\nVolume: before = 1, after = 0.\nThe determinant is exactly 0.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("det=0 means the transformation is SINGULAR:\nit collapses the space into lower dimension.", font_size=26, color=RED).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("det(A) = 0 is equivalent to ALL of these:\n  Columns are linearly dependent\n  A is NOT invertible (singular)\n  Ax=0 has non-trivial solutions\n  null(A) != {0}  (non-trivial null space)\n  A squashes space to lower dimension", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=RED, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Visualizing Collapse")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        col1 = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=BLUE, stroke_width=5, buff=0)
        col2 = Arrow(plane.c2p(0,0), plane.c2p(-1,2), color=RED, stroke_width=5, buff=0)
        self.play(Create(col1), Create(col2), run_time=1.5); self.wait(0.8)
        r1 = Text("Independent columns:\ndet = 2*2-1*(-1) = 5 != 0\nUnit square -> 5x larger", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(3.0)
        col2_dep = Arrow(plane.c2p(0,0), plane.c2p(4,2), color=RED, stroke_width=5, buff=0)
        line = Line(plane.c2p(-3,-1.5), plane.c2p(3,1.5), color=YELL, stroke_width=2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        self.play(Transform(col2, col2_dep), Create(line), run_time=1.5); self.wait(0.6)
        r2 = Text("Dependent columns: (4,2) = 2*(2,1)\ndet = 2*2-1*4 = 0\nAll of R^2 -> collapses to 1 line!", font_size=22, color=RED)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Why det=0 Matters")
        eq = Text("det(A) = 0  <->  A is SINGULAR", font_size=34, color=RED).move_to(UP*2.5)
        eb = self._box(eq, border=RED, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(1.8)
        chain = Text("Chain of equivalences (all the same!):\n\n  det(A)=0\n  -> columns linearly dependent\n  -> rank < n  (not full rank)\n  -> null(A) != {0}  (free variable in Ax=0)\n  -> A NOT invertible (no A^{-1})\n  -> Ax=b may have 0 or inf solutions\n  -> transformation squashes dimension", font_size=23, color=WHITE).next_to(eq, DOWN, buff=0.5)
        cb = self._box(chain, border=BLUE, buff=0.38)
        self.play(FadeIn(cb), Write(chain), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Examples of Singular Matrices")
        examples = [
            ("[[1,2],[2,4]] -> det=4-4=0 (row2=2*row1)", RED, 2.8),
            ("[[1,0,0],[0,1,0],[0,0,0]] -> det=0 (zero row)", RED, 2.0),
            ("[[a,b],[ka,kb]] -> det=ab*k-ab*k=0 (proportional rows)", RED, 1.2),
            ("Near-singular: [[1,1],[1,1.001]] -> det~0.001", YELL, 0.4),
            ("Ill-conditioned: sensitive to tiny changes!", YELL, -0.4),
            ("Condition number = sigma_max/sigma_min -> infinity", RED, -1.2),
            ("Numerically unstable near det=0!", RED, -2.0),
        ]
        for txt, col, yp in examples:
            mob = Text(txt, font_size=23, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Singular matrices are everywhere (and problematic):\n\n  Overfitting in ML: Gram matrix A^T A is singular\n  -> regularization adds lambda*I to make invertible\n\n  Multicollinearity in regression:\n  correlated features -> near-singular design matrix\n  -> coefficients blow up!\n\n  Why pseudoinverse A+: handles singular A via SVD\n  sigma_i > epsilon: keep. sigma_i <= epsilon: discard.\n\n  det=0 is a MEASURE-ZERO event (rare!) in practice", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=RED, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        geom = Text("Geometric insight:\n\ndet=0 means the unit hypercube gets flattened.\n3D cube -> 2D plane -> area=0, volume=0.\n\nA matrix with det=0 cannot be inverted because\nthe transformation is not reversible:\nyou cannot unflatten what was flattened!\n\nThis is why det=0 is the boundary between\ninvertible and non-invertible.", font_size=22, color=YELL).move_to(ORIGIN)
        gb = self._box(geom, border=YELL, buff=0.38)
        self.play(FadeIn(gb), Write(geom), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("det = 0: Singular Matrix\n\n  All equivalent:\n  - Columns linearly dependent\n  - Rank < n (not full rank)\n  - Null space is non-trivial\n  - Not invertible (no A^{-1})\n\n  Geometric: dimension collapses\n  (area or volume -> zero)\n\n  Causes: multicollinearity, zero rows,\n  proportional columns, repeated eigenvalue=0", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=RED, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
