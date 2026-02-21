"""Feynman – Column Space (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class ColumnSpaceScene(Scene):
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
        t = Text("Column Space", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("All reachable outputs of a matrix", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("For the transformation Ax, as x ranges\nover all possible input vectors,\nwhere can Ax land?", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("The set of all reachable outputs\nis the column space of A.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("col(A) = {Ax : x in R^n} = span of columns of A\n\nAx = x1*col1 + x2*col2 + ... + xn*coln\n(linear combination of columns!)\n\nAx=b has a solution iff b is in col(A).", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Column Space as Image")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        c1 = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=BLUE, stroke_width=5, buff=0)
        c2 = Arrow(plane.c2p(0,0), plane.c2p(-1,2), color=RED, stroke_width=5, buff=0)
        c1l = Text("col1=(2,1)", font_size=20, color=BLUE).next_to(plane.c2p(1,0.5), DOWN, buff=0.1)
        c2l = Text("col2=(-1,2)", font_size=20, color=RED).next_to(plane.c2p(-0.5,1), LEFT, buff=0.1)
        self.play(Create(c1), Create(c2), Write(c1l), Write(c2l), run_time=2.0); self.wait(0.8)
        r1 = Text("Two independent columns:\ncol(A) = entire R^2\n(rank 2 = full column rank)", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(b1), FadeOut(r1), FadeOut(c2), FadeOut(c2l), run_time=0.3)
        c2_dep = Arrow(plane.c2p(0,0), plane.c2p(4,2), color=RED, stroke_width=5, buff=0)
        line_col = Line(plane.c2p(-3,-1.5), plane.c2p(3,1.5), color=YELL, stroke_width=2)
        self.play(Create(c2_dep), Create(line_col), run_time=1.5); self.wait(0.6)
        r2 = Text("Parallel columns:\ncol(A) = just a line\n(rank 1, cannot reach off-line b)", font_size=22, color=RED)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Finding the Column Space")
        method = Text("col(A) = span of the PIVOT COLUMNS of A\n(after row reduction, identify pivot columns,\nthen take those ORIGINAL columns)\n\ndim(col(A)) = rank(A) = number of pivots\n\nNote: row operations change col(A)!\nAlways go back to ORIGINAL columns.", font_size=24, color=WHITE).move_to(UP*0.8)
        mb = self._box(method, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(method), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(mb), FadeOut(method), run_time=0.5)
        key = Text("Fundamental relationships:\n\n  Ax = b solvable  iff  b in col(A)\n  col(A) = image/range of A as transformation\n  row(A) = col(A^T) = image of A^T\n  null(A) perp to row(A)  (orthogonal complement!)\n  col(A) perp to null(A^T)\n\nFour fundamental subspaces of A!", font_size=23, color=YELL).move_to(ORIGIN)
        kb = self._box(key, border=YELL, buff=0.38)
        self.play(FadeIn(kb), Write(key), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Column Space of [[1,3,2],[2,6,4]]")
        steps = [
            ("A = [[1,3,2],[2,6,4]]", WHITE, 2.5),
            ("Row reduce: R2 = R2 - 2*R1", BLUE, 1.7),
            ("-> [[1,3,2],[0,0,0]]", GREEN, 0.9),
            ("Only 1 pivot (column 1).", WHITE, 0.1),
            ("col(A) = span{original col 1} = span{(1,2)}", YELL, -0.7),
            ("rank = 1, col(A) is a line in R^2", GREEN, -1.5),
            ("b=(3,6) is in col(A): 3*(1,2)=(3,6) ✓", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Four Fundamental Subspaces")
        ins = Text("Every m x n matrix A has four subspaces:\n\n  1. Column space col(A) in R^m   dim=rank\n  2. Null space null(A) in R^n   dim=n-rank\n  3. Row space row(A) in R^n     dim=rank\n  4. Left null space null(A^T) in R^m  dim=m-rank\n\n  Orthogonal pairs:\n  null(A) perp row(A)  (in R^n)\n  null(A^T) perp col(A)  (in R^m)\n\nGilbert Strang: the four subspaces are\nthe heart of linear algebra.", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications:\n\n  Least squares: project b onto col(A)\n  -> normal equations: A^T A x = A^T b\n  -> solution minimizes |Ax-b|\n\n  Dimensionality: col(A) tells output dimension\n  null(A) tells lost dimensions\n\n  Image of transformation = col(A)\n  Every ML model has a column space!", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Column Space  col(A)\n\n  = span of columns = all possible Ax\n  = image/range of transformation\n\n  dim = rank(A) = number of pivots\n\n  Ax=b solvable iff b in col(A)\n\n  Four subspaces: col, null, row, left null\n  Orthogonal pairs: null perp row, col perp left-null\n\n  Foundation of least squares", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
