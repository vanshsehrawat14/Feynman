"""
Feynman – Chain Rule (Gold Standard)
6-section narrative, 3–5 minutes.
Uses Text/Cairo only — no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

CURVE_COLOR = BLUE
INNER_COLOR = GREEN
AX_COLOR    = "#888888"


def _mk_axes():
    return Axes(
        x_range=[-3.5, 3.5, 1], y_range=[-1.5, 10.5, 2],
        x_length=8.5, y_length=5.0,
        axis_config={"color": AX_COLOR, "stroke_width": 2,
                     "include_tip": True, "tip_width": 0.15,
                     "tip_height": 0.2, "include_ticks": True},
    ).shift(LEFT * 0.5 + DOWN * 0.4)


class ChainRuleScene(Scene):
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
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)
        self.wait(0.3)

    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)

    def _rp(self, mob, y=0.0, x=4.2):
        mob.move_to(RIGHT * x + UP * y)
        return mob

    def s1_hook(self):
        t1 = Text("The Chain Rule", font_size=52, color=WHITE)
        t2 = Text("Differentiating Compositions", font_size=24, color=CURVE_COLOR)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("How do you differentiate sin(x^2)?", font_size=34, color=WHITE)
        q2 = Text("Or (3x + 5)^100?", font_size=34, color=WHITE)
        q3 = Text("These are functions inside functions.", font_size=30, color=YELL)
        q1.move_to(UP * 1.5); q2.next_to(q1, DOWN, buff=0.45); q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        ans = Text(
            "The chain rule tells us:\n\n"
            "d/dx f(g(x))  =  f'(g(x))  times  g'(x)\n\n"
            "Derivative of outer times derivative of inner.",
            font_size=26, color=WHITE,
        )
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=CURVE_COLOR, buff=0.35)
        self.play(FadeIn(ab), Write(ans), run_time=1.5); self.wait(2.5)

    def s2_geometry(self):
        sec_label(self, "Intuition: Gears and Rates")

        r1 = Text(
            "Think of two gears:\n\n"
            "x --> g(x) --> f(g(x))\n\n"
            "x changes by dx\n"
            "g changes by g'(x) * dx\n"
            "f then changes by f'(g(x)) * g'(x) * dx\n\n"
            "The rates MULTIPLY along the chain.",
            font_size=26, color=WHITE,
        )
        r1.move_to(LEFT * 1.5)
        b1 = self._box(r1, border=WHITE, buff=0.32)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.5); self.wait(0.3)

        axes = _mk_axes()
        g = lambda x: x ** 2          # inner function
        f_of_g = lambda x: np.sin(x ** 2)  # outer composed

        curve_g = axes.plot(g, x_range=[-3.0, 3.0], color=INNER_COLOR, stroke_width=3.5)
        curve_fg = axes.plot(f_of_g, x_range=[-3.0, 3.0], color=CURVE_COLOR, stroke_width=3.5)

        self.play(Create(axes), run_time=1.2); self.wait(0.3)

        r_g = Text("g(x) = x^2  (inner)", font_size=22, color=GREEN)
        self._rp(r_g, y=2.5)
        bg = self._box(r_g, border=GREEN)
        self.play(FadeIn(bg), Write(r_g), Create(curve_g), run_time=1.5); self.wait(1)

        self.play(FadeOut(bg), FadeOut(r_g), FadeOut(curve_g), run_time=0.3)
        r_fg = Text("f(g(x)) = sin(x^2)  (composed)", font_size=22, color=BLUE)
        self._rp(r_fg, y=2.5)
        bfg = self._box(r_fg, border=BLUE)
        self.play(FadeIn(bfg), Write(r_fg), Create(curve_fg), run_time=1.5); self.wait(1.5)

        x_t = ValueTracker(-2.5)

        def tan_fg():
            xv = x_t.get_value()
            dg = 2 * xv                              # g'(x)
            df = np.cos(xv ** 2)                     # f'(g(x))
            m  = df * dg                             # chain rule slope
            yv = np.sin(xv ** 2)
            norm = np.linalg.norm([1, m])
            if norm < 0.05:
                return VMobject()
            return Line(
                axes.c2p(xv - 0.8, yv + m * (-0.8)),
                axes.c2p(xv + 0.8, yv + m * 0.8),
                color=YELL, stroke_width=3.5,
            )

        def tan_dot():
            xv = x_t.get_value()
            return Dot(axes.c2p(xv, np.sin(xv ** 2)), color=YELL, radius=0.1)

        sw_t = always_redraw(tan_fg)
        sw_d = always_redraw(tan_dot)
        self.play(Create(sw_t), Create(sw_d))

        r_sweep = Text("Chain rule slope:\nf'(g(x)) * g'(x)", font_size=22, color=YELL)
        self._rp(r_sweep, y=1.2)
        bs = self._box(r_sweep, border=YELL)
        self.play(FadeIn(bs), Write(r_sweep))
        self.play(x_t.animate.set_value(2.5), run_time=5, rate_func=smooth); self.wait(2)

    def s3_notation(self):
        sec_label(self, "The Chain Rule Formula")

        chain = Text(
            "d/dx f(g(x))  =  f'(g(x)) * g'(x)",
            font_size=36, color=YELL,
        )
        chain.move_to(UP * 2.2)
        cb = self._box(chain, border=YELL, buff=0.4)
        self.play(FadeIn(cb), Write(chain), run_time=2); self.wait(1)

        leibniz = Text(
            "Leibniz notation:\n\n"
            "dy/dx  =  dy/du  *  du/dx\n\n"
            "where u = g(x) and y = f(u)\n\n"
            "The du's 'cancel' intuitively.",
            font_size=26, color=WHITE,
        )
        leibniz.move_to(UP * 0.3)
        lb = self._box(leibniz, border=WHITE, buff=0.35)
        self.play(FadeIn(lb), Write(leibniz), run_time=1.5); self.wait(3)
        self.play(FadeOut(lb), FadeOut(leibniz), FadeOut(cb), FadeOut(chain), run_time=0.5)
        self.wait(0.3)

        common = Text(
            "Common applications:\n\n"
            "  d/dx sin(x^2) = cos(x^2) * 2x\n\n"
            "  d/dx e^(3x) = e^(3x) * 3\n\n"
            "  d/dx (x^2+1)^5 = 5(x^2+1)^4 * 2x\n\n"
            "  d/dx sqrt(x^2+1) = x / sqrt(x^2+1)",
            font_size=25, color=BLUE,
        )
        common.move_to(ORIGIN)
        combb = self._box(common, border=BLUE, buff=0.38)
        self.play(FadeIn(combb), Write(common), run_time=2); self.wait(3.5)

    def s4_example(self):
        sec_label(self, "Worked Examples")

        def L(y): return LEFT * 1.5 + UP * y

        # Example 1
        ex1h = Text("Find d/dx sin(x^2)", font_size=28, color=WHITE)
        ex1h.move_to(L(2.8))
        b1h = self._box(ex1h, border=WHITE)
        self.play(FadeIn(b1h), Write(ex1h)); self.wait(0.4)

        steps1 = [
            ("Outer: f(u) = sin(u)  => f'(u) = cos(u)", BLUE),
            ("Inner: g(x) = x^2     => g'(x) = 2x", GREEN),
            ("Chain: cos(x^2) * 2x", YELL),
        ]
        y1 = 1.8
        s1boxes = []
        for s, c in steps1:
            mob = Text(s, font_size=24, color=c).move_to(L(y1))
            b = self._box(mob, border=c)
            self.play(FadeIn(b), Write(mob)); self.wait(0.6)
            s1boxes.append((b, mob)); y1 -= 0.9

        self.wait(1)
        self.play(*[FadeOut(b) for b, _ in s1boxes], *[FadeOut(m) for _, m in s1boxes],
                  FadeOut(b1h), FadeOut(ex1h), run_time=0.5); self.wait(0.3)

        # Example 2
        ex2h = Text("Find d/dx (3x+5)^4", font_size=28, color=WHITE)
        ex2h.move_to(L(2.8))
        b2h = self._box(ex2h, border=WHITE)
        self.play(FadeIn(b2h), Write(ex2h)); self.wait(0.4)

        steps2 = [
            ("Outer: f(u) = u^4  =>  f'(u) = 4u^3", BLUE),
            ("Inner: g(x) = 3x+5  =>  g'(x) = 3", GREEN),
            ("Chain: 4(3x+5)^3 * 3 = 12(3x+5)^3", YELL),
        ]
        y2 = 1.8
        s2boxes = []
        for s, c in steps2:
            mob = Text(s, font_size=24, color=c).move_to(L(y2))
            b = self._box(mob, border=c)
            self.play(FadeIn(b), Write(mob)); self.wait(0.6)
            s2boxes.append((b, mob)); y2 -= 0.9

        self.wait(1)
        self.play(*[FadeOut(b) for b, _ in s2boxes], *[FadeOut(m) for _, m in s2boxes],
                  FadeOut(b2h), FadeOut(ex2h), run_time=0.5); self.wait(0.3)

        # Nested chain rule
        ex3h = Text("Find d/dx sin(cos(x^2))", font_size=28, color=WHITE)
        ex3h.move_to(L(2.8))
        b3h = self._box(ex3h, border=WHITE)
        self.play(FadeIn(b3h), Write(ex3h)); self.wait(0.4)

        steps3 = [
            ("3 layers: outer sin, middle cos, inner x^2", WHITE),
            ("Outer: cos(cos(x^2))", BLUE),
            ("Middle: -sin(x^2) * 2x", GREEN),
            ("Result: -cos(cos(x^2)) * sin(x^2) * 2x", YELL),
        ]
        y3 = 1.8
        for s, c in steps3:
            mob = Text(s, font_size=22, color=c).move_to(L(y3))
            b = self._box(mob, border=c)
            self.play(FadeIn(b), Write(mob)); self.wait(0.7)
            y3 -= 0.95

        self.wait(2)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")

        ins = Text(
            "The chain rule is everywhere:\n\n"
            "  Machine Learning:\n"
            "    Backpropagation IS the chain rule\n"
            "    dL/dw = dL/da * da/dz * dz/dw\n\n"
            "  Physics:\n"
            "    Speed of shadow: dx_shadow/dt\n"
            "    = dx_shadow/dx_object * dx_object/dt\n\n"
            "  Thermodynamics:\n"
            "    dP/dT = dP/dV * dV/dT\n\n"
            "  Computer Graphics:\n"
            "    Transform derivatives for animation",
            font_size=22, color=WHITE,
        )
        ins.move_to(LEFT * 1.0)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=2); self.wait(4)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5); self.wait(0.3)

        backprop = Text(
            "Backpropagation (neural networks):\n\n"
            "Loss L depends on output y\n"
            "y depends on hidden z\n"
            "z depends on weights w\n\n"
            "dL/dw = dL/dy * dy/dz * dz/dw\n\n"
            "This is just the chain rule, 3 layers deep.",
            font_size=23, color=YELL,
        )
        backprop.move_to(ORIGIN)
        bpb = self._box(backprop, border=YELL, buff=0.35)
        self.play(FadeIn(bpb), Write(backprop), run_time=1.5); self.wait(4)

    def s6_summary(self):
        sec_label(self, "Summary")

        axes = _mk_axes()
        f_of_g = lambda x: np.sin(x ** 2)
        curve_fg = axes.plot(f_of_g, x_range=[-3.0, 3.0], color=CURVE_COLOR, stroke_width=3.5)
        x_t = ValueTracker(-2.5)

        def tan_line():
            xv = x_t.get_value()
            m  = np.cos(xv ** 2) * 2 * xv
            yv = np.sin(xv ** 2)
            norm = abs(m)
            if norm > 20:
                return VMobject()
            return Line(
                axes.c2p(xv - 0.7, yv + m * (-0.7)),
                axes.c2p(xv + 0.7, yv + m * 0.7),
                color=YELL, stroke_width=3.5,
            )

        sw = always_redraw(tan_line)
        sd = always_redraw(lambda: Dot(axes.c2p(x_t.get_value(), f_of_g(x_t.get_value())), color=YELL, radius=0.1))
        self.play(Create(axes), Create(curve_fg), Create(sw), Create(sd), run_time=1.5)

        sm = Text(
            "The Chain Rule\n\n"
            "  d/dx f(g(x)) = f'(g(x)) * g'(x)\n\n"
            "  'Outer derivative times inner derivative'\n\n"
            "  Leibniz: dy/dx = dy/du * du/dx\n\n"
            "  Powers the backpropagation\n"
            "  algorithm that trains all neural networks.\n\n"
            "  Chain rules can be nested:\n"
            "  d/dx f(g(h(x))) = f' * g' * h'",
            font_size=21, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=1.5)
        self.play(x_t.animate.set_value(2.5), run_time=4, rate_func=smooth); self.wait(2.5)
