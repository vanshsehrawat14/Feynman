"""
Master scene generator — writes all under-2-min scenes with gold-standard content.
Run: python _gen_scenes.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

HEADER = '''"""
Feynman – {title} (Gold Standard)
6-section narrative, 3-5 minutes. Text/Cairo only, no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

AX_COLOR = "#888888"
'''

def TEMPLATE(cls):
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

    def _mk_axes(self, xr=(-0.5, 4.5, 1), yr=(-0.5, 4.5, 1)):
        return Axes(
            x_range=[*xr], y_range=[*yr],
            x_length=7.0, y_length=5.0,
            axis_config={{"color": AX_COLOR, "stroke_width": 2,
                         "include_tip": True, "include_ticks": True}},
        ).shift(LEFT * 1.5 + DOWN * 0.5)
'''

# ── Individual scene bodies ─────────────────────────────────────────────────

GRADIENT_DESCENT = HEADER.format(title="Gradient Descent") + TEMPLATE("GradientDescentScene") + '''
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
            "Gradient descent is the optimization\\n"
            "algorithm behind all neural networks.\\n\\n"
            "It minimizes a loss function by stepping\\n"
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
            "Variants:\\n\\n"
            "  Batch GD:      use ALL examples per step\\n"
            "  Stochastic GD: use ONE example per step\\n"
            "  Mini-batch GD: use k examples (standard)\\n\\n"
            "  Adam:  adapts lr per parameter\\n"
            "  Momentum: accumulate gradient history\\n"
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
            "Gradient descent trains ALL of modern AI:\\n\\n"
            "  GPT-4:    ~1 trillion parameters\\n"
            "  Each step: compute gradient for every\\n"
            "  parameter via backpropagation\\n\\n"
            "  Loss landscapes in high dimensions:\\n"
            "  • Saddle points (not local minima!)\\n"
            "  • Flat regions (vanishing gradients)\\n"
            "  • Sharp vs flat minima\\n\\n"
            "  Flat minima generalize better to new data",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)

        lr_text = Text(
            "Learning rate is the most important hyperparameter:\\n\\n"
            "  Too large  ->  overshoot, diverge\\n"
            "  Too small  ->  takes forever, gets stuck\\n"
            "  Just right ->  smooth convergence\\n\\n"
            "  Modern solutions:\\n"
            "  Warmup: increase lr gradually at start\\n"
            "  Cosine annealing: cycle the learning rate\\n"
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
            "Gradient Descent\\n\\n"
            "  w := w - lr * dL/dw\\n\\n"
            "  Follow the negative gradient\\n"
            "  Repeat until convergence\\n\\n"
            "  lr too large  -> diverge\\n"
            "  lr too small  -> slow\\n\\n"
            "  Mini-batch GD is standard practice\\n"
            "  Adam optimizer is most widely used\\n"
            "  The engine of deep learning",
            font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

VECTORS = HEADER.format(title="Vectors") + TEMPLATE("VectorsScene") + '''
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
            "A vector captures BOTH direction AND magnitude.\\n\\n"
            "It is the fundamental language of physics,\\n"
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
        r1 = Text("x-component: 3\\ny-component: 2", font_size=22, color=YELL)
        self._rp(r1, y=2.0); b1 = self._box(r1, border=YELL)
        self.play(FadeIn(b1), Write(r1), run_time=2.0); self.wait(2.0)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4)
        v2 = Arrow(axes.c2p(1,0.5), axes.c2p(4,2.5), color=BLUE, stroke_width=3, stroke_opacity=0.5, buff=0)
        v3 = Arrow(axes.c2p(0.5,1.5), axes.c2p(3.5,3.5), color=BLUE, stroke_width=3, stroke_opacity=0.4, buff=0)
        r2 = Text("Vectors are FREE --\\nposition does not matter,\\nonly direction + length.", font_size=22, color=WHITE)
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
            "Vector operations:\\n\\n"
            "  Addition:      v + w = (vx+wx, vy+wy)\\n"
            "  Scalar mult:   c*v = (c*vx, c*vy)\\n"
            "  Subtraction:   v - w = v + (-w)\\n"
            "  Dot product:   v . w = vx*wx + vy*wy\\n"
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
            "Vectors appear everywhere:\\n\\n"
            "  Physics: velocity, force, acceleration, momentum\\n"
            "  Computer graphics: surface normals, ray directions\\n"
            "  Machine learning: word embeddings (50000-D vectors)\\n"
            "  GPS: displacement vectors on Earth's surface\\n"
            "  Economics: price baskets (multi-dimensional)\\n\\n"
            "  In ML, a document is a vector in vocabulary space.\\n"
            "  Cosine similarity = angle between two vectors.\\n"
            "  king - man + woman ~ queen  (vector arithmetic!)",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        dot2 = Text(
            "Key insight:\\n\\n"
            "  A vector is a geometric OBJECT.\\n"
            "  Its components depend on your coordinate system\\n"
            "  (your choice of basis vectors).\\n\\n"
            "  Change your basis, change its components --\\n"
            "  but the vector itself does not change.\\n\\n"
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
            "Vectors\\n\\n"
            "  v = (vx, vy) -- direction + magnitude\\n"
            "  |v| = sqrt(vx^2 + vy^2)\\n\\n"
            "  Standard basis: e1=(1,0), e2=(0,1)\\n"
            "  Any vector: v = vx*e1 + vy*e2\\n\\n"
            "  Translation invariant (free vector)\\n"
            "  Foundation of linear algebra",
            font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

QUICKSORT = HEADER.format(title="Quicksort") + TEMPLATE("QuicksortScene") + '''
    def s1_hook(self):
        t1 = Text("Quicksort", font_size=52, color=WHITE)
        t2 = Text("Divide, Conquer, Sort", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        q1 = Text("You have 8 unsorted numbers.", font_size=28, color=WHITE)
        q2 = Text("What is the fastest way to sort them?", font_size=28, color=YELL)
        q1.move_to(UP * 1.2); q2.next_to(q1, DOWN, buff=0.5)
        self.play(Write(q1), run_time=2.0); self.wait(1.0)
        self.play(Write(q2), run_time=1.5); self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), run_time=0.5)
        ans = Text(
            "Quicksort: pick a pivot, partition around it,\\n"
            "then recursively sort each half.\\n\\n"
            "Average time: O(n log n)\\n"
            "Used in Python, C++, Java standard libraries.",
            font_size=26, color=WHITE)
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(3.5)

    def _draw_array(self, arr, colors=None, y=-1.0):
        mobs = VGroup()
        if colors is None: colors = [BLUE]*len(arr)
        for i, (val, col) in enumerate(zip(arr, colors)):
            x = -3.5 + i * 0.85
            box = Rectangle(width=0.75, height=0.75, color=col, fill_color=col, fill_opacity=0.4, stroke_width=2)
            box.move_to(RIGHT*x + UP*y)
            lbl = Text(str(val), font_size=22, color=WHITE).move_to(box.get_center())
            mobs.add(box, lbl)
        return mobs

    def s2_geometry(self):
        sec_label(self, "Quicksort in Action")
        arr = [5, 3, 8, 1, 9, 2, 7, 4]
        cols = [BLUE]*8
        mobs = self._draw_array(arr, cols)
        title = Text("Unsorted array:", font_size=24, color=WHITE).move_to(UP * 2.5)
        self.play(FadeIn(title), FadeIn(mobs), run_time=2.0); self.wait(1.5)

        # Show pivot = 5
        pivot_lbl = Text("Pivot = 5 (first element)", font_size=22, color=YELL).move_to(UP * 1.5)
        self.play(Write(pivot_lbl), run_time=1.5); self.wait(1.0)

        # Partition visualization
        less_label = Text("< 5: [3, 1, 2, 4]", font_size=22, color=GREEN).move_to(UP * 0.5 + LEFT * 2.5)
        pivot_show = Text("pivot: [5]", font_size=22, color=YELL).move_to(UP * 0.5)
        more_label = Text("> 5: [8, 9, 7]", font_size=22, color=RED).move_to(UP * 0.5 + RIGHT * 2.5)
        self.play(Write(less_label), Write(pivot_show), Write(more_label), run_time=2.5); self.wait(2.0)

        step2 = Text("Recursively sort [3,1,2,4] and [8,9,7]", font_size=22, color=WHITE).move_to(DOWN * 0.3)
        self.play(Write(step2), run_time=2.0); self.wait(1.5)

        sorted_arr = [1, 2, 3, 4, 5, 7, 8, 9]
        sorted_cols = [GREEN]*8
        sorted_mobs = self._draw_array(sorted_arr, sorted_cols, y=-1.8)
        sorted_title = Text("Result: sorted!", font_size=22, color=GREEN).move_to(DOWN * 1.0)
        self.play(Write(sorted_title), FadeIn(sorted_mobs), run_time=2.0); self.wait(3.0)

    def s3_notation(self):
        sec_label(self, "The Algorithm")
        algo = Text(
            "quicksort(arr, low, high):\\n"
            "  if low >= high: return\\n"
            "  pivot = arr[high]\\n"
            "  i = low - 1\\n"
            "  for j from low to high-1:\\n"
            "    if arr[j] <= pivot:\\n"
            "      i += 1\\n"
            "      swap arr[i], arr[j]\\n"
            "  swap arr[i+1], arr[high]\\n"
            "  p = i + 1\\n"
            "  quicksort(arr, low, p-1)\\n"
            "  quicksort(arr, p+1, high)",
            font_size=22, color=BLUE)
        algo.move_to(ORIGIN)
        ab = self._box(algo, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(algo), run_time=3.0); self.wait(3.5)
        self.play(FadeOut(ab), FadeOut(algo), run_time=0.5)

        complexity = Text(
            "Time complexity:\\n\\n"
            "  Average case: O(n log n)\\n"
            "  Best case:    O(n log n)\\n"
            "  Worst case:   O(n^2)  (already sorted + bad pivot)\\n\\n"
            "  Space: O(log n) for recursion stack\\n\\n"
            "  Pivot strategies to avoid worst case:\\n"
            "  Median-of-three, random pivot, Sedgewick",
            font_size=23, color=WHITE)
        complexity.move_to(ORIGIN)
        cb = self._box(complexity, border=YELL, buff=0.38)
        self.play(FadeIn(cb), Write(complexity), run_time=2.5); self.wait(3.5)

    def s4_example(self):
        sec_label(self, "Step-by-Step: [3, 1, 2]")
        steps = [
            ("Array: [3, 1, 2]", WHITE),
            ("Pivot = 2 (last element)", YELL),
            ("Compare 3 > 2: stays right", RED),
            ("Compare 1 < 2: move left -> [1, 3, 2]", GREEN),
            ("Swap pivot: [1, 2, 3]", YELL),
            ("Left partition [1]: already sorted", GREEN),
            ("Right partition [3]: already sorted", GREEN),
            ("Final: [1, 2, 3] -- sorted!", BLUE),
        ]
        y = 3.0
        for txt, col in steps:
            mob = Text(txt, font_size=26, color=col).move_to(UP * y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(1.2)
            y -= 0.9
        self.wait(2.0)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Why quicksort is fast in practice:\\n\\n"
            "  Cache-friendly: works in place on array\\n"
            "  Low overhead: minimal extra memory\\n"
            "  Average O(n log n): most inputs behave well\\n\\n"
            "  Comparison: Merge sort always O(n log n)\\n"
            "  but requires O(n) extra space\\n\\n"
            "  Python uses Timsort (hybrid merge + insertion)\\n"
            "  C++ std::sort: introsort (quicksort + heapsort)\\n\\n"
            "  Random pivot eliminates pathological worst-case",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        dc = Text(
            "Divide and conquer strategy:\\n\\n"
            "  Split problem into smaller subproblems\\n"
            "  Solve each subproblem independently\\n"
            "  Combine solutions\\n\\n"
            "  The PIVOT is the key creative insight!\\n"
            "  After partitioning, pivot is in FINAL position.\\n"
            "  Reduces problem size by half each time on average.",
            font_size=22, color=WHITE)
        dc.move_to(ORIGIN)
        db = self._box(dc, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(dc), run_time=2.5); self.wait(4.0)

    def s6_summary(self):
        sec_label(self, "Summary")
        arr_sorted = [1, 2, 3, 4, 5, 6, 7, 8]
        mobs = self._draw_array(arr_sorted, [GREEN]*8)
        self.play(FadeIn(mobs), run_time=1.5); self.wait(0.5)
        sm = Text(
            "Quicksort\\n\\n"
            "  1. Pick a pivot\\n"
            "  2. Partition: smaller left, larger right\\n"
            "  3. Pivot is now in final sorted position\\n"
            "  4. Recurse on both halves\\n\\n"
            "  Average: O(n log n)\\n"
            "  Worst case: O(n^2) -- avoid with random pivot\\n"
            "  In-place, cache-friendly -- fast in practice\\n"
            "  Used in C++, Java standard libraries",
            font_size=20, color=WHITE)
        sm.move_to(RIGHT * 3.0 + UP * 0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

INTEGRAL_SCENE = HEADER.format(title="The Integral") + TEMPLATE("IntegralScene") + '''
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
            "An integral is an infinite sum.\\n\\n"
            "Split the area into infinitely thin slices,\\n"
            "add up all their areas.\\n"
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
        r4 = Text("n -> infinity\\n= exact integral", font_size=24, color=WHITE).move_to(RIGHT * 4.0 + UP * 2.0)
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
            "Fundamental Theorem of Calculus:\\n\\n"
            "  integral(a,b) f(x) dx  =  F(b) - F(a)\\n\\n"
            "  where F is the ANTIDERIVATIVE: F prime = f\\n\\n"
            "  Integration and differentiation are\\n"
            "  inverse operations!", font_size=25, color=WHITE)
        ftc.move_to(ORIGIN)
        fb = self._box(ftc, border=GREEN, buff=0.38)
        self.play(FadeIn(fb), Write(ftc), run_time=2.5); self.wait(3.5)
        self.play(FadeOut(fb), FadeOut(ftc), run_time=0.5)
        rules = Text(
            "Integration rules:\\n\\n"
            "  integral(x^n dx) = x^(n+1)/(n+1) + C\\n"
            "  integral(cos x dx) = sin(x) + C\\n"
            "  integral(e^x dx) = e^x + C\\n"
            "  integral(1/x dx) = ln|x| + C\\n"
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
            "Integrals appear everywhere:\\n\\n"
            "  Physics: Work = integral(F dx)\\n"
            "           Charge = integral(I dt)\\n"
            "           Center of mass = integral(x dm / M)\\n\\n"
            "  Probability: P(a<X<b) = integral(a,b) f(x) dx\\n"
            "  Statistics: Expected value = integral(x f(x) dx)\\n\\n"
            "  ML: KL divergence, VAE loss, Fourier features\\n"
            "  Engineering: signal processing, control theory\\n\\n"
            "  Anything that accumulates over time or space.",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        acc = Text(
            "The fundamental duality:\\n\\n"
            "  DERIVATIVE = rate of change (instantaneous)\\n"
            "  INTEGRAL   = accumulated change (total)\\n\\n"
            "  FTC Part 1: d/dx integral(a,x) f(t) dt = f(x)\\n"
            "  FTC Part 2: integral(a,b) f(x)dx = F(b)-F(a)\\n\\n"
            "  They are INVERSES of each other.\\n"
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
            "The Integral\\n\\n"
            "  Area under f from a to b\\n\\n"
            "  = limit of Riemann sums as n -> infinity\\n\\n"
            "  Computed via antiderivative:\\n"
            "  F(b) - F(a)  where F prime = f\\n\\n"
            "  Derivative and integral are inverses\\n"
            "  (Fundamental Theorem of Calculus)\\n\\n"
            "  The language of accumulation",
            font_size=20, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

GAME_THEORY = HEADER.format(title="Game Theory") + TEMPLATE("GameTheoryScene") + '''
    def s1_hook(self):
        t1 = Text("Game Theory", font_size=52, color=WHITE)
        t2 = Text("Strategic Decision Making", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.5)
        self.play(FadeIn(t2), run_time=1.0); self.wait(2.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        q1 = Text("Two suspects. Separate interrogation rooms.", font_size=28, color=WHITE)
        q2 = Text("Both stay silent: 1 year each.", font_size=26, color=GREEN)
        q3 = Text("One confesses, one stays silent: 0 vs 10 years.", font_size=26, color=YELL)
        q4 = Text("Both confess: 5 years each.", font_size=26, color=RED)
        q1.move_to(UP * 2.0); q2.next_to(q1, DOWN, buff=0.4)
        q3.next_to(q2, DOWN, buff=0.3); q4.next_to(q3, DOWN, buff=0.3)
        for m in [q1, q2, q3, q4]:
            self.play(Write(m), run_time=1.5); self.wait(0.8)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [q1,q2,q3,q4]], run_time=0.5)
        ans = Text(
            "What should each prisoner do?\\n\\n"
            "Game theory reveals the answer --\\n"
            "and it is not what you might expect.",
            font_size=28, color=WHITE)
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.0); self.wait(3.5)

    def s2_geometry(self):
        sec_label(self, "The Payoff Matrix")
        header = Text("Prisoner B stays silent    Prisoner B confesses", font_size=20, color=WHITE)
        header.move_to(UP * 2.8 + RIGHT * 1.0)
        self.play(Write(header), run_time=2.0); self.wait(0.5)

        row1h = Text("Prisoner A\\nstays silent", font_size=20, color=WHITE).move_to(LEFT * 3.5 + UP * 1.0)
        row2h = Text("Prisoner A\\nconfesses", font_size=20, color=WHITE).move_to(LEFT * 3.5 + DOWN * 0.8)
        self.play(Write(row1h), Write(row2h), run_time=2.0); self.wait(0.5)

        cells = [
            (UP*1.0 + LEFT*0.5, "-1, -1", GREEN, "Both silent (best!)"),
            (UP*1.0 + RIGHT*2.5, "-10, 0", RED, "A stays, B confesses"),
            (DOWN*0.8 + LEFT*0.5, "0, -10", YELL, "A confesses, B stays"),
            (DOWN*0.8 + RIGHT*2.5, "-5, -5", RED, "Both confess (Nash!)"),
        ]
        for pos, txt, col, desc in cells:
            mob = Text(txt, font_size=24, color=col).move_to(pos)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(0.8)
        self.wait(2.5)

    def s3_notation(self):
        sec_label(self, "Nash Equilibrium")
        defn = Text(
            "Nash Equilibrium:\\n\\n"
            "  A strategy profile where NO player can\\n"
            "  improve their outcome by changing their\\n"
            "  strategy ALONE.\\n\\n"
            "  Named after John Nash (Nobel Prize 1994)\\n"
            "  (A Beautiful Mind)",
            font_size=24, color=WHITE)
        defn.move_to(UP * 1.0)
        db = self._box(defn, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(defn), run_time=2.5); self.wait(2.0)

        nash = Text(
            "In the Prisoner Dilemma:\\n"
            "  Both confessing IS the Nash equilibrium!\\n\\n"
            "  If B confesses: A should confess (5 < 10 years)\\n"
            "  If B stays silent: A should confess (0 < 1 year)\\n\\n"
            "  Confessing is a DOMINANT STRATEGY for A\\n"
            "  (and by symmetry, for B too).",
            font_size=22, color=RED)
        nash.move_to(DOWN * 1.0)
        nb = self._box(nash, border=RED, buff=0.35)
        self.play(FadeIn(nb), Write(nash), run_time=2.5); self.wait(3.5)

    def s4_example(self):
        sec_label(self, "Dominant Strategy Analysis")
        steps = [
            ("From A perspective: what if B confesses?", WHITE, 3.0),
            ("  A confesses: 5 years. A stays silent: 10 years.", GREEN, 2.2),
            ("  -> A should CONFESS", YELL, 1.4),
            ("From A perspective: what if B stays silent?", WHITE, 0.6),
            ("  A confesses: 0 years. A stays silent: 1 year.", GREEN, -0.2),
            ("  -> A should CONFESS (again!)", YELL, -1.0),
            ("Confess is dominant strategy for A.", RED, -1.8),
            ("Same logic applies to B. Both confess!", RED, -2.6),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP * yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(1.0)
        self.wait(2.5)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Rational individuals -> collectively bad outcome!\\n\\n"
            "  This is the tragedy of game theory --\\n"
            "  rational self-interest does not always\\n"
            "  lead to the best collective outcome.\\n\\n"
            "  Applications:\\n"
            "  Arms races (countries all arm themselves)\\n"
            "  Climate change (nations overpollute)\\n"
            "  Auctions (bidding strategy)\\n"
            "  Evolutionary biology (fitness strategies)\\n"
            "  AI agents negotiating and competing",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(4.0)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        types_text = Text(
            "Other game types:\\n\\n"
            "  Zero-sum: one player wins, other loses\\n"
            "    (chess, poker, rock-paper-scissors)\\n\\n"
            "  Coordination: both benefit from aligning\\n"
            "    (driving on same side of road)\\n\\n"
            "  Repeated games: cooperation can emerge!\\n"
            "    (tit-for-tat strategy)\\n\\n"
            "  Mixed strategies: randomize to prevent exploitation",
            font_size=22, color=WHITE)
        types_text.move_to(ORIGIN)
        tb = self._box(types_text, border=YELL, buff=0.38)
        self.play(FadeIn(tb), Write(types_text), run_time=2.5); self.wait(4.0)

    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text(
            "Game Theory\\n\\n"
            "  Models strategic interaction between agents\\n\\n"
            "  Nash Equilibrium:\\n"
            "  No player gains by changing strategy alone\\n\\n"
            "  Prisoner Dilemma:\\n"
            "  Rational play -> collectively bad outcome\\n\\n"
            "  Dominant strategy: best regardless of others\\n\\n"
            "  Applications: economics, AI, biology,\\n"
            "  auctions, negotiations, climate policy",
            font_size=20, color=WHITE)
        sm.move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(4.5)
'''

# Write all files
scenes = {
    'ml_02_gradient_descent.py': GRADIENT_DESCENT,
    'la_01_vectors.py': VECTORS,
    'algo_02_quicksort.py': QUICKSORT,
    'integral.py': INTEGRAL_SCENE,
    'econ_05_game_theory.py': GAME_THEORY,
}

for fname, content in scenes.items():
    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {fname}: {len(content)} bytes")

print("Done.")
