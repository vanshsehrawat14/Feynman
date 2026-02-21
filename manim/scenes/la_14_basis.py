"""Feynman – Basis (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class BasisScene(Scene):
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
        t = Text("Basis", font_size=56, color=WHITE).move_to(UP*0.5)
        t2 = Text("The coordinate system", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("The x-y axes we use are just one choice.\nYou could measure the same world using\ndifferent rulers pointing in different directions.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("A basis is a choice of coordinate system.\nEvery vector has unique coordinates in that basis.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("A BASIS of R^n is a set of vectors that:\n  1. Spans R^n  (can reach every point)\n  2. Is linearly independent  (no redundancy)\n\nEvery vector v has a UNIQUE representation:\n  v = c1*b1 + c2*b2 + ... + cn*bn", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Standard vs Non-Standard Basis")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        e1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=5, buff=0)
        e2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=5, buff=0)
        e1l = Text("e1=(1,0)", font_size=20, color=BLUE).next_to(plane.c2p(1,0), UP, buff=0.1)
        e2l = Text("e2=(0,1)", font_size=20, color=RED).next_to(plane.c2p(0,1), RIGHT, buff=0.1)
        self.play(Create(e1), Create(e2), Write(e1l), Write(e2l), run_time=2.0); self.wait(0.8)
        r1 = Text("Standard basis\nfor R^2", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(2.3)
        b1_vec = Arrow(plane.c2p(0,0), plane.c2p(1,1), color=YELL, stroke_width=5, buff=0)
        b2_vec = Arrow(plane.c2p(0,0), plane.c2p(-1,1), color=GREEN, stroke_width=5, buff=0)
        b1l = Text("b1=(1,1)", font_size=20, color=YELL).next_to(plane.c2p(0.5,0.5), LEFT, buff=0.1)
        b2l = Text("b2=(-1,1)", font_size=20, color=GREEN).next_to(plane.c2p(-0.5,0.5), LEFT, buff=0.1)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        r2 = Text("Rotated basis:\nalso valid!\nStill spans R^2, still independent", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(Create(b1_vec), Create(b2_vec), Write(b1l), Write(b2l), run_time=2.0)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Coordinates in a Basis")
        coord = Text("If B = {b1, b2} is a basis, then for any v:\n  v = c1*b1 + c2*b2  (unique c1, c2)\n  [v]_B = (c1, c2)  <- coordinates in basis B\n\nChange of basis: [v]_B = B^{-1} * [v]_std\nwhere B = matrix of basis vectors as columns.", font_size=24, color=WHITE).move_to(UP*0.8)
        cb = self._box(coord, border=BLUE, buff=0.38)
        self.play(FadeIn(cb), Write(coord), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(cb), FadeOut(coord), run_time=0.5)
        props = Text("Key facts:\n\n  All bases of R^n have exactly n vectors\n  (= dimension of the space)\n\n  Any n linearly independent vectors in R^n\n  form a basis of R^n\n\n  Standard basis: {e1=(1,0,...), e2=(0,1,...),...,en}\n  Orthonormal basis: all unit vectors, mutually perpendicular", font_size=23, color=YELL).move_to(ORIGIN)
        pb = self._box(props, border=YELL, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Find coordinates of v=(3,1) in B={(1,1),(-1,1)}")
        steps = [
            ("v = c1*(1,1) + c2*(-1,1) = (3,1)", WHITE, 2.5),
            ("c1 - c2 = 3   (x-equation)", BLUE, 1.7),
            ("c1 + c2 = 1   (y-equation)", BLUE, 0.9),
            ("Adding: 2*c1 = 4  ->  c1 = 2", GREEN, 0.1),
            ("Subtracting: 2*c2 = -2  ->  c2 = -1", GREEN, -0.7),
            ("[v]_B = (2, -1)", YELL, -1.5),
            ("Check: 2*(1,1) + (-1)*(-1,1) = (2,2)+(1,-1) = (3,1) ✓", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Choosing the RIGHT basis makes problems trivial:\n\n  Diagonal matrix in its eigenbasis:\n  -> matrix powers are trivial (just raise eigenvalues)\n\n  Signal in Fourier basis:\n  -> convolution becomes multiplication!\n\n  PCA: data in eigenvector basis\n  -> each coordinate is independent\n\n  The basis is a LANGUAGE for describing vectors.\n  Different languages, same mathematical truth.", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        practical = Text("Practical applications:\n\n  Computer graphics: local vs world coordinates\n  (object's own axes = its basis)\n\n  GPS: WGS84 coordinate basis\n  (specific basis for Earth's surface)\n\n  Quantum mechanics: measurement basis\n  (choice of basis = choice of measurement)\n\n  Audio: Fourier basis = frequency basis", font_size=22, color=YELL).move_to(ORIGIN)
        pb = self._box(practical, border=YELL, buff=0.38)
        self.play(FadeIn(pb), Write(practical), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        e1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=4, buff=0)
        e2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=4, buff=0)
        self.play(Create(plane), Create(e1), Create(e2), run_time=2.0); self.wait(0.8)
        sm = Text("Basis\n\n  Spans the space AND independent\n  Size = dimension of space\n\n  Unique coordinates for every vector\n  v = c1*b1 + ... + cn*bn\n\n  Standard: {e1,e2,...,en}\n  Change basis: B^{-1} * v\n\n  Right basis = trivial computation", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
