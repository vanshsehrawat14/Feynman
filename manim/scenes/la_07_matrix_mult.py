"""la_07_matrix_mult.py — Matrix Multiplication

6-section narrative, ≈ 4 minutes.
"""
from manim import *
from la_utils import *
import numpy as np


def _mk_plane():
    return make_plane().scale(0.72).shift(LEFT * 2.6)


def _arr(plane, start, end, color=BLUE, sw=3):
    s = plane.c2p(*start)
    e = plane.c2p(*end)
    if np.linalg.norm(e - s) < 0.08:
        return VMobject()
    return Arrow(s, e, buff=0, color=color,
                 stroke_width=sw, max_tip_length_to_length_ratio=0.18)


class MatrixMultScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.s1_hook(); self._fade_all()
        self.s2_geometry(); self._fade_all()
        self.s3_notation(); self._fade_all()
        self.s4_example(); self._fade_all()
        self.s5_insight(); self._fade_all()
        self.s6_summary()

    def _fade_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)
        self.wait(0.3)

    def _sec(self, title): sec_label(self, title)
    def _box(self, mob, border=WHITE, buff=0.28): return text_box(mob, border=border, buff=buff)
    def _rp(self, mob, y=0.0, x=4.1):
        mob.move_to(RIGHT * x + UP * y); return mob

    def s1_hook(self):
        t1 = Text("Matrix Multiplication", font_size=46, color=WHITE)
        t2 = Text("Composing Transformations", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("Matrix multiplication looks complicated.", font_size=36, color=WHITE)
        q2 = Text("But geometrically, it's simple:", font_size=36, color=WHITE)
        q3 = Text("AB means 'apply B, then apply A'.", font_size=36, color=YELL)
        q1.move_to(UP * 1.4); q2.next_to(q1, DOWN, buff=0.45); q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        intro = Text("Two transformations.\nApply them in sequence.", font_size=26, color=WHITE)
        self._rp(intro, y=1.2)
        bi = self._box(intro, border=WHITE)
        self.play(FadeIn(bi), Write(intro)); self.wait(0.8)

        B = [[0, -1], [1, 0]]   # rotate 90°
        A = [[2,  0], [0, 2]]   # scale 2x

        self.play(FadeOut(bi), FadeOut(intro), run_time=0.3); self.wait(0.2)
        r1 = Text("Step 1: Rotate 90\u00b0 (matrix B)...", font_size=24, color=YELL)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1)); self.wait(0.4)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        self.play(plane.animate.apply_matrix(B), run_time=3); self.wait(1)

        r2 = Text("Step 2: Scale x2 (matrix A).", font_size=24, color=BLUE)
        self._rp(r2, y=1.5)
        b2 = self._box(r2, border=BLUE)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.4)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        self.play(plane.animate.apply_matrix(A), run_time=3); self.wait(1)

        r3 = Text("AB combined both steps\ninto one matrix.", font_size=26, color=GREEN)
        self._rp(r3, y=1.2)
        b3 = self._box(r3, border=GREEN)
        self.play(FadeIn(b3), Write(r3)); self.wait(2.5)

    def s2_geometry(self):
        self._sec("Composition Is the Key")

        AB = np.array([[2, 0], [0, 2]]) @ np.array([[0, -1], [1, 0]])

        r1 = Text(
            "Matrix multiplication AB\nmeans: apply B first,\nthen apply A.\n\n"
            "Order matters!\nAB is generally NOT equal to BA.",
            font_size=26, color=WHITE,
        )
        r1.move_to(LEFT * 1.5 + UP * 0.5)
        b1 = self._box(r1, border=WHITE, buff=0.32)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.5); self.wait(0.3)

        # Demonstrate non-commutativity
        plane1 = _mk_plane()
        self.play(Create(plane1), run_time=1.2); self.wait(0.4)

        A = [[2, 0], [0, 1]]   # scale x
        B = [[1, 0], [0, 2]]   # scale y
        # AB: scale x then scale y = [[2,0],[0,2]] (same here, bad example)
        # Better: rotation then shear vs shear then rotation
        R = [[0, -1], [1, 0]]    # rotate 90
        S = [[1, 1], [0, 1]]     # shear

        r2 = Text("Apply shear first, then rotate:", font_size=24, color=BLUE)
        self._rp(r2, y=2.2)
        b2 = self._box(r2, border=BLUE)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.3)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        self.play(plane1.animate.apply_matrix(S), run_time=2.5); self.wait(0.5)
        self.play(plane1.animate.apply_matrix(R), run_time=2.5); self.wait(1)

        rs_note = Text("R(Sv): shear then rotate", font_size=22, color=BLUE)
        self._rp(rs_note, y=2.2)
        brs = self._box(rs_note, border=BLUE)
        self.play(FadeIn(brs), Write(rs_note)); self.wait(1.5)

        # Reset and show opposite order
        RS = np.array(R) @ np.array(S)
        inv_RS = np.linalg.inv(RS)
        self.play(FadeOut(brs), FadeOut(rs_note),
                  plane1.animate.apply_matrix(inv_RS.tolist()), run_time=1.5); self.wait(0.3)

        r3 = Text("Now rotate first, then shear:", font_size=24, color=YELL)
        self._rp(r3, y=2.2)
        b3 = self._box(r3, border=YELL)
        self.play(FadeIn(b3), Write(r3)); self.wait(0.3)
        self.play(FadeOut(b3), FadeOut(r3), run_time=0.3)
        self.play(plane1.animate.apply_matrix(R), run_time=2.5); self.wait(0.5)
        self.play(plane1.animate.apply_matrix(S), run_time=2.5); self.wait(1)

        r4 = Text("S(Rv): rotate then shear.\nDifferent result!", font_size=22, color=YELL)
        self._rp(r4, y=2.2)
        b4 = self._box(r4, border=YELL)
        self.play(FadeIn(b4), Write(r4)); self.wait(3)

    def s3_notation(self):
        self._sec("The Formula")

        eq = Text(
            "(AB)\u1d62\u2C7C = \u03a3  A\u1d62\u2096 \u00d7 B\u2096\u2C7C",
            font_size=44, color=GREEN,
        )
        eq.move_to(UP * 2.2)
        self.play(Write(eq), run_time=2); self.wait(0.5)

        note = Text(
            "Each entry (i,j) of AB\n"
            "= dot product of row i of A\n"
            "  with column j of B.",
            font_size=28, color=WHITE,
        )
        note.move_to(UP * 0.5)
        nb = self._box(note, border=WHITE, buff=0.32)
        self.play(FadeIn(nb), Write(note), run_time=1.5); self.wait(3)
        self.play(FadeOut(nb), FadeOut(note), FadeOut(eq), run_time=0.5); self.wait(0.4)

        cond = Text(
            "Dimension rule:\n\n"
            "A is (m \u00d7 n)\n"
            "B is (n \u00d7 p)\n"
            "AB is (m \u00d7 p)\n\n"
            "Inner dimensions must match!",
            font_size=26, color=YELL,
        )
        cond.move_to(ORIGIN)
        cb = self._box(cond, border=YELL, buff=0.35)
        self.play(FadeIn(cb), Write(cond), run_time=1.5); self.wait(3)

    def s4_example(self):
        self._sec("Worked Example")

        def L(y): return LEFT * 3.2 + UP * y

        mA = Text("A = [ 1   2 ]\n    [ 3   4 ]", font_size=28, color=BLUE)
        mA.move_to(RIGHT * 2.8 + UP * 2.5)
        bA = self._box(mA, border=BLUE, buff=0.26)
        self.play(FadeIn(bA), Write(mA)); self.wait(0.4)

        mB = Text("B = [ 5   6 ]\n    [ 7   8 ]", font_size=28, color=YELL)
        mB.move_to(RIGHT * 2.8 + UP * 0.8)
        bB = self._box(mB, border=YELL, buff=0.26)
        self.play(FadeIn(bB), Write(mB)); self.wait(0.8)

        s1 = Text("AB entry (1,1):", font_size=24, color=WHITE)
        s1.move_to(L(1.2)); self.play(FadeIn(s1)); self.wait(0.3)

        s2 = Text("row1(A) \u00b7 col1(B)", font_size=22, color=WHITE)
        s2.move_to(L(0.4)); self.play(Write(s2)); self.wait(0.3)

        s3 = Text("= 1\u00d75 + 2\u00d77 = 19", font_size=24, color=GREEN)
        s3.move_to(L(-0.4)); self.play(Write(s3)); self.wait(0.5)

        s4 = Text("AB entry (1,2) = 1\u00d76 + 2\u00d78 = 22", font_size=22, color=WHITE)
        s4.move_to(L(-1.2)); self.play(Write(s4)); self.wait(0.5)

        s5 = Text("AB entry (2,1) = 3\u00d75 + 4\u00d77 = 43", font_size=22, color=WHITE)
        s5.move_to(L(-2.0)); self.play(Write(s5)); self.wait(0.5)

        result = Text("AB = [ 19   22 ]\n     [ 43   50 ]", font_size=28, color=GREEN)
        result.move_to(RIGHT * 2.8 + UP * -1.5)
        rb = self._box(result, border=GREEN, buff=0.26)
        self.play(FadeIn(rb), Write(result)); self.wait(3)

    def s5_insight(self):
        self._sec("The Deeper Insight")

        ins = Text(
            "Matrix multiplication is\ntransformation composition.\n\n"
            "This connects to:\n\n"
            "Computer graphics: 3D rotations,\n"
            "  translations = matrix products\n\n"
            "Deep learning: neural networks\n"
            "  = stacked matrix multiplications\n\n"
            "Quantum mechanics: observables\n"
            "  = matrix operators",
            font_size=23, color=WHITE,
        )
        ins.move_to(LEFT * 1.5)
        ib = self._box(ins, border=BLUE, buff=0.32)
        self.play(FadeIn(ib), Write(ins), run_time=1.5); self.wait(3)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5); self.wait(0.3)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.4)

        # Show associativity: A(BC) = (AB)C
        A = [[1.5, 0.3], [0.1, 1.2]]
        B = [[0, -1], [1, 0]]
        C = [[1, 0.5], [0, 1]]
        ABC = np.array(A) @ np.array(B) @ np.array(C)

        r1 = Text("A(BC) = (AB)C\nOrder of grouping does\nnot change the result.", font_size=24, color=YELL)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1)); self.wait(0.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3); self.wait(0.2)
        self.play(plane.animate.apply_matrix(ABC.tolist()), run_time=3.5); self.wait(2.5)

    def s6_summary(self):
        self._sec("Summary")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)
        A = [[1.2, 0.4], [0, 1.3]]
        B = [[0, -1], [1, 0]]
        self.play(plane.animate.apply_matrix(B), run_time=2); self.wait(0.3)
        self.play(plane.animate.apply_matrix(A), run_time=2); self.wait(0.5)

        sm = Text(
            "Matrix Multiplication\n\n"
            "  AB = apply B, then A\n\n"
            "  NOT commutative: AB \u2260 BA\n"
            "  IS associative: A(BC) = (AB)C\n\n"
            "  Each entry = dot product\n"
            "  of a row with a column.",
            font_size=24, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
