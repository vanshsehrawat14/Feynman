"""
Feynman – Game Theory (Gold Standard)
6-section narrative, 3-5 minutes. Text/Cairo only, no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

AX_COLOR = "#888888"

class GameTheoryScene(Scene):
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

    def _mk_axes(self, xr=(-0.5, 4.5, 1), yr=(-0.5, 4.5, 1)):
        return Axes(
            x_range=[*xr], y_range=[*yr],
            x_length=7.0, y_length=5.0,
            axis_config={"color": AX_COLOR, "stroke_width": 2,
                         "include_tip": True, "include_ticks": True},
        ).shift(LEFT * 1.5 + DOWN * 0.5)

    def s1_hook(self):
        t1 = Text("Game Theory", font_size=52, color=WHITE)
        t2 = Text("Strategic Decision Making", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        q1 = Text("Two suspects. Separate interrogation rooms.", font_size=28, color=WHITE)
        q2 = Text("Both stay silent: 1 year each.", font_size=26, color=GREEN)
        q3 = Text("One confesses, one stays silent: 0 vs 10 years.", font_size=26, color=YELL)
        q4 = Text("Both confess: 5 years each.", font_size=26, color=RED)
        q1.move_to(UP * 2.0); q2.next_to(q1, DOWN, buff=0.4)
        q3.next_to(q2, DOWN, buff=0.3); q4.next_to(q3, DOWN, buff=0.3)
        for m in [q1, q2, q3, q4]:
            self.play(Write(m), run_time=1.5); self.wait(1.6)
        self.wait(2.3)
        self.play(*[FadeOut(m) for m in [q1,q2,q3,q4]], run_time=0.5)
        ans = Text(
            "What should each prisoner do?\n\n"
            "Game theory reveals the answer --\n"
            "and it is not what you might expect.",
            font_size=28, color=WHITE)
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.0); self.wait(4.5)

    def s2_geometry(self):
        sec_label(self, "The Payoff Matrix")
        header = Text("Prisoner B stays silent    Prisoner B confesses", font_size=20, color=WHITE)
        header.move_to(UP * 2.8 + RIGHT * 1.0)
        self.play(Write(header), run_time=2.0); self.wait(0.8)

        row1h = Text("Prisoner A\nstays silent", font_size=20, color=WHITE).move_to(LEFT * 3.5 + UP * 1.0)
        row2h = Text("Prisoner A\nconfesses", font_size=20, color=WHITE).move_to(LEFT * 3.5 + DOWN * 0.8)
        self.play(Write(row1h), Write(row2h), run_time=2.0); self.wait(0.8)

        cells = [
            (UP*1.0 + LEFT*0.5, "-1, -1", GREEN, "Both silent (best!)"),
            (UP*1.0 + RIGHT*2.5, "-10, 0", RED, "A stays, B confesses"),
            (DOWN*0.8 + LEFT*0.5, "0, -10", YELL, "A confesses, B stays"),
            (DOWN*0.8 + RIGHT*2.5, "-5, -5", RED, "Both confess (Nash!)"),
        ]
        for pos, txt, col, desc in cells:
            mob = Text(txt, font_size=24, color=col).move_to(pos)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(1.6)
        self.wait(3.5)

    def s3_notation(self):
        sec_label(self, "Nash Equilibrium")
        defn = Text(
            "Nash Equilibrium:\n\n"
            "  A strategy profile where NO player can\n"
            "  improve their outcome by changing their\n"
            "  strategy ALONE.\n\n"
            "  Named after John Nash (Nobel Prize 1994)\n"
            "  (A Beautiful Mind)",
            font_size=24, color=WHITE)
        defn.move_to(UP * 1.0)
        db = self._box(defn, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(defn), run_time=2.5); self.wait(3.0)

        nash = Text(
            "In the Prisoner Dilemma:\n"
            "  Both confessing IS the Nash equilibrium!\n\n"
            "  If B confesses: A should confess (5 < 10 years)\n"
            "  If B stays silent: A should confess (0 < 1 year)\n\n"
            "  Confessing is a DOMINANT STRATEGY for A\n"
            "  (and by symmetry, for B too).",
            font_size=22, color=RED)
        nash.move_to(DOWN * 1.0)
        nb = self._box(nash, border=RED, buff=0.35)
        self.play(FadeIn(nb), Write(nash), run_time=2.5); self.wait(4.5)

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
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(1.8)
        self.wait(3.5)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Rational individuals -> collectively bad outcome!\n\n"
            "  This is the tragedy of game theory --\n"
            "  rational self-interest does not always\n"
            "  lead to the best collective outcome.\n\n"
            "  Applications:\n"
            "  Arms races (countries all arm themselves)\n"
            "  Climate change (nations overpollute)\n"
            "  Auctions (bidding strategy)\n"
            "  Evolutionary biology (fitness strategies)\n"
            "  AI agents negotiating and competing",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        types_text = Text(
            "Other game types:\n\n"
            "  Zero-sum: one player wins, other loses\n"
            "    (chess, poker, rock-paper-scissors)\n\n"
            "  Coordination: both benefit from aligning\n"
            "    (driving on same side of road)\n\n"
            "  Repeated games: cooperation can emerge!\n"
            "    (tit-for-tat strategy)\n\n"
            "  Mixed strategies: randomize to prevent exploitation",
            font_size=22, color=WHITE)
        types_text.move_to(ORIGIN)
        tb = self._box(types_text, border=YELL, buff=0.38)
        self.play(FadeIn(tb), Write(types_text), run_time=2.5); self.wait(5.5)

    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text(
            "Game Theory\n\n"
            "  Models strategic interaction between agents\n\n"
            "  Nash Equilibrium:\n"
            "  No player gains by changing strategy alone\n\n"
            "  Prisoner Dilemma:\n"
            "  Rational play -> collectively bad outcome\n\n"
            "  Dominant strategy: best regardless of others\n\n"
            "  Applications: economics, AI, biology,\n"
            "  auctions, negotiations, climate policy",
            font_size=20, color=WHITE)
        sm.move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
