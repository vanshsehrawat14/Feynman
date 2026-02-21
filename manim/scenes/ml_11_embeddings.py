"""ml_11_embeddings.py — Embeddings"""
from manim import *
from la_utils import *
import numpy as np


class EmbeddingsScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        sec_label(self, "Embeddings")
        plane = make_plane().scale(0.6).shift(LEFT * 2)
        self.play(Create(plane)); self.wait(0.5)
        cluster1 = VGroup(*[Dot(plane.c2p(0.5 + i*0.1, 1 + j*0.1), color=BLUE, radius=0.06) for i in range(3) for j in range(2)])
        cluster2 = VGroup(*[Dot(plane.c2p(-1 + i*0.1, -0.5 + j*0.1), color=YELL, radius=0.06) for i in range(3) for j in range(2)])
        self.play(FadeIn(cluster1), FadeIn(cluster2)); self.wait(0.5)
        txt = Text("Words as vectors.\nSimilar words cluster.", font_size=26, color=WHITE)
        txt.move_to(RIGHT * 2.5)
        bl = text_box(txt, border=BLUE)
        self.play(FadeIn(bl), Write(txt)); self.wait(3)
