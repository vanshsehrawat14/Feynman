"""
Feynman – The Integral (Gold Standard)
6-section narrative, 3-5 minutes. Text/Cairo only, no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

AX_COLOR = "#888888"

class IntegralScene(Scene):
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
        t1 = Text("The Integral", font_size=52, color=WHITE)
        t2 = Text("Accumulation and Area", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        q1 = Text("Water flows into a tank at varying speed.", font_size=28, color=WHITE)
        q2 = Text("How much water is in the tank after 5 min?", font_size=28, color=YELL)
        q3 = Text("The integral adds it all up.", font_size=28, color=GREEN)
        q1.move_to(UP * 1.5); q2.next_to(q1, DOWN, buff=0.5); q3.next_to(q2, DOWN, buff=0.5)
        self.play(Write(q1), run_time=2.0); self.wait(0.8)
        self.play(Write(q2), run_time=1.5); self.wait(0.8)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5)
        intro = Text(
            "An integral is an infinite sum.\n\n"
            "Split the area into infinitely thin slices,\n"
            "add up all their areas.\n"
            "That sum IS the integral.", font_size=28, color=WHITE)
        intro.move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(3.5)

    def s2_geometry(self):
        sec_label(self, "Riemann Sums to Exact Area")
        axes = Axes(x_range=[-0.3,4,1], y_range=[-0.2,6.5,1], x_length=8.0, y_length=5.0,
            axis_config={"color": AX_COLOR, "stroke_width": 2, "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 0.5 + DOWN * 0.5)
        f = lambda x: 0.4*x**2 + 0.5
        curve = axes.plot(f, x_range=[0.0,3.8], color=BLUE, stroke_width=3.5)
        self.play(Create(axes), run_time=2.0); self.wait(0.3)
        self.play(Create(curve), run_time=2.0); self.wait(0.5)
        a, b = 0.3, 3.5

        def make_rects(n):
            dx = (b-a)/n; rs = VGroup()
            for i in range(n):
                xi = a + i*dx; h = f(xi + dx/2)
                p = axes.c2p(xi, 0); p2 = axes.c2p(xi+dx, h)
                rect = Rectangle(width=abs(p2[0]-p[0]), height=abs(p2[1]-p[1]),
                    color=BLUE, fill_color=BLUE, fill_opacity=0.35, stroke_width=1)
                rect.move_to([(p[0]+p2[0])/2, (p[1]+p2[1])/2, 0])
                rs.add(rect)
            return rs

        for n, col, desc in [(4, YELL, "n=4: rough"), (12, GREEN, "n=12: better"), (40, BLUE, "n=40: close")]:
            rects = make_rects(n)
            r = Text(desc, font_size=24, color=col).move_to(RIGHT * 4.0 + UP * 2.5)
            b_r = self._box(r, border=col)
            self.play(FadeIn(b_r), Write(r), FadeIn(rects), run_time=2.0); self.wait(2.0)
            self.play(FadeOut(b_r), FadeOut(r), FadeOut(rects), run_time=0.4)

        region = axes.get_area(curve, x_range=[a,b], color=BLUE, opacity=0.45)
        r4 = Text("n -> infinity\n= exact integral", font_size=24, color=WHITE).move_to(RIGHT * 4.0 + UP * 2.0)
        b4 = self._box(r4)
        self.play(FadeIn(b4), Write(r4), FadeIn(region), run_time=2.0); self.wait(3.5)

    def s3_notation(self):
        sec_label(self, "Integral Notation")
        eq = Text("integral from a to b of  f(x) dx", font_size=34, color=YELL)
        eq.move_to(UP * 2.8)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(1.0)
        parts = [
            ("integral  =  the S symbol (Sum)", BLUE),
            ("a, b      =  limits of integration", GREEN),
            ("f(x)      =  height of each slice", WHITE),
            ("dx        =  infinitely thin slice width", YELL),
        ]
        y = 1.5; boxes = []
        for txt, col in parts:
            mob = Text(txt, font_size=26, color=col).move_to(UP * y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.2)
            boxes.append((b, mob)); y -= 0.9
        self.wait(1.0)
        self.play(*[FadeOut(b) for b,_ in boxes], *[FadeOut(m) for _,m in boxes],
                  FadeOut(eb), FadeOut(eq), run_time=0.5)
        ftc = Text(
            "Fundamental Theorem of Calculus:\n\n"
            "  integral(a,b) f(x) dx  =  F(b) - F(a)\n\n"
            "  where F is the ANTIDERIVATIVE: F prime = f\n\n"
            "  Integration and differentiation are\n"
            "  inverse operations!", font_size=25, color=WHITE)
        ftc.move_to(ORIGIN)
        fb = self._box(ftc, border=GREEN, buff=0.38)
        self.play(FadeIn(fb), Write(ftc), run_time=2.5); self.wait(3.5)
        self.play(FadeOut(fb), FadeOut(ftc), run_time=0.5)
        rules = Text(
            "Integration rules:\n\n"
            "  integral(x^n dx) = x^(n+1)/(n+1) + C\n"
            "  integral(cos x dx) = sin(x) + C\n"
            "  integral(e^x dx) = e^x + C\n"
            "  integral(1/x dx) = ln|x| + C\n"
            "  integral(c dx) = cx + C",
            font_size=25, color=BLUE)
        rules.move_to(ORIGIN)
        rb = self._box(rules, border=BLUE, buff=0.38)
        self.play(FadeIn(rb), Write(rules), run_time=2.0); self.wait(3.5)

    def s4_example(self):
        sec_label(self, "Worked Example: integral(0 to 2) x^2 dx")
        axes = Axes(x_range=[-0.3,4,1], y_range=[-0.2,6.5,1], x_length=8.0, y_length=5.0,
            axis_config={"color": AX_COLOR, "stroke_width": 2, "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 0.5 + DOWN * 0.5)
        f = lambda x: x**2
        curve = axes.plot(f, x_range=[0.0,3.5], color=BLUE, stroke_width=3.5)
        region = axes.get_area(curve, x_range=[0,2], color=BLUE, opacity=0.4)
        self.play(Create(axes), Create(curve), run_time=2.0)
        self.play(FadeIn(region)); self.wait(0.5)
        steps = [
            ("integral(0 to 2) x^2 dx", WHITE, 2.5),
            ("Antiderivative of x^2 = x^3/3", BLUE, 1.6),
            ("= [x^3/3] from 0 to 2", WHITE, 0.7),
            ("= 2^3/3 - 0^3/3", WHITE, -0.2),
            ("= 8/3 - 0 = 8/3", YELL, -1.1),
            ("~ 2.667 square units", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=26, color=col).move_to(LEFT * 2.0 + UP * yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.2)
        self.wait(2.5)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Integrals appear everywhere:\n\n"
            "  Physics: Work = integral(F dx)\n"
            "           Charge = integral(I dt)\n"
            "           Center of mass = integral(x dm / M)\n\n"
            "  Probability: P(a<X<b) = integral(a,b) f(x) dx\n"
            "  Statistics: Expected value = integral(x f(x) dx)\n\n"
            "  ML: KL divergence, VAE loss, Fourier features\n"
            "  Engineering: signal processing, control theory\n\n"
            "  Anything that accumulates over time or space.",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        acc = Text(
            "The fundamental duality:\n\n"
            "  DERIVATIVE = rate of change (instantaneous)\n"
            "  INTEGRAL   = accumulated change (total)\n\n"
            "  FTC Part 1: d/dx integral(a,x) f(t) dt = f(x)\n"
            "  FTC Part 2: integral(a,b) f(x)dx = F(b)-F(a)\n\n"
            "  They are INVERSES of each other.\n"
            "  The two pillars of calculus.",
            font_size=23, color=YELL)
        acc.move_to(ORIGIN)
        ab = self._box(acc, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(acc), run_time=2.5); self.wait(4.0)

    def s6_summary(self):
        sec_label(self, "Summary")
        axes = Axes(x_range=[-0.3,4,1], y_range=[-0.2,6.5,1], x_length=8.0, y_length=5.0,
            axis_config={"color": AX_COLOR, "stroke_width": 2, "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 0.5 + DOWN * 0.5)
        f = lambda x: 0.4*x**2 + 0.5
        curve = axes.plot(f, x_range=[0.0,3.8], color=BLUE, stroke_width=3.5)
        region = axes.get_area(curve, x_range=[0.3,3.5], color=BLUE, opacity=0.45)
        self.play(Create(axes), Create(curve), FadeIn(region), run_time=2.0); self.wait(0.5)
        sm = Text(
            "The Integral\n\n"
            "  Area under f from a to b\n\n"
            "  = limit of Riemann sums as n -> infinity\n\n"
            "  Computed via antiderivative:\n"
            "  F(b) - F(a)  where F prime = f\n\n"
            "  Derivative and integral are inverses\n"
            "  (Fundamental Theorem of Calculus)\n\n"
            "  The language of accumulation",
            font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
