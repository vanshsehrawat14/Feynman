"""la_11_determinant.py — Determinants

6-section narrative, ≈ 4 minutes.
Zone discipline: left = visuals, right = text panels.
"""
from manim import *
from la_utils import *
import numpy as np


def _mk_plane():
    return make_plane(x_range=(-4, 4, 1), y_range=(-3, 3, 1)).scale(0.78).shift(LEFT * 2.4)


def _arr(plane, start, end, color=BLUE, sw=3):
    s = plane.c2p(*start)
    e = plane.c2p(*end)
    if np.linalg.norm(e - s) < 0.08:
        return VMobject()
    return Arrow(s, e, buff=0, color=color,
                 stroke_width=sw, max_tip_length_to_length_ratio=0.18)


class DeterminantScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.s1_hook()
        self._fade_all()
        self.s2_geometry()
        self._fade_all()
        self.s3_notation()
        self._fade_all()
        self.s4_example()
        self._fade_all()
        self.s5_insight()
        self._fade_all()
        self.s6_summary()

    def _fade_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)
        self.wait(0.3)

    def _sec(self, title):
        sec_label(self, title)

    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)

    def _rp(self, mob, y=0.0, x=4.1):
        mob.move_to(RIGHT * x + UP * y)
        return mob

    def _sq(self, plane, c0, c1, color=BLUE, opacity=0.25):
        """Filled polygon from four corners in plane coords."""
        p00 = plane.c2p(*c0)
        p10 = plane.c2p(c1[0], c0[1])
        p11 = plane.c2p(*c1)
        p01 = plane.c2p(c0[0], c1[1])
        return Polygon(p00, p10, p11, p01,
                       color=color, fill_color=color,
                       fill_opacity=opacity, stroke_width=2)

    # ── Section 1 — Hook ─────────────────────────────────────────────────
    def s1_hook(self):
        t1 = Text("The Determinant", font_size=50, color=WHITE)
        t2 = Text("How Much Does a Matrix Stretch Space?", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5)
        t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("When a matrix transforms space...", font_size=36, color=WHITE)
        q2 = Text("by how much does it scale area?", font_size=36, color=WHITE)
        q3 = Text("The answer is one number: the determinant.", font_size=30, color=YELL)
        q1.move_to(UP * 1.4)
        q2.next_to(q1, DOWN, buff=0.45)
        q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        # Show a unit square growing
        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)
        sq = self._sq(plane, (0, 0), (1, 1), BLUE, 0.3)
        self.play(Create(sq)); self.wait(0.5)

        intro = Text("This unit square\nhas area = 1.", font_size=26, color=BLUE)
        self._rp(intro, y=1.5)
        bi = self._box(intro, border=BLUE)
        self.play(FadeIn(bi), Write(intro)); self.wait(1)
        self.play(FadeOut(bi), FadeOut(intro), run_time=0.3); self.wait(0.3)

        # Apply matrix with det=3
        M = [[3, 0], [0, 1]]
        self.play(plane.animate.apply_matrix(M), sq.animate.apply_matrix(M), run_time=3)
        self.wait(1)

        r1 = Text("After the matrix,\nthe square has area = 3.\ndet(M) = 3.", font_size=26, color=YELL)
        self._rp(r1, y=1.2)
        b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1)); self.wait(3)

    # ── Section 2 — Geometric Intuition ──────────────────────────────────
    def s2_geometry(self):
        self._sec("Area Scaling")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        sq = self._sq(plane, (0, 0), (1, 1), BLUE, 0.3)
        self.play(Create(sq)); self.wait(0.3)
        lbl_sq = Text("Area = 1", font_size=22, color=BLUE)
        lbl_sq.move_to(plane.c2p(0.5, 0.5))
        b_sq = self._box(lbl_sq, border=BLUE, buff=0.12)
        self.play(FadeIn(b_sq), Write(lbl_sq)); self.wait(0.5)

        r1 = Text("Start with\nthe unit square.", font_size=26, color=BLUE)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1)); self.wait(2)

        # det = 4
        M4 = [[2, 0], [0, 2]]
        self.play(FadeOut(b1), FadeOut(r1), FadeOut(b_sq), FadeOut(lbl_sq), run_time=0.4)
        self.wait(0.3)

        r2 = Text("Apply M with det = 4...", font_size=26, color=WHITE)
        self._rp(r2, y=1.5)
        b2 = self._box(r2, border=WHITE)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.4)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3); self.wait(0.2)
        self.play(plane.animate.apply_matrix(M4), sq.animate.apply_matrix(M4), run_time=3.5)
        self.wait(1)

        lbl_4 = Text("Area = 4", font_size=22, color=YELL)
        lbl_4.move_to(plane.c2p(1.0, 1.0))
        b4 = self._box(lbl_4, border=YELL, buff=0.12)
        self.play(FadeIn(b4), Write(lbl_4))
        r3 = Text("Area grew by factor of 4.\nThat IS the determinant!", font_size=26, color=YELL)
        self._rp(r3, y=1.5)
        b3 = self._box(r3, border=YELL)
        self.play(FadeIn(b3), Write(r3)); self.wait(3)

        # Reset, show det = 0 (collapse)
        inv4 = np.linalg.inv(np.array(M4, dtype=float))
        self.play(
            FadeOut(b3), FadeOut(r3), FadeOut(b4), FadeOut(lbl_4),
            plane.animate.apply_matrix(inv4.tolist()),
            sq.animate.apply_matrix(inv4.tolist()),
            run_time=1.5,
        ); self.wait(0.3)

        M0 = [[1, 0], [0, 0]]   # det = 0: squish to a line
        r4 = Text("What if det = 0?", font_size=28, color=RED)
        self._rp(r4, y=1.5)
        b4r = self._box(r4, border=RED)
        self.play(FadeIn(b4r), Write(r4)); self.wait(0.5)
        self.play(FadeOut(b4r), FadeOut(r4), run_time=0.3); self.wait(0.2)
        self.play(plane.animate.apply_matrix(M0), sq.animate.apply_matrix(M0), run_time=3)
        self.wait(1)

        r5 = Text("Space collapsed to a line!\nAll area = 0.\nThis is det = 0.", font_size=26, color=RED)
        self._rp(r5, y=1.2)
        b5 = self._box(r5, border=RED)
        self.play(FadeIn(b5), Write(r5)); self.wait(3)

    # ── Section 3 — Formal Notation ──────────────────────────────────────
    def s3_notation(self):
        self._sec("The Formula")

        eq = Text("det( [ a  b ] )  =  ad \u2212 bc", font_size=46, color=GREEN)
        eq.move_to(UP * 2.0)
        self.play(Write(eq), run_time=2); self.wait(0.5)

        eq2 = Text("    ( [ c  d ] )", font_size=46, color=GREEN)
        eq2.move_to(UP * 1.0)
        self.play(FadeIn(eq2)); self.wait(1)

        note = Text(
            "ad = product of the diagonal.\nbc = product of the off-diagonal.\n\n"
            "The difference gives\nthe signed area scaling.",
            font_size=26, color=WHITE,
        )
        note.move_to(DOWN * 0.5)
        nb = self._box(note, border=WHITE, buff=0.32)
        self.play(FadeIn(nb), Write(note), run_time=1.5); self.wait(3)
        self.play(FadeOut(nb), FadeOut(note), FadeOut(eq), FadeOut(eq2), run_time=0.5)
        self.wait(0.4)

        sign_note = Text(
            "Sign of the determinant:\n\n"
            "det > 0  \u2192  orientation preserved\n"
            "det < 0  \u2192  orientation FLIPPED\n"
            "det = 0  \u2192  space collapses",
            font_size=26, color=WHITE,
        )
        sign_note.move_to(UP * 0.3)
        snb = self._box(sign_note, border=YELL, buff=0.35)
        self.play(FadeIn(snb), Write(sign_note), run_time=1.5); self.wait(3)

    # ── Section 4 — Worked Example ───────────────────────────────────────
    def s4_example(self):
        self._sec("Worked Example")

        mh = Text("A = [ 3   1 ]\n    [ 0   2 ]", font_size=36, color=BLUE)
        mh.move_to(RIGHT * 3.5 + UP * 2.3)
        mb = self._box(mh, border=BLUE, buff=0.30)
        self.play(FadeIn(mb), Write(mh)); self.wait(0.8)

        def L(y): return LEFT * 3.0 + UP * y

        s1 = Text("det(A) = ad \u2212 bc", font_size=28, color=GREEN)
        s1.move_to(L(1.2)); self.play(Write(s1)); self.wait(0.5)

        s2 = Text("     = (3)(2) \u2212 (1)(0)", font_size=26, color=WHITE)
        s2.move_to(L(0.3)); self.play(Write(s2)); self.wait(0.5)

        s3 = Text("     = 6 \u2212 0", font_size=26, color=WHITE)
        s3.move_to(L(-0.6)); self.play(Write(s3)); self.wait(0.5)

        s4 = Text("det(A) = 6", font_size=32, color=YELL)
        s4.move_to(L(-1.6))
        s4b = self._box(s4, border=YELL, buff=0.24)
        self.play(FadeIn(s4b), Write(s4)); self.wait(1.5)

        # Geometric confirmation
        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)
        sq = self._sq(plane, (0, 0), (1, 1), BLUE, 0.3)
        self.play(Create(sq)); self.wait(0.3)

        M = [[3, 1], [0, 2]]
        self.play(plane.animate.apply_matrix(M), sq.animate.apply_matrix(M), run_time=3.5)
        self.wait(1)

        r_c = Text("Area started at 1.\nAfter A, area = 6.\ndet(A) = 6. \u2713",
                   font_size=24, color=YELL)
        self._rp(r_c, y=-0.5)
        rc = self._box(r_c, border=YELL)
        self.play(FadeIn(rc), Write(r_c)); self.wait(3)

    # ── Section 5 — Deeper Insight ───────────────────────────────────────
    def s5_insight(self):
        self._sec("The Deeper Insight")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.5)

        ins = Text(
            "The determinant is the\nsigned area scale factor.\n\n"
            "For 3D matrices, it's the\nsigned VOLUME scale factor.\n\n"
            "det(AB) = det(A) \u00d7 det(B)\n\n"
            "Composing transforms\nmultiplies their determinants.",
            font_size=23, color=WHITE,
        )
        self._rp(ins, y=0.3)
        ib = self._box(ins, border=BLUE, buff=0.30)
        self.play(FadeIn(ib), Write(ins), run_time=1.5); self.wait(2)

        # Show negative det (orientation flip)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.4); self.wait(0.3)

        sq = self._sq(plane, (0, 0), (1, 1), BLUE, 0.3)
        self.play(Create(sq)); self.wait(0.3)

        r1 = Text("Apply M with det = \u22122\n(negative!)", font_size=26, color=RED)
        self._rp(r1, y=1.8)
        b1 = self._box(r1, border=RED)
        self.play(FadeIn(b1), Write(r1)); self.wait(0.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3); self.wait(0.2)

        M_flip = [[-2, 0], [0, 1]]  # det = -2
        self.play(plane.animate.apply_matrix(M_flip), sq.animate.apply_matrix(M_flip), run_time=3.5)
        self.wait(1)

        r2 = Text("Space flipped AND stretched.\nArea scaled by 2,\nbut orientation reversed.",
                  font_size=24, color=RED)
        self._rp(r2, y=1.2)
        b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2)); self.wait(3)

    # ── Section 6 — Summary ──────────────────────────────────────────────
    def s6_summary(self):
        self._sec("Summary")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)
        sq = self._sq(plane, (0, 0), (1, 1), BLUE, 0.3)
        self.play(Create(sq)); self.wait(0.3)

        M = [[2, 0.5], [0, 1.5]]
        self.play(plane.animate.apply_matrix(M), sq.animate.apply_matrix(M), run_time=3)
        self.wait(0.5)

        sm = Text(
            "The Determinant\n\n"
            "det(A) = ad \u2212 bc\n\n"
            "  > 0  \u2192  area grows, same orientation\n"
            "  < 0  \u2192  area scales, flipped\n"
            "  = 0  \u2192  space collapses\n\n"
            "It measures how much a matrix\n"
            "scales area (or volume).",
            font_size=22, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.32)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
