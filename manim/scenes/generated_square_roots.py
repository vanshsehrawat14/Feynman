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

class GeneratedScene(Scene):
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
        t1 = Text("Square Roots", font_size=52, color=WHITE)
        t2 = Text("The Inverse of Squaring", font_size=24, color=CURVE_COLOR)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1), run_time=1); self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8); self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5); self.wait(0.4)

        q1 = Text("What is the number that, when multiplied by itself, gives 16?", font_size=30, color=YELL)
        q1.move_to(UP * 1.4)
        self.play(Write(q1), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), run_time=0.5); self.wait(0.4)

        ans = Text(
            "The square root of a number is a value that, when multiplied by itself, gives the original number.",
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
        curve = axes.plot(f, x_range=[-3.2, 3.2], color=CURVE_COLOR, stroke_width=3.5)
        self.play(Create(axes), run_time=1.5); self.wait(0.3)
        self.play(Create(curve), run_time=2); self.wait(0.5)

        # ── Square root of 4 ────────────────────────────────────────────────
        x0 = 2.0
        y0 = f(x0)
        dot = Dot(axes.c2p(x0, y0), color=TAN_COLOR, radius=0.12)
        self.play(FadeIn(dot)); self.wait(0.3)

        r1 = Text("The square root of 4 is 2, because 2 × 2 = 4.", font_size=24, color=TAN_COLOR)
        self._rp(r1, y=2.0)
        b1 = self._box(r1, border=TAN_COLOR)
        self.play(FadeIn(b1), Write(r1)); self.wait(0.5)

        # ── Square root of 9 ────────────────────────────────────────────────
        x1 = 3.0
        y1 = f(x1)
        dot1 = Dot(axes.c2p(x1, y1), color=TAN_COLOR, radius=0.12)
        self.play(FadeIn(dot1)); self.wait(0.3)

        r2 = Text("The square root of 9 is 3, because 3 × 3 = 9.", font_size=24, color=TAN_COLOR)
        self._rp(r2, y=1.6)
        b2 = self._box(r2, border=TAN_COLOR)
        self.play(FadeIn(b2), Write(r2)); self.wait(2.5)

    # ── S3 — Notation ────────────────────────────────────────────────────────
    def s3_notation(self):
        sec_label(self, "Mathematical Notation")

        notation = Text(
            "The square root of a number x is denoted by √x or x¹/².",
            font_size=34, color=YELL,
        )
        notation.move_to(UP * 2.0)
        lb = self._box(notation, border=YELL, buff=0.35)
        self.play(FadeIn(lb), Write(notation), run_time=2.5); self.wait(1.5)
        self.play(FadeOut(lb), FadeOut(notation), run_time=0.5); self.wait(0.3)

        properties = Text(
            "Properties of square roots:\n\n"
            "  √(ab) = √a × √b\n\n"
            "  √(a/b) = √a / √b",
            font_size=24, color=WHITE,
        )
        properties.move_to(ORIGIN)
        rb = self._box(properties, border=BLUE, buff=0.38)
        self.play(FadeIn(rb), Write(properties), run_time=2); self.wait(3.5)
        self.play(FadeOut(rb), FadeOut(properties), run_time=0.5); self.wait(0.3)

    # ── S4 — Worked Example ──────────────────────────────────────────────────
    def s4_example(self):
        sec_label(self, "Worked Example: Simplifying Square Roots")

        example = Text(
            "Simplify: √(16 × 9) = ?",
            font_size=34, color=YELL,
        )
        example.move_to(UP * 2.0)
        lb = self._box(example, border=YELL, buff=0.35)
        self.play(FadeIn(lb), Write(example), run_time=2.5); self.wait(1.5)
        self.play(FadeOut(lb), FadeOut(example), run_time=0.5); self.wait(0.3)

        steps = [
            ("√(16 × 9) = √16 × √9", WHITE),
            ("= 4 × 3", BLUE),
            ("= 12", YELL),
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

        self.play(*[FadeOut(b) for b, _ in boxes], run_time=0.5); self.wait(0.3)

    # ── S5 — Insight ─────────────────────────────────────────────────────────
    def s5_insight(self):
        sec_label(self, "Real-World Applications")

        ins = Text(
            "Square roots have many real-world applications, including:\n\n"
            "  Physics: calculating distances and velocities\n"
            "  Engineering: designing buildings and bridges\n"
            "  Computer Science: algorithms for solving equations",
            font_size=22, color=WHITE,
        )
        ins.move_to(LEFT * 1.0)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=2); self.wait(3.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5); self.wait(0.3)

        key = Text(
            "The square root is an essential mathematical concept that has numerous applications in various fields.",
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
        curve = axes.plot(f, x_range=[-3.1, 3.1], color=CURVE_COLOR, stroke_width=3.5)
        self.play(Create(axes), Create(curve), run_time=1.5)

        sm = Text(
            "The square root of a number x is a value that, when multiplied by itself, gives the original number.\n\n"
            "  √x = y if and only if y × y = x",
            font_size=22, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=1.5)
        self.wait(4)