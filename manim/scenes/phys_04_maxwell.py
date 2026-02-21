"""Feynman – Maxwell Equations (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class MaxwellScene(Scene):
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
        self.wait(0.6)
    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)
    def _rp(self, mob, y=0.0, x=4.3):
        mob.move_to(RIGHT * x + UP * y); return mob
    def _axes(self, xr=(-0.3,4.5,1), yr=(-0.3,4.5,1)):
        return Axes(x_range=[*xr], y_range=[*yr], x_length=7.2, y_length=5.0,
            axis_config={"color": AX_COLOR,"stroke_width":2,"include_tip":True,"include_ticks":True}
        ).shift(LEFT*1.5+DOWN*0.5)

    def s1_hook(self):
        t = Text("Maxwell Equations", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("The laws governing all electromagnetic phenomena", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Light, radio, WiFi, MRI, electric motors.\nAll governed by four elegant equations\nwritten down by James Clerk Maxwell in 1865.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Maxwell unified electricity, magnetism, and optics.\nHe showed light IS an electromagnetic wave.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("4 equations. Complete theory of electromagnetism.\n\nGauss (E), Gauss (B), Faraday, Ampere-Maxwell.\nIn vacuum: wave solutions traveling at c = 1/sqrt(eps_0 mu_0)\nThis equals the measured speed of light!", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "The Four Laws")
        eqs = [
            ("1. Gauss's Law (E field):", WHITE, 2.5),
            ("   div(E) = rho/epsilon_0", BLUE, 1.7),
            ("   Electric field diverges from charges", BLUE, 1.1),
            ("2. Gauss's Law (B field):", WHITE, 0.3),
            ("   div(B) = 0", RED, -0.5),
            ("   No magnetic monopoles!", RED, -1.1),
        ]
        for txt, col, yp in eqs:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(1.6)
        self.wait(3.5)
    def s3_notation(self):
        sec_label(self, "Faraday and Ampere")
        eqs2 = [
            ("3. Faraday's Law:", WHITE, 2.5),
            ("   curl(E) = -dB/dt", YELL, 1.7),
            ("   Changing B creates E field (motors!)", YELL, 1.1),
            ("4. Ampere-Maxwell Law:", WHITE, 0.3),
            ("   curl(B) = mu_0 J + mu_0 eps_0 dE/dt", GREEN, -0.5),
            ("   Current OR changing E creates B field", GREEN, -1.1),
            ("Maxwell added the dE/dt term! -> wave eq.", BLUE, -1.9),
        ]
        for txt, col, yp in eqs2:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(1.6)
        self.wait(3.5)
    def s4_example(self):
        sec_label(self, "Wave Speed = Speed of Light")
        steps = [
            ("Combine Faraday + Ampere in vacuum:", WHITE, 2.8),
            ("curl(curl(E)) = -mu_0 eps_0 d^2E/dt^2", WHITE, 2.0),
            ("Wave equation: d^2E/dx^2 = (1/c^2) d^2E/dt^2", YELL, 1.2),
            ("c = 1/sqrt(mu_0 * eps_0)", YELL, 0.4),
            ("mu_0 = 4pi*10^-7,  eps_0 = 8.85*10^-12", BLUE, -0.4),
            ("c = 299,792,458 m/s", GREEN, -1.2),
            ("= measured speed of light! Light IS EM wave!", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=25, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Maxwell equations are relativistically covariant.\n\nEinstein noticed: if light travels at c for all observers,\ntime and space must mix -> special relativity.\n\nMaxwell's equations are the same for all inertial frames!\n(Unlike Newton's laws -- they had to be fixed.)\n\nFour equations in differential form:\n  2 div equations (sources)\n  2 curl equations (dynamics)\nAll of electromagnetism from these 4!", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications of Maxwell equations:\n\n  Antenna design: electromagnetic waves\n  Optical fiber: total internal reflection\n  MRI machines: magnetic resonance\n  Electric motors: Faraday induction\n  Wireless communication: all EM waves\n  Laser technology: stimulated emission\n  GPS: needs relativistic EM corrections\n\nEvery electronic device uses Maxwell implicitly!", font_size=21, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Maxwell Equations\n\n  1. div(E) = rho/eps_0  (electric sources)\n  2. div(B) = 0  (no magnetic monopoles)\n  3. curl(E) = -dB/dt  (Faraday)\n  4. curl(B) = mu_0 J + mu_0 eps_0 dE/dt  (Ampere)\n\n  Predict EM waves: c = 1/sqrt(mu_0 eps_0)\n  = measured speed of light\n\n  Complete theory of light, electricity, magnetism\n  Foundation of all modern technology", font_size=18, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
