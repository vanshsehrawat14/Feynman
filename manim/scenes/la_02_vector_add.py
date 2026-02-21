"""Feynman – Vector Addition (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class VectorAdditionScene(Scene):
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
    def _axes(self, xr=(-0.3,4.5,1), yr=(-0.3,4.5,1)):
        return Axes(x_range=[*xr], y_range=[*yr], x_length=7.2, y_length=5.0,
            axis_config={"color": AX_COLOR,"stroke_width":2,"include_tip":True,"include_ticks":True}
        ).shift(LEFT*1.5+DOWN*0.5)

    def s1_hook(self):
        t = Text("Vector Addition", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Walking in two directions", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("You walk 3 km east, then 4 km north.\nWhere are you?", font_size=28, color=WHITE).move_to(UP*1.0)
        ans = Text("(3, 0) + (0, 4) = (3, 4)\nDistance from start: 5 km (Pythagoras!)", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Vector addition is the tip-to-tail operation:\nplace the second vector at the tip of the first.\n\nComponent-wise: (a+c, b+d)\nThe foundation of linear combinations.", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Tip-to-Tail Visualized")
        ax = self._axes(xr=(-0.3,5,1), yr=(-0.3,5,1))
        self.play(Create(ax), run_time=2.0); self.wait(0.5)
        v = Arrow(ax.c2p(0,0), ax.c2p(3,1), color=BLUE, stroke_width=5, buff=0)
        w = Arrow(ax.c2p(3,1), ax.c2p(4,3), color=RED, stroke_width=5, buff=0)
        s = Arrow(ax.c2p(0,0), ax.c2p(4,3), color=GREEN, stroke_width=4, buff=0)
        vl = Text("v=(3,1)", font_size=20, color=BLUE).next_to(ax.c2p(1.5,0.5), DOWN, buff=0.1)
        wl = Text("w=(1,2)", font_size=20, color=RED).next_to(ax.c2p(3.5,2), RIGHT, buff=0.1)
        sl = Text("v+w=(4,3)", font_size=20, color=GREEN).next_to(ax.c2p(2,1.5), LEFT, buff=0.1)
        self.play(Create(v), Write(vl), run_time=2.0); self.wait(0.8)
        self.play(Create(w), Write(wl), run_time=2.0); self.wait(0.8)
        self.play(Create(s), Write(sl), run_time=2.0); self.wait(2.0)
        r1 = Text("Tip-to-tail rule:\nPlace w at tip of v,\nthen draw resultant", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Also: parallelogram rule\n(both orders give same result)", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Formal Notation")
        items = [
            ("v + w = (vx+wx, vy+wy)", YELL),
            ("Component-wise addition", GREEN),
            ("Commutative: v+w = w+v", BLUE),
            ("Associative: (u+v)+w = u+(v+w)", WHITE),
            ("Identity: v + 0 = v", GREEN),
            ("Inverse: v + (-v) = 0", RED),
        ]
        y = 2.8; boxes = []
        for txt, col in items:
            mob = Text(txt, font_size=28, color=col).move_to(UP*y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.2)
            boxes.append((b,mob)); y -= 0.95
        self.wait(1.0)
        self.play(*[FadeOut(b) for b,_ in boxes], *[FadeOut(m) for _,m in boxes], run_time=0.5)
        lc = Text("Linear combinations:\n\n  c1*v + c2*w + ... cn*vn\n\n  Every point in the plane reachable\n  from two linearly independent vectors.\n\n  This is the SPAN concept.", font_size=24, color=WHITE).move_to(ORIGIN)
        lb = self._box(lc, border=BLUE, buff=0.38)
        self.play(FadeIn(lb), Write(lc), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: v=(2,3), w=(-1,2)")
        steps = [
            ("v = (2, 3)", BLUE, 2.5),
            ("w = (-1, 2)", RED, 1.7),
            ("v + w = (2+(-1), 3+2) = (1, 5)", GREEN, 0.9),
            ("v - w = (2-(-1), 3-2) = (3, 1)", YELL, 0.1),
            ("2v + w = (4+(-1), 6+2) = (3, 8)", WHITE, -0.7),
            ("3v - 2w = (6+2, 9-4) = (8, 5)", BLUE, -1.5),
            ("Linear combination of any scalars!", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=26, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Vector spaces are defined by 8 axioms\n(including vector addition laws).\n\nAny structure satisfying these axioms\nbehaves like vectors:\n\n  Polynomials: p(x) + q(x)\n  Matrices: A + B\n  Functions: f(x) + g(x)\n  Signals: audio1 + audio2 (superposition)\n\nAll share identical mathematical structure!", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        ml = Text("Machine learning connections:\n\n  Word embeddings: king - man + woman = queen\n  This is VECTOR ARITHMETIC!\n\n  Gradient descent: w := w - lr * grad\n  Weight update = vector subtraction\n\n  Every neural layer: output = Wx + b\n  Matrix times vector plus bias vector.", font_size=22, color=YELL).move_to(ORIGIN)
        mb = self._box(ml, border=YELL, buff=0.38)
        self.play(FadeIn(mb), Write(ml), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes(xr=(-0.3,5,1), yr=(-0.3,5,1))
        v = Arrow(ax.c2p(0,0), ax.c2p(3,1), color=BLUE, stroke_width=4, buff=0)
        w = Arrow(ax.c2p(3,1), ax.c2p(4,3), color=RED, stroke_width=4, buff=0)
        s = Arrow(ax.c2p(0,0), ax.c2p(4,3), color=GREEN, stroke_width=4, buff=0)
        self.play(Create(ax), Create(v), Create(w), Create(s), run_time=2.5); self.wait(0.5)
        sm = Text("Vector Addition\n\n  v + w = (vx+wx, vy+wy)\n\n  Tip-to-tail rule (geometric)\n  Component-wise (algebraic)\n\n  Commutative and associative\n  Basis for linear combinations\n  Fundamental to vector spaces", font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
