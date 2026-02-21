"""ml_01_neural_networks.py — What is a Neural Network — Full 6-Section Scene
Target: 3+ minutes total animation time.
Uses Text/Cairo only — no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

CORAL = RED


def _arr(start, end, color=BLUE, sw=2.0):
    s = np.array(start)
    e = np.array(end)
    if np.linalg.norm(e - s) < 0.05:
        return VMobject()
    return Arrow(s, e, buff=0.05, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.15)


class NeuralNetworksScene(Scene):
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

    def _make_arrows(self, frm, to, color=BLUE):
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
        # Title
        t1 = Text("Neural Networks", font_size=56, color=WHITE)
        t2 = Text("Information Flowing Through Layers", font_size=26, color=BLUE)
        t1.move_to(UP * 1.0)
        t2.next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1), run_time=2)
        self.wait(1)
        self.play(FadeIn(t2), run_time=2)
        self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=1)
        self.wait(1)

        # Hook questions
        q1 = Text("Your brain has 86 billion neurons.", font_size=32, color=WHITE)
        q2 = Text("Each neuron fires or stays silent.", font_size=32, color=WHITE)
        q3 = Text("Together they recognize faces,\nlearn languages, solve problems.", font_size=28, color=YELL)
        q1.move_to(UP * 1.8)
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

        # Teaser
        teaser = Text(
            "Artificial neural networks\nborrow this same idea.\n\n"
            "Numbers flow in.\nNumbers transform layer by layer.\n"
            "Useful output comes out.",
            font_size=28, color=WHITE,
        )
        teaser.move_to(ORIGIN)
        tb = self._box(teaser, border=BLUE, buff=0.38)
        self.play(FadeIn(tb), Write(teaser), run_time=2)
        self.wait(5)

    # =========================================================================
    # SECTION 2 — GEOMETRIC INTUITION (target: 90 seconds)
    # =========================================================================
    def s2_geometry(self):
        sec_label(self, "Layer by Layer")

        # Node positions
        inp = [LEFT * 4.5 + UP * 0.8, LEFT * 4.5, LEFT * 4.5 + DOWN * 0.8]
        hid = [LEFT * 1.5 + UP * 1.0, LEFT * 1.5, LEFT * 1.5 + DOWN * 1.0]
        out = [RIGHT * 1.5 + UP * 0.4, RIGHT * 1.5 + DOWN * 0.4]

        dots_in = VGroup(*[Dot(p, color=BLUE, radius=0.14) for p in inp])
        dots_h  = VGroup(*[Dot(p, color=YELL, radius=0.14) for p in hid])
        dots_o  = VGroup(*[Dot(p, color=GREEN, radius=0.14) for p in out])

        lbl_in = Text("Input Layer\n3 neurons", font_size=18, color=BLUE)
        lbl_in.next_to(dots_in, DOWN, buff=0.3)
        lbl_h = Text("Hidden Layer\n3 neurons", font_size=18, color=YELL)
        lbl_h.next_to(dots_h, DOWN, buff=0.3)
        lbl_o = Text("Output Layer\n2 neurons", font_size=18, color=GREEN)
        lbl_o.next_to(dots_o, DOWN, buff=0.3)

        # STEP 1: Input layer
        self.play(FadeIn(dots_in), FadeIn(lbl_in), run_time=2)
        self.wait(2)

        r1 = Text("Each input neuron holds a number.\nFor images: pixel brightness.", font_size=22, color=WHITE)
        self._rp(r1, y=2.5, x=3.5)
        b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1), run_time=2)
        self.wait(2)

        # STEP 2: Connections to hidden layer
        arrows_ih = self._make_arrows(inp, hid, color=BLUE)
        self.play(GrowFromCenter(arrows_ih), FadeIn(dots_h), FadeIn(lbl_h), run_time=2)
        self.wait(2)

        r2 = Text("Each connection has a weight.\nWeights control how strongly\none neuron influences another.", font_size=22, color=WHITE)
        self._rp(r2, y=1.0, x=3.5)
        b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2)
        self.wait(2)

        # STEP 3: Connections to output layer
        arrows_ho = self._make_arrows(hid, out, color=YELL)
        self.play(GrowFromCenter(arrows_ho), FadeIn(dots_o), FadeIn(lbl_o), run_time=2)
        self.wait(2)

        r3 = Text("Output neurons give the answer.\nFor image classification:\none output per class.", font_size=22, color=WHITE)
        self._rp(r3, y=-1.0, x=3.5)
        b3 = self._box(r3, border=GREEN)
        self.play(FadeIn(b3), Write(r3), run_time=2)
        self.wait(2)

        # STEP 4: Show information flowing (flash arrows)
        self.play(
            arrows_ih.animate.set_color(WHITE),
            run_time=2,
        )
        self.wait(2)
        self.play(
            arrows_ho.animate.set_color(WHITE),
            run_time=2,
        )
        self.wait(2)

        # STEP 5: Highlight the hidden layer role
        highlight = Text(
            "The hidden layer finds PATTERNS\nthat the input can't see directly.",
            font_size=24, color=YELL,
        )
        highlight.move_to(DOWN * 3.0)
        bh = self._box(highlight, border=YELL)
        self.play(
            FadeOut(b1), FadeOut(r1),
            FadeOut(b2), FadeOut(r2),
            FadeOut(b3), FadeOut(r3),
            run_time=1,
        )
        self.play(
            dots_h.animate.set_color(YELL).scale(1.3),
            FadeIn(bh), Write(highlight),
            run_time=2,
        )
        self.wait(3)

        # STEP 6: Key insight
        key = Text(
            "More layers = more abstract patterns.\n"
            "Edge -> Shape -> Object -> Category",
            font_size=24, color=WHITE,
        )
        key.to_edge(UP, buff=0.4)
        bk = self._box(key, border=WHITE)
        self.play(FadeIn(bk), Write(key), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 3 — FORMAL NOTATION (target: 60 seconds)
    # =========================================================================
    def s3_notation(self):
        sec_label(self, "The Mathematics of a Layer")

        # Formula
        formula = Text("Layer output:   a = sigma( W x + b )", font_size=30, color=YELL)
        formula.move_to(UP * 2.5)
        bf = self._box(formula, border=YELL, buff=0.35)
        self.play(FadeIn(bf), Write(formula), run_time=2)
        self.wait(1)

        # Explain x
        sym_x = Text("x  =  input vector (numbers coming in)", font_size=26, color=BLUE)
        sym_x.move_to(UP * 1.3)
        bx = self._box(sym_x, border=BLUE)
        self.play(FadeIn(bx), Write(sym_x), run_time=2)
        self.wait(2)

        # Explain W
        sym_w = Text("W  =  weight matrix (what the network learned)", font_size=26, color=WHITE)
        sym_w.move_to(UP * 0.1)
        bw = self._box(sym_w, border=WHITE)
        self.play(FadeIn(bw), Write(sym_w), run_time=2)
        self.wait(2)

        # Explain b
        sym_b = Text("b  =  bias (shifts the output)", font_size=26, color=GREEN)
        sym_b.move_to(DOWN * 1.1)
        bb = self._box(sym_b, border=GREEN)
        self.play(FadeIn(bb), Write(sym_b), run_time=2)
        self.wait(2)

        # Explain sigma
        sym_s = Text("sigma  =  activation function\n(ReLU, sigmoid, tanh)", font_size=26, color=CORAL)
        sym_s.move_to(DOWN * 2.5)
        bs = self._box(sym_s, border=CORAL)
        self.play(FadeIn(bs), Write(sym_s), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 4 — WORKED EXAMPLE (target: 90 seconds)
    # =========================================================================
    def s4_example(self):
        sec_label(self, "One Neuron, Step by Step")

        # STEP 1: Setup
        step1 = Text(
            "STEP 1 — Setup\n\n"
            "One neuron with 2 inputs:\n"
            "  x1 = 0.5,  x2 = 0.3\n"
            "  w1 = 0.8,  w2 = 0.4\n"
            "  bias b = 0.1",
            font_size=24, color=WHITE,
        )
        step1.move_to(UP * 1.2)
        b1 = self._box(step1, border=BLUE)
        self.play(FadeIn(b1), Write(step1), run_time=2)
        self.wait(5)
        self.play(FadeOut(b1), FadeOut(step1), run_time=1)
        self.wait(0.5)

        # STEP 2: Weighted sum
        step2 = Text(
            "STEP 2 — Weighted Sum\n\n"
            "z = w1 x x1  +  w2 x x2  +  b\n"
            "z = 0.8 x 0.5  +  0.4 x 0.3  +  0.1\n"
            "z = 0.4  +  0.12  +  0.1\n"
            "z = 0.62",
            font_size=24, color=WHITE,
        )
        step2.move_to(UP * 1.0)
        b2 = self._box(step2, border=YELL)
        self.play(FadeIn(b2), Write(step2), run_time=2)
        self.wait(3)
        self.play(FadeOut(b2), FadeOut(step2), run_time=1)
        self.wait(0.5)

        # STEP 3: Activation function (ReLU)
        step3 = Text(
            "STEP 3 — Activation Function\n\n"
            "ReLU(z) = max(0, z)\n\n"
            "ReLU(0.62) = max(0, 0.62) = 0.62\n\n"
            "Neuron output = 0.62",
            font_size=24, color=WHITE,
        )
        step3.move_to(UP * 1.0)
        b3 = self._box(step3, border=GREEN)
        self.play(FadeIn(b3), Write(step3), run_time=2)
        self.wait(3)
        self.play(FadeOut(b3), FadeOut(step3), run_time=1)
        self.wait(0.5)

        # STEP 4: Why ReLU
        step4 = Text(
            "STEP 4 — Why Activation Functions?\n\n"
            "Without sigma:  output = Wx + b\n"
            "Any two layers collapse into one layer.\n\n"
            "With sigma:  network can learn\n"
            "non-linear boundaries.\n"
            "That's what makes deep learning powerful.",
            font_size=22, color=WHITE,
        )
        step4.move_to(UP * 0.6)
        b4 = self._box(step4, border=BLUE)
        self.play(FadeIn(b4), Write(step4), run_time=2)
        self.wait(3)
        self.play(FadeOut(b4), FadeOut(step4), run_time=1)
        self.wait(0.5)

        # STEP 5: Multiple layers
        step5 = Text(
            "STEP 5 — Stack the Layers\n\n"
            "Layer 1 output becomes Layer 2 input.\n"
            "Each layer refines the representation.\n\n"
            "With 3 layers and ReLU:\n"
            "the network can approximate\n"
            "any continuous function.",
            font_size=22, color=YELL,
        )
        step5.move_to(UP * 0.6)
        b5 = self._box(step5, border=YELL)
        self.play(FadeIn(b5), Write(step5), run_time=2)
        self.wait(4)

    # =========================================================================
    # SECTION 5 — DEEPER INSIGHT (target: 60 seconds)
    # =========================================================================
    def s5_insight(self):
        sec_label(self, "Universal Function Approximators")

        insight1 = Text(
            "The Universal Approximation Theorem:\n\n"
            "A neural network with even a single\n"
            "hidden layer (wide enough) can approximate\n"
            "ANY continuous function\n"
            "to arbitrary precision.",
            font_size=24, color=WHITE,
        )
        insight1.move_to(UP * 0.8)
        bi1 = self._box(insight1, border=BLUE, buff=0.38)
        self.play(FadeIn(bi1), Write(insight1), run_time=2)
        self.wait(3)
        self.play(FadeOut(bi1), FadeOut(insight1), run_time=1)
        self.wait(0.5)

        insight2 = Text(
            "Real-world applications:\n\n"
            "  Vision — ResNet identifies 1000 image classes\n"
            "  Language — GPT generates human text\n"
            "  Games — AlphaGo beats world champion\n"
            "  Science — AlphaFold solves protein folding\n"
            "  Medicine — neural nets detect cancer in scans\n\n"
            "All are neural networks with the same\n"
            "simple building block:  a = sigma(Wx + b)",
            font_size=21, color=WHITE,
        )
        insight2.move_to(ORIGIN)
        bi2 = self._box(insight2, border=GREEN, buff=0.38)
        self.play(FadeIn(bi2), Write(insight2), run_time=2)
        self.wait(5)
        self.play(FadeOut(bi2), FadeOut(insight2), run_time=1)
        self.wait(0.5)

        # Why depth matters
        depth = Text(
            "Why depth matters:\n\n"
            "A shallow network needs exponentially\n"
            "more neurons to match a deep network.\n\n"
            "Deep networks build hierarchy:\n"
            "  Layer 1 — pixels and edges\n"
            "  Layer 2 — shapes and textures\n"
            "  Layer 3 — parts of objects\n"
            "  Layer 4 — whole objects and scenes\n\n"
            "Each layer re-uses what previous layers learned.",
            font_size=20, color=WHITE,
        )
        depth.move_to(ORIGIN)
        bd = self._box(depth, border=BLUE, buff=0.38)
        self.play(FadeIn(bd), Write(depth), run_time=2)
        self.wait(5)

    # =========================================================================
    # SECTION 6 — SUMMARY (target: 30 seconds)
    # =========================================================================
    def s6_summary(self):
        sec_label(self, "Summary")

        # Replay the network
        inp = [LEFT * 4.5 + UP * 0.8, LEFT * 4.5, LEFT * 4.5 + DOWN * 0.8]
        hid = [LEFT * 1.5 + UP * 1.0, LEFT * 1.5, LEFT * 1.5 + DOWN * 1.0]
        out = [RIGHT * 1.5 + UP * 0.4, RIGHT * 1.5 + DOWN * 0.4]

        dots_in = VGroup(*[Dot(p, color=BLUE, radius=0.14) for p in inp])
        dots_h  = VGroup(*[Dot(p, color=YELL, radius=0.14) for p in hid])
        dots_o  = VGroup(*[Dot(p, color=GREEN, radius=0.14) for p in out])

        arrows_ih = self._make_arrows(inp, hid, color=BLUE)
        arrows_ho = self._make_arrows(hid, out, color=YELL)

        self.play(
            FadeIn(dots_in), GrowFromCenter(arrows_ih), FadeIn(dots_h),
            GrowFromCenter(arrows_ho), FadeIn(dots_o),
            run_time=2,
        )
        self.wait(1)

        summary = Text(
            "Neural Network\n\n"
            "  Layers of neurons\n"
            "  Each layer: a = sigma(Wx + b)\n"
            "  Input flows forward\n"
            "  Weights learned by backpropagation\n\n"
            "  More layers = more powerful patterns\n"
            "  Foundation of all modern AI",
            font_size=22, color=WHITE,
        )
        self._rp(summary, y=0.0, x=3.6)
        sb = self._box(summary, border=BLUE)
        self.play(FadeIn(sb), Write(summary), run_time=2)
        self.wait(8)
