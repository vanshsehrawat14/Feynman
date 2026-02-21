"""la_08_rotation.py — Rotation Matrices

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


def _rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return [[c, -s], [s, c]]


class RotationScene(Scene):
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
        t1 = Text("Rotation Matrices", font_size=50, color=WHITE)
        t2 = Text("Spinning Space Without Distortion", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("How do you rotate a vector by exactly 45 degrees?", font_size=30, color=WHITE)
        q2 = Text("Or spin the entire coordinate system?", font_size=30, color=WHITE)
        q3 = Text("Two numbers encode any rotation: cos and sin.", font_size=30, color=YELL)
        q1.move_to(UP * 1.4); q2.next_to(q1, DOWN, buff=0.45); q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        v = _arr(plane, (0, 0), (2.0, 0.5), BLUE, sw=4)
        self.play(GrowArrow(v), run_time=0.8); self.wait(0.5)

        r1 = Text("A vector at some angle.", font_size=26, color=BLUE)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1)); self.wait(0.8)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3); self.wait(0.2)

        theta = PI / 4
        tip_rot = (np.array(_rot(theta)) @ np.array([2.0, 0.5])).tolist()
        v2 = _arr(plane, (0, 0), tuple(tip_rot), YELL, sw=4)
        r2 = Text("Rotate by 45\u00b0.", font_size=26, color=YELL)
        self._rp(r2, y=1.5)
        b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.4)
        self.play(Transform(v, v2), run_time=3); self.wait(2)

    def s2_geometry(self):
        self._sec("Geometric Intuition")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        r1 = Text("Rotation preserves:\n  - vector length\n  - angles between vectors\n  - the origin",
                  font_size=26, color=WHITE)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=WHITE)
        self.play(FadeIn(b1), Write(r1)); self.wait(2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3); self.wait(0.3)

        # Show multiple rotations
        for angle, col, desc in [(PI / 6, BLUE, "Rotate 30\u00b0"),
                                  (PI / 4, YELL, "Rotate 45\u00b0"),
                                  (PI / 2, GREEN, "Rotate 90\u00b0"),
                                  (PI,     RED,   "Rotate 180\u00b0")]:
            r_desc = Text(desc, font_size=26, color=col)
            self._rp(r_desc, y=2.0)
            br = self._box(r_desc, border=col)
            self.play(FadeIn(br), Write(r_desc)); self.wait(0.3)
            self.play(FadeOut(br), FadeOut(r_desc), run_time=0.2)
            self.play(plane.animate.apply_matrix(_rot(angle)), run_time=2.5)
            self.wait(1)
            # reset
            inv = np.linalg.inv(np.array(_rot(angle)))
            self.play(plane.animate.apply_matrix(inv.tolist()), run_time=1); self.wait(0.3)

        r2 = Text("All rotations keep the\ngrid perfectly undistorted.", font_size=26, color=YELL)
        self._rp(r2, y=2.0)
        b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2)); self.wait(2.5)

    def s3_notation(self):
        self._sec("The Rotation Matrix")

        eq = Text(
            "R(\u03b8) = [ cos\u03b8   \u2212sin\u03b8 ]\n"
            "        [ sin\u03b8    cos\u03b8  ]",
            font_size=38, color=GREEN,
        )
        eq.move_to(UP * 1.8)
        self.play(Write(eq), run_time=2.5); self.wait(1)

        note = Text(
            "Reading the columns:\n\n"
            "Col 1: where [1,0] goes = [cos\u03b8, sin\u03b8]\n"
            "Col 2: where [0,1] goes = [-sin\u03b8, cos\u03b8]",
            font_size=24, color=WHITE,
        )
        note.move_to(DOWN * 0.3)
        nb = self._box(note, border=WHITE, buff=0.32)
        self.play(FadeIn(nb), Write(note), run_time=1.5); self.wait(3)
        self.play(FadeOut(nb), FadeOut(note), FadeOut(eq), run_time=0.5); self.wait(0.4)

        props = Text(
            "Key properties:\n\n"
            "  det(R) = 1  (preserves area)\n"
            "  R\u1d40 = R\u207b\u00b9  (transpose = inverse)\n"
            "  R(\u03b1)R(\u03b2) = R(\u03b1+\u03b2)  (angles add)\n"
            "  R(\u03b8)R(-\u03b8) = I  (rotate then un-rotate)",
            font_size=24, color=YELL,
        )
        props.move_to(ORIGIN)
        pb = self._box(props, border=YELL, buff=0.35)
        self.play(FadeIn(pb), Write(props), run_time=1.5); self.wait(3)

    def s4_example(self):
        self._sec("Worked Example: Rotate 90\u00b0")

        def L(y): return LEFT * 3.0 + UP * y

        mh = Text("R(90\u00b0) = ?", font_size=30, color=WHITE)
        mh.move_to(RIGHT * 3.5 + UP * 2.8)
        self.play(Write(mh)); self.wait(0.4)

        s1 = Text("cos(90\u00b0) = 0", font_size=26, color=WHITE)
        s1.move_to(L(1.5)); self.play(Write(s1)); self.wait(0.4)

        s2 = Text("sin(90\u00b0) = 1", font_size=26, color=WHITE)
        s2.move_to(L(0.6)); self.play(Write(s2)); self.wait(0.4)

        s3 = Text(
            "R(90\u00b0) = [ 0   -1 ]\n"
            "          [ 1    0 ]",
            font_size=30, color=GREEN,
        )
        s3.move_to(L(-0.5))
        s3b = self._box(s3, border=GREEN, buff=0.26)
        self.play(FadeIn(s3b), Write(s3)); self.wait(1)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)

        ei = _arr(plane, (0, 0), (1.5, 0), BLUE, sw=4)
        ej = _arr(plane, (0, 0), (0, 1.5), YELL, sw=4)
        self.play(GrowArrow(ei), GrowArrow(ej)); self.wait(0.5)

        ei_t = _arr(plane, (0, 0), (0, 1.5), BLUE, sw=4)
        ej_t = _arr(plane, (0, 0), (-1.5, 0), YELL, sw=4)

        self.play(Transform(ei, ei_t), Transform(ej, ej_t), run_time=3); self.wait(1)

        check = Text("[1,0] \u2192 [0,1]  \u2713\n[0,1] \u2192 [-1,0] \u2713", font_size=24, color=GREEN)
        self._rp(check, y=-0.5)
        cb = self._box(check, border=GREEN)
        self.play(FadeIn(cb), Write(check)); self.wait(2.5)

    def s5_insight(self):
        self._sec("The Deeper Insight")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.5)

        ins = Text(
            "Rotation matrices are ORTHOGONAL:\n\n"
            "  R\u1d40R = I\n\n"
            "This means:\n"
            "  - Columns are orthonormal\n"
            "  - det(R) = 1\n"
            "  - Inverse = transpose (very fast!)\n\n"
            "Used in: 3D graphics, robotics,\n"
            "computer vision, physics simulations.",
            font_size=23, color=WHITE,
        )
        self._rp(ins, y=0.3)
        ib = self._box(ins, border=BLUE, buff=0.28)
        self.play(FadeIn(ib), Write(ins), run_time=1.5); self.wait(3)

        # Show the rotation composing: rotate by PI/6 seven times = PI/6 * 7 ≈ PI*7/6
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.4); self.wait(0.3)

        r2 = Text("Rotating by \u03b8 seven times\n= rotating by 7\u03b8 once.", font_size=26, color=YELL)
        self._rp(r2, y=1.8)
        b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.5)

        for _ in range(7):
            self.play(plane.animate.apply_matrix(_rot(PI / 6)), run_time=0.8)
            self.wait(0.15)
        self.wait(2)

    def s6_summary(self):
        self._sec("Summary")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)
        self.play(plane.animate.apply_matrix(_rot(PI / 4)), run_time=2.5); self.wait(0.5)

        sm = Text(
            "Rotation Matrices\n\n"
            "R(\u03b8) = [ cos\u03b8  -sin\u03b8 ]\n"
            "        [ sin\u03b8   cos\u03b8 ]\n\n"
            "  Preserves lengths and angles\n"
            "  det(R) = 1\n"
            "  R\u1d40 = R\u207b\u00b9\n"
            "  R(\u03b1+\u03b2) = R(\u03b1)R(\u03b2)",
            font_size=23, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
