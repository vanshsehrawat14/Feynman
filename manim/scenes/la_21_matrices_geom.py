"""la_21_matrices_geom.py — What Matrices Actually Do to Space

6-section narrative, ≈ 4 minutes.
Zone discipline: left = visuals, right = text panels.
"""
from manim import *
from la_utils import *
import numpy as np


def _mk_plane():
    return make_plane().scale(0.72).shift(LEFT * 2.6)


def _arr(plane, start, end, color=BLUE, sw=3, tr=0.18):
    s = plane.c2p(*start)
    e = plane.c2p(*end)
    if np.linalg.norm(e - s) < 0.08:
        return VMobject()
    return Arrow(s, e, buff=0, color=color,
                 stroke_width=sw, max_tip_length_to_length_ratio=tr)


class MatricesGeomScene(Scene):
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

    # ── Section 1 — Hook ─────────────────────────────────────────────────
    def s1_hook(self):
        t1 = Text("What Do Matrices Actually Do?", font_size=44, color=WHITE)
        t2 = Text("A Visual Tour of Space Transformations", font_size=24, color=BLUE)
        t1.move_to(UP * 0.5)
        t2.next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("You've seen matrices as grids of numbers.", font_size=34, color=WHITE)
        q2 = Text("But each matrix is secretly a recipe", font_size=34, color=WHITE)
        q3 = Text("for warping, rotating, or squishing space.", font_size=34, color=YELL)
        q1.move_to(UP * 1.4)
        q2.next_to(q1, DOWN, buff=0.45)
        q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        # Show a plane and apply a simple scale transform
        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        intro = Text("Watch what happens\nwhen we apply a matrix\nto the entire plane...",
                     font_size=26, color=WHITE)
        self._rp(intro, y=1.0)
        bi = self._box(intro, border=WHITE)
        self.play(FadeIn(bi), Write(intro)); self.wait(1)
        self.play(FadeOut(bi), FadeOut(intro), run_time=0.3); self.wait(0.2)

        # Apply scale 2x — visual and dramatic
        self.play(plane.animate.apply_matrix([[2, 0], [0, 2]]), run_time=3)
        self.wait(1)

        r1 = Text("Every point moved.\nThe whole plane stretched.", font_size=26, color=YELL)
        self._rp(r1, y=1.0)
        b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1)); self.wait(2.5)

    # ── Section 2 — Geometric Intuition ──────────────────────────────────
    def s2_geometry(self):
        self._sec("The Four Primitive Transforms")

        transforms = [
            ([[2, 0], [0, 2]],    BLUE,  "Scale (x2)",
             "Every vector stretched\nto twice its length."),
            ([[0, -1], [1, 0]],   YELL,  "Rotate 90\u00b0",
             "Every vector rotated\n90\u00b0 counterclockwise."),
            ([[1, 0.8], [0, 1]],  RED,   "Horizontal Shear",
             "Vertical lines tilt.\nHorizontal lines stay."),
            ([[-1, 0], [0, 1]],   GREEN, "Reflect over Y-axis",
             "Left becomes right.\nRight becomes left."),
        ]

        for M_list, col, label_str, desc_str in transforms:
            plane = _mk_plane()
            self.play(Create(plane), run_time=1); self.wait(0.3)

            lab = Text(label_str, font_size=30, color=col)
            self._rp(lab, y=2.2)
            bl = self._box(lab, border=col)
            self.play(FadeIn(bl), Write(lab)); self.wait(0.5)

            self.play(FadeOut(bl), FadeOut(lab), run_time=0.3); self.wait(0.2)
            self.play(plane.animate.apply_matrix(M_list), run_time=3.5)
            self.wait(1)

            desc = Text(desc_str, font_size=26, color=col)
            self._rp(desc, y=1.2)
            bd = self._box(desc, border=col)
            self.play(FadeIn(bd), Write(desc)); self.wait(2.5)

            # Reset plane
            inv = np.linalg.inv(np.array(M_list, dtype=float))
            self.play(
                FadeOut(bd), FadeOut(desc),
                plane.animate.apply_matrix(inv.tolist()),
                run_time=1.5
            )
            self.play(FadeOut(plane), run_time=0.4); self.wait(0.3)

    # ── Section 3 — Formal Notation ──────────────────────────────────────
    def s3_notation(self):
        self._sec("Reading a Matrix Geometrically")

        eq = Text("A =  [ a   b ]\n      [ c   d ]", font_size=48, color=GREEN)
        eq.move_to(UP * 1.8)
        self.play(Write(eq), run_time=2); self.wait(0.5)

        note = Text(
            "The columns of A tell you\nwhere the basis vectors land.\n\n"
            "Column 1 = where [1, 0] goes\n"
            "Column 2 = where [0, 1] goes",
            font_size=26, color=WHITE,
        )
        note.move_to(DOWN * 0.5)
        nb = self._box(note, border=WHITE, buff=0.32)
        self.play(FadeIn(nb), Write(note), run_time=1.5); self.wait(3)
        self.play(FadeOut(nb), FadeOut(note), FadeOut(eq), run_time=0.5); self.wait(0.4)

        # Show basis vector interpretation on plane
        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.4)

        ei = _arr(plane, (0, 0), (1, 0), BLUE, sw=4)
        ej = _arr(plane, (0, 0), (0, 1), YELL, sw=4)
        self.play(GrowArrow(ei), GrowArrow(ej)); self.wait(0.5)

        r1 = Text("[1, 0] = first basis vector\n[0, 1] = second basis vector",
                  font_size=24, color=WHITE)
        self._rp(r1, y=1.2)
        b1 = self._box(r1, border=WHITE)
        self.play(FadeIn(b1), Write(r1)); self.wait(1)

        # Apply shear: [[1, 0.8], [0, 1]]
        M = [[1, 0.8], [0, 1]]
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3); self.wait(0.2)

        r2 = Text("Apply M = [ 1  0.8 ]\n          [ 0   1  ]", font_size=24, color=GREEN)
        self._rp(r2, y=1.5)
        b2 = self._box(r2, border=GREEN)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.5)

        self.play(plane.animate.apply_matrix(M), run_time=3)
        self.wait(1.5)

        r3 = Text("Column 1 → [1, 0] stayed.\nColumn 2 → [0.8, 1] is new [0,1].",
                  font_size=23, color=YELL)
        r3.next_to(b2, DOWN, buff=0.4)
        b3 = self._box(r3, border=YELL)
        self.play(FadeIn(b3), Write(r3)); self.wait(2.5)

    # ── Section 4 — Worked Example ───────────────────────────────────────
    def s4_example(self):
        self._sec("A Full Worked Example")

        mh = Text("Matrix A = [ 2   1 ]\n           [ 0   2 ]", font_size=32, color=BLUE)
        mh.move_to(RIGHT * 3.5 + UP * 2.3)
        mb = self._box(mh, border=BLUE, buff=0.30)
        self.play(FadeIn(mb), Write(mh)); self.wait(0.8)

        def L(y): return LEFT * 3.0 + UP * y

        s1 = Text("Column 1 = [2, 0]", font_size=26, color=WHITE)
        s1.move_to(L(1.2)); self.play(FadeIn(s1)); self.wait(0.5)

        s2 = Text("[1, 0]  \u2192  [2, 0]", font_size=24, color=BLUE)
        s2.move_to(L(0.4)); self.play(Write(s2)); self.wait(0.5)

        s3 = Text("Column 2 = [1, 2]", font_size=26, color=WHITE)
        s3.move_to(L(-0.5)); self.play(FadeIn(s3)); self.wait(0.5)

        s4 = Text("[0, 1]  \u2192  [1, 2]", font_size=24, color=YELL)
        s4.move_to(L(-1.3)); self.play(Write(s4)); self.wait(0.5)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)

        ei = _arr(plane, (0, 0), (1, 0), BLUE, sw=4)
        ej = _arr(plane, (0, 0), (0, 1), YELL, sw=4)
        self.play(GrowArrow(ei), GrowArrow(ej)); self.wait(0.5)

        self.play(FadeOut(s1), FadeOut(s2), FadeOut(s3), FadeOut(s4), run_time=0.4)
        self.wait(0.3)

        M = [[2, 1], [0, 2]]
        self.play(plane.animate.apply_matrix(M), run_time=4)
        self.wait(1.5)

        r_conf = Text("[1,0] landed at [2, 0]\n[0,1] landed at [1, 2]",
                      font_size=24, color=YELL)
        self._rp(r_conf, y=0.0)
        rc = self._box(r_conf, border=YELL)
        self.play(FadeIn(rc), Write(r_conf)); self.wait(2.5)

    # ── Section 5 — Deeper Insight ───────────────────────────────────────
    def s5_insight(self):
        self._sec("The Deeper Insight")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.5)

        ins1 = Text(
            "Matrix multiplication\n= transformation composition.\n\n"
            "AB means: apply B first,\nthen apply A.",
            font_size=26, color=WHITE,
        )
        self._rp(ins1, y=1.2)
        b1 = self._box(ins1, border=WHITE)
        self.play(FadeIn(b1), Write(ins1)); self.wait(0.5)

        # Apply rotate then scale
        R = [[0, -1], [1, 0]]    # 90° rotation
        S = [[2,  0], [0, 2]]    # scale 2x
        self.play(FadeOut(b1), FadeOut(ins1), run_time=0.3); self.wait(0.2)

        r2 = Text("Apply rotation first...", font_size=26, color=YELL)
        self._rp(r2, y=2.0)
        b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.4)
        self.play(plane.animate.apply_matrix(R), run_time=3); self.wait(1)

        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3); self.wait(0.2)
        r3 = Text("...then scale by 2.", font_size=26, color=BLUE)
        self._rp(r3, y=2.0)
        b3 = self._box(r3, border=BLUE)
        self.play(FadeIn(b3), Write(r3)); self.wait(0.4)
        self.play(plane.animate.apply_matrix(S), run_time=3); self.wait(1.5)

        self.play(FadeOut(b3), FadeOut(r3), run_time=0.3); self.wait(0.2)

        SR = np.array(S) @ np.array(R)
        r4 = Text(
            "S \u00d7 R = single combined matrix.\n\n"
            "One matrix = one transformation.\n"
            "No matter how complex.",
            font_size=24, color=YELL,
        )
        self._rp(r4, y=0.5)
        b4 = self._box(r4, border=YELL)
        self.play(FadeIn(b4), Write(r4)); self.wait(3)

    # ── Section 6 — Summary ──────────────────────────────────────────────
    def s6_summary(self):
        self._sec("Summary")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)
        self.play(plane.animate.apply_matrix([[1.5, 0.5], [0, 1.5]]), run_time=3)
        self.wait(0.5)

        sm = Text(
            "What Matrices Do to Space\n\n"
            "  Scale  \u2014 stretch or shrink\n"
            "  Rotate \u2014 spin around origin\n"
            "  Shear  \u2014 tilt one axis\n"
            "  Reflect \u2014 flip over a line\n\n"
            "Columns tell you where\n"
            "the basis vectors land.",
            font_size=23, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.32)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
