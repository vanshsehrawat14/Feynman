"""ml_06_train_test.py — Train Test Split"""
from manim import *
from la_utils import *


class TrainTestScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Train Test Split")
        txt = Text(
            "Training on exam answers = memorization.\n\n"
            "Test set = unseen data.\n"
            "Evaluates true generalization.\n\n"
            "Split: 80% train, 20% test.",
            font_size=28, color=WHITE,
        )
        txt.move_to(ORIGIN)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(4)
