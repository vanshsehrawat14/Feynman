"""
Feynman – Gradient Descent (Gold Standard)
6-section narrative, 3-5 minutes. Text/Cairo only, no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

AX_COLOR = "#888888"

class GradientDescentScene(Scene):
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
        t1 = Text("Gradient Descent", font_size=48, color=WHITE)
        t2 = Text("How Machines Learn", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)

        q1 = Text("You are blindfolded on a hilly landscape.", font_size=28, color=WHITE)
        q2 = Text("How do you find the lowest valley?", font_size=28, color=YELL)
        q3 = Text("Feel the slope. Step downhill. Repeat.", font_size=26, color=GREEN)
        q1.move_to(UP * 1.5); q2.next_to(q1, DOWN, buff=0.5); q3.next_to(q2, DOWN, buff=0.5)
        self.play(Write(q1), run_time=2.0); self.wait(1.0)
        self.play(Write(q2), run_time=1.5); self.wait(1.0)
        self.play(Write(q3), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5)

        ans = Text(
            "Gradient descent is the optimization\n"
            "algorithm behind all neural networks.\n\n"
            "It minimizes a loss function by stepping\n"
            "in the direction of steepest descent.",
            font_size=26, color=WHITE)
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(3.5)

    def s2_geometry(self):
        sec_label(self, "Visualizing the Loss Landscape")
        axes = Axes(x_range=[-3,3,1], y_range=[-0.5,9,2], x_length=7.5, y_length=5.2,
            axis_config={"color": AX_COLOR, "stroke_width": 2, "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        f = lambda x: x**2
        curve = axes.plot(f, x_range=[-2.8,2.8], color=BLUE, stroke_width=3.5)
        self.play(Create(axes), run_time=2.0); self.wait(0.3)
        self.play(Create(curve), run_time=2.0); self.wait(0.5)

        r1 = Text("Loss L(w) = w^2  (minimum at w=0)", font_size=22, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(1.5)

        x_t = ValueTracker(2.5)
        dot_mob = always_redraw(lambda: Dot(axes.c2p(x_t.get_value(), f(x_t.get_value())), color=YELL, radius=0.15))
        self.play(Create(dot_mob)); self.wait(0.5)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)

        r2 = Text("Start: w = 2.5", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=1.5); self.wait(1.0)

        for wn in [1.8, 1.2, 0.65, 0.28, 0.08]:
            self.play(x_t.animate.set_value(wn), run_time=1.5, rate_func=smooth); self.wait(0.4)

        self.play(FadeOut(b2), FadeOut(r2), run_time=0.4)
        r3 = Text("Converged!  w ~ 0, L(w) ~ 0", font_size=22, color=GREEN)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=GREEN)
        self.play(FadeIn(b3), Write(r3), run_time=1.5); self.wait(3.0)

    def s3_notation(self):
        sec_label(self, "The Update Rule")
        eq = Text("w  :=  w  -  lr * dL/dw", font_size=36, color=YELL)
        eq.move_to(UP * 2.8)
        eb = self._box(eq, border=YELL, buff=0.4)
        self.play(FadeIn(eb), Write(eq), run_time=2.0); self.wait(1.0)

        items = [
            ("w           parameter (weight)", BLUE),
            ("lr          learning rate (step size)", GREEN),
            ("dL/dw       gradient of loss", RED),
            (":=          repeated update", WHITE),
        ]
        y = 1.6; boxes = []
        for txt, col in items:
            mob = Text(txt, font_size=24, color=col).move_to(UP * y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=2.0); self.wait(1.0)
            boxes.append((b, mob)); y -= 0.9
        self.wait(1.0)
        self.play(*[FadeOut(b) for b,_ in boxes], *[FadeOut(m) for _,m in boxes],
                  FadeOut(eb), FadeOut(eq), run_time=0.5)

        variants = Text(
            "Variants:\n\n"
            "  Batch GD:      use ALL examples per step\n"
            "  Stochastic GD: use ONE example per step\n"
            "  Mini-batch GD: use k examples (standard)\n\n"
            "  Adam:  adapts lr per parameter\n"
            "  Momentum: accumulate gradient history\n"
            "  RMSprop: scale by gradient magnitude",
            font_size=23, color=WHITE)
        variants.move_to(ORIGIN)
        vb = self._box(variants, border=BLUE, buff=0.38)
        self.play(FadeIn(vb), Write(variants), run_time=2.5); self.wait(3.5)

    def s4_example(self):
        sec_label(self, "Worked Example: L(w)=w^2, lr=0.3")
        axes = Axes(x_range=[-3,3,1], y_range=[-0.5,9,2], x_length=7.5, y_length=5.2,
            axis_config={"color": AX_COLOR, "stroke_width": 2, "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        f = lambda x: x**2
        curve = axes.plot(f, x_range=[-2.8,2.8], color=BLUE, stroke_width=3.5)
        self.play(Create(axes), Create(curve), run_time=2.5); self.wait(0.5)

        steps = [
            ("w0 = 2.0,  L = 4.0", WHITE, 2.8),
            ("grad = 2*2.0 = 4.0", YELL, 2.0),
            ("w1 = 2.0 - 0.3*4.0 = 0.80", GREEN, 1.2),
            ("grad = 2*0.8 = 1.6", YELL, 0.4),
            ("w2 = 0.80 - 0.3*1.6 = 0.32", GREEN, -0.4),
            ("grad = 2*0.32 = 0.64", YELL, -1.2),
            ("w3 = 0.32 - 0.3*0.64 = 0.13", GREEN, -2.0),
            ("Exponential convergence!", BLUE, -2.8),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=22, color=col)
            self._rp(mob, y=yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(0.8)
        self.wait(2.5)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Gradient descent trains ALL of modern AI:\n\n"
            "  GPT-4:    ~1 trillion parameters\n"
            "  Each step: compute gradient for every\n"
            "  parameter via backpropagation\n\n"
            "  Loss landscapes in high dimensions:\n"
            "  • Saddle points (not local minima!)\n"
            "  • Flat regions (vanishing gradients)\n"
            "  • Sharp vs flat minima\n\n"
            "  Flat minima generalize better to new data",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)

        lr_text = Text(
            "Learning rate is the most important hyperparameter:\n\n"
            "  Too large  ->  overshoot, diverge\n"
            "  Too small  ->  takes forever, gets stuck\n"
            "  Just right ->  smooth convergence\n\n"
            "  Modern solutions:\n"
            "  Warmup: increase lr gradually at start\n"
            "  Cosine annealing: cycle the learning rate\n"
            "  Adam: per-parameter adaptive learning rates",
            font_size=22, color=WHITE)
        lr_text.move_to(ORIGIN)
        lb = self._box(lr_text, border=YELL, buff=0.38)
        self.play(FadeIn(lb), Write(lr_text), run_time=2.5); self.wait(4.0)

    def s6_summary(self):
        sec_label(self, "Summary")
        axes = Axes(x_range=[-3,3,1], y_range=[-0.5,9,2], x_length=7.5, y_length=5.2,
            axis_config={"color": AX_COLOR, "stroke_width": 2, "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 1.5 + DOWN * 0.5)
        f = lambda x: x**2
        curve = axes.plot(f, x_range=[-2.8,2.8], color=BLUE, stroke_width=3.5)
        min_dot = Dot(axes.c2p(0,0), color=GREEN, radius=0.18)
        self.play(Create(axes), Create(curve), run_time=2.0)
        self.play(Create(min_dot), run_time=1.0); self.wait(0.5)

        sm = Text(
            "Gradient Descent\n\n"
            "  w := w - lr * dL/dw\n\n"
            "  Follow the negative gradient\n"
            "  Repeat until convergence\n\n"
            "  lr too large  -> diverge\n"
            "  lr too small  -> slow\n\n"
            "  Mini-batch GD is standard practice\n"
            "  Adam optimizer is most widely used\n"
            "  The engine of deep learning",
            font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
