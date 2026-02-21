"""la_03_scalar_mult.py — Scalar Multiplication

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


class ScalarMultScene(Scene):
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
        t1 = Text("Scalar Multiplication", font_size=50, color=WHITE)
        t2 = Text("Stretching, Shrinking, and Flipping Vectors", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("A single number can transform a vector.", font_size=36, color=WHITE)
        q2 = Text("Multiply by 2: it doubles in length.", font_size=34, color=WHITE)
        q3 = Text("Multiply by -1: it completely reverses direction.", font_size=30, color=YELL)
        q1.move_to(UP * 1.5); q2.next_to(q1, DOWN, buff=0.45); q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        v = _arr(plane, (0, 0), (1.5, 0.8), BLUE, sw=4)
        self.play(GrowArrow(v), run_time=0.8); self.wait(0.5)

        r1 = Text("Start with vector v.", font_size=26, color=BLUE)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1)); self.wait(1)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3); self.wait(0.2)

        v2 = _arr(plane, (0, 0), (3.0, 1.6), YELL, sw=5)
        r2 = Text("Multiply by 2:\nv doubles in length.", font_size=26, color=YELL)
        self._rp(r2, y=1.5)
        b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.4)
        self.play(Transform(v, v2), run_time=2.5); self.wait(2)

    def s2_geometry(self):
        self._sec("Geometric Intuition")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        base_tip = (1.5, 0.8)
        v_orig = _arr(plane, (0, 0), base_tip, BLUE, sw=4)
        self.play(GrowArrow(v_orig), run_time=0.8); self.wait(0.5)

        r_base = Text("Original vector v", font_size=26, color=BLUE)
        self._rp(r_base, y=2.0)
        b_base = self._box(r_base, border=BLUE)
        self.play(FadeIn(b_base), Write(r_base)); self.wait(1)

        scalars = [(2.0, YELL, "2v — doubled length"),
                   (0.5, GREEN, "0.5v — halved length"),
                   (-1.0, RED, "-1v — reversed direction"),
                   (-2.0, RED, "-2v — doubled + reversed")]

        for c, col, desc in scalars:
            tip = (base_tip[0] * c, base_tip[1] * c)
            # zero-length guard
            if abs(c) < 0.05:
                continue
            v_new = _arr(plane, (0, 0), tip, col, sw=4)
            self.play(FadeOut(b_base), FadeOut(r_base), run_time=0.3); self.wait(0.2)
            r_new = Text(desc, font_size=26, color=col)
            self._rp(r_new, y=2.0)
            b_new = self._box(r_new, border=col)
            self.play(FadeIn(b_new), Write(r_new)); self.wait(0.3)
            self.play(Transform(v_orig, v_new), run_time=2.5); self.wait(1.5)
            b_base, r_base = b_new, r_new

        self.wait(1)

    def s3_notation(self):
        self._sec("The Formal Definition")

        eq = Text("c  \u00d7  v  =  cv", font_size=58, color=GREEN)
        eq.move_to(UP * 2.0)
        self.play(Write(eq), run_time=2); self.wait(0.5)

        note = Text(
            "If v = [v\u2081, v\u2082], then:\n\n"
            "cv = [c\u00b7v\u2081,  c\u00b7v\u2082]\n\n"
            "Each component multiplied by c.",
            font_size=28, color=WHITE,
        )
        note.move_to(UP * 0.2)
        nb = self._box(note, border=WHITE, buff=0.32)
        self.play(FadeIn(nb), Write(note), run_time=1.5); self.wait(3)
        self.play(FadeOut(nb), FadeOut(note), FadeOut(eq), run_time=0.5); self.wait(0.4)

        props = Text(
            "Key properties:\n\n"
            "  c(u + v) = cu + cv\n"
            "  (c + d)v = cv + dv\n"
            "  (cd)v = c(dv)\n"
            "  1v = v\n"
            "  0v = zero vector",
            font_size=26, color=WHITE,
        )
        props.move_to(ORIGIN)
        pb = self._box(props, border=YELL, buff=0.35)
        self.play(FadeIn(pb), Write(props), run_time=1.5); self.wait(3)

    def s4_example(self):
        self._sec("Worked Example")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.4)

        mh = Text("v = [2, 1]", font_size=30, color=BLUE)
        mh.move_to(RIGHT * 3.5 + UP * 2.8)
        mb = self._box(mh, border=BLUE)
        self.play(FadeIn(mb), Write(mh)); self.wait(0.5)

        v = _arr(plane, (0, 0), (2.0, 1.0), BLUE, sw=4)
        self.play(GrowArrow(v), run_time=0.8); self.wait(0.5)

        def L(y): return LEFT * 3.0 + UP * y

        cases = [
            (3.0,  YELL,  "3v = [6, 3]",  (3 * 2.0, 3 * 1.0)),
            (0.5,  GREEN, "0.5v = [1, 0.5]", (0.5 * 2.0, 0.5 * 1.0)),
            (-1.0, RED,   "-v = [-2, -1]", (-2.0, -1.0)),
        ]

        y_pos = 1.5
        for c, col, desc, tip in cases:
            s = Text(desc, font_size=26, color=col)
            s.move_to(L(y_pos))
            sb = self._box(s, border=col, buff=0.22)
            self.play(FadeIn(sb), Write(s)); self.wait(0.4)

            v_new = _arr(plane, (0, 0), tip, col, sw=4)
            self.play(Transform(v, v_new), run_time=2.5); self.wait(1.5)
            y_pos -= 1.1

        self.wait(1)

    def s5_insight(self):
        self._sec("The Deeper Insight")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.5)

        v = _arr(plane, (0, 0), (1.5, 1.0), BLUE, sw=4)
        self.play(GrowArrow(v), run_time=0.8); self.wait(0.5)

        ins = Text(
            "Scalar multiplication preserves DIRECTION.\nOnly the magnitude changes.\n\n"
            "This is a 1D linear transformation\nalong the vector's own axis.\n\n"
            "Eigenvectors are exactly the vectors\nthat behave this way under a MATRIX:",
            font_size=23, color=WHITE,
        )
        self._rp(ins, y=0.5)
        ib = self._box(ins, border=WHITE, buff=0.28)
        self.play(FadeIn(ib), Write(ins), run_time=1.5); self.wait(2)

        eigen_note = Text("Av = \u03bbv\n(matrix multiplication = scalar multiplication)", font_size=24, color=YELL)
        eigen_note.next_to(ib, DOWN, buff=0.5)
        eb = self._box(eigen_note, border=YELL)
        self.play(FadeIn(eb), Write(eigen_note)); self.wait(3)

    def s6_summary(self):
        self._sec("Summary")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)

        v = _arr(plane, (0, 0), (1.5, 0.8), BLUE, sw=4)
        v2 = _arr(plane, (0, 0), (3.0, 1.6), YELL, sw=4)
        vm = _arr(plane, (0, 0), (-1.5, -0.8), RED, sw=4)
        self.play(GrowArrow(v), GrowArrow(v2), GrowArrow(vm)); self.wait(0.5)

        sm = Text(
            "Scalar Multiplication\n\n"
            "  cv = [cv\u2081, cv\u2082]\n\n"
            "  c > 1  \u2192  stretches\n"
            "  0 < c < 1  \u2192  shrinks\n"
            "  c < 0  \u2192  reverses + scales\n"
            "  c = 0  \u2192  zero vector",
            font_size=24, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
