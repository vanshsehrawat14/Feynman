"""Feynman – Why Eigenvalues Matter (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class EigenWhyScene(Scene):
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
        t = Text("Why Eigenvalues Matter", font_size=40, color=WHITE).move_to(UP*0.5)
        t2 = Text("The natural vibration frequencies of a matrix", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("A matrix acts on every vector differently.\nAre there special vectors it only SCALES?\n\nA*v = lambda*v  (just scaling, no rotation!)", font_size=26, color=WHITE).move_to(UP*0.5)
        self.play(Write(q), run_time=2.5); self.wait(3.5)
        self.play(FadeOut(q), run_time=0.5)
        ans = Text("These special vectors = eigenvectors.\nTheir scale factors = eigenvalues.\n\nThey reveal the SKELETON of any transformation.", font_size=26, color=GREEN).move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Eigenvectors Stay on Their Line")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=RED, stroke_width=5, buff=0)
        l1 = Text("eigenvector 1", font_size=18, color=BLUE).next_to(plane.c2p(1,0), UP, buff=0.1)
        l2 = Text("eigenvector 2", font_size=18, color=RED).next_to(plane.c2p(0,1), RIGHT, buff=0.1)
        self.play(Create(v1), Create(v2), Write(l1), Write(l2), run_time=2.0); self.wait(0.8)
        v1_scaled = Arrow(plane.c2p(0,0), plane.c2p(3,0), color=BLUE, stroke_width=5, buff=0)
        v2_scaled = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=5, buff=0)
        r1 = Text("After matrix A acts:\nv1 scaled by lambda1=1.5\nv2 scaled by lambda2=0.5", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), Transform(v1, v1_scaled), Transform(v2, v2_scaled), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Only THESE directions stay on same line!\nAll other vectors rotate AND scale.\nEigenvectors = transformation invariant axes.", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Computing Eigenvalues")
        eq = Text("A*v = lambda*v\n(A - lambda*I)*v = 0\ndet(A - lambda*I) = 0  <- characteristic equation", font_size=26, color=YELL).move_to(UP*2.0)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.5); self.wait(2.3)
        procedure = Text("Procedure:\n  1. Form (A - lambda*I)\n  2. Set det = 0 -> characteristic polynomial\n  3. Solve for lambda (eigenvalues)\n  4. For each lambda: solve (A-lambda*I)v=0\n     -> get eigenvectors", font_size=24, color=WHITE).next_to(eq, DOWN, buff=0.5)
        pb = self._box(procedure, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(procedure), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Why Eigenvalues Drive Everything")
        steps = [
            ("Matrix powers: A^n = P D^n P^{-1}", WHITE, 2.8),
            ("D^n: just raise each eigenvalue to n!", BLUE, 2.0),
            ("Population dynamics: next = A * current", WHITE, 1.2),
            ("Long-term behavior: largest eigenvalue wins", GREEN, 0.4),
            ("PageRank: dominant eigenvector of link matrix", YELL, -0.4),
            ("Stability: system stable iff all |lambda| < 1", RED, -1.2),
            ("Vibration frequencies: eigenvalues of stiffness matrix", WHITE, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Eigenvalues ARE the matrix (in the right coordinates):\n\n  Diagonalization: A = P D P^{-1}\n  P = eigenvector matrix\n  D = diagonal of eigenvalues\n\n  In eigenbasis: A is purely diagonal!\n  Each direction scaled independently.\n  This is why eigenvectors are called\n  the natural coordinates of A.", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications everywhere:\n\n  PCA: eigenvectors of covariance matrix\n  = principal components (max variance directions)\n\n  Quantum mechanics: energy levels = eigenvalues\n  of Hamiltonian operator\n\n  Google PageRank: dominant eigenvector\n  of web graph transition matrix\n\n  Facial recognition, compression, simulation", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Why Eigenvalues Matter\n\n  Av = lambda*v  (scaling only, no rotation!)\n  Solve: det(A - lambda*I) = 0\n\n  Eigenvalues = natural scaling factors\n  Eigenvectors = invariant directions\n\n  Diagonalization: A = P D P^{-1}\n  In eigenbasis: trivial computation!\n\n  Powers, stability, PageRank, PCA,\n  quantum states, vibration modes", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
