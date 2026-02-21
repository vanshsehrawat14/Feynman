"""Feynman – Electromagnetic Induction (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class InductionScene(Scene):
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
        t = Text("Electromagnetic Induction", font_size=40, color=WHITE).move_to(UP*0.5)
        t2 = Text("Faraday discovery that powers the world", font_size=22, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Move a magnet through a coil of wire.\nA current appears from nothing!\nNo battery. No connection to power.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("Faraday discovered this in 1831.\nChanging magnetic flux INDUCES a voltage.\nThis powers every generator on Earth.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Faraday Law: EMF = -d(Phi_B)/dt\n\n  EMF = induced voltage (electromotive force)\n  Phi_B = magnetic flux through the loop\n       = B dot A = B*A*cos(theta)\n\nThe minus sign: Lenz law (opposes the change)", font_size=25, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Magnetic Flux and Induction")
        ax = self._axes(xr=(-0.3,6,1), yr=(-0.3,4,1))
        t = ValueTracker(0)
        B_curve = ax.plot(lambda x: 2*np.sin(x), x_range=[0,5.5], color=BLUE, stroke_width=3)
        self.play(Create(ax), run_time=1.5)
        self.play(Create(B_curve), run_time=2.0); self.wait(0.8)
        r1 = Text("B(t) = B0 sin(t)  (alternating B field)", font_size=22, color=BLUE)
        self._rp(r1, y=2.5); b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1), run_time=1.5); self.wait(2.3)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        emf_curve = ax.plot(lambda x: -2*np.cos(x), x_range=[0,5.5], color=YELL, stroke_width=3)
        self.play(Create(emf_curve), run_time=2.0); self.wait(0.8)
        r2 = Text("EMF = -dB/dt = -B0 cos(t)\n90 degree phase shift!", font_size=22, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Faraday Law and Lenz Law")
        faraday = Text("Faraday's Law:\n  EMF = -N * d(Phi_B)/dt\n  N = number of turns in coil\n  Phi_B = integral(B . dA)  over surface\n\nLenz Law (explains the minus sign):\n  Induced current opposes the change!\n  (Nature resists change to flux)", font_size=24, color=WHITE).move_to(UP*0.8)
        fb = self._box(faraday, border=BLUE, buff=0.38)
        self.play(FadeIn(fb), Write(faraday), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(fb), FadeOut(faraday), run_time=0.5)
        maxwell3 = Text("Maxwell 3rd equation:\n  curl(E) = -dB/dt\n\nThis IS Faraday law in differential form!\nChanging B creates circulating E field\n(even without a wire -- the field exists in space)\n\nWith wire: circulating E drives current = induction.", font_size=23, color=YELL).move_to(ORIGIN)
        mb = self._box(maxwell3, border=YELL, buff=0.38)
        self.play(FadeIn(mb), Write(maxwell3), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Example: Generator Calculation")
        steps = [
            ("Coil: N=100 turns, area A=0.01 m^2", WHITE, 2.8),
            ("B rotates: B(t) = 1.0 * sin(120*pi*t)  [60 Hz]", BLUE, 2.0),
            ("Phi_B = N*A*B = 100*0.01*sin(120*pi*t)", WHITE, 1.2),
            ("Phi_B = sin(120*pi*t) Wb (Weber)", WHITE, 0.4),
            ("EMF = -d(Phi_B)/dt = -120*pi*cos(120*pi*t)", YELL, -0.4),
            ("Peak EMF = 120*pi ~ 377 V", GREEN, -1.2),
            ("This is how AC power plants generate 60 Hz!", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text("Induction is the bridge between electricity and magnetism:\n\n  Faraday (1831): moving magnet -> current\n  Ampere: current -> magnetic field\n  Together: electricity and magnetism are coupled!\n\n  Maxwell added dE/dt term to Ampere law,\n  creating displacement current.\n  Result: self-sustaining EM waves -> light!\n\n  Faraday and Maxwell together = electromagnetic theory", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        apps = Text("Applications of electromagnetic induction:\n\n  Generators: rotating coil in B field -> AC power\n  Transformers: change voltage/current (power grid)\n  Electric motors: reverse of generator\n  Wireless charging: inductive charging (Qi)\n  MRI: NMR uses Faraday induction\n  Metal detectors: eddy current induction\n  Guitar pickup: vibrating string inductance\n  RFID cards: inductive coupling", font_size=21, color=YELL).move_to(ORIGIN)
        ab = self._box(apps, border=YELL, buff=0.38)
        self.play(FadeIn(ab), Write(apps), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Electromagnetic Induction\n\n  EMF = -N * d(Phi_B)/dt  (Faraday)\n  Phi_B = B * A * cos(theta)\n\n  Lenz law: opposes the change (minus sign)\n\n  Maxwell 3: curl(E) = -dB/dt\n  (field form of Faraday law)\n\n  Applications:\n  Generators, transformers, motors,\n  wireless charging, MRI, RFID\n\n  Powers all electrical civilization", font_size=18, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
