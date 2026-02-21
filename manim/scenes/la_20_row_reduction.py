"""Feynman – Row Reduction (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class RowReductionScene(Scene):
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
        t = Text("Row Reduction", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Gaussian elimination step by step", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("How do you solve 3 equations with 3 unknowns?\nEliminate one variable at a time.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Row reduction (Gaussian elimination)\nsystematically simplifies any system of equations.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Three elementary row operations:\n  1. Swap two rows\n  2. Multiply a row by a non-zero scalar\n  3. Add a multiple of one row to another\n\nThese preserve the solution set!\nGoal: Reduced Row Echelon Form (RREF)", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Visualizing Row Reduction")
        steps = [
            ("System:  2x+y=5,  4x+3y=11", WHITE, 2.8),
            ("Matrix:  [[2,1|5],[4,3|11]]", BLUE, 2.0),
            ("R2 = R2 - 2*R1:", WHITE, 1.2),
            ("-> [[2,1|5],[0,1|1]]", GREEN, 0.4),
            ("Back substitute: y=1", YELL, -0.4),
            ("2x + 1 = 5  ->  x = 2", YELL, -1.2),
            ("Solution: x=2, y=1", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=26, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "RREF and Pivot Structure")
        rref = Text("Row Echelon Form (REF):\n  Leading entry (pivot) in each row\n  > all entries below it\n  Rows of zeros at bottom\n\nReduced REF (RREF) - extra conditions:\n  Each pivot = 1\n  Each pivot is only nonzero in its column\n\nRREF is unique for any matrix!", font_size=24, color=WHITE).move_to(UP*0.8)
        rb = self._box(rref, border=BLUE, buff=0.38)
        self.play(FadeIn(rb), Write(rref), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(rb), FadeOut(rref), run_time=0.5)
        info = Text("What RREF reveals:\n  Pivot columns -> linearly independent columns\n  Free columns -> dependent, free variables\n  Number of pivots = rank(A)\n  Zero rows -> dimension of left null space\n  RREF directly gives basis for null space!", font_size=23, color=YELL).move_to(ORIGIN)
        ib = self._box(info, border=YELL, buff=0.38)
        self.play(FadeIn(ib), Write(info), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Full RREF: 3x3 System")
        steps = [
            ("A = [[1,2,1],[2,4,3],[3,6,4]]", WHITE, 2.8),
            ("R2=R2-2R1: [[1,2,1],[0,0,1],[3,6,4]]", BLUE, 2.0),
            ("R3=R3-3R1: [[1,2,1],[0,0,1],[0,0,1]]", BLUE, 1.2),
            ("R3=R3-R2:  [[1,2,1],[0,0,1],[0,0,0]]", GREEN, 0.4),
            ("R1=R1-R2:  [[1,2,0],[0,0,1],[0,0,0]]", GREEN, -0.4),
            ("Pivots: cols 1,3. Free: col 2 (x2=t)", YELL, -1.2),
            ("Solution: x1=-2t, x2=t, x3=0", WHITE, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Row reduction IS LU decomposition:\n\n  Each row operation = a shear matrix L_i\n  A = L1 * L2 * ... * Lk * U\n  -> A = L * U  (L lower triangular, U upper triangular)\n\n  LU decomposition is the practical algorithm\n  for solving Ax=b (with pivoting: PLU)\n\n  Cost: O(n^3) operations\n  Used in every numerical linear algebra solver!", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications of Gaussian elimination:\n\n  Circuit analysis (Kirchhoff laws -> linear system)\n  Computer graphics (intersection of planes)\n  Economics (input-output models: Leontief)\n  Cryptography (solving modular linear systems)\n  Finite element method (engineering simulation)\n\n  LAPACK/BLAS: optimized for modern CPUs\n  NumPy solve, MATLAB \\: all use LU/QR internally", font_size=21, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Row Reduction (Gaussian Elimination)\n\n  Three operations: swap, scale, add multiple\n  Preserve solution set\n\n  Goal: RREF (unique for any matrix)\n  Pivots = independent columns = rank\n  Free columns = null space directions\n\n  LU decomposition = row reduction stored\n  Cost: O(n^3)\n\n  Solves Ax=b, finds rank, null space, basis", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
