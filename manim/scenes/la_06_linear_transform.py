"""la_06_linear_transform.py — Linear Transformations

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


class LinearTransformScene(Scene):
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
        t1 = Text("Linear Transformations", font_size=46, color=WHITE)
        t2 = Text("The Mathematics of Warping Space", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("What makes a transformation 'linear'?", font_size=36, color=WHITE)
        q2 = Text("Lines must stay lines.", font_size=36, color=WHITE)
        q3 = Text("And the origin must stay fixed.", font_size=36, color=YELL)
        q1.move_to(UP * 1.4); q2.next_to(q1, DOWN, buff=0.45); q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        intro = Text("Watch the grid lines\nas we transform space...", font_size=26, color=WHITE)
        self._rp(intro, y=1.0)
        bi = self._box(intro, border=WHITE)
        self.play(FadeIn(bi), Write(intro)); self.wait(0.8)
        self.play(FadeOut(bi), FadeOut(intro), run_time=0.3); self.wait(0.2)

        self.play(plane.animate.apply_matrix([[1.5, 0.5], [0.2, 1.2]]), run_time=3)
        self.wait(1)
        r1 = Text("Grid lines stayed straight.\nOrigin stayed fixed.\nThat is linear!", font_size=26, color=YELL)
        self._rp(r1, y=1.0)
        b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1)); self.wait(2.5)

    def s2_geometry(self):
        self._sec("The Two Rules of Linearity")

        rule1 = Text(
            "Rule 1 — Additivity:\n\n"
            "T(u + v) = T(u) + T(v)\n\n"
            "Transform the sum =\nsum of the transforms.",
            font_size=26, color=BLUE,
        )
        rule1.move_to(LEFT * 2.8 + UP * 0.5)
        b1 = self._box(rule1, border=BLUE, buff=0.30)
        self.play(FadeIn(b1), Write(rule1), run_time=1.5); self.wait(2)

        rule2 = Text(
            "Rule 2 — Scaling:\n\n"
            "T(cv) = c x T(v)\n\n"
            "Scale first then transform\n= transform then scale.",
            font_size=26, color=YELL,
        )
        rule2.move_to(RIGHT * 2.8 + UP * 0.5)
        b2 = self._box(rule2, border=YELL, buff=0.30)
        self.play(FadeIn(b2), Write(rule2), run_time=1.5); self.wait(3)
        self.play(FadeOut(b1), FadeOut(rule1), FadeOut(b2), FadeOut(rule2), run_time=0.5)
        self.wait(0.3)

        # Visual demo of additivity
        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.4)

        u_tip = (1.0, 0.5)
        v_tip = (0.5, 1.0)
        uv_tip = (1.5, 1.5)

        u_arr  = _arr(plane, (0,0), u_tip,  BLUE, sw=3)
        v_arr  = _arr(plane, (0,0), v_tip,  YELL, sw=3)
        uv_arr = _arr(plane, (0,0), uv_tip, GREEN, sw=3)

        r_add = Text("u + v = green arrow", font_size=24, color=GREEN)
        self._rp(r_add, y=2.0)
        b_add = self._box(r_add, border=GREEN)
        self.play(GrowArrow(u_arr), GrowArrow(v_arr)); self.wait(0.5)
        self.play(GrowArrow(uv_arr), FadeIn(b_add), Write(r_add)); self.wait(1)

        M = [[2, 0.5], [0, 1.5]]
        u_t  = tuple((np.array(M) @ np.array(u_tip)).tolist())
        v_t  = tuple((np.array(M) @ np.array(v_tip)).tolist())
        uv_t = tuple((np.array(M) @ np.array(uv_tip)).tolist())
        u_arr2  = _arr(plane, (0,0), u_t,  BLUE, sw=3)
        v_arr2  = _arr(plane, (0,0), v_t,  YELL, sw=3)
        uv_arr2 = _arr(plane, (0,0), uv_t, GREEN, sw=3)

        self.play(FadeOut(b_add), FadeOut(r_add), run_time=0.3); self.wait(0.2)
        self.play(
            Transform(u_arr, u_arr2),
            Transform(v_arr, v_arr2),
            Transform(uv_arr, uv_arr2),
            run_time=3,
        ); self.wait(1)

        r_conf = Text("T(u+v) = T(u)+T(v)  confirmed!", font_size=26, color=GREEN)
        self._rp(r_conf, y=2.0)
        bc = self._box(r_conf, border=GREEN)
        self.play(FadeIn(bc), Write(r_conf)); self.wait(2.5)

    def s3_notation(self):
        self._sec("Matrix Representation")

        eq = Text("T(x) = A x", font_size=60, color=GREEN)
        eq.move_to(UP * 2.0)
        self.play(Write(eq), run_time=2); self.wait(0.5)

        note = Text(
            "Every linear transformation\ncan be written as matrix multiplication.\n\n"
            "The matrix A captures everything\nabout the transformation.",
            font_size=26, color=WHITE,
        )
        note.move_to(UP * 0.2)
        nb = self._box(note, border=WHITE, buff=0.32)
        self.play(FadeIn(nb), Write(note), run_time=1.5); self.wait(3)
        self.play(FadeOut(nb), FadeOut(note), FadeOut(eq), run_time=0.5); self.wait(0.4)

        find_eq = Text(
            "How to find matrix A:\n\n"
            "Column 1 = T([1, 0])\n"
            "Column 2 = T([0, 1])\n\n"
            "Transform the basis vectors.\nThat is your matrix.",
            font_size=26, color=YELL,
        )
        find_eq.move_to(ORIGIN)
        fb = self._box(find_eq, border=YELL, buff=0.35)
        self.play(FadeIn(fb), Write(find_eq), run_time=1.5); self.wait(3)

    def s4_example(self):
        self._sec("Worked Example: 45 Degree Rotation")

        mh = Text("Rotation by 45 degrees", font_size=30, color=WHITE)
        mh.move_to(RIGHT * 3.5 + UP * 2.8)
        self.play(Write(mh)); self.wait(0.4)

        def L(y): return LEFT * 3.0 + UP * y

        cos45 = np.cos(np.pi / 4)
        sin45 = np.sin(np.pi / 4)

        s1 = Text("[1,0]  rotates to  [0.71, 0.71]", font_size=22, color=BLUE)
        s1.move_to(L(1.8)); self.play(Write(s1)); self.wait(0.5)

        s2 = Text("[0,1]  rotates to  [-0.71, 0.71]", font_size=22, color=YELL)
        s2.move_to(L(0.9)); self.play(Write(s2)); self.wait(0.5)

        s3 = Text(
            "Matrix A =\n[ 0.71  -0.71 ]\n[ 0.71   0.71 ]",
            font_size=26, color=GREEN,
        )
        s3.move_to(L(-0.3))
        s3b = self._box(s3, border=GREEN, buff=0.26)
        self.play(FadeIn(s3b), Write(s3)); self.wait(1)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)

        ei = _arr(plane, (0,0), (1.5, 0), BLUE, sw=4)
        ej = _arr(plane, (0,0), (0, 1.5), YELL, sw=4)
        self.play(GrowArrow(ei), GrowArrow(ej)); self.wait(0.5)

        R45 = [[cos45, -sin45], [sin45, cos45]]
        ei_t = _arr(plane, (0,0), tuple((np.array(R45) @ np.array([1.5, 0])).tolist()), BLUE, sw=4)
        ej_t = _arr(plane, (0,0), tuple((np.array(R45) @ np.array([0, 1.5])).tolist()), YELL, sw=4)
        self.play(Transform(ei, ei_t), Transform(ej, ej_t), run_time=3.5); self.wait(2.5)

    def s5_insight(self):
        self._sec("The Deeper Insight")

        ins = Text(
            "Linear transforms are powerful because:\n\n"
            "1. Fully described by 4 numbers (2D)\n\n"
            "2. Composition = matrix multiply\n\n"
            "3. Invertible iff det is not zero\n\n"
            "4. Foundation of all of linear algebra,\n"
            "   machine learning, graphics, physics.",
            font_size=24, color=WHITE,
        )
        ins.move_to(LEFT * 1.5)
        ib = self._box(ins, border=BLUE, buff=0.35)
        self.play(FadeIn(ib), Write(ins), run_time=2); self.wait(3)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5); self.wait(0.3)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.5)

        r1 = Text("Non-linear:\ncurved paths...", font_size=24, color=RED)
        self._rp(r1, y=2.0)
        b1 = self._box(r1, border=RED)
        self.play(FadeIn(b1), Write(r1)); self.wait(0.5)

        arrows_nl = [_arr(plane, (0,0), (x, 0.5 * x * x), RED, sw=2)
                     for x in [-1.5, -1.0, -0.5, 0.5, 1.0, 1.5]]
        arrows_nl = [a for a in arrows_nl if isinstance(a, Arrow)]
        self.play(*[GrowArrow(a) for a in arrows_nl], run_time=1.5); self.wait(0.5)

        r2 = Text("Lines curved - NOT linear.", font_size=24, color=RED)
        r2.next_to(b1, DOWN, buff=0.4)
        b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2)); self.wait(3)

    def s6_summary(self):
        self._sec("Summary")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)
        self.play(plane.animate.apply_matrix([[1.5, 0.3], [0.1, 1.2]]), run_time=3)
        self.wait(0.5)

        sm = Text(
            "Linear Transformations\n\n"
            "  T(u+v) = T(u) + T(v)\n"
            "  T(cv) = c T(v)\n\n"
            "  T(x) = Ax  for some matrix A\n\n"
            "  Lines stay lines.\n"
            "  Origin stays fixed.",
            font_size=24, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
