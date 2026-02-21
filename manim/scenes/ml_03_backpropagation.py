"""ml_03_backpropagation.py — Backpropagation — Full 6-Section Scene
Target: 3+ minutes total animation time.
Uses Text/Cairo only — no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

CORAL = RED


def _arr(start, end, color=BLUE, sw=2.5):
    s = np.array(start)
    e = np.array(end)
    if np.linalg.norm(e - s) < 0.05:
        return VMobject()
    return Arrow(s, e, buff=0.05, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.15)


class BackpropagationScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.s1_hook()
        self._fade_all()
        self.s2_geometry()
        self._fade_all()
        self.s3_notation()
        self._fade_all()
        self.s4_example()
        self._fade_all()
        self.s5_insight()
        self._fade_all()
        self.s6_summary()

    def _fade_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=1)
        self.wait(0.5)

    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)

    def _rp(self, mob, y=0.0, x=3.8):
        mob.move_to(RIGHT * x + UP * y)
        return mob

    def _lp(self, mob, y=0.0, x=-3.8):
        mob.move_to(LEFT * abs(x) + UP * y)
        return mob

    # ── Draw a simple 3-layer network ────────────────────────────────────────
    def _make_network(self, inp_positions, hid_positions, out_positions,
                      inp_color=BLUE, hid_color=YELL, out_color=GREEN):
        dots_in = VGroup(*[Dot(p, color=inp_color, radius=0.14) for p in inp_positions])
        dots_h = VGroup(*[Dot(p, color=hid_color, radius=0.14) for p in hid_positions])
        dots_o = VGroup(*[Dot(p, color=out_color, radius=0.14) for p in out_positions])
        return dots_in, dots_h, dots_o

    def _fwd_arrows(self, frm, to, color=BLUE):
        arrows = VGroup()
        for pf in frm:
            for pt in to:
                a = _arr(pf, pt, color=color, sw=1.5)
                if isinstance(a, Arrow):
                    arrows.add(a)
        return arrows

    def _back_arrows(self, frm, to, color=CORAL):
        arrows = VGroup()
        for pf in frm:
            for pt in to:
                a = _arr(pf, pt, color=color, sw=1.5)
                if isinstance(a, Arrow):
                    arrows.add(a)
        return arrows

    # =========================================================================
    # SECTION 1 — HOOK (target: 40 seconds)
    # =========================================================================
    def s1_hook(self):
        # Opening title
        t1 = Text("Backpropagation", font_size=52, color=WHITE)
        t2 = Text("How Neural Networks Actually Learn", font_size=26, color=BLUE)
        t1.move_to(UP * 1.0)
        t2.next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1), run_time=2)
        self.wait(1)
        self.play(FadeIn(t2), run_time=2)
        self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=1)
        self.wait(1)

        # Opening question
        q1 = Text("You build a neural network.", font_size=32, color=WHITE)
        q2 = Text("It makes terrible predictions.", font_size=32, color=WHITE)
        q3 = Text("How does it know what to fix?", font_size=32, color=YELL)
        q1.move_to(UP * 1.5)
        q2.next_to(q1, DOWN, buff=0.5)
        q3.next_to(q2, DOWN, buff=0.5)
        self.play(FadeIn(q1), run_time=2)
        self.wait(1)
        self.play(FadeIn(q2), run_time=2)
        self.wait(1)
        self.play(Write(q3), run_time=2)
        self.wait(2)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=1)
        self.wait(0.5)

        # Answer teaser
        ans = Text(
            "Backpropagation.\n\n"
            "Error flows forward to measure mistakes.\n"
            "Then gradients flow backward\n"
            "to fix each weight.",
            font_size=28, color=WHITE,
        )
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.35)
        self.play(FadeIn(ab), Write(ans), run_time=2)
        self.wait(3)

    # =========================================================================
    # SECTION 2 — GEOMETRIC INTUITION (target: 90 seconds)
    # =========================================================================
    def s2_geometry(self):
        sec_label(self, "How the Error Flows Back")

        # Network node positions
        inp = [LEFT * 4.5 + UP * 0.8, LEFT * 4.5, LEFT * 4.5 + DOWN * 0.8]
        hid = [LEFT * 1.5 + UP * 1.0, LEFT * 1.5, LEFT * 1.5 + DOWN * 1.0]
        out = [RIGHT * 1.5]

        dots_in, dots_h, dots_o = self._make_network(inp, hid, out)

        # Layer labels
        lbl_in = Text("Input\nLayer", font_size=20, color=BLUE)
        lbl_in.next_to(dots_in, DOWN, buff=0.3)
        lbl_h = Text("Hidden\nLayer", font_size=20, color=YELL)
        lbl_h.next_to(dots_h, DOWN, buff=0.3)
        lbl_o = Text("Output\nLayer", font_size=20, color=GREEN)
        lbl_o.next_to(dots_o, DOWN, buff=0.3)

        # STEP 1: Show the input layer
        self.play(FadeIn(dots_in), FadeIn(lbl_in), run_time=2)
        self.wait(2)

        # STEP 2: Draw forward connections input→hidden
        arrows_ih = self._fwd_arrows(inp, hid, color=BLUE)
        self.play(GrowFromCenter(arrows_ih), FadeIn(dots_h), FadeIn(lbl_h), run_time=2)
        self.wait(2)

        # STEP 3: Draw forward connections hidden→output
        arrows_ho = self._fwd_arrows(hid, out, color=BLUE)
        self.play(GrowFromCenter(arrows_ho), FadeIn(dots_o), FadeIn(lbl_o), run_time=2)
        self.wait(2)

        # STEP 4: Show prediction vs target
        pred_lbl = Text("Prediction: 0.9", font_size=24, color=GREEN)
        pred_lbl.next_to(dots_o, RIGHT, buff=0.4)
        target_lbl = Text("Target: 0.0", font_size=24, color=RED)
        target_lbl.next_to(pred_lbl, DOWN, buff=0.3)
        error_lbl = Text("Error = 0.9", font_size=24, color=CORAL)
        error_lbl.next_to(target_lbl, DOWN, buff=0.3)

        self.play(FadeIn(pred_lbl), run_time=2)
        self.wait(1)
        self.play(FadeIn(target_lbl), run_time=2)
        self.wait(1)
        self.play(FadeIn(error_lbl), run_time=2)
        self.wait(3)

        # STEP 5: Error flows BACKWARD — back arrows
        insight1 = Text("Now the error flows BACKWARD.", font_size=26, color=YELL)
        insight1.to_edge(UP, buff=0.4)
        bi = self._box(insight1, border=YELL)
        self.play(FadeIn(bi), Write(insight1), run_time=2)
        self.wait(2)

        # Backward arrows output→hidden
        back_oh = self._back_arrows(out, hid, color=CORAL)
        self.play(GrowFromCenter(back_oh), run_time=2)
        self.wait(2)

        # STEP 6: Backward arrows hidden→input
        back_hi = self._back_arrows(hid, inp, color=CORAL)
        self.play(GrowFromCenter(back_hi), run_time=2)
        self.wait(3)

        # Key insight highlight
        key = Text(
            "Each weight learns how much\nit contributed to the error.",
            font_size=26, color=YELL,
        )
        key.move_to(DOWN * 2.8)
        kb = self._box(key, border=YELL)
        self.play(FadeIn(kb), Write(key), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 3 — FORMAL NOTATION (target: 60 seconds)
    # =========================================================================
    def s3_notation(self):
        sec_label(self, "The Chain Rule Powers It All")

        # Step 1: Loss function
        step1 = Text("Loss L = (prediction - target)²", font_size=30, color=WHITE)
        step1.move_to(UP * 2.5)
        b1 = self._box(step1, border=BLUE)
        self.play(FadeIn(b1), Write(step1), run_time=2)
        self.wait(2)

        # Step 2: Chain rule formula
        step2 = Text("Chain Rule:", font_size=28, color=YELL)
        step2.move_to(UP * 1.3)
        b2 = self._box(step2, border=YELL)
        self.play(FadeIn(b2), Write(step2), run_time=2)
        self.wait(2)

        # Step 3: Gradient expression
        step3 = Text(
            "dL/dw  =  dL/da  x  da/dz  x  dz/dw",
            font_size=26, color=GREEN,
        )
        step3.move_to(UP * 0.1)
        b3 = self._box(step3, border=GREEN)
        self.play(FadeIn(b3), Write(step3), run_time=2)
        self.wait(3)

        # Step 4: Explain each symbol
        syms = Text(
            "dL/da  = how loss changes with activation\n"
            "da/dz  = derivative of activation function\n"
            "dz/dw  = how output changes with weight",
            font_size=22, color=WHITE,
        )
        syms.move_to(DOWN * 1.3)
        bs = self._box(syms, border=WHITE)
        self.play(FadeIn(bs), Write(syms), run_time=2)
        self.wait(3)

        # Step 5: Weight update rule
        update = Text(
            "Weight update:\n"
            "w  =  w  -  learning_rate  x  dL/dw",
            font_size=26, color=BLUE,
        )
        update.move_to(DOWN * 3.0)
        bu = self._box(update, border=BLUE)
        self.play(FadeIn(bu), Write(update), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 4 — WORKED EXAMPLE (target: 90 seconds)
    # =========================================================================
    def s4_example(self):
        sec_label(self, "Worked Example: One Weight")

        # Setup: simple 1-neuron network
        title = Text("Simple network: input=1, weight w=0.5", font_size=26, color=WHITE)
        title.to_edge(UP, buff=0.4)
        bt = self._box(title, border=BLUE)
        self.play(FadeIn(bt), Write(title), run_time=2)
        self.wait(1)

        # STEP 1: Forward pass
        step1 = Text(
            "STEP 1 — Forward Pass\n\n"
            "z = w x input = 0.5 x 1.0 = 0.5\n"
            "a = sigmoid(z) = sigmoid(0.5) = 0.62\n"
            "Prediction = 0.62",
            font_size=24, color=WHITE,
        )
        step1.move_to(UP * 1.0)
        b1 = self._box(step1, border=BLUE)
        self.play(FadeIn(b1), Write(step1), run_time=2)
        self.wait(2)
        self.play(FadeOut(b1), FadeOut(step1), run_time=1)
        self.wait(0.5)

        # STEP 2: Compute loss
        step2 = Text(
            "STEP 2 — Compute Loss\n\n"
            "Target = 0.0\n"
            "L = (0.62 - 0.0)^2 = 0.384",
            font_size=24, color=WHITE,
        )
        step2.move_to(UP * 1.0)
        b2 = self._box(step2, border=CORAL)
        self.play(FadeIn(b2), Write(step2), run_time=2)
        self.wait(2)
        self.play(FadeOut(b2), FadeOut(step2), run_time=1)
        self.wait(0.5)

        # STEP 3: Gradient of loss wrt prediction
        step3 = Text(
            "STEP 3 — dL/da\n\n"
            "dL/da = 2 x (a - target)\n"
            "      = 2 x (0.62 - 0.0)\n"
            "      = 1.24",
            font_size=24, color=WHITE,
        )
        step3.move_to(UP * 1.0)
        b3 = self._box(step3, border=YELL)
        self.play(FadeIn(b3), Write(step3), run_time=2)
        self.wait(2)
        self.play(FadeOut(b3), FadeOut(step3), run_time=1)
        self.wait(0.5)

        # STEP 4: Gradient wrt weight via chain rule
        step4 = Text(
            "STEP 4 — dL/dw (Chain Rule)\n\n"
            "da/dz = sigmoid'(0.5) = 0.235\n"
            "dz/dw = input = 1.0\n\n"
            "dL/dw = 1.24 x 0.235 x 1.0 = 0.291",
            font_size=24, color=WHITE,
        )
        step4.move_to(UP * 0.8)
        b4 = self._box(step4, border=GREEN)
        self.play(FadeIn(b4), Write(step4), run_time=2)
        self.wait(2)
        self.play(FadeOut(b4), FadeOut(step4), run_time=1)
        self.wait(0.5)

        # STEP 5: Update weight
        step5 = Text(
            "STEP 5 — Update Weight\n\n"
            "learning rate = 0.1\n\n"
            "w_new = 0.5 - 0.1 x 0.291\n"
            "      = 0.5 - 0.029\n"
            "      = 0.471",
            font_size=24, color=YELL,
        )
        step5.move_to(UP * 0.8)
        b5 = self._box(step5, border=YELL)
        self.play(FadeIn(b5), Write(step5), run_time=2)
        self.wait(2)
        self.play(FadeOut(b5), FadeOut(step5), run_time=1)
        self.wait(0.5)

        # Result
        result = Text(
            "Weight moved from 0.5 to 0.471.\n\n"
            "Repeat 1000 times = trained network.",
            font_size=26, color=YELL,
        )
        result.move_to(ORIGIN)
        br = self._box(result, border=YELL)
        self.play(FadeIn(br), Write(result), run_time=2)
        self.wait(3)
        self.play(FadeOut(br), FadeOut(result), run_time=1)
        self.wait(0.5)

        # One full training loop recap
        recap = Text(
            "One full training step:\n\n"
            "1. Forward pass — compute prediction\n"
            "2. Loss — measure how wrong we are\n"
            "3. Backward pass — chain rule all the way back\n"
            "4. Update — nudge every weight slightly\n\n"
            "After thousands of steps,\n"
            "the network learns to predict correctly.",
            font_size=22, color=WHITE,
        )
        recap.move_to(ORIGIN)
        br2 = self._box(recap, border=GREEN, buff=0.38)
        self.play(FadeIn(br2), Write(recap), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 5 — DEEPER INSIGHT (target: 60 seconds)
    # =========================================================================
    def s5_insight(self):
        sec_label(self, "Why Backpropagation Changed Everything")

        insight = Text(
            "Before 1986:\n"
            "No efficient way to train deep networks.\n\n"
            "After Rumelhart, Hinton, Williams:\n"
            "Backprop made deep learning possible.\n\n"
            "Every modern AI — GPT, image recognition,\n"
            "AlphaFold, self-driving — runs on backprop.",
            font_size=24, color=WHITE,
        )
        insight.move_to(UP * 0.5)
        bi = self._box(insight, border=BLUE, buff=0.38)
        self.play(FadeIn(bi), Write(insight), run_time=2)
        self.wait(3)
        self.play(FadeOut(bi), FadeOut(insight), run_time=1)
        self.wait(0.5)

        # Real-world visual
        apps = Text(
            "Where backprop lives:\n\n"
            "  Image recognition — millions of weights updated\n"
            "  Language models — billions of parameters\n"
            "  Drug discovery — protein structure prediction\n"
            "  Game playing — AlphaGo beat the world champion\n\n"
            "All trained by the same simple idea:\n"
            "measure error, flow gradients backward, update.",
            font_size=22, color=WHITE,
        )
        apps.move_to(ORIGIN)
        ba = self._box(apps, border=GREEN, buff=0.38)
        self.play(FadeIn(ba), Write(apps), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 6 — SUMMARY (target: 30 seconds)
    # =========================================================================
    def s6_summary(self):
        sec_label(self, "Summary")

        # Replay the key network visual with both arrows
        inp = [LEFT * 4.5 + UP * 0.8, LEFT * 4.5, LEFT * 4.5 + DOWN * 0.8]
        hid = [LEFT * 1.5 + UP * 1.0, LEFT * 1.5, LEFT * 1.5 + DOWN * 1.0]
        out = [RIGHT * 1.5]

        dots_in = VGroup(*[Dot(p, color=BLUE, radius=0.14) for p in inp])
        dots_h = VGroup(*[Dot(p, color=YELL, radius=0.14) for p in hid])
        dots_o = VGroup(*[Dot(p, color=GREEN, radius=0.14) for p in out])

        arrows_ih = self._fwd_arrows(inp, hid, color=BLUE)
        arrows_ho = self._fwd_arrows(hid, out, color=BLUE)
        back_oh = self._back_arrows(out, hid, color=CORAL)
        back_hi = self._back_arrows(hid, inp, color=CORAL)

        self.play(
            FadeIn(dots_in), FadeIn(dots_h), FadeIn(dots_o),
            GrowFromCenter(arrows_ih), GrowFromCenter(arrows_ho),
            run_time=2,
        )
        self.wait(1)
        self.play(GrowFromCenter(back_oh), GrowFromCenter(back_hi), run_time=2)
        self.wait(1)

        summary = Text(
            "Backpropagation\n\n"
            "  Forward: input flows to prediction\n"
            "  Loss: measure error at output\n"
            "  Backward: gradients via chain rule\n"
            "  Update: w = w - lr x dL/dw\n\n"
            "  Repeat until loss is minimized.",
            font_size=22, color=WHITE,
        )
        self._rp(summary, y=0.0, x=3.6)
        sb = self._box(summary, border=BLUE)
        self.play(FadeIn(sb), Write(summary), run_time=2)
        self.wait(6)
