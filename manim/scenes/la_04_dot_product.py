"""Feynman – The Dot Product (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class DotProductScene(Scene):
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
        t = Text("The Dot Product", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Measuring alignment", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("How much does one vector point in\nthe direction of another?", font_size=28, color=WHITE).move_to(UP*1.0)
        ans = Text("The dot product answers this exactly.\nIt is the signed length of the projection.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("v . w = vx*wx + vy*wy\n       = |v| |w| cos(theta)\n\nPositive: vectors point same way\nZero: perpendicular (orthogonal)\nNegative: vectors point opposite ways", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Geometric Meaning: Projection")
        ax = self._axes()
        self.play(Create(ax), run_time=2.0); self.wait(0.8)
        v = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=5, buff=0)
        w = Arrow(ax.c2p(0,0), ax.c2p(2,2), color=RED, stroke_width=5, buff=0)
        vl = Text("v=(3,0)", font_size=20, color=BLUE).next_to(ax.c2p(1.5,0), DOWN, buff=0.15)
        wl = Text("w=(2,2)", font_size=20, color=RED).next_to(ax.c2p(1,1), LEFT, buff=0.1)
        self.play(Create(v), Create(w), Write(vl), Write(wl), run_time=2.5); self.wait(0.8)
        proj_tip = ax.c2p(2, 0)
        proj = DashedLine(ax.c2p(2,2), proj_tip, color=YELL)
        proj_vec = Arrow(ax.c2p(0,0), proj_tip, color=GREEN, stroke_width=4, buff=0)
        self.play(Create(proj), Create(proj_vec), run_time=2.0); self.wait(0.8)
        r1 = Text("Projection of w onto v = 2\n(the shadow of w on v)\nv.w = 3*2 + 0*2 = 6 = |v|*proj", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        w2 = Arrow(ax.c2p(0,0), ax.c2p(0,3), color=RED, stroke_width=5, buff=0)
        w2l = Text("w=(0,3) perpendicular to v", font_size=20, color=RED).next_to(ax.c2p(0,1.5), RIGHT, buff=0.1)
        self.play(Transform(w, w2), Transform(wl, w2l), run_time=1.5); self.wait(0.8)
        r2 = Text("v . w = 3*0 + 0*3 = 0\nOrthogonal vectors -> dot product 0", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Formulas and Properties")
        eq1 = Text("v . w = vx*wx + vy*wy  (component form)", font_size=26, color=YELL).move_to(UP*2.5)
        eq2 = Text("v . w = |v| |w| cos(theta)  (geometric form)", font_size=26, color=GREEN).move_to(UP*1.6)
        b1 = self._box(eq1, border=YELL, buff=0.3)
        b2 = self._box(eq2, border=GREEN, buff=0.3)
        self.play(FadeIn(b1), Write(eq1), run_time=2.0); self.wait(1.8)
        self.play(FadeIn(b2), Write(eq2), run_time=2.0); self.wait(1.8)
        props = Text("Properties:\n\n  Commutative:  v . w = w . v\n  Distributive: v . (w+u) = v.w + v.u\n  Scalar:       (cv) . w = c(v.w)\n  Self:         v . v = |v|^2\n\n  cos(theta) = (v.w)/(|v||w|)\n  (extract angle between vectors)", font_size=23, color=WHITE).move_to(DOWN*0.5)
        pb = self._box(props, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Example: v=(1,2,3), w=(4,-1,2)")
        steps = [
            ("v = (1, 2, 3)   w = (4, -1, 2)", WHITE, 2.8),
            ("v . w = 1*4 + 2*(-1) + 3*2", BLUE, 2.0),
            ("      = 4 - 2 + 6 = 8", GREEN, 1.2),
            ("|v| = sqrt(1+4+9) = sqrt(14) ~ 3.742", WHITE, 0.4),
            ("|w| = sqrt(16+1+4) = sqrt(21) ~ 4.583", WHITE, -0.4),
            ("cos(theta) = 8 / (3.742 * 4.583) ~ 0.466", YELL, -1.2),
            ("theta ~ 62.2 degrees", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("The dot product is the most important\noperation in applied mathematics:\n\n  Physics: Work = F . d (force dot displacement)\n  Graphics: Lighting = N . L (normal dot light)\n  ML: Attention = Q . K^T / sqrt(d)\n  Signal: Correlation of two signals\n  Statistics: Covariance (normalized dot product)\n\n  Cosine similarity = dot product of unit vectors\n  Used in recommendation systems, search engines", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        ortho = Text("Orthogonality is a superpower:\n\n  v . w = 0  <->  v perpendicular to w\n\n  Orthonormal bases: every vector written\n  as v = (v.e1)*e1 + (v.e2)*e2 + ...\n\n  QR decomposition, Gram-Schmidt:\n  Turn any basis into orthonormal basis\n\n  PCA: find orthogonal directions of variation", font_size=22, color=YELL).move_to(ORIGIN)
        ob = self._box(ortho, border=YELL, buff=0.38)
        self.play(FadeIn(ob), Write(ortho), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes()
        v = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=4, buff=0)
        w = Arrow(ax.c2p(0,0), ax.c2p(2,2), color=RED, stroke_width=4, buff=0)
        self.play(Create(ax), Create(v), Create(w), run_time=2.0); self.wait(0.8)
        sm = Text("The Dot Product\n\n  v . w = vx*wx + vy*wy\n       = |v||w|cos(theta)\n\n  = 0  <->  orthogonal\n  > 0  <->  same direction\n  < 0  <->  opposite direction\n\n  Projection, angle, similarity\n  Work, lighting, attention, cosine sim", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
