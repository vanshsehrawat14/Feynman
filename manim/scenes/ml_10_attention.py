"""ml_10_attention.py — Attention Mechanism"""
from manim import *
from la_utils import *


class AttentionScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Attention Mechanism")
        txt = Text(
            "Which words to focus on?\n\n"
            "Transformers compute attention scores.\n"
            "Each word attends to relevant others.\n"
            "Enables understanding context.",
            font_size=26, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=YELL)
        self.play(FadeIn(bl), Write(txt)); self.wait(4)
