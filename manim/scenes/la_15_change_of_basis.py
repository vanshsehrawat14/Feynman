"""Feynman – Change of Basis (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class ChangeBasisScene(Scene):
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
        t = Text("Change of Basis", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("Translating between coordinate systems", font_size=24, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Your friend uses different axes than you.\nThe SAME physical point has different coordinates\ndepending on who measures it.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Change of basis converts between coordinate systems.\nSame vector, different language.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("If B = [b1 | b2 | ... | bn] (basis as matrix of columns)\n\n  Standard to B coordinates: [v]_B = B^{-1} * v\n  B coordinates to standard: v = B * [v]_B\n\nTransformation in new basis:\n  A_B = B^{-1} * A * B  (change of basis formula)", font_size=24, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Two Coordinate Systems")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        std1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=4, buff=0)
        std2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=BLUE, stroke_width=4, buff=0)
        self.play(Create(std1), Create(std2), run_time=1.5)
        r1 = Text("Standard basis: e1=(1,0), e2=(0,1)", font_size=22, color=BLUE)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(2.3)
        b1_v = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=YELL, stroke_width=4, buff=0)
        b2_v = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=GREEN, stroke_width=4, buff=0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        r2 = Text("New basis: b1=(2,1), b2=(0,2)\nDifferent grid, same plane", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(Create(b1_v), Create(b2_v), run_time=1.5)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
        pt = Dot(plane.c2p(2,3), color=RED, radius=0.12)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        r3 = Text("Point (2,3) in standard\ncoords = what in new basis?", font_size=22, color=RED)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=RED)
        self.play(Create(pt), FadeIn(b3), Write(r3), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "The Change-of-Basis Formula")
        formula = Text("B = [[2, 0],   (columns are basis vectors)\n     [1, 2]]\n\nB^{-1} = (1/det) * [[2, 0],  det = 4\n                    [-1, 2]]\n       = [[0.5, 0],\n          [-0.25, 0.5]]", font_size=24, color=YELL).move_to(UP*0.8)
        fb = self._box(formula, border=YELL, buff=0.38)
        self.play(FadeIn(fb), Write(formula), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(fb), FadeOut(formula), run_time=0.5)
        similar = Text("Similarity transformation:\n  A_B = B^{-1} A B\n\nWhy?  The matrix A acts in standard coords.\n  B converts FROM new TO standard\n  A does the transformation\n  B^{-1} converts BACK to new coordinates\n\nSimilar matrices represent the SAME transformation\nin different coordinate systems!", font_size=23, color=WHITE).move_to(ORIGIN)
        sb = self._box(similar, border=BLUE, buff=0.38)
        self.play(FadeIn(sb), Write(similar), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Example: (2,3) in basis {(2,1),(0,2)}")
        steps = [
            ("B = [[2,0],[1,2]], v = (2,3)", WHITE, 2.5),
            ("B^{-1} = (1/4)*[[2,0],[-1,2]]", BLUE, 1.7),
            ("[v]_B = B^{-1} * v", WHITE, 0.9),
            ("= (1/4) * [[2,0],[-1,2]] * (2,3)", WHITE, 0.1),
            ("= (1/4) * (4, 4) = (1, 1)", GREEN, -0.7),
            ("So v = 1*b1 + 1*b2 = (2,1)+(0,2) = (2,3) ✓", YELL, -1.5),
            ("Coordinates (1,1) in the new basis!", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "Why This Matters")
        ins = Text("Diagonalization is change of basis!\n\n  A = P D P^{-1}\n  P = eigenvectors  (basis change matrix)\n  D = diagonal (eigenvalues)\n\n  In eigenbasis, A becomes diagonal.\n  D is the same transformation in a better language.\n\n  Matrix powers: A^n = P D^n P^{-1}\n  Just raise diagonal entries to nth power!", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications everywhere:\n\n  Computer graphics: model->world->camera->screen\n  (4 different bases, 4 coordinate transforms)\n\n  Fourier transform: time basis -> frequency basis\n  Convolution in time = multiplication in frequency!\n\n  Quantum: measurement collapses to measurement basis\n\n  PCA: data basis -> principal component basis", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Change of Basis\n\n  B = matrix of new basis vectors (columns)\n  Standard -> new: [v]_B = B^{-1} v\n  New -> standard: v = B [v]_B\n\n  Transform in new basis:\n  A_B = B^{-1} A B  (similarity)\n\n  Diagonalization: A = P D P^{-1}\n  (eigenbasis is the BEST basis)\n\n  Fourier, PCA, graphics all use this", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
