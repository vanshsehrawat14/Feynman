"""
Generator 2 — writes remaining 18 gold-standard scenes (3+ min target).
Run: python _gen_scenes2.py
"""
import os
BASE = os.path.dirname(os.path.abspath(__file__))

HEADER = '''"""Feynman – {title} (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"
'''

def TPLATE(cls):
    return f'''
class {cls}(Scene):
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
            axis_config={{"color": AX_COLOR,"stroke_width":2,"include_tip":True,"include_ticks":True}}
        ).shift(LEFT*1.5+DOWN*0.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
LIMIT = HEADER.format(title="Limits") + TPLATE("LimitScene") + '''
    def s1_hook(self):
        t = Text("The Limit", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("Getting infinitely close", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("What is sin(x)/x as x approaches 0?", font_size=28, color=WHITE).move_to(UP*1.0)
        q2 = Text("x=0 gives 0/0.  Undefined!", font_size=28, color=RED).next_to(q, DOWN, buff=0.5)
        q3 = Text("But the LIMIT exists and equals 1.", font_size=28, color=GREEN).next_to(q2, DOWN, buff=0.5)
        self.play(Write(q), run_time=2.0); self.wait(0.8)
        self.play(Write(q2), run_time=1.5); self.wait(0.8)
        self.play(Write(q3), run_time=1.5); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(q2), FadeOut(q3), run_time=0.5)
        ans = Text("A limit describes where a function is HEADING,\\nnot where it is.\\n\\nThis distinction unlocks all of calculus.", font_size=27, color=WHITE).move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Approaching a Point")
        ax = self._axes(xr=(-0.3,5,1), yr=(-0.3,2.5,0.5))
        f = lambda x: np.sin(x)/x if abs(x) > 0.001 else 1.0
        left  = ax.plot(f, x_range=[0.05, 4.8], color=BLUE, stroke_width=3.5)
        self.play(Create(ax), run_time=2.0); self.wait(0.3)
        self.play(Create(left), run_time=2.0); self.wait(0.5)
        r1 = Text("f(x) = sin(x)/x", font_size=24, color=BLUE)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(1.0)
        dot_hole = Circle(radius=0.1, color=RED, fill_color=BG, fill_opacity=1, stroke_width=2)
        dot_hole.move_to(ax.c2p(0, 1))
        self.play(Create(dot_hole), run_time=1.0); self.wait(0.5)
        r2 = Text("Hole at x=0\\n(0/0 undefined)", font_size=22, color=RED)
        self._rp(r2, y=1.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=1.5); self.wait(1.5)
        x_t = ValueTracker(3.0)
        dot_r = always_redraw(lambda: Dot(ax.c2p(x_t.get_value(), f(x_t.get_value())), color=YELL, radius=0.12))
        self.play(Create(dot_r)); self.wait(0.3)
        self.play(x_t.animate.set_value(0.15), run_time=3.0, rate_func=smooth); self.wait(0.5)
        r3 = Text("As x -> 0, f(x) -> 1", font_size=22, color=GREEN)
        self._rp(r3, y=0.8); b3 = self._box(r3, border=GREEN)
        self.play(FadeIn(b3), Write(r3), run_time=1.5); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Limit Notation")
        eq = Text("lim  f(x) = L", font_size=38, color=YELL).move_to(UP*2.8)
        eq2 = Text("x -> c", font_size=28, color=YELL).next_to(eq, DOWN, buff=0.1)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(0.5)
        self.play(Write(eq2), run_time=1.0); self.wait(1.0)
        items = [
            ("c       the point being approached (may not exist in domain)", BLUE),
            ("L       the limit value (the destination)", GREEN),
            ("lim     the limiting process (not evaluation!)", WHITE),
            ("f(c)    may or may not equal L", RED),
        ]
        y = 1.4; boxes = []
        for txt, col in items:
            mob = Text(txt, font_size=23, color=col).move_to(UP*y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.2)
            boxes.append((b,mob)); y -= 0.9
        self.wait(1.0)
        self.play(*[FadeOut(b) for b,_ in boxes], *[FadeOut(m) for _,m in boxes], FadeOut(eb), FadeOut(eq), FadeOut(eq2), run_time=0.5)
        rules = Text("Limit laws:\\n\\n  lim(f+g) = lim f + lim g\\n  lim(f*g) = lim f * lim g\\n  lim(f/g) = lim f / lim g  (if lim g != 0)\\n  lim(c*f) = c * lim f\\n\\nOne-sided limits:\\n  lim from right (x->c+) and left (x->c-)\\n  Limit exists iff both sides equal L.", font_size=22, color=WHITE).move_to(ORIGIN)
        rb = self._box(rules, border=BLUE, buff=0.38)
        self.play(FadeIn(rb), Write(rules), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: lim(x->2) (x^2-4)/(x-2)")
        steps = [
            ("f(x) = (x^2-4)/(x-2)", WHITE, 2.8),
            ("At x=2: (4-4)/(2-2) = 0/0  (indeterminate!)", RED, 2.0),
            ("Factor: x^2-4 = (x+2)(x-2)", BLUE, 1.2),
            ("f(x) = (x+2)(x-2)/(x-2) = x+2  for x != 2", GREEN, 0.4),
            ("lim(x->2) f(x) = lim(x->2) (x+2) = 4", YELL, -0.4),
            ("Note: f(2) is undefined, but limit = 4!", GREEN, -1.2),
            ("Limit describes APPROACH, not arrival.", WHITE, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "Why Limits Matter")
        ins = Text("Limits are the foundation of calculus:\\n\\n  Derivative = limit of difference quotient\\n    f\'(x) = lim(h->0) [f(x+h)-f(x)] / h\\n\\n  Integral = limit of Riemann sums\\n    area = lim(n->inf) sum of n rectangles\\n\\n  Continuity = lim(x->c) f(x) = f(c)\\n\\n  Without limits, calculus does not exist.", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        eps = Text("Epsilon-delta definition (rigorous):\\n\\n  lim(x->c) f(x) = L means:\\n  For every epsilon > 0,\\n  there exists delta > 0 such that:\\n  if 0 < |x-c| < delta  then  |f(x)-L| < epsilon\\n\\n  This is the formal foundation\\n  that makes analysis rigorous.", font_size=22, color=YELL).move_to(ORIGIN)
        eb = self._box(eps, border=YELL, buff=0.38)
        self.play(FadeIn(eb), Write(eps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes(xr=(-0.3,5,1), yr=(-0.3,2.5,0.5))
        f = lambda x: np.sin(x)/x if abs(x) > 0.001 else 1.0
        curve = ax.plot(f, x_range=[0.05, 4.8], color=BLUE, stroke_width=3.5)
        hole = Circle(radius=0.1, color=RED, fill_color=BG, fill_opacity=1, stroke_width=2).move_to(ax.c2p(0,1))
        self.play(Create(ax), Create(curve), Create(hole), run_time=2.0); self.wait(0.5)
        sm = Text("Limits\\n\\n  lim(x->c) f(x) = L\\n\\n  Direction of approach matters\\n  Function value at c does not\\n\\n  Powers calculus:\\n  Derivatives, integrals, continuity\\n\\n  Epsilon-delta: the rigorous definition\\n  The language of infinitesimals", font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
VECTOR_ADD = HEADER.format(title="Vector Addition") + TPLATE("VectorAdditionScene") + '''
    def s1_hook(self):
        t = Text("Vector Addition", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Walking in two directions", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("You walk 3 km east, then 4 km north.\\nWhere are you?", font_size=28, color=WHITE).move_to(UP*1.0)
        ans = Text("(3, 0) + (0, 4) = (3, 4)\\nDistance from start: 5 km (Pythagoras!)", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Vector addition is the tip-to-tail operation:\\nplace the second vector at the tip of the first.\\n\\nComponent-wise: (a+c, b+d)\\nThe foundation of linear combinations.", font_size=26, color=WHITE).move_to(ORIGIN)
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
        r1 = Text("Tip-to-tail rule:\\nPlace w at tip of v,\\nthen draw resultant", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Also: parallelogram rule\\n(both orders give same result)", font_size=22, color=YELL)
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
        lc = Text("Linear combinations:\\n\\n  c1*v + c2*w + ... cn*vn\\n\\n  Every point in the plane reachable\\n  from two linearly independent vectors.\\n\\n  This is the SPAN concept.", font_size=24, color=WHITE).move_to(ORIGIN)
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
        ins = Text("Vector spaces are defined by 8 axioms\\n(including vector addition laws).\\n\\nAny structure satisfying these axioms\\nbehaves like vectors:\\n\\n  Polynomials: p(x) + q(x)\\n  Matrices: A + B\\n  Functions: f(x) + g(x)\\n  Signals: audio1 + audio2 (superposition)\\n\\nAll share identical mathematical structure!", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        ml = Text("Machine learning connections:\\n\\n  Word embeddings: king - man + woman = queen\\n  This is VECTOR ARITHMETIC!\\n\\n  Gradient descent: w := w - lr * grad\\n  Weight update = vector subtraction\\n\\n  Every neural layer: output = Wx + b\\n  Matrix times vector plus bias vector.", font_size=22, color=YELL).move_to(ORIGIN)
        mb = self._box(ml, border=YELL, buff=0.38)
        self.play(FadeIn(mb), Write(ml), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes(xr=(-0.3,5,1), yr=(-0.3,5,1))
        v = Arrow(ax.c2p(0,0), ax.c2p(3,1), color=BLUE, stroke_width=4, buff=0)
        w = Arrow(ax.c2p(3,1), ax.c2p(4,3), color=RED, stroke_width=4, buff=0)
        s = Arrow(ax.c2p(0,0), ax.c2p(4,3), color=GREEN, stroke_width=4, buff=0)
        self.play(Create(ax), Create(v), Create(w), Create(s), run_time=2.5); self.wait(0.5)
        sm = Text("Vector Addition\\n\\n  v + w = (vx+wx, vy+wy)\\n\\n  Tip-to-tail rule (geometric)\\n  Component-wise (algebraic)\\n\\n  Commutative and associative\\n  Basis for linear combinations\\n  Fundamental to vector spaces", font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
DOT_PRODUCT = HEADER.format(title="The Dot Product") + TPLATE("DotProductScene") + '''
    def s1_hook(self):
        t = Text("The Dot Product", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Measuring alignment", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("How much does one vector point in\\nthe direction of another?", font_size=28, color=WHITE).move_to(UP*1.0)
        ans = Text("The dot product answers this exactly.\\nIt is the signed length of the projection.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("v . w = vx*wx + vy*wy\\n       = |v| |w| cos(theta)\\n\\nPositive: vectors point same way\\nZero: perpendicular (orthogonal)\\nNegative: vectors point opposite ways", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Geometric Meaning: Projection")
        ax = self._axes()
        self.play(Create(ax), run_time=2.0); self.wait(0.5)
        v = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=5, buff=0)
        w = Arrow(ax.c2p(0,0), ax.c2p(2,2), color=RED, stroke_width=5, buff=0)
        vl = Text("v=(3,0)", font_size=20, color=BLUE).next_to(ax.c2p(1.5,0), DOWN, buff=0.15)
        wl = Text("w=(2,2)", font_size=20, color=RED).next_to(ax.c2p(1,1), LEFT, buff=0.1)
        self.play(Create(v), Create(w), Write(vl), Write(wl), run_time=2.5); self.wait(0.5)
        proj_tip = ax.c2p(2, 0)
        proj = DashedLine(ax.c2p(2,2), proj_tip, color=YELL)
        proj_vec = Arrow(ax.c2p(0,0), proj_tip, color=GREEN, stroke_width=4, buff=0)
        self.play(Create(proj), Create(proj_vec), run_time=2.0); self.wait(0.5)
        r1 = Text("Projection of w onto v = 2\\n(the shadow of w on v)\\nv.w = 3*2 + 0*2 = 6 = |v|*proj", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        w2 = Arrow(ax.c2p(0,0), ax.c2p(0,3), color=RED, stroke_width=5, buff=0)
        w2l = Text("w=(0,3) perpendicular to v", font_size=20, color=RED).next_to(ax.c2p(0,1.5), RIGHT, buff=0.1)
        self.play(Transform(w, w2), Transform(wl, w2l), run_time=1.5); self.wait(0.5)
        r2 = Text("v . w = 3*0 + 0*3 = 0\\nOrthogonal vectors -> dot product 0", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Formulas and Properties")
        eq1 = Text("v . w = vx*wx + vy*wy  (component form)", font_size=26, color=YELL).move_to(UP*2.5)
        eq2 = Text("v . w = |v| |w| cos(theta)  (geometric form)", font_size=26, color=GREEN).move_to(UP*1.6)
        b1 = self._box(eq1, border=YELL, buff=0.3)
        b2 = self._box(eq2, border=GREEN, buff=0.3)
        self.play(FadeIn(b1), Write(eq1), run_time=2.0); self.wait(1.0)
        self.play(FadeIn(b2), Write(eq2), run_time=2.0); self.wait(1.0)
        props = Text("Properties:\\n\\n  Commutative:  v . w = w . v\\n  Distributive: v . (w+u) = v.w + v.u\\n  Scalar:       (cv) . w = c(v.w)\\n  Self:         v . v = |v|^2\\n\\n  cos(theta) = (v.w)/(|v||w|)\\n  (extract angle between vectors)", font_size=23, color=WHITE).move_to(DOWN*0.5)
        pb = self._box(props, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: v=(1,2,3), w=(4,-1,2)")
        steps = [
            ("v = (1, 2, 3)   w = (4, -1, 2)", WHITE, 2.8),
            ("v . w = 1*4 + 2*(-1) + 3*2", BLUE, 2.0),
            ("      = 4 - 2 + 6 = 8", GREEN, 1.2),
            ("|v| = sqrt(1+4+9) = sqrt(14) ~ 3.742", WHITE, 0.4),
            ("|w| = sqrt(16+1+4) = sqrt(21) ~ 4.583", WHITE, -0.4),
            ("cos(theta) = 8 / (3.742 * 4.583) ~ 0.466", YELL, -1.2),
            ("theta ~ 62.2 degrees", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("The dot product is the most important\\noperation in applied mathematics:\\n\\n  Physics: Work = F . d (force dot displacement)\\n  Graphics: Lighting = N . L (normal dot light)\\n  ML: Attention = Q . K^T / sqrt(d)\\n  Signal: Correlation of two signals\\n  Statistics: Covariance (normalized dot product)\\n\\n  Cosine similarity = dot product of unit vectors\\n  Used in recommendation systems, search engines", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        ortho = Text("Orthogonality is a superpower:\\n\\n  v . w = 0  <->  v perpendicular to w\\n\\n  Orthonormal bases: every vector written\\n  as v = (v.e1)*e1 + (v.e2)*e2 + ...\\n\\n  QR decomposition, Gram-Schmidt:\\n  Turn any basis into orthonormal basis\\n\\n  PCA: find orthogonal directions of variation", font_size=22, color=YELL).move_to(ORIGIN)
        ob = self._box(ortho, border=YELL, buff=0.38)
        self.play(FadeIn(ob), Write(ortho), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes()
        v = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=4, buff=0)
        w = Arrow(ax.c2p(0,0), ax.c2p(2,2), color=RED, stroke_width=4, buff=0)
        self.play(Create(ax), Create(v), Create(w), run_time=2.0); self.wait(0.5)
        sm = Text("The Dot Product\\n\\n  v . w = vx*wx + vy*wy\\n       = |v||w|cos(theta)\\n\\n  = 0  <->  orthogonal\\n  > 0  <->  same direction\\n  < 0  <->  opposite direction\\n\\n  Projection, angle, similarity\\n  Work, lighting, attention, cosine sim", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
CROSS_PRODUCT = HEADER.format(title="The Cross Product") + TPLATE("CrossProductScene") + '''
    def s1_hook(self):
        t = Text("The Cross Product", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Perpendicularity in 3D", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Two vectors define a plane.\\nWhat vector is perpendicular to that plane?", font_size=28, color=WHITE).move_to(UP*1.0)
        ans = Text("The cross product gives you exactly that vector.\\nAnd its magnitude = area of parallelogram.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("v x w = (vy*wz - vz*wy, vz*wx - vx*wz, vx*wy - vy*wx)\\n\\nResult is a VECTOR (unlike dot product = scalar)\\n|v x w| = |v||w|sin(theta) = area of parallelogram\\nDirection: right-hand rule", font_size=24, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "The Right-Hand Rule")
        text1 = Text("Cross product: v x w", font_size=32, color=BLUE).move_to(UP*2.5)
        self.play(Write(text1), run_time=1.5); self.wait(0.5)
        vtext = Text("v = (1, 0, 0)  [x-axis]", font_size=26, color=RED).move_to(UP*1.5)
        wtext = Text("w = (0, 1, 0)  [y-axis]", font_size=26, color=GREEN).next_to(vtext, DOWN, buff=0.4)
        self.play(Write(vtext), Write(wtext), run_time=2.0); self.wait(0.8)
        cross = Text("v x w = (0*0-0*1, 0*0-1*0, 1*1-0*0)\\n      = (0, 0, 1)  [z-axis!]", font_size=26, color=YELL).next_to(wtext, DOWN, buff=0.4)
        self.play(Write(cross), run_time=2.0); self.wait(1.5)
        rhr = Text("Right-hand rule:\\nCurl fingers from v to w\\nThumb points in direction of v x w", font_size=26, color=WHITE).next_to(cross, DOWN, buff=0.5)
        self.play(Write(rhr), run_time=2.0); self.wait(1.5)
        anti = Text("Anti-commutative: w x v = -(v x w)\\n(order matters! flip both vectors -> flip result)", font_size=24, color=RED).next_to(rhr, DOWN, buff=0.4)
        self.play(Write(anti), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Formal Definition and Properties")
        formula = Text("v x w = det | i    j    k  |\\n            | vx   vy   vz |\\n            | wx   wy   wz |", font_size=26, color=YELL).move_to(UP*2.0)
        fb = self._box(formula, border=YELL, buff=0.4)
        self.play(FadeIn(fb), Write(formula), run_time=2.5); self.wait(1.5)
        expanded = Text("= i(vy*wz - vz*wy)\\n- j(vx*wz - vz*wx)\\n+ k(vx*wy - vy*wx)", font_size=24, color=GREEN).next_to(formula, DOWN, buff=0.5)
        eb = self._box(expanded, border=GREEN, buff=0.3)
        self.play(FadeIn(eb), Write(expanded), run_time=2.0); self.wait(1.0)
        props = Text("Key properties:\\n  Anti-commutative: v x w = -(w x v)\\n  Not associative: (u x v) x w != u x (v x w)\\n  Distributive: v x (w+u) = v x w + v x u\\n  |v x w| = |v||w|sin(theta)\\n  v x w = 0  iff  v and w are parallel", font_size=22, color=WHITE).next_to(expanded, DOWN, buff=0.4)
        pb = self._box(props, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: v=(1,2,3), w=(4,5,6)")
        steps = [
            ("v = (1, 2, 3)   w = (4, 5, 6)", WHITE, 2.8),
            ("v x w: i component = 2*6 - 3*5 = 12-15 = -3", BLUE, 2.0),
            ("       j component = -(1*6 - 3*4) = -(6-12) = 6", GREEN, 1.2),
            ("       k component = 1*5 - 2*4 = 5-8 = -3", BLUE, 0.4),
            ("v x w = (-3, 6, -3)", YELL, -0.4),
            ("Check: v.(vxw) = 1*(-3)+2*6+3*(-3) = -3+12-9 = 0", GREEN, -1.2),
            ("And w.(vxw) = 4*(-3)+5*6+6*(-3) = 0  (perpendicular!)", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "Applications")
        ins = Text("Cross product powers 3D graphics:\\n\\n  Surface normals: n = v x w\\n  (perpendicular to surface -> lighting calculations)\\n\\n  Physics: torque = r x F\\n  Angular momentum: L = r x p\\n  Magnetic force: F = q(v x B)\\n\\n  Computing area of triangle:\\n  Area = 0.5 * |v x w|\\n\\n  Only defined in 3D (and 7D with octonions)", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        comp = Text("Dot vs Cross product:\\n\\n  Dot product:   v . w = scalar\\n    -> measures alignment, projection\\n    -> works in any dimension\\n\\n  Cross product: v x w = vector\\n    -> gives perpendicular direction\\n    -> measures area, rotation axis\\n    -> only in 3D!\\n\\n  Together they completely describe 3D geometry.", font_size=22, color=YELL).move_to(ORIGIN)
        cb = self._box(comp, border=YELL, buff=0.38)
        self.play(FadeIn(cb), Write(comp), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Cross Product  v x w\\n\\n  v x w = (vy*wz-vz*wy, vz*wx-vx*wz, vx*wy-vy*wx)\\n  |v x w| = |v||w|sin(theta)\\n\\n  PERPENDICULAR to both v and w\\n  Anti-commutative: w x v = -(v x w)\\n  Magnitude = parallelogram area\\n\\n  Applications:\\n  3D normals, torque, magnetic force,\\n  triangle area, rotation axes", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
SHEAR = HEADER.format(title="Shear Transformation") + TPLATE("ShearScene") + '''
    def s1_hook(self):
        t = Text("Shear Transformations", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("Tilting without scaling", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Imagine a stack of papers.\\nPush the top sideways, bottom stays fixed.\\nEach layer slides a little more than the one below.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("This is a shear transformation.\\nArea is preserved, but shape is distorted.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.5); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Shear matrix (horizontal):\\n\\n  S = [[1, k],    applied to vector (x,y):\\n       [0, 1]]    -> (x + k*y, y)\\n\\n  y-coordinates unchanged\\n  x-coordinates shift by k*y", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Visualizing Shear on a Grid")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        r1 = Text("Before shear: unit square", font_size=24, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=1.5)
        corners = [(-1,-1),(1,-1),(1,1),(-1,1)]
        square = Polygon(*[plane.c2p(x,y) for x,y in corners], color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
        self.play(Create(square), run_time=1.5); self.wait(1.0)
        k = 1.0
        sheared_corners = [(x + k*y, y) for x,y in corners]
        sheared = Polygon(*[plane.c2p(x,y) for x,y in sheared_corners], color=YELL, stroke_width=3, fill_color=YELL, fill_opacity=0.2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        r2 = Text("After shear (k=1):\\nx -> x + y", font_size=24, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), Transform(square, sheared), run_time=2.5); self.wait(1.5)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        r3 = Text("Area unchanged!\\ndet([[1,k],[0,1]]) = 1", font_size=24, color=GREEN)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=GREEN)
        self.play(FadeIn(b3), Write(r3), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Shear Matrices")
        mats = Text("Horizontal shear (k):\\n  S = [[1, k],  (x,y) -> (x+ky, y)\\n       [0, 1]]\\n\\nVertical shear (k):\\n  S = [[1, 0],  (x,y) -> (x, kx+y)\\n       [k, 1]]\\n\\n3D shear (x by z):\\n  S = [[1, 0, k],  (x,y,z) -> (x+kz, y, z)\\n       [0, 1, 0],\\n       [0, 0, 1]]", font_size=24, color=WHITE).move_to(UP*0.5)
        mb = self._box(mats, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(mats), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(mb), FadeOut(mats), run_time=0.5)
        props = Text("Key properties of shear:\\n\\n  det(S) = 1  (area preserved in 2D)\\n  Eigenvalues: both = 1\\n  Not orthogonal (angles distorted)\\n  Composition: S(k1) * S(k2) = S(k1+k2)\\n  Inverse: S(-k) undoes shear", font_size=24, color=YELL).move_to(ORIGIN)
        pb = self._box(props, border=YELL, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: Shear k=0.5 on (3, 2)")
        steps = [
            ("S = [[1, 0.5], [0, 1]],  v = (3, 2)", WHITE, 2.5),
            ("S * v = (1*3 + 0.5*2,  0*3 + 1*2)", BLUE, 1.7),
            ("      = (3 + 1.0,  2)", GREEN, 0.9),
            ("      = (4.0,  2)", YELL, 0.1),
            ("y unchanged: 2 -> 2", GREEN, -0.7),
            ("x shifted by k*y = 0.5*2 = 1.0", WHITE, -1.5),
            ("Area of unit square: still = 1", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=26, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "Where Shear Appears")
        ins = Text("Shear transforms appear everywhere:\\n\\n  Computer graphics: italicizing text!\\n  (Fake italic = horizontal shear)\\n\\n  Stress/strain in materials:\\n  (Material deforms under tangential force)\\n\\n  Image processing: perspective correction\\n\\n  LU decomposition: elimination steps are shears\\n  (Row subtraction = shear transformation)\\n\\n  Crystal deformation in solid-state physics", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        det_insight = Text("Deep insight: Shear has det=1.\\n\\nAll volume-preserving linear maps\\nare products of shear matrices.\\n\\nSpecial Linear group SL(n):\\n= all matrices with det=1\\nGenerated entirely by elementary shears!\\n\\nThis makes shear the fundamental\\nbuilding block of volume-preserving maps.", font_size=22, color=YELL).move_to(ORIGIN)
        db = self._box(det_insight, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(det_insight), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        corners = [(-1,-1),(1,-1),(1,1),(-1,1)]
        original = Polygon(*[plane.c2p(x,y) for x,y in corners], color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
        sheared_c = [(x+0.8*y,y) for x,y in corners]
        sheared = Polygon(*[plane.c2p(x,y) for x,y in sheared_c], color=YELL, stroke_width=3, fill_color=YELL, fill_opacity=0.2)
        self.play(Create(plane), Create(original), Create(sheared), run_time=2.0); self.wait(0.5)
        sm = Text("Shear  S = [[1,k],[0,1]]\\n\\n  (x,y) -> (x+ky, y)\\n  Tilts shape, preserves area\\n  det = 1 always\\n\\n  Found in: text italics,\\n  LU decomposition, stress,\\n  perspective correction\\n\\n  Builds all volume-preserving maps", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
PROJECTION = HEADER.format(title="Projection") + TPLATE("ProjectionScene") + '''
    def s1_hook(self):
        t = Text("Projection", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("Finding the shadow", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Sunlight shining straight down.\\nA stick casts a shadow on the ground.\\nThe shadow is the projection.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Projection = the closest point on a line (or plane)\\nto a given vector. The mathematical shadow.", font_size=24, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("proj_u(v) = (v.u / u.u) * u\\n\\nProject v onto direction u:\\n  Scale u by the dot product fraction.\\nResult = component of v along u.", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Geometric Projection")
        ax = self._axes()
        self.play(Create(ax), run_time=2.0); self.wait(0.5)
        u = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=5, buff=0)
        v = Arrow(ax.c2p(0,0), ax.c2p(2,2.5), color=RED, stroke_width=5, buff=0)
        ul = Text("u=(3,0)", font_size=20, color=BLUE).next_to(ax.c2p(1.5,0), DOWN, buff=0.15)
        vl = Text("v=(2,2.5)", font_size=20, color=RED).next_to(ax.c2p(1,1.25), LEFT, buff=0.1)
        self.play(Create(u), Create(v), Write(ul), Write(vl), run_time=2.5); self.wait(0.5)
        proj_x = 2.0
        proj = Arrow(ax.c2p(0,0), ax.c2p(proj_x, 0), color=GREEN, stroke_width=5, buff=0)
        drop = DashedLine(ax.c2p(2,2.5), ax.c2p(2,0), color=YELL)
        self.play(Create(drop), Create(proj), run_time=2.0); self.wait(0.5)
        r1 = Text("proj = (v.u/|u|^2) * u\\n= (6/9)*(3,0) = (2,0)", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(1.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Error (rejection):\\nv - proj = (0, 2.5)\\nPerpendicular to u!", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Projection Formula")
        eq = Text("proj_u(v) = (v . u) / (u . u)  *  u", font_size=30, color=YELL).move_to(UP*2.5)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(1.0)
        matrix_form = Text("Projection matrix onto unit vector u:\\n\\n  P = u * u^T\\n\\n  (outer product of u with itself)\\n  P^2 = P  (idempotent: projecting twice = projecting once)\\n  P is symmetric: P^T = P", font_size=24, color=WHITE).move_to(UP*0.2)
        mb = self._box(matrix_form, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(matrix_form), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(mb), FadeOut(matrix_form), FadeOut(eb), FadeOut(eq), run_time=0.5)
        subspace = Text("Projection onto subspace (column space of A):\\n\\n  P = A(A^T A)^{-1} A^T\\n\\n  The projection that minimizes |v - Pv|^2\\n  Key in least squares regression:\\n  b_hat = (A^T A)^{-1} A^T b  = pseudo-inverse * b", font_size=23, color=GREEN).move_to(ORIGIN)
        sb = self._box(subspace, border=GREEN, buff=0.38)
        self.play(FadeIn(sb), Write(subspace), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: proj of v=(3,4) onto u=(1,0)")
        steps = [
            ("v = (3, 4)   u = (1, 0)  (x-axis)", WHITE, 2.5),
            ("v . u = 3*1 + 4*0 = 3", BLUE, 1.7),
            ("u . u = 1^2 + 0^2 = 1", WHITE, 0.9),
            ("proj = (3/1) * (1,0) = (3, 0)", GREEN, 0.1),
            ("rejection = v - proj = (3,4)-(3,0) = (0,4)", YELL, -0.7),
            ("Check: (0,4).(1,0) = 0 (perpendicular!)", GREEN, -1.5),
            ("v = proj + rejection  (decomposition!)", WHITE, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Projection is the core of least squares:\\n\\n  Given overdetermined system Ax = b (no exact solution)\\n  Find x that minimizes |Ax - b|^2\\n\\n  Solution: project b onto column space of A\\n  b_hat = A(A^T A)^{-1} A^T b\\n\\n  This is linear regression!\\n  Fitting a line = projecting data onto\\n  the subspace spanned by [1, x]", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        gram = Text("Gram-Schmidt orthogonalization:\\n\\n  Turn any basis into orthogonal basis\\n  using repeated projections:\\n\\n  u1 = v1\\n  u2 = v2 - proj_{u1}(v2)\\n  u3 = v3 - proj_{u1}(v3) - proj_{u2}(v3)\\n  ...\\n\\n  Foundation of QR decomposition", font_size=22, color=YELL).move_to(ORIGIN)
        gb = self._box(gram, border=YELL, buff=0.38)
        self.play(FadeIn(gb), Write(gram), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes()
        u = Arrow(ax.c2p(0,0), ax.c2p(3,0), color=BLUE, stroke_width=4, buff=0)
        v = Arrow(ax.c2p(0,0), ax.c2p(2,2.5), color=RED, stroke_width=4, buff=0)
        proj = Arrow(ax.c2p(0,0), ax.c2p(2,0), color=GREEN, stroke_width=4, buff=0)
        drop = DashedLine(ax.c2p(2,2.5), ax.c2p(2,0), color=YELL)
        self.play(Create(ax), Create(u), Create(v), Create(proj), Create(drop), run_time=2.5); self.wait(0.5)
        sm = Text("Projection\\n\\n  proj_u(v) = (v.u/u.u) * u\\n\\n  Component of v along u\\n  Minimizes distance (least squares)\\n\\n  P = u*u^T  (projection matrix)\\n  P^2 = P  (idempotent)\\n\\n  Powers: linear regression, QR,\\n  Gram-Schmidt, PCA", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
SPAN = HEADER.format(title="Span") + TPLATE("SpanScene") + '''
    def s1_hook(self):
        t = Text("Span", font_size=56, color=WHITE).move_to(UP*0.5)
        t2 = Text("All reachable destinations", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("You have two vectors.\\nBy scaling and adding them in all possible ways,\\nwhat destinations can you reach?", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("The SET of all reachable points is the span.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("span{v1, v2, ..., vn} =\\n{ c1*v1 + c2*v2 + ... + cn*vn | ci in R }\\n\\nThe set of ALL linear combinations.\\nAlways a subspace (contains 0, closed under + and *).", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Three Cases for Span")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=5, buff=0)
        self.play(Create(v1), Create(v2), run_time=1.5); self.wait(0.5)
        r1 = Text("Case 1: v1=(1,0), v2=(0,1)\\nspan = entire R^2 plane", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        v2b = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=RED, stroke_width=5, buff=0)
        line = Line(plane.c2p(-4,0), plane.c2p(4,0), color=YELL, stroke_width=2)
        self.play(Transform(v2, v2b), Create(line), run_time=1.5); self.wait(0.5)
        r2 = Text("Case 2: v1=(1,0), v2=(2,0)\\nParallel! span = x-axis only (line)", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b2), FadeOut(r2), FadeOut(line), run_time=0.3)
        dot = Dot(plane.c2p(0,0), color=GREEN, radius=0.15)
        self.play(FadeOut(v1), FadeOut(v2), run_time=0.3)
        self.play(FadeIn(dot), run_time=0.5)
        r3 = Text("Case 3: v=0 only\\nspan = just the origin (point)", font_size=22, color=RED)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=RED)
        self.play(FadeIn(b3), Write(r3), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Span and Subspaces")
        defn = Text("A subspace must satisfy:\\n  1. Contains the zero vector\\n  2. Closed under addition\\n  3. Closed under scalar multiplication\\n\\nspan{v1,...,vn} always satisfies all three.\\nTherefore span is always a subspace.", font_size=24, color=WHITE).move_to(UP*0.8)
        db = self._box(defn, border=BLUE, buff=0.38)
        self.play(FadeIn(db), Write(defn), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(db), FadeOut(defn), run_time=0.5)
        dim = Text("Dimension of span:\\n\\n  span{v1} in R^2: dim 1 (line)\\n  span{v1,v2} in R^2: dim 2 if independent, 1 if parallel\\n  span{v1,...,vn}: dim = rank (number of independent vectors)\\n\\n  span fills R^n  iff  rank = n  (vectors span the full space)", font_size=23, color=YELL).move_to(ORIGIN)
        yb = self._box(dim, border=YELL, buff=0.38)
        self.play(FadeIn(yb), Write(dim), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Does v=(3,5) lie in span{(1,2),(2,3)}?")
        steps = [
            ("Find c1, c2 such that c1*(1,2) + c2*(2,3) = (3,5)", WHITE, 2.8),
            ("c1 + 2*c2 = 3   (x-equation)", BLUE, 2.0),
            ("2*c1 + 3*c2 = 5  (y-equation)", BLUE, 1.2),
            ("From eq1: c1 = 3 - 2*c2", WHITE, 0.4),
            ("Sub into eq2: 2(3-2*c2) + 3*c2 = 5", WHITE, -0.4),
            ("6 - 4*c2 + 3*c2 = 5  ->  c2 = 1,  c1 = 1", GREEN, -1.2),
            ("YES! v = 1*(1,2) + 1*(2,3) = (3,5) in span.", YELL, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "Span is Everywhere")
        ins = Text("Column space of a matrix = span of its columns\\n\\nAx = b  has a solution iff  b is in span(cols of A)\\n\\nThis is why span determines solvability!\\n\\n  Rank of matrix = dim of column space\\n  = dim of span of columns\\n\\nFull column rank -> can solve Ax=b for any b\\nRank deficient -> some b unreachable (no solution)", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Real applications of span:\\n\\n  Graphics: span{right, up, forward} = 3D space\\n  Signals: Fourier basis spans all periodic functions\\n  ML: span of training data = what model can represent\\n  Control: reachable states = span of control inputs\\n  Quantum: superposition = span of basis states", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        self.play(Create(plane), run_time=1.5)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=4, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=4, buff=0)
        self.play(Create(v1), Create(v2), run_time=1.5); self.wait(0.5)
        sm = Text("Span\\n\\n  span{v1,...,vn} = all linear combinations\\n  c1*v1 + ... + cn*vn  (ci in R)\\n\\n  Always a subspace\\n  dim = number of independent vectors\\n\\n  2 independent vectors in R^2 -> spans R^2\\n  Parallel vectors -> span is a line only\\n\\n  Column space = span of columns", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
LIN_INDEP = HEADER.format(title="Linear Independence") + TPLATE("LinearIndepScene") + '''
    def s1_hook(self):
        t = Text("Linear Independence", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("No redundancy in directions", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Can any of your vectors be written as a\\ncombination of the others?\\nIf not: they are linearly independent.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Redundant vectors waste dimensions.\\nIndependent vectors give you new directions.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Formally: v1,...,vn are linearly independent if\\n\\n  c1*v1 + c2*v2 + ... + cn*vn = 0\\n  implies c1=c2=...=cn=0\\n\\nOnly the trivial solution! No vector is\\na combination of the others.", font_size=24, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Independent vs Dependent")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=RED, stroke_width=5, buff=0)
        self.play(Create(v1), Create(v2), run_time=2.0); self.wait(0.5)
        r1 = Text("(2,0) and (0,2):\\nIndependent! Different directions.\\nSpan all of R^2", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), FadeOut(v2), run_time=0.3)
        v2dep = Arrow(plane.c2p(0,0), plane.c2p(4,0), color=RED, stroke_width=5, buff=0)
        self.play(Create(v2dep), run_time=1.5); self.wait(0.5)
        r2 = Text("(2,0) and (4,0):\\nDependent! (4,0) = 2*(2,0)\\nSpan only x-axis, dim=1", font_size=22, color=RED)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b2), FadeOut(r2), FadeOut(v2dep), run_time=0.3)
        v3 = Arrow(plane.c2p(0,0), plane.c2p(1,1), color=GREEN, stroke_width=5, buff=0)
        self.play(Create(v3), run_time=1.5); self.wait(0.3)
        r3 = Text("3 vectors in R^2: always dependent!\\n(2 dimensions can only hold 2 independent)", font_size=22, color=YELL)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=YELL)
        self.play(FadeIn(b3), Write(r3), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Testing Independence")
        method = Text("Method: form matrix A = [v1|v2|...|vn]\\nThen row reduce.\\n\\n  Independent iff no free variables\\n  (every column has a pivot)\\n  <-> rank(A) = number of vectors\\n  <-> det(A) != 0  (for square matrices)\\n\\nNumber of independent vectors = rank", font_size=24, color=WHITE).move_to(UP*0.5)
        mb = self._box(method, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(method), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(mb), FadeOut(method), run_time=0.5)
        rules = Text("Key rules:\\n\\n  n+1 vectors in R^n are always dependent\\n  n vectors in R^n: independent iff det != 0\\n  Subset of independent set is independent\\n  Span = same if add dependent vector\\n  Basis = maximal independent set = minimal spanning set", font_size=23, color=YELL).move_to(ORIGIN)
        rb = self._box(rules, border=YELL, buff=0.38)
        self.play(FadeIn(rb), Write(rules), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Test: (1,2), (3,4), (5,6) in R^2")
        steps = [
            ("Form matrix:  [[1,3,5],[2,4,6]]", WHITE, 2.5),
            ("Row reduce: R2 = R2 - 2*R1", BLUE, 1.7),
            ("-> [[1,3,5],[0,-2,-4]]", GREEN, 0.9),
            ("R2 = R2/(-2): -> [[1,3,5],[0,1,2]]", GREEN, 0.1),
            ("R1 = R1-3*R2: -> [[1,0,-1],[0,1,2]]", GREEN, -0.7),
            ("Free variable in column 3: DEPENDENT", RED, -1.5),
            ("(5,6) = -1*(1,2) + 2*(3,4)  [verify!]", YELL, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Linear independence is THE central concept\\nin linear algebra:\\n\\n  Rank-Nullity theorem: rank + nullity = n\\n  (independent cols + dependent cols = total cols)\\n\\n  Basis = maximal independent set\\n  Dimension = size of any basis\\n\\n  Gram-Schmidt turns dependent set into independent!\\n  SVD reveals true independence structure", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        ml = Text("In machine learning:\\n\\n  Features: independent = carry unique information\\n  Dependent = redundant, causes multicollinearity\\n\\n  PCA: find directions of maximum variance\\n  = independent principal components\\n\\n  Attention heads in transformers:\\n  Should attend to independent aspects\\n  of the input (diversity is valuable)", font_size=22, color=YELL).move_to(ORIGIN)
        mb = self._box(ml, border=YELL, buff=0.38)
        self.play(FadeIn(mb), Write(ml), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=BLUE, stroke_width=4, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=RED, stroke_width=4, buff=0)
        self.play(Create(plane), Create(v1), Create(v2), run_time=2.0); self.wait(0.5)
        sm = Text("Linear Independence\\n\\n  c1*v1+...+cn*vn=0 => all ci=0\\n  No vector is combo of others\\n\\n  Test: row reduce, check rank\\n  n vectors in R^n: det != 0 <-> indep\\n\\n  Basis = maximal independent set\\n  Rank = count of independent cols\\n  Foundation of dimension theory", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
BASIS = HEADER.format(title="Basis") + TPLATE("BasisScene") + '''
    def s1_hook(self):
        t = Text("Basis", font_size=56, color=WHITE).move_to(UP*0.5)
        t2 = Text("The coordinate system", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("The x-y axes we use are just one choice.\\nYou could measure the same world using\\ndifferent rulers pointing in different directions.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("A basis is a choice of coordinate system.\\nEvery vector has unique coordinates in that basis.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("A BASIS of R^n is a set of vectors that:\\n  1. Spans R^n  (can reach every point)\\n  2. Is linearly independent  (no redundancy)\\n\\nEvery vector v has a UNIQUE representation:\\n  v = c1*b1 + c2*b2 + ... + cn*bn", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Standard vs Non-Standard Basis")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        e1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=5, buff=0)
        e2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=5, buff=0)
        e1l = Text("e1=(1,0)", font_size=20, color=BLUE).next_to(plane.c2p(1,0), UP, buff=0.1)
        e2l = Text("e2=(0,1)", font_size=20, color=RED).next_to(plane.c2p(0,1), RIGHT, buff=0.1)
        self.play(Create(e1), Create(e2), Write(e1l), Write(e2l), run_time=2.0); self.wait(0.5)
        r1 = Text("Standard basis\\nfor R^2", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(1.5)
        b1_vec = Arrow(plane.c2p(0,0), plane.c2p(1,1), color=YELL, stroke_width=5, buff=0)
        b2_vec = Arrow(plane.c2p(0,0), plane.c2p(-1,1), color=GREEN, stroke_width=5, buff=0)
        b1l = Text("b1=(1,1)", font_size=20, color=YELL).next_to(plane.c2p(0.5,0.5), LEFT, buff=0.1)
        b2l = Text("b2=(-1,1)", font_size=20, color=GREEN).next_to(plane.c2p(-0.5,0.5), LEFT, buff=0.1)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        r2 = Text("Rotated basis:\\nalso valid!\\nStill spans R^2, still independent", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(Create(b1_vec), Create(b2_vec), Write(b1l), Write(b2l), run_time=2.0)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Coordinates in a Basis")
        coord = Text("If B = {b1, b2} is a basis, then for any v:\\n  v = c1*b1 + c2*b2  (unique c1, c2)\\n  [v]_B = (c1, c2)  <- coordinates in basis B\\n\\nChange of basis: [v]_B = B^{-1} * [v]_std\\nwhere B = matrix of basis vectors as columns.", font_size=24, color=WHITE).move_to(UP*0.8)
        cb = self._box(coord, border=BLUE, buff=0.38)
        self.play(FadeIn(cb), Write(coord), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(cb), FadeOut(coord), run_time=0.5)
        props = Text("Key facts:\\n\\n  All bases of R^n have exactly n vectors\\n  (= dimension of the space)\\n\\n  Any n linearly independent vectors in R^n\\n  form a basis of R^n\\n\\n  Standard basis: {e1=(1,0,...), e2=(0,1,...),...,en}\\n  Orthonormal basis: all unit vectors, mutually perpendicular", font_size=23, color=YELL).move_to(ORIGIN)
        pb = self._box(props, border=YELL, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Find coordinates of v=(3,1) in B={(1,1),(-1,1)}")
        steps = [
            ("v = c1*(1,1) + c2*(-1,1) = (3,1)", WHITE, 2.5),
            ("c1 - c2 = 3   (x-equation)", BLUE, 1.7),
            ("c1 + c2 = 1   (y-equation)", BLUE, 0.9),
            ("Adding: 2*c1 = 4  ->  c1 = 2", GREEN, 0.1),
            ("Subtracting: 2*c2 = -2  ->  c2 = -1", GREEN, -0.7),
            ("[v]_B = (2, -1)", YELL, -1.5),
            ("Check: 2*(1,1) + (-1)*(-1,1) = (2,2)+(1,-1) = (3,1) ✓", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Choosing the RIGHT basis makes problems trivial:\\n\\n  Diagonal matrix in its eigenbasis:\\n  -> matrix powers are trivial (just raise eigenvalues)\\n\\n  Signal in Fourier basis:\\n  -> convolution becomes multiplication!\\n\\n  PCA: data in eigenvector basis\\n  -> each coordinate is independent\\n\\n  The basis is a LANGUAGE for describing vectors.\\n  Different languages, same mathematical truth.", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        practical = Text("Practical applications:\\n\\n  Computer graphics: local vs world coordinates\\n  (object's own axes = its basis)\\n\\n  GPS: WGS84 coordinate basis\\n  (specific basis for Earth's surface)\\n\\n  Quantum mechanics: measurement basis\\n  (choice of basis = choice of measurement)\\n\\n  Audio: Fourier basis = frequency basis", font_size=22, color=YELL).move_to(ORIGIN)
        pb = self._box(practical, border=YELL, buff=0.38)
        self.play(FadeIn(pb), Write(practical), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        e1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=4, buff=0)
        e2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=4, buff=0)
        self.play(Create(plane), Create(e1), Create(e2), run_time=2.0); self.wait(0.5)
        sm = Text("Basis\\n\\n  Spans the space AND independent\\n  Size = dimension of space\\n\\n  Unique coordinates for every vector\\n  v = c1*b1 + ... + cn*bn\\n\\n  Standard: {e1,e2,...,en}\\n  Change basis: B^{-1} * v\\n\\n  Right basis = trivial computation", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
CHANGE_BASIS = HEADER.format(title="Change of Basis") + TPLATE("ChangeBasisScene") + '''
    def s1_hook(self):
        t = Text("Change of Basis", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("Translating between coordinate systems", font_size=24, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Your friend uses different axes than you.\\nThe SAME physical point has different coordinates\\ndepending on who measures it.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Change of basis converts between coordinate systems.\\nSame vector, different language.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("If B = [b1 | b2 | ... | bn] (basis as matrix of columns)\\n\\n  Standard to B coordinates: [v]_B = B^{-1} * v\\n  B coordinates to standard: v = B * [v]_B\\n\\nTransformation in new basis:\\n  A_B = B^{-1} * A * B  (change of basis formula)", font_size=24, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Two Coordinate Systems")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        std1 = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=BLUE, stroke_width=4, buff=0)
        std2 = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=BLUE, stroke_width=4, buff=0)
        self.play(Create(std1), Create(std2), run_time=1.5)
        r1 = Text("Standard basis: e1=(1,0), e2=(0,1)", font_size=22, color=BLUE)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(1.5)
        b1_v = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=YELL, stroke_width=4, buff=0)
        b2_v = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=GREEN, stroke_width=4, buff=0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        r2 = Text("New basis: b1=(2,1), b2=(0,2)\\nDifferent grid, same plane", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(Create(b1_v), Create(b2_v), run_time=1.5)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(2.0)
        pt = Dot(plane.c2p(2,3), color=RED, radius=0.12)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        r3 = Text("Point (2,3) in standard\\ncoords = what in new basis?", font_size=22, color=RED)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=RED)
        self.play(Create(pt), FadeIn(b3), Write(r3), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "The Change-of-Basis Formula")
        formula = Text("B = [[2, 0],   (columns are basis vectors)\\n     [1, 2]]\\n\\nB^{-1} = (1/det) * [[2, 0],  det = 4\\n                    [-1, 2]]\\n       = [[0.5, 0],\\n          [-0.25, 0.5]]", font_size=24, color=YELL).move_to(UP*0.8)
        fb = self._box(formula, border=YELL, buff=0.38)
        self.play(FadeIn(fb), Write(formula), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(fb), FadeOut(formula), run_time=0.5)
        similar = Text("Similarity transformation:\\n  A_B = B^{-1} A B\\n\\nWhy?  The matrix A acts in standard coords.\\n  B converts FROM new TO standard\\n  A does the transformation\\n  B^{-1} converts BACK to new coordinates\\n\\nSimilar matrices represent the SAME transformation\\nin different coordinate systems!", font_size=23, color=WHITE).move_to(ORIGIN)
        sb = self._box(similar, border=BLUE, buff=0.38)
        self.play(FadeIn(sb), Write(similar), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: (2,3) in basis {(2,1),(0,2)}")
        steps = [
            ("B = [[2,0],[1,2]], v = (2,3)", WHITE, 2.5),
            ("B^{-1} = (1/4)*[[2,0],[-1,2]]", BLUE, 1.7),
            ("[v]_B = B^{-1} * v", WHITE, 0.9),
            ("= (1/4) * [[2,0],[-1,2]] * (2,3)", WHITE, 0.1),
            ("= (1/4) * (4, 4) = (1, 1)", GREEN, -0.7),
            ("So v = 1*b1 + 1*b2 = (2,1)+(0,2) = (2,3) ✓", YELL, -1.5),
            ("Coordinates (1,1) in the new basis!", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "Why This Matters")
        ins = Text("Diagonalization is change of basis!\\n\\n  A = P D P^{-1}\\n  P = eigenvectors  (basis change matrix)\\n  D = diagonal (eigenvalues)\\n\\n  In eigenbasis, A becomes diagonal.\\n  D is the same transformation in a better language.\\n\\n  Matrix powers: A^n = P D^n P^{-1}\\n  Just raise diagonal entries to nth power!", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications everywhere:\\n\\n  Computer graphics: model->world->camera->screen\\n  (4 different bases, 4 coordinate transforms)\\n\\n  Fourier transform: time basis -> frequency basis\\n  Convolution in time = multiplication in frequency!\\n\\n  Quantum: measurement collapses to measurement basis\\n\\n  PCA: data basis -> principal component basis", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Change of Basis\\n\\n  B = matrix of new basis vectors (columns)\\n  Standard -> new: [v]_B = B^{-1} v\\n  New -> standard: v = B [v]_B\\n\\n  Transform in new basis:\\n  A_B = B^{-1} A B  (similarity)\\n\\n  Diagonalization: A = P D P^{-1}\\n  (eigenbasis is the BEST basis)\\n\\n  Fourier, PCA, graphics all use this", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
SVD = HEADER.format(title="Singular Value Decomposition") + TPLATE("SVDScene") + '''
    def s1_hook(self):
        t = Text("SVD", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("The most important decomposition in data science", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Any matrix, no matter how complex,\\ncan be decomposed into three simple operations:\\nrotation, stretching, rotation again.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("SVD reveals the hidden geometry\\nof ANY linear transformation.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("SVD: A = U * Sigma * V^T\\n\\n  U:     m x m orthogonal (left singular vectors)\\n  Sigma: m x n diagonal (singular values)\\n  V^T:   n x n orthogonal (right singular vectors)\\n\\nWorks for ANY matrix (square or not)!", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Geometric Interpretation")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        circ = Circle(radius=1.5, color=BLUE, stroke_width=3).move_to(plane.c2p(0,0))
        self.play(Create(circ), run_time=1.5); self.wait(0.5)
        r1 = Text("Step 1: V^T rotates input space", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(1.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        ell = Ellipse(width=3.0, height=1.5, color=YELL, stroke_width=3).move_to(plane.c2p(0,0))
        r2 = Text("Step 2: Sigma stretches along axes\\n(singular values = stretch factors)", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(Transform(circ, ell), FadeIn(b2), Write(r2), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        ell2 = Ellipse(width=3.0, height=1.5, color=GREEN, stroke_width=3).move_to(plane.c2p(0,0)).rotate(PI/4)
        r3 = Text("Step 3: U rotates output space\\nResult: any matrix = rotation+scale+rotation", font_size=22, color=GREEN)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=GREEN)
        self.play(Transform(circ, ell2), FadeIn(b3), Write(r3), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "SVD Properties")
        props = Text("Singular values (sigma_1 >= sigma_2 >= ... >= 0):\\n  Square roots of eigenvalues of A^T A\\n  = stretch factors of the transformation\\n  = 'strength' of each independent component\\n\\nRank of A = number of non-zero singular values\\n\\nCondition number = sigma_max / sigma_min\\n(measures numerical stability)", font_size=23, color=WHITE).move_to(UP*0.5)
        pb = self._box(props, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(pb), FadeOut(props), run_time=0.5)
        low_rank = Text("Low-rank approximation (truncated SVD):\\n  A_k = U_k * Sigma_k * V_k^T\\n  Keep only top k singular values/vectors!\\n\\n  Minimizes |A - A_k|_F (Frobenius norm)\\n  = best rank-k approximation\\n  = image compression, noise reduction!", font_size=23, color=YELL).move_to(ORIGIN)
        lb = self._box(low_rank, border=YELL, buff=0.38)
        self.play(FadeIn(lb), Write(low_rank), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "SVD Applications")
        steps = [
            ("Recommender systems (Netflix, Spotify):", WHITE, 2.8),
            ("  Matrix: users x items (ratings)", BLUE, 2.0),
            ("  SVD reveals latent factors (genres, themes)", GREEN, 1.2),
            ("  Low-rank approx. fills in missing ratings", YELL, 0.4),
            ("Image compression (JPEG-like):", WHITE, -0.4),
            ("  Image = matrix of pixel values", BLUE, -1.2),
            ("  Keep top k singular values -> compressed image", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("SVD is the cornerstone of numerical linear algebra:\\n\\n  PCA: principal components = right singular vectors of\\n  centered data matrix (V columns of SVD)\\n\\n  Pseudoinverse: A+ = V Sigma+ U^T\\n  (solves least squares for non-square A)\\n\\n  LSI (NLP): SVD of term-document matrix\\n  reveals semantic structure of language\\n\\n  Numerical rank: count sigma_i > epsilon", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        compare = Text("SVD vs Eigendecomposition:\\n  Eigendecomposition: A = P D P^{-1}\\n  Only for square diagonalizable matrices\\n\\n  SVD: A = U Sigma V^T\\n  Works for ANY matrix (m x n)!\\n  U, V are orthogonal (not inverse of each other)\\n  Sigma has singular values (not eigenvalues)\\n\\n  SVD is more general and more numerically stable.", font_size=22, color=YELL).move_to(ORIGIN)
        cb = self._box(compare, border=YELL, buff=0.38)
        self.play(FadeIn(cb), Write(compare), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("SVD  A = U Sigma V^T\\n\\n  U: left singular vectors (output directions)\\n  Sigma: singular values (stretch factors)\\n  V^T: right singular vectors (input directions)\\n\\n  Works for ANY matrix (m x n)\\n  Singular values: sqrt(eigenvalues of A^T A)\\n\\n  Applications:\\n  PCA, compression, recommenders,\\n  least squares, noise reduction, NLP", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
NULL_SPACE = HEADER.format(title="Null Space") + TPLATE("NullSpaceScene") + '''
    def s1_hook(self):
        t = Text("Null Space", font_size=52, color=WHITE).move_to(UP*0.5)
        t2 = Text("What gets sent to zero?", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("A transformation crushes some information.\\nThe vectors it sends to zero —\\nthose are the ones it destroys.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("The null space (kernel) is the collection\\nof all vectors that A maps to zero: Av=0.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("null(A) = ker(A) = {x : Ax = 0}\\n\\nAlways a subspace (contains 0, closed under + and *)\\nDimension = nullity(A)\\n\\nRank-Nullity theorem: rank + nullity = n\\n(columns + null space = full input space)", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Null Space as Lost Information")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(-2,-1), color=RED, stroke_width=4, buff=0)
        line = Line(plane.c2p(-3,-1.5), plane.c2p(3,1.5), color=YELL, stroke_width=2)
        self.play(Create(line), Create(v1), Create(v2), run_time=2.0); self.wait(0.5)
        r1 = Text("A projection onto x-axis:\\nAll vectors on this line map to 0\\n(That line IS the null space)", font_size=22, color=YELL)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Null space of projection:\\n  All vectors perpendicular to x-axis\\n  = the y-axis\\nnullity = 1,  rank = 1,  1+1 = 2", font_size=22, color=GREEN)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=GREEN)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Finding the Null Space")
        method = Text("Algorithm: row reduce [A] -> RREF, set free variables\\n\\nExample: A = [[1,2,3],[2,4,6]]\\nRow reduce: [[1,2,3],[0,0,0]]\\nFree vars: x2, x3\\nx1 = -2*x2 - 3*x3\\n\\nnull(A) = span{(-2,1,0), (-3,0,1)}\\nnullity = 2", font_size=24, color=WHITE).move_to(UP*0.5)
        mb = self._box(method, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(method), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(mb), FadeOut(method), run_time=0.5)
        rank_null = Text("Rank-Nullity Theorem:\\n\\n  rank(A) + nullity(A) = n   (number of columns)\\n\\n  rank = dim(column space) = pivot columns\\n  nullity = dim(null space) = free variables\\n\\n  Full column rank -> nullity=0 -> Ax=0 has only x=0\\n  -> A is injective (one-to-one)", font_size=23, color=YELL).move_to(ORIGIN)
        rb = self._box(rank_null, border=YELL, buff=0.38)
        self.play(FadeIn(rb), Write(rank_null), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Null Space of [[2,4],[1,2]]")
        steps = [
            ("A = [[2,4],[1,2]]", WHITE, 2.5),
            ("Row reduce: R1/2 -> [[1,2],[1,2]]", BLUE, 1.7),
            ("R2 = R2-R1: -> [[1,2],[0,0]]", GREEN, 0.9),
            ("Pivot: x1. Free: x2 = t (parameter)", WHITE, 0.1),
            ("x1 + 2*x2 = 0  ->  x1 = -2t", YELL, -0.7),
            ("null(A) = span{(-2, 1)}", GREEN, -1.5),
            ("rank=1, nullity=1, 1+1=2=cols ✓", BLUE, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("The null space reveals invertibility:\\n\\n  null(A) = {0} only  <->  A is invertible\\n  (no information is destroyed)\\n\\n  Null space tells you solution structure:\\n  If Ax=b has one solution x0,\\n  ALL solutions are: x0 + null(A)\\n  (particular + homogeneous solutions)\\n\\n  Dimensions: null(A) = n - rank(A)\\n  Every dimension in null space = a 'destroyed' direction", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications:\\n\\n  Signal processing: null space of sensing matrix\\n  = signals that cannot be detected\\n  (blind spots of the system)\\n\\n  Control theory: null space of control matrix\\n  = motions that the controller cannot affect\\n\\n  Neural networks: null space of weight matrix\\n  = directions that produce zero activation", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Null Space  null(A) = {x : Ax = 0}\\n\\n  Always a subspace\\n  nullity = number of free variables\\n\\n  Rank-Nullity: rank + nullity = n\\n\\n  null={0}  <->  A invertible\\n  null={0}  <->  unique solution to Ax=b\\n\\n  Solution structure:\\n  Ax=b solutions = x_particular + null(A)\\n\\n  Reveals destroyed information", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
COL_SPACE = HEADER.format(title="Column Space") + TPLATE("ColumnSpaceScene") + '''
    def s1_hook(self):
        t = Text("Column Space", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("All reachable outputs of a matrix", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("For the transformation Ax, as x ranges\\nover all possible input vectors,\\nwhere can Ax land?", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("The set of all reachable outputs\\nis the column space of A.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("col(A) = {Ax : x in R^n} = span of columns of A\\n\\nAx = x1*col1 + x2*col2 + ... + xn*coln\\n(linear combination of columns!)\\n\\nAx=b has a solution iff b is in col(A).", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Column Space as Image")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        c1 = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=BLUE, stroke_width=5, buff=0)
        c2 = Arrow(plane.c2p(0,0), plane.c2p(-1,2), color=RED, stroke_width=5, buff=0)
        c1l = Text("col1=(2,1)", font_size=20, color=BLUE).next_to(plane.c2p(1,0.5), DOWN, buff=0.1)
        c2l = Text("col2=(-1,2)", font_size=20, color=RED).next_to(plane.c2p(-0.5,1), LEFT, buff=0.1)
        self.play(Create(c1), Create(c2), Write(c1l), Write(c2l), run_time=2.0); self.wait(0.5)
        r1 = Text("Two independent columns:\\ncol(A) = entire R^2\\n(rank 2 = full column rank)", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), FadeOut(c2), FadeOut(c2l), run_time=0.3)
        c2_dep = Arrow(plane.c2p(0,0), plane.c2p(4,2), color=RED, stroke_width=5, buff=0)
        line_col = Line(plane.c2p(-3,-1.5), plane.c2p(3,1.5), color=YELL, stroke_width=2)
        self.play(Create(c2_dep), Create(line_col), run_time=1.5); self.wait(0.3)
        r2 = Text("Parallel columns:\\ncol(A) = just a line\\n(rank 1, cannot reach off-line b)", font_size=22, color=RED)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Finding the Column Space")
        method = Text("col(A) = span of the PIVOT COLUMNS of A\\n(after row reduction, identify pivot columns,\\nthen take those ORIGINAL columns)\\n\\ndim(col(A)) = rank(A) = number of pivots\\n\\nNote: row operations change col(A)!\\nAlways go back to ORIGINAL columns.", font_size=24, color=WHITE).move_to(UP*0.8)
        mb = self._box(method, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(method), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(mb), FadeOut(method), run_time=0.5)
        key = Text("Fundamental relationships:\\n\\n  Ax = b solvable  iff  b in col(A)\\n  col(A) = image/range of A as transformation\\n  row(A) = col(A^T) = image of A^T\\n  null(A) perp to row(A)  (orthogonal complement!)\\n  col(A) perp to null(A^T)\\n\\nFour fundamental subspaces of A!", font_size=23, color=YELL).move_to(ORIGIN)
        kb = self._box(key, border=YELL, buff=0.38)
        self.play(FadeIn(kb), Write(key), run_time=2.5); self.wait(3.5)
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
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Four Fundamental Subspaces")
        ins = Text("Every m x n matrix A has four subspaces:\\n\\n  1. Column space col(A) in R^m   dim=rank\\n  2. Null space null(A) in R^n   dim=n-rank\\n  3. Row space row(A) in R^n     dim=rank\\n  4. Left null space null(A^T) in R^m  dim=m-rank\\n\\n  Orthogonal pairs:\\n  null(A) perp row(A)  (in R^n)\\n  null(A^T) perp col(A)  (in R^m)\\n\\nGilbert Strang: the four subspaces are\\nthe heart of linear algebra.", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications:\\n\\n  Least squares: project b onto col(A)\\n  -> normal equations: A^T A x = A^T b\\n  -> solution minimizes |Ax-b|\\n\\n  Dimensionality: col(A) tells output dimension\\n  null(A) tells lost dimensions\\n\\n  Image of transformation = col(A)\\n  Every ML model has a column space!", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Column Space  col(A)\\n\\n  = span of columns = all possible Ax\\n  = image/range of transformation\\n\\n  dim = rank(A) = number of pivots\\n\\n  Ax=b solvable iff b in col(A)\\n\\n  Four subspaces: col, null, row, left null\\n  Orthogonal pairs: null perp row, col perp left-null\\n\\n  Foundation of least squares", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
ROW_REDUCTION = HEADER.format(title="Row Reduction") + TPLATE("RowReductionScene") + '''
    def s1_hook(self):
        t = Text("Row Reduction", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Gaussian elimination step by step", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("How do you solve 3 equations with 3 unknowns?\\nEliminate one variable at a time.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Row reduction (Gaussian elimination)\\nsystematically simplifies any system of equations.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Three elementary row operations:\\n  1. Swap two rows\\n  2. Multiply a row by a non-zero scalar\\n  3. Add a multiple of one row to another\\n\\nThese preserve the solution set!\\nGoal: Reduced Row Echelon Form (RREF)", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
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
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.0)
    def s3_notation(self):
        sec_label(self, "RREF and Pivot Structure")
        rref = Text("Row Echelon Form (REF):\\n  Leading entry (pivot) in each row\\n  > all entries below it\\n  Rows of zeros at bottom\\n\\nReduced REF (RREF) - extra conditions:\\n  Each pivot = 1\\n  Each pivot is only nonzero in its column\\n\\nRREF is unique for any matrix!", font_size=24, color=WHITE).move_to(UP*0.8)
        rb = self._box(rref, border=BLUE, buff=0.38)
        self.play(FadeIn(rb), Write(rref), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(rb), FadeOut(rref), run_time=0.5)
        info = Text("What RREF reveals:\\n  Pivot columns -> linearly independent columns\\n  Free columns -> dependent, free variables\\n  Number of pivots = rank(A)\\n  Zero rows -> dimension of left null space\\n  RREF directly gives basis for null space!", font_size=23, color=YELL).move_to(ORIGIN)
        ib = self._box(info, border=YELL, buff=0.38)
        self.play(FadeIn(ib), Write(info), run_time=2.5); self.wait(3.5)
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
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Row reduction IS LU decomposition:\\n\\n  Each row operation = a shear matrix L_i\\n  A = L1 * L2 * ... * Lk * U\\n  -> A = L * U  (L lower triangular, U upper triangular)\\n\\n  LU decomposition is the practical algorithm\\n  for solving Ax=b (with pivoting: PLU)\\n\\n  Cost: O(n^3) operations\\n  Used in every numerical linear algebra solver!", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications of Gaussian elimination:\\n\\n  Circuit analysis (Kirchhoff laws -> linear system)\\n  Computer graphics (intersection of planes)\\n  Economics (input-output models: Leontief)\\n  Cryptography (solving modular linear systems)\\n  Finite element method (engineering simulation)\\n\\n  LAPACK/BLAS: optimized for modern CPUs\\n  NumPy solve, MATLAB \\\\: all use LU/QR internally", font_size=21, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Row Reduction (Gaussian Elimination)\\n\\n  Three operations: swap, scale, add multiple\\n  Preserve solution set\\n\\n  Goal: RREF (unique for any matrix)\\n  Pivots = independent columns = rank\\n  Free columns = null space directions\\n\\n  LU decomposition = row reduction stored\\n  Cost: O(n^3)\\n\\n  Solves Ax=b, finds rank, null space, basis", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
DET_ZERO = HEADER.format(title="Determinant = 0") + TPLATE("DetZeroScene") + '''
    def s1_hook(self):
        t = Text("When det = 0", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Singular matrices and collapsed dimensions", font_size=24, color=RED).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("A transformation flattens 3D space into a plane.\\nVolume: before = 1, after = 0.\\nThe determinant is exactly 0.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("det=0 means the transformation is SINGULAR:\\nit collapses the space into lower dimension.", font_size=26, color=RED).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("det(A) = 0 is equivalent to ALL of these:\\n  Columns are linearly dependent\\n  A is NOT invertible (singular)\\n  Ax=0 has non-trivial solutions\\n  null(A) != {0}  (non-trivial null space)\\n  A squashes space to lower dimension", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=RED, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Visualizing Collapse")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        col1 = Arrow(plane.c2p(0,0), plane.c2p(2,1), color=BLUE, stroke_width=5, buff=0)
        col2 = Arrow(plane.c2p(0,0), plane.c2p(-1,2), color=RED, stroke_width=5, buff=0)
        self.play(Create(col1), Create(col2), run_time=1.5); self.wait(0.5)
        r1 = Text("Independent columns:\\ndet = 2*2-1*(-1) = 5 != 0\\nUnit square -> 5x larger", font_size=22, color=GREEN)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=GREEN)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        col2_dep = Arrow(plane.c2p(0,0), plane.c2p(4,2), color=RED, stroke_width=5, buff=0)
        line = Line(plane.c2p(-3,-1.5), plane.c2p(3,1.5), color=YELL, stroke_width=2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        self.play(Transform(col2, col2_dep), Create(line), run_time=1.5); self.wait(0.3)
        r2 = Text("Dependent columns: (4,2) = 2*(2,1)\\ndet = 2*2-1*4 = 0\\nAll of R^2 -> collapses to 1 line!", font_size=22, color=RED)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=RED)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Why det=0 Matters")
        eq = Text("det(A) = 0  <->  A is SINGULAR", font_size=34, color=RED).move_to(UP*2.5)
        eb = self._box(eq, border=RED, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(1.0)
        chain = Text("Chain of equivalences (all the same!):\\n\\n  det(A)=0\\n  -> columns linearly dependent\\n  -> rank < n  (not full rank)\\n  -> null(A) != {0}  (free variable in Ax=0)\\n  -> A NOT invertible (no A^{-1})\\n  -> Ax=b may have 0 or inf solutions\\n  -> transformation squashes dimension", font_size=23, color=WHITE).next_to(eq, DOWN, buff=0.5)
        cb = self._box(chain, border=BLUE, buff=0.38)
        self.play(FadeIn(cb), Write(chain), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Examples of Singular Matrices")
        examples = [
            ("[[1,2],[2,4]] -> det=4-4=0 (row2=2*row1)", RED, 2.8),
            ("[[1,0,0],[0,1,0],[0,0,0]] -> det=0 (zero row)", RED, 2.0),
            ("[[a,b],[ka,kb]] -> det=ab*k-ab*k=0 (proportional rows)", RED, 1.2),
            ("Near-singular: [[1,1],[1,1.001]] -> det~0.001", YELL, 0.4),
            ("Ill-conditioned: sensitive to tiny changes!", YELL, -0.4),
            ("Condition number = sigma_max/sigma_min -> infinity", RED, -1.2),
            ("Numerically unstable near det=0!", RED, -2.0),
        ]
        for txt, col, yp in examples:
            mob = Text(txt, font_size=23, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Singular matrices are everywhere (and problematic):\\n\\n  Overfitting in ML: Gram matrix A^T A is singular\\n  -> regularization adds lambda*I to make invertible\\n\\n  Multicollinearity in regression:\\n  correlated features -> near-singular design matrix\\n  -> coefficients blow up!\\n\\n  Why pseudoinverse A+: handles singular A via SVD\\n  sigma_i > epsilon: keep. sigma_i <= epsilon: discard.\\n\\n  det=0 is a MEASURE-ZERO event (rare!) in practice", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=RED, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        geom = Text("Geometric insight:\\n\\ndet=0 means the unit hypercube gets flattened.\\n3D cube -> 2D plane -> area=0, volume=0.\\n\\nA matrix with det=0 cannot be inverted because\\nthe transformation is not reversible:\\nyou cannot unflatten what was flattened!\\n\\nThis is why det=0 is the boundary between\\ninvertible and non-invertible.", font_size=22, color=YELL).move_to(ORIGIN)
        gb = self._box(geom, border=YELL, buff=0.38)
        self.play(FadeIn(gb), Write(geom), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("det = 0: Singular Matrix\\n\\n  All equivalent:\\n  - Columns linearly dependent\\n  - Rank < n (not full rank)\\n  - Null space is non-trivial\\n  - Not invertible (no A^{-1})\\n\\n  Geometric: dimension collapses\\n  (area or volume -> zero)\\n\\n  Causes: multicollinearity, zero rows,\\n  proportional columns, repeated eigenvalue=0", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=RED, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
EIGEN_WHY = HEADER.format(title="Why Eigenvalues Matter") + TPLATE("EigenWhyScene") + '''
    def s1_hook(self):
        t = Text("Why Eigenvalues Matter", font_size=40, color=WHITE).move_to(UP*0.5)
        t2 = Text("The natural vibration frequencies of a matrix", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("A matrix acts on every vector differently.\\nAre there special vectors it only SCALES?\\n\\nA*v = lambda*v  (just scaling, no rotation!)", font_size=26, color=WHITE).move_to(UP*0.5)
        self.play(Write(q), run_time=2.5); self.wait(2.5)
        self.play(FadeOut(q), run_time=0.5)
        ans = Text("These special vectors = eigenvectors.\\nTheir scale factors = eigenvalues.\\n\\nThey reveal the SKELETON of any transformation.", font_size=26, color=GREEN).move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Eigenvectors Stay on Their Line")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.5)
        v1 = Arrow(plane.c2p(0,0), plane.c2p(2,0), color=BLUE, stroke_width=5, buff=0)
        v2 = Arrow(plane.c2p(0,0), plane.c2p(0,2), color=RED, stroke_width=5, buff=0)
        l1 = Text("eigenvector 1", font_size=18, color=BLUE).next_to(plane.c2p(1,0), UP, buff=0.1)
        l2 = Text("eigenvector 2", font_size=18, color=RED).next_to(plane.c2p(0,1), RIGHT, buff=0.1)
        self.play(Create(v1), Create(v2), Write(l1), Write(l2), run_time=2.0); self.wait(0.5)
        v1_scaled = Arrow(plane.c2p(0,0), plane.c2p(3,0), color=BLUE, stroke_width=5, buff=0)
        v2_scaled = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=RED, stroke_width=5, buff=0)
        r1 = Text("After matrix A acts:\\nv1 scaled by lambda1=1.5\\nv2 scaled by lambda2=0.5", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), Transform(v1, v1_scaled), Transform(v2, v2_scaled), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        r2 = Text("Only THESE directions stay on same line!\\nAll other vectors rotate AND scale.\\nEigenvectors = transformation invariant axes.", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Computing Eigenvalues")
        eq = Text("A*v = lambda*v\\n(A - lambda*I)*v = 0\\ndet(A - lambda*I) = 0  <- characteristic equation", font_size=26, color=YELL).move_to(UP*2.0)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.5); self.wait(1.5)
        procedure = Text("Procedure:\\n  1. Form (A - lambda*I)\\n  2. Set det = 0 -> characteristic polynomial\\n  3. Solve for lambda (eigenvalues)\\n  4. For each lambda: solve (A-lambda*I)v=0\\n     -> get eigenvectors", font_size=24, color=WHITE).next_to(eq, DOWN, buff=0.5)
        pb = self._box(procedure, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(procedure), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Why Eigenvalues Drive Everything")
        steps = [
            ("Matrix powers: A^n = P D^n P^{-1}", WHITE, 2.8),
            ("D^n: just raise each eigenvalue to n!", BLUE, 2.0),
            ("Population dynamics: next = A * current", WHITE, 1.2),
            ("Long-term behavior: largest eigenvalue wins", GREEN, 0.4),
            ("PageRank: dominant eigenvector of link matrix", YELL, -0.4),
            ("Stability: system stable iff all |lambda| < 1", RED, -1.2),
            ("Vibration frequencies: eigenvalues of stiffness matrix", WHITE, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Eigenvalues ARE the matrix (in the right coordinates):\\n\\n  Diagonalization: A = P D P^{-1}\\n  P = eigenvector matrix\\n  D = diagonal of eigenvalues\\n\\n  In eigenbasis: A is purely diagonal!\\n  Each direction scaled independently.\\n  This is why eigenvectors are called\\n  the natural coordinates of A.", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications everywhere:\\n\\n  PCA: eigenvectors of covariance matrix\\n  = principal components (max variance directions)\\n\\n  Quantum mechanics: energy levels = eigenvalues\\n  of Hamiltonian operator\\n\\n  Google PageRank: dominant eigenvector\\n  of web graph transition matrix\\n\\n  Facial recognition, compression, simulation", font_size=22, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Why Eigenvalues Matter\\n\\n  Av = lambda*v  (scaling only, no rotation!)\\n  Solve: det(A - lambda*I) = 0\\n\\n  Eigenvalues = natural scaling factors\\n  Eigenvectors = invariant directions\\n\\n  Diagonalization: A = P D P^{-1}\\n  In eigenbasis: trivial computation!\\n\\n  Powers, stability, PageRank, PCA,\\n  quantum states, vibration modes", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
MAXWELL = HEADER.format(title="Maxwell Equations") + TPLATE("MaxwellScene") + '''
    def s1_hook(self):
        t = Text("Maxwell Equations", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("The laws governing all electromagnetic phenomena", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Light, radio, WiFi, MRI, electric motors.\\nAll governed by four elegant equations\\nwritten down by James Clerk Maxwell in 1865.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Maxwell unified electricity, magnetism, and optics.\\nHe showed light IS an electromagnetic wave.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("4 equations. Complete theory of electromagnetism.\\n\\nGauss (E), Gauss (B), Faraday, Ampere-Maxwell.\\nIn vacuum: wave solutions traveling at c = 1/sqrt(eps_0 mu_0)\\nThis equals the measured speed of light!", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "The Four Laws")
        eqs = [
            ("1. Gauss's Law (E field):", WHITE, 2.5),
            ("   div(E) = rho/epsilon_0", BLUE, 1.7),
            ("   Electric field diverges from charges", BLUE, 1.1),
            ("2. Gauss's Law (B field):", WHITE, 0.3),
            ("   div(B) = 0", RED, -0.5),
            ("   No magnetic monopoles!", RED, -1.1),
        ]
        for txt, col, yp in eqs:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(0.8)
        self.wait(2.5)
    def s3_notation(self):
        sec_label(self, "Faraday and Ampere")
        eqs2 = [
            ("3. Faraday's Law:", WHITE, 2.5),
            ("   curl(E) = -dB/dt", YELL, 1.7),
            ("   Changing B creates E field (motors!)", YELL, 1.1),
            ("4. Ampere-Maxwell Law:", WHITE, 0.3),
            ("   curl(B) = mu_0 J + mu_0 eps_0 dE/dt", GREEN, -0.5),
            ("   Current OR changing E creates B field", GREEN, -1.1),
            ("Maxwell added the dE/dt term! -> wave eq.", BLUE, -1.9),
        ]
        for txt, col, yp in eqs2:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(0.8)
        self.wait(2.5)
    def s4_example(self):
        sec_label(self, "Wave Speed = Speed of Light")
        steps = [
            ("Combine Faraday + Ampere in vacuum:", WHITE, 2.8),
            ("curl(curl(E)) = -mu_0 eps_0 d^2E/dt^2", WHITE, 2.0),
            ("Wave equation: d^2E/dx^2 = (1/c^2) d^2E/dt^2", YELL, 1.2),
            ("c = 1/sqrt(mu_0 * eps_0)", YELL, 0.4),
            ("mu_0 = 4pi*10^-7,  eps_0 = 8.85*10^-12", BLUE, -0.4),
            ("c = 299,792,458 m/s", GREEN, -1.2),
            ("= measured speed of light! Light IS EM wave!", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Maxwell equations are relativistically covariant.\\n\\nEinstein noticed: if light travels at c for all observers,\\ntime and space must mix -> special relativity.\\n\\nMaxwell's equations are the same for all inertial frames!\\n(Unlike Newton's laws -- they had to be fixed.)\\n\\nFour equations in differential form:\\n  2 div equations (sources)\\n  2 curl equations (dynamics)\\nAll of electromagnetism from these 4!", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications of Maxwell equations:\\n\\n  Antenna design: electromagnetic waves\\n  Optical fiber: total internal reflection\\n  MRI machines: magnetic resonance\\n  Electric motors: Faraday induction\\n  Wireless communication: all EM waves\\n  Laser technology: stimulated emission\\n  GPS: needs relativistic EM corrections\\n\\nEvery electronic device uses Maxwell implicitly!", font_size=21, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Maxwell Equations\\n\\n  1. div(E) = rho/eps_0  (electric sources)\\n  2. div(B) = 0  (no magnetic monopoles)\\n  3. curl(E) = -dB/dt  (Faraday)\\n  4. curl(B) = mu_0 J + mu_0 eps_0 dE/dt  (Ampere)\\n\\n  Predict EM waves: c = 1/sqrt(mu_0 eps_0)\\n  = measured speed of light\\n\\n  Complete theory of light, electricity, magnetism\\n  Foundation of all modern technology", font_size=18, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ─────────────────────────────────────────────────────────────────────────────
INDUCTION = HEADER.format(title="Electromagnetic Induction") + TPLATE("InductionScene") + '''
    def s1_hook(self):
        t = Text("Electromagnetic Induction", font_size=40, color=WHITE).move_to(UP*0.5)
        t2 = Text("Faraday discovery that powers the world", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Move a magnet through a coil of wire.\\nA current appears from nothing!\\nNo battery. No connection to power.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Faraday discovered this in 1831.\\nChanging magnetic flux INDUCES a voltage.\\nThis powers every generator on Earth.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(1.5)
        self.play(Write(ans), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Faraday Law: EMF = -d(Phi_B)/dt\\n\\n  EMF = induced voltage (electromotive force)\\n  Phi_B = magnetic flux through the loop\\n       = B dot A = B*A*cos(theta)\\n\\nThe minus sign: Lenz law (opposes the change)", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)
    def s2_geometry(self):
        sec_label(self, "Magnetic Flux and Induction")
        ax = self._axes(xr=(-0.3,6,1), yr=(-0.3,4,1))
        t = ValueTracker(0)
        B_curve = ax.plot(lambda x: 2*np.sin(x), x_range=[0,5.5], color=BLUE, stroke_width=3)
        self.play(Create(ax), run_time=1.5)
        self.play(Create(B_curve), run_time=2.0); self.wait(0.5)
        r1 = Text("B(t) = B0 sin(t)  (alternating B field)", font_size=22, color=BLUE)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(1.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        emf_curve = ax.plot(lambda x: -2*np.cos(x), x_range=[0,5.5], color=YELL, stroke_width=3)
        self.play(Create(emf_curve), run_time=2.0); self.wait(0.5)
        r2 = Text("EMF = -dB/dt = -B0 cos(t)\\n90 degree phase shift!", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(3.0)
    def s3_notation(self):
        sec_label(self, "Faraday Law and Lenz Law")
        faraday = Text("Faraday's Law:\\n  EMF = -N * d(Phi_B)/dt\\n  N = number of turns in coil\\n  Phi_B = integral(B . dA)  over surface\\n\\nLenz Law (explains the minus sign):\\n  Induced current opposes the change!\\n  (Nature resists change to flux)", font_size=24, color=WHITE).move_to(UP*0.8)
        fb = self._box(faraday, border=BLUE, buff=0.38)
        self.play(FadeIn(fb), Write(faraday), run_time=2.5); self.wait(2.0)
        self.play(FadeOut(fb), FadeOut(faraday), run_time=0.5)
        maxwell3 = Text("Maxwell 3rd equation:\\n  curl(E) = -dB/dt\\n\\nThis IS Faraday law in differential form!\\nChanging B creates circulating E field\\n(even without a wire -- the field exists in space)\\n\\nWith wire: circulating E drives current = induction.", font_size=23, color=YELL).move_to(ORIGIN)
        mb = self._box(maxwell3, border=YELL, buff=0.38)
        self.play(FadeIn(mb), Write(maxwell3), run_time=2.5); self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Example: Generator Calculation")
        steps = [
            ("Coil: N=100 turns, area A=0.01 m^2", WHITE, 2.8),
            ("B rotates: B(t) = 1.0 * sin(120*pi*t)  [60 Hz]", BLUE, 2.0),
            ("Phi_B = N*A*B = 100*0.01*sin(120*pi*t)", WHITE, 1.2),
            ("Phi_B = sin(120*pi*t) Wb (Weber)", WHITE, 0.4),
            ("EMF = -d(Phi_B)/dt = -120*pi*cos(120*pi*t)", YELL, -0.4),
            ("Peak EMF = 120*pi ~ 377 V", GREEN, -1.2),
            ("This is how AC power plants generate 60 Hz!", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(1.2)
        self.wait(2.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Induction is the bridge between electricity and magnetism:\\n\\n  Faraday (1831): moving magnet -> current\\n  Ampere: current -> magnetic field\\n  Together: electricity and magnetism are coupled!\\n\\n  Maxwell added dE/dt term to Ampere law,\\n  creating displacement current.\\n  Result: self-sustaining EM waves -> light!\\n\\n  Faraday and Maxwell together = electromagnetic theory", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications of electromagnetic induction:\\n\\n  Generators: rotating coil in B field -> AC power\\n  Transformers: change voltage/current (power grid)\\n  Electric motors: reverse of generator\\n  Wireless charging: inductive charging (Qi)\\n  MRI: NMR uses Faraday induction\\n  Metal detectors: eddy current induction\\n  Guitar pickup: vibrating string inductance\\n  RFID cards: inductive coupling", font_size=21, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Electromagnetic Induction\\n\\n  EMF = -N * d(Phi_B)/dt  (Faraday)\\n  Phi_B = B * A * cos(theta)\\n\\n  Lenz law: opposes the change (minus sign)\\n\\n  Maxwell 3: curl(E) = -dB/dt\\n  (field form of Faraday law)\\n\\n  Applications:\\n  Generators, transformers, motors,\\n  wireless charging, MRI, RFID\\n\\n  Powers all electrical civilization", font_size=18, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# ── Write all files ──────────────────────────────────────────────────────────
scenes = {
    'limit.py': LIMIT,
    'la_02_vector_add.py': VECTOR_ADD,
    'la_04_dot_product.py': DOT_PRODUCT,
    'la_05_cross_product.py': CROSS_PRODUCT,
    'la_09_shear.py': SHEAR,
    'la_10_projection.py': PROJECTION,
    'la_12_span.py': SPAN,
    'la_13_lin_indep.py': LIN_INDEP,
    'la_14_basis.py': BASIS,
    'la_15_change_of_basis.py': CHANGE_BASIS,
    'la_17_svd.py': SVD,
    'la_18_null_space.py': NULL_SPACE,
    'la_19_column_space.py': COL_SPACE,
    'la_20_row_reduction.py': ROW_REDUCTION,
    'la_22_det_zero.py': DET_ZERO,
    'la_23_eigen_why.py': EIGEN_WHY,
    'phys_04_maxwell.py': MAXWELL,
    'phys_03_induction.py': INDUCTION,
}

for fname, content in scenes.items():
    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {fname}: {len(content):,} bytes")

print(f"\nDone. Wrote {len(scenes)} scene files.")
