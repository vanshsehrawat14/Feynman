"""Feynman – Limits (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class LimitScene(Scene):
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
        ans = Text("A limit describes where a function is HEADING,\nnot where it is.\n\nThis distinction unlocks all of calculus.", font_size=27, color=WHITE).move_to(ORIGIN)
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
        r2 = Text("Hole at x=0\n(0/0 undefined)", font_size=22, color=RED)
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
        rules = Text("Limit laws:\n\n  lim(f+g) = lim f + lim g\n  lim(f*g) = lim f * lim g\n  lim(f/g) = lim f / lim g  (if lim g != 0)\n  lim(c*f) = c * lim f\n\nOne-sided limits:\n  lim from right (x->c+) and left (x->c-)\n  Limit exists iff both sides equal L.", font_size=22, color=WHITE).move_to(ORIGIN)
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
        ins = Text("Limits are the foundation of calculus:\n\n  Derivative = limit of difference quotient\n    f'(x) = lim(h->0) [f(x+h)-f(x)] / h\n\n  Integral = limit of Riemann sums\n    area = lim(n->inf) sum of n rectangles\n\n  Continuity = lim(x->c) f(x) = f(c)\n\n  Without limits, calculus does not exist.", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        eps = Text("Epsilon-delta definition (rigorous):\n\n  lim(x->c) f(x) = L means:\n  For every epsilon > 0,\n  there exists delta > 0 such that:\n  if 0 < |x-c| < delta  then  |f(x)-L| < epsilon\n\n  This is the formal foundation\n  that makes analysis rigorous.", font_size=22, color=YELL).move_to(ORIGIN)
        eb = self._box(eps, border=YELL, buff=0.38)
        self.play(FadeIn(eb), Write(eps), run_time=2.5); self.wait(4.0)
    def s6_summary(self):
        sec_label(self, "Summary")
        ax = self._axes(xr=(-0.3,5,1), yr=(-0.3,2.5,0.5))
        f = lambda x: np.sin(x)/x if abs(x) > 0.001 else 1.0
        curve = ax.plot(f, x_range=[0.05, 4.8], color=BLUE, stroke_width=3.5)
        hole = Circle(radius=0.1, color=RED, fill_color=BG, fill_opacity=1, stroke_width=2).move_to(ax.c2p(0,1))
        self.play(Create(ax), Create(curve), Create(hole), run_time=2.0); self.wait(0.5)
        sm = Text("Limits\n\n  lim(x->c) f(x) = L\n\n  Direction of approach matters\n  Function value at c does not\n\n  Powers calculus:\n  Derivatives, integrals, continuity\n\n  Epsilon-delta: the rigorous definition\n  The language of infinitesimals", font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
