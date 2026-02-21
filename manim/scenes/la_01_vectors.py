"""
Feynman – Vectors (Gold Standard)
6-section narrative, 3-5 minutes. Text/Cairo only, no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

AX_COLOR = "#888888"

class VectorsScene(Scene):
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
        self.wait(0.3)

    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)

    def _rp(self, mob, y=0.0, x=4.3):
        mob.move_to(RIGHT * x + UP * y); return mob

    def _mk_axes(self, xr=(-0.5, 4.5, 1), yr=(-0.5, 4.5, 1)):
        return Axes(
            x_range=[*xr], y_range=[*yr],
            x_length=7.0, y_length=5.0,
            axis_config={"color": AX_COLOR, "stroke_width": 2,
                         "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 1.5 + DOWN * 0.5)

    def s1_hook(self):
        t1 = Text("Vectors", font_size=52, color=WHITE)
        t2 = Text("Direction and Magnitude", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        q1 = Text("A car drives 3 km east, then 4 km north.", font_size=28, color=WHITE)
        q2 = Text("Where does it end up?", font_size=28, color=YELL)
        q1.move_to(UP * 1.2); q2.next_to(q1, DOWN, buff=0.5)
        self.play(Write(q1), run_time=2.0); self.wait(1.0)
        self.play(Write(q2), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), run_time=0.5)
        ans = Text(
            "A vector captures BOTH direction AND magnitude.\n\n"
            "It is the fundamental language of physics,\n"
            "engineering, and machine learning.", font_size=26, color=WHITE)
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(3.5)

    def s2_geometry(self):
        sec_label(self, "Geometric Intuition")
        axes = self._mk_axes()
        self.play(Create(axes), run_time=2.0); self.wait(0.5)
        e1 = Arrow(axes.c2p(0,0), axes.c2p(1,0), color=RED, stroke_width=4, buff=0)
        e2 = Arrow(axes.c2p(0,0), axes.c2p(0,1), color=GREEN, stroke_width=4, buff=0)
        e1l = Text("e1=(1,0)", font_size=20, color=RED).next_to(axes.c2p(1,0), UP, buff=0.1)
        e2l = Text("e2=(0,1)", font_size=20, color=GREEN).next_to(axes.c2p(0,1), RIGHT, buff=0.1)
        self.play(Create(e1), Create(e2), run_time=2.0); self.wait(0.5)
        self.play(Write(e1l), Write(e2l), run_time=1.5); self.wait(1.5)
        v = Arrow(axes.c2p(0,0), axes.c2p(3,2), color=BLUE, stroke_width=5, buff=0)
        vl = Text("v = (3,2)", font_size=22, color=BLUE).next_to(axes.c2p(1.5,1), UP, buff=0.15)
        self.play(Create(v), run_time=2.5); self.wait(0.5)
        self.play(Write(vl), run_time=1.5); self.wait(1.5)
        cx = DashedLine(axes.c2p(0,0), axes.c2p(3,0), color=YELL)
        cy = DashedLine(axes.c2p(3,0), axes.c2p(3,2), color=YELL)
        self.play(Create(cx), Create(cy), run_time=2.0); self.wait(1.0)
        r1 = Text("x-component: 3\ny-component: 2", font_size=22, color=YELL)
        self._rp(r1, y=2.0); b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        v2 = Arrow(axes.c2p(1,0.5), axes.c2p(4,2.5), color=BLUE, stroke_width=3, stroke_opacity=0.5, buff=0)
        v3 = Arrow(axes.c2p(0.5,1.5), axes.c2p(3.5,3.5), color=BLUE, stroke_width=3, stroke_opacity=0.4, buff=0)
        r2 = Text("Vectors are FREE --\nposition does not matter,\nonly direction + length.", font_size=22, color=WHITE)
        self._rp(r2, y=2.0); b2 = self._box(r2)
        self.play(Create(v2), Create(v3), run_time=2.0)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)

    def s3_notation(self):
        sec_label(self, "Formal Notation")
        items = [
            ("v = (vx, vy)   or   v = vx*e1 + vy*e2", YELL),
            ("|v| = sqrt(vx^2 + vy^2)   (magnitude)", GREEN),
            ("angle = arctan(vy / vx)   (direction)", BLUE),
            ("In 3D:  v = (vx, vy, vz)", WHITE),
        ]
        y = 2.5; boxes = []
        for txt, col in items:
            mob = Text(txt, font_size=26, color=col).move_to(UP * y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.5)
            boxes.append((b, mob)); y -= 1.1
        self.wait(1.0)
        self.play(*[FadeOut(b) for b,_ in boxes], *[FadeOut(m) for _,m in boxes], run_time=0.5)
        ops = Text(
            "Vector operations:\n\n"
            "  Addition:      v + w = (vx+wx, vy+wy)\n"
            "  Scalar mult:   c*v = (c*vx, c*vy)\n"
            "  Subtraction:   v - w = v + (-w)\n"
            "  Dot product:   v . w = vx*wx + vy*wy\n"
            "  Magnitude:     |v| = sqrt(v . v)",
            font_size=24, color=WHITE)
        ops.move_to(ORIGIN)
        ob = self._box(ops, border=BLUE, buff=0.38)
        self.play(FadeIn(ob), Write(ops), run_time=2.5); self.wait(3.5)

    def s4_example(self):
        sec_label(self, "Worked Example: v = (3, 2)")
        axes = self._mk_axes()
        self.play(Create(axes), run_time=2.0); self.wait(0.5)
        v = Arrow(axes.c2p(0,0), axes.c2p(3,2), color=BLUE, stroke_width=5, buff=0)
        self.play(Create(v), run_time=2.5); self.wait(0.5)
        steps = [
            ("|v| = sqrt(3^2 + 2^2)", YELL, 2.5),
            ("    = sqrt(9 + 4) = sqrt(13)", WHITE, 1.7),
            ("    ~ 3.606 units long", GREEN, 0.9),
            ("angle = arctan(2/3)", BLUE, 0.1),
            ("      ~ 33.7 degrees", GREEN, -0.7),
            ("Unit vector: v/|v| = (0.832, 0.555)", WHITE, -1.5),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col)
            self._rp(mob, y=yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.2)
        self.wait(2.0)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Vectors appear everywhere:\n\n"
            "  Physics: velocity, force, acceleration, momentum\n"
            "  Computer graphics: surface normals, ray directions\n"
            "  Machine learning: word embeddings (50000-D vectors)\n"
            "  GPS: displacement vectors on Earth's surface\n"
            "  Economics: price baskets (multi-dimensional)\n\n"
            "  In ML, a document is a vector in vocabulary space.\n"
            "  Cosine similarity = angle between two vectors.\n"
            "  king - man + woman ~ queen  (vector arithmetic!)",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        dot2 = Text(
            "Key insight:\n\n"
            "  A vector is a geometric OBJECT.\n"
            "  Its components depend on your coordinate system\n"
            "  (your choice of basis vectors).\n\n"
            "  Change your basis, change its components --\n"
            "  but the vector itself does not change.\n\n"
            "  This is why change of basis matters in linear algebra.",
            font_size=22, color=WHITE)
        dot2.move_to(ORIGIN)
        db = self._box(dot2, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(dot2), run_time=2.5); self.wait(4.0)

    def s6_summary(self):
        sec_label(self, "Summary")
        axes = self._mk_axes()
        v = Arrow(axes.c2p(0,0), axes.c2p(3,2), color=BLUE, stroke_width=5, buff=0)
        e1 = Arrow(axes.c2p(0,0), axes.c2p(1,0), color=RED, stroke_width=3, buff=0)
        e2 = Arrow(axes.c2p(0,0), axes.c2p(0,1), color=GREEN, stroke_width=3, buff=0)
        self.play(Create(axes), run_time=1.5)
        self.play(Create(e1), Create(e2), Create(v), run_time=2.5); self.wait(0.5)
        sm = Text(
            "Vectors\n\n"
            "  v = (vx, vy) -- direction + magnitude\n"
            "  |v| = sqrt(vx^2 + vy^2)\n\n"
            "  Standard basis: e1=(1,0), e2=(0,1)\n"
            "  Any vector: v = vx*e1 + vy*e2\n\n"
            "  Translation invariant (free vector)\n"
            "  Foundation of linear algebra",
            font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
