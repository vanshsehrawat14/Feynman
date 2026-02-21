"""
Feynman – Derivative (Gold Standard)
6-section narrative, 3–5 minutes.
Uses Text/Cairo only — no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

CURVE_COLOR = BLUE
TAN_COLOR   = YELL
SEC_COLOR   = RED
AX_COLOR    = "#888888"


def _mk_axes():
    return Axes(
        x_range=[-3.5, 3.5, 1], y_range=[-0.3, 11, 2],
        x_length=8.5, y_length=5.2,
        axis_config={"color": AX_COLOR, "stroke_width": 2,
                     "include_tip": True, "tip_width": 0.15,
                     "tip_height": 0.2, "include_ticks": True},
    ).shift(LEFT * 0.5 + DOWN * 0.6)


class DerivativeScene(Scene):
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

    # ── S1 — Hook ────────────────────────────────────────────────────────────
    def s1_hook(self):
        t1 = Text("The Derivative", font_size=52, color=WHITE)
        t2 = Text("Instantaneous Rate of Change", font_size=24, color=CURVE_COLOR)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("A car drives 100 km in 2 hours.", font_size=34, color=WHITE)
        q2 = Text("Average speed = 50 km/h. Easy.", font_size=34, color=WHITE)
        q3 = Text("But how fast is it going at this EXACT moment?", font_size=30, color=YELL)
        q1.move_to(UP * 1.4); q2.next_to(q1, DOWN, buff=0.45); q3.next_to(q2, DOWN, buff=0.45)
        self.play(FadeIn(q1), run_time=1); self.wait(0.5)
        self.play(FadeIn(q2), run_time=1); self.wait(0.5)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5); self.wait(0.4)

        ans = Text(
            "The derivative answers exactly this.\n\n"
            "It captures the instantaneous rate of change\n"
            "at any single point on a curve.",
            font_size=28, color=WHITE,
        )
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=CURVE_COLOR, buff=0.35)
        self.play(FadeIn(ab), Write(ans), run_time=1.5); self.wait(2.5)

    # ── S2 — Geometry ────────────────────────────────────────────────────────
    def s2_geometry(self):
        sec_label(self, "Geometric Intuition")

        axes = _mk_axes()
        f  = lambda x: x ** 2
        df = lambda x: 2 * x
        curve = axes.plot(f, x_range=[-3.2, 3.2], color=CURVE_COLOR, stroke_width=3.5)
        self.play(Create(axes), run_time=1.5); self.wait(0.3)
        self.play(Create(curve), run_time=2); self.wait(0.5)

        # ── Secant line that shrinks into tangent ──────────────────────────
        x0 = 1.0
        h_tracker = ValueTracker(2.0)

        def secant():
            h = h_tracker.get_value()
            x1, y1 = x0, f(x0)
            x2, y2 = x0 + h, f(x0 + h)
            if abs(h) < 0.01:
                return VMobject()
            slope = (y2 - y1) / h
            # extend line ±1.5 in x
            ext = 1.5
            p1 = axes.c2p(x0 - ext, y1 + slope * (-ext))
            p2 = axes.c2p(x0 + ext + h, y1 + slope * (ext + h))
            return Line(p1, p2, color=SEC_COLOR, stroke_width=3)

        def sec_dot():
            h = h_tracker.get_value()
            return Dot(axes.c2p(x0 + h, f(x0 + h)), color=SEC_COLOR, radius=0.1)

        sec_line = always_redraw(secant)
        sec_dt   = always_redraw(sec_dot)
        fixed_dot = Dot(axes.c2p(x0, f(x0)), color=TAN_COLOR, radius=0.12)

        r1 = Text("Secant line between two points.", font_size=24, color=SEC_COLOR)
        self._rp(r1, y=2.0)
        b1 = self._box(r1, border=SEC_COLOR)

        self.play(Create(sec_line), Create(sec_dt), Create(fixed_dot))
        self.play(FadeIn(b1), Write(r1)); self.wait(0.5)

        # shrink h toward 0
        self.play(h_tracker.animate.set_value(0.01), run_time=5, rate_func=smooth)
        self.wait(0.5)

        self.play(FadeOut(b1), FadeOut(r1), FadeOut(sec_line), FadeOut(sec_dt), run_time=0.4)

        # real tangent at x0
        m0 = df(x0)
        y0 = f(x0)
        tan_line = Line(
            axes.c2p(x0 - 1.5, y0 + m0 * (-1.5)),
            axes.c2p(x0 + 1.5, y0 + m0 * 1.5),
            color=TAN_COLOR, stroke_width=4,
        )
        r2 = Text("As h → 0, secant becomes tangent.\nSlope = f'(x) = 2x.\nAt x=1: slope = 2.", font_size=24, color=TAN_COLOR)
        self._rp(r2, y=1.6)
        b2 = self._box(r2, border=TAN_COLOR)
        self.play(Create(tan_line), FadeIn(b2), Write(r2)); self.wait(2.5)

        # Sweep tangent across the curve
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        x_track = ValueTracker(-2.5)

        def sweep_tangent():
            xv = x_track.get_value()
            mv = df(xv); yv = f(xv)
            return Line(
                axes.c2p(xv - 1.0, yv + mv * (-1.0)),
                axes.c2p(xv + 1.0, yv + mv * 1.0),
                color=TAN_COLOR, stroke_width=3.5,
            )

        def sweep_dot():
            xv = x_track.get_value()
            return Dot(axes.c2p(xv, f(xv)), color=TAN_COLOR, radius=0.1)

        sw_tan = always_redraw(sweep_tangent)
        sw_dot = always_redraw(sweep_dot)
        self.play(FadeOut(tan_line), FadeOut(fixed_dot))
        self.play(Create(sw_tan), Create(sw_dot))

        r3 = Text("The derivative is a FUNCTION:\nit gives slope at every x.", font_size=24, color=WHITE)
        self._rp(r3, y=2.0)
        b3 = self._box(r3, border=WHITE)
        self.play(FadeIn(b3), Write(r3)); self.wait(0.5)
        self.play(x_track.animate.set_value(2.5), run_time=5, rate_func=smooth); self.wait(1)
        self.play(x_track.animate.set_value(-1.0), run_time=3, rate_func=smooth); self.wait(2)

    # ── S3 — Notation ────────────────────────────────────────────────────────
    def s3_notation(self):
        sec_label(self, "The Limit Definition")

        limit_def = Text(
            "f'(x) = lim      f(x+h) - f(x)\n"
            "         h→0    ─────────────────\n"
            "                        h",
            font_size=34, color=YELL,
        )
        limit_def.move_to(UP * 2.0)
        lb = self._box(limit_def, border=YELL, buff=0.35)
        self.play(FadeIn(lb), Write(limit_def), run_time=2.5); self.wait(1.5)
        self.play(FadeOut(lb), FadeOut(limit_def), run_time=0.5); self.wait(0.3)

        rules = Text(
            "Power rule:    d/dx(xⁿ) = n·xⁿ⁻¹\n\n"
            "Constant:      d/dx(c) = 0\n\n"
            "Sum:           d/dx(f+g) = f' + g'\n\n"
            "Product:       d/dx(fg) = f'g + fg'\n\n"
            "Chain:         d/dx(f(g(x))) = f'(g(x))·g'(x)",
            font_size=24, color=WHITE,
        )
        rules.move_to(ORIGIN)
        rb = self._box(rules, border=BLUE, buff=0.38)
        self.play(FadeIn(rb), Write(rules), run_time=2); self.wait(3.5)
        self.play(FadeOut(rb), FadeOut(rules), run_time=0.5); self.wait(0.3)

        notations = Text(
            "Three ways to write a derivative:\n\n"
            "  f'(x)     (Lagrange notation)\n"
            "  dy/dx     (Leibniz notation)\n"
            "  Df        (Euler notation)",
            font_size=26, color=WHITE,
        )
        notations.move_to(ORIGIN)
        nb = self._box(notations, border=GREEN, buff=0.35)
        self.play(FadeIn(nb), Write(notations), run_time=1.5); self.wait(3)

    # ── S4 — Worked Example ──────────────────────────────────────────────────
    def s4_example(self):
        sec_label(self, "Worked Example: f(x) = x³ - 3x")

        axes = _mk_axes()
        f  = lambda x: x ** 3 - 3 * x
        df = lambda x: 3 * x ** 2 - 3
        curve = axes.plot(f, x_range=[-2.4, 2.4], color=CURVE_COLOR, stroke_width=3.5)
        self.play(Create(axes), Create(curve), run_time=2); self.wait(0.5)

        # derivative step-by-step on the right
        steps = [
            ("f(x) = x³ - 3x", WHITE),
            ("Power rule on x³:  3x²", BLUE),
            ("Power rule on 3x:  3", BLUE),
            ("f'(x) = 3x² - 3", YELL),
        ]
        y_start = 2.5
        boxes = []
        for txt, col in steps:
            mob = Text(txt, font_size=26, color=col)
            self._rp(mob, y=y_start)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob)); self.wait(0.6)
            boxes.append((b, mob))
            y_start -= 1.1

        # critical points where f'=0 → 3x²-3=0 → x=±1
        cp_dots = []
        for xc in [-1.0, 1.0]:
            d = Dot(axes.c2p(xc, f(xc)), color=RED, radius=0.14)
            self.play(FadeIn(d)); self.wait(0.3)
            cp_dots.append(d)

        r_cp = Text("Critical pts at x=±1\n(where f'=0: max/min)", font_size=24, color=RED)
        self._rp(r_cp, y=-1.8)
        b_cp = self._box(r_cp, border=RED)
        self.play(FadeIn(b_cp), Write(r_cp)); self.wait(2.5)

        # tangent at x=0
        tan0 = Line(
            axes.c2p(-1.2, f(0) + df(0) * (-1.2)),
            axes.c2p(1.2,  f(0) + df(0) * 1.2),
            color=TAN_COLOR, stroke_width=4,
        )
        r_t0 = Text("At x=0: f'(0) = 3(0)-3 = -3\n(curve falling steeply)", font_size=22, color=YELL)
        self._rp(r_t0, y=-3.0)
        b_t0 = self._box(r_t0, border=YELL)
        self.play(Create(tan0), FadeIn(b_t0), Write(r_t0)); self.wait(2.5)

    # ── S5 — Insight ─────────────────────────────────────────────────────────
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")

        ins = Text(
            "Where the derivative lives in the real world:\n\n"
            "  Physics:\n"
            "    velocity = ds/dt  (position → speed)\n"
            "    acceleration = dv/dt  (speed → accel)\n\n"
            "  Economics:\n"
            "    marginal cost = dC/dq\n\n"
            "  Machine Learning:\n"
            "    gradient = derivative of the loss\n"
            "    gradient descent moves toward f'=0\n\n"
            "  Biology:\n"
            "    population growth rate = dP/dt",
            font_size=22, color=WHITE,
        )
        ins.move_to(LEFT * 1.0)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=2); self.wait(3.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5); self.wait(0.3)

        key = Text(
            "The Fundamental Theorem of Calculus:\n\n"
            "Differentiation and integration are inverses.\n\n"
            "d/dx ∫f(t)dt = f(x)",
            font_size=26, color=YELL,
        )
        key.move_to(ORIGIN)
        kb = self._box(key, border=YELL, buff=0.35)
        self.play(FadeIn(kb), Write(key), run_time=1.5); self.wait(3.5)

    # ── S6 — Summary ─────────────────────────────────────────────────────────
    def s6_summary(self):
        sec_label(self, "Summary")

        axes = _mk_axes()
        f  = lambda x: x ** 2
        df = lambda x: 2 * x
        curve = axes.plot(f, x_range=[-3.1, 3.1], color=CURVE_COLOR, stroke_width=3.5)
        x_t = ValueTracker(-2.0)

        def tan():
            xv = x_t.get_value(); mv = df(xv); yv = f(xv)
            return Line(
                axes.c2p(xv - 1.0, yv + mv * (-1.0)),
                axes.c2p(xv + 1.0, yv + mv * 1.0),
                color=TAN_COLOR, stroke_width=3.5,
            )

        def dt():
            return Dot(axes.c2p(x_t.get_value(), f(x_t.get_value())), color=TAN_COLOR, radius=0.1)

        sw = always_redraw(tan); sd = always_redraw(dt)
        self.play(Create(axes), Create(curve), Create(sw), Create(sd), run_time=1.5)

        sm = Text(
            "The Derivative\n\n"
            "  f'(x) = slope of tangent at x\n"
            "  = instantaneous rate of change\n\n"
            "  Power rule: d/dx(xⁿ) = nxⁿ⁻¹\n"
            "  At critical points: f'(x) = 0\n\n"
            "  Backbone of calculus, physics,\n"
            "  economics, and machine learning.",
            font_size=22, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=1.5)
        self.play(x_t.animate.set_value(2.0), run_time=4, rate_func=smooth); self.wait(2.5)
