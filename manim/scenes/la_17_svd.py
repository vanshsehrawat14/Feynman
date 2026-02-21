"""Feynman – Singular Value Decomposition (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class SVDScene(Scene):
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
        t = Text("SVD", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("The most important decomposition in data science", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Any matrix, no matter how complex,\ncan be decomposed into three simple operations:\nrotation, stretching, rotation again.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("SVD reveals the hidden geometry\nof ANY linear transformation.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("SVD: A = U * Sigma * V^T\n\n  U:     m x m orthogonal (left singular vectors)\n  Sigma: m x n diagonal (singular values)\n  V^T:   n x n orthogonal (right singular vectors)\n\nWorks for ANY matrix (square or not)!", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Geometric Interpretation")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        circ = Circle(radius=1.5, color=BLUE, stroke_width=3).move_to(plane.c2p(0,0))
        self.play(Create(circ), run_time=1.5); self.wait(0.8)
        r1 = Text("Step 1: V^T rotates input space", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(2.3)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        ell = Ellipse(width=3.0, height=1.5, color=YELL, stroke_width=3).move_to(plane.c2p(0,0))
        r2 = Text("Step 2: Sigma stretches along axes\n(singular values = stretch factors)", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(Transform(circ, ell), FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        ell2 = Ellipse(width=3.0, height=1.5, color=GREEN, stroke_width=3).move_to(plane.c2p(0,0)).rotate(PI/4)
        r3 = Text("Step 3: U rotates output space\nResult: any matrix = rotation+scale+rotation", font_size=22, color=GREEN)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=GREEN)
        self.play(Transform(circ, ell2), FadeIn(b3), Write(r3), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "SVD Properties")
        props = Text("Singular values (sigma_1 >= sigma_2 >= ... >= 0):\n  Square roots of eigenvalues of A^T A\n  = stretch factors of the transformation\n  = 'strength' of each independent component\n\nRank of A = number of non-zero singular values\n\nCondition number = sigma_max / sigma_min\n(measures numerical stability)", font_size=23, color=WHITE).move_to(UP*0.5)
        pb = self._box(props, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(pb), FadeOut(props), run_time=0.5)
        low_rank = Text("Low-rank approximation (truncated SVD):\n  A_k = U_k * Sigma_k * V_k^T\n  Keep only top k singular values/vectors!\n\n  Minimizes |A - A_k|_F (Frobenius norm)\n  = best rank-k approximation\n  = image compression, noise reduction!", font_size=23, color=YELL).move_to(ORIGIN)
        lb = self._box(low_rank, border=YELL, buff=0.38)
        self.play(FadeIn(lb), Write(low_rank), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "SVD Applications")
        steps = [
            ("Recommender systems (Netflix, Spotify):", WHITE, 2.8),
            ("  Matrix: users x items (ratings)", BLUE, 2.0),
            ("  SVD reveals latent factors (genres, themes)", GREEN, 1.2),
            ("  Low-rank approx. fills in missing ratings", YELL, 0.4),
            ("Image compression (JPEG-like):", WHITE, -0.4),
            ("  Image = matrix of pixel values", BLUE, -1.2),
            ("  Keep top k singular values -> compressed image", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("SVD is the cornerstone of numerical linear algebra:\n\n  PCA: principal components = right singular vectors of\n  centered data matrix (V columns of SVD)\n\n  Pseudoinverse: A+ = V Sigma+ U^T\n  (solves least squares for non-square A)\n\n  LSI (NLP): SVD of term-document matrix\n  reveals semantic structure of language\n\n  Numerical rank: count sigma_i > epsilon", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        compare = Text("SVD vs Eigendecomposition:\n  Eigendecomposition: A = P D P^{-1}\n  Only for square diagonalizable matrices\n\n  SVD: A = U Sigma V^T\n  Works for ANY matrix (m x n)!\n  U, V are orthogonal (not inverse of each other)\n  Sigma has singular values (not eigenvalues)\n\n  SVD is more general and more numerically stable.", font_size=22, color=YELL).move_to(ORIGIN)
        cb = self._box(compare, border=YELL, buff=0.38)
        self.play(FadeIn(cb), Write(compare), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("SVD  A = U Sigma V^T\n\n  U: left singular vectors (output directions)\n  Sigma: singular values (stretch factors)\n  V^T: right singular vectors (input directions)\n\n  Works for ANY matrix (m x n)\n  Singular values: sqrt(eigenvalues of A^T A)\n\n  Applications:\n  PCA, compression, recommenders,\n  least squares, noise reduction, NLP", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
