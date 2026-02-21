"""Feynman – The Cross Product (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class CrossProductScene(Scene):
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
        t = Text("The Cross Product", font_size=48, color=WHITE).move_to(UP*0.5)
        t2 = Text("Perpendicularity in 3D", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Two vectors define a plane.\nWhat vector is perpendicular to that plane?", font_size=28, color=WHITE).move_to(UP*1.0)
        ans = Text("The cross product gives you exactly that vector.\nAnd its magnitude = area of parallelogram.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.0); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("v x w = (vy*wz - vz*wy, vz*wx - vx*wz, vx*wy - vy*wx)\n\nResult is a VECTOR (unlike dot product = scalar)\n|v x w| = |v||w|sin(theta) = area of parallelogram\nDirection: right-hand rule", font_size=24, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "The Right-Hand Rule")
        text1 = Text("Cross product: v x w", font_size=32, color=BLUE).move_to(UP*2.5)
        self.play(Write(text1), run_time=1.5); self.wait(0.8)
        vtext = Text("v = (1, 0, 0)  [x-axis]", font_size=26, color=RED).move_to(UP*1.5)
        wtext = Text("w = (0, 1, 0)  [y-axis]", font_size=26, color=GREEN).next_to(vtext, DOWN, buff=0.4)
        self.play(Write(vtext), Write(wtext), run_time=2.0); self.wait(1.6)
        cross = Text("v x w = (0*0-0*1, 0*0-1*0, 1*1-0*0)\n      = (0, 0, 1)  [z-axis!]", font_size=26, color=YELL).next_to(wtext, DOWN, buff=0.4)
        self.play(Write(cross), run_time=2.0); self.wait(2.3)
        rhr = Text("Right-hand rule:\nCurl fingers from v to w\nThumb points in direction of v x w", font_size=26, color=WHITE).next_to(cross, DOWN, buff=0.5)
        self.play(Write(rhr), run_time=2.0); self.wait(2.3)
        anti = Text("Anti-commutative: w x v = -(v x w)\n(order matters! flip both vectors -> flip result)", font_size=24, color=RED).next_to(rhr, DOWN, buff=0.4)
        self.play(Write(anti), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Formal Definition and Properties")
        formula = Text("v x w = det | i    j    k  |\n            | vx   vy   vz |\n            | wx   wy   wz |", font_size=26, color=YELL).move_to(UP*2.0)
        fb = self._box(formula, border=YELL, buff=0.4)
        self.play(FadeIn(fb), Write(formula), run_time=2.5); self.wait(2.3)
        expanded = Text("= i(vy*wz - vz*wy)\n- j(vx*wz - vz*wx)\n+ k(vx*wy - vy*wx)", font_size=24, color=GREEN).next_to(formula, DOWN, buff=0.5)
        eb = self._box(expanded, border=GREEN, buff=0.3)
        self.play(FadeIn(eb), Write(expanded), run_time=2.0); self.wait(1.8)
        props = Text("Key properties:\n  Anti-commutative: v x w = -(w x v)\n  Not associative: (u x v) x w != u x (v x w)\n  Distributive: v x (w+u) = v x w + v x u\n  |v x w| = |v||w|sin(theta)\n  v x w = 0  iff  v and w are parallel", font_size=22, color=WHITE).next_to(expanded, DOWN, buff=0.4)
        pb = self._box(props, border=BLUE, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Example: v=(1,2,3), w=(4,5,6)")
        steps = [
            ("v = (1, 2, 3)   w = (4, 5, 6)", WHITE, 2.8),
            ("v x w: i component = 2*6 - 3*5 = 12-15 = -3", BLUE, 2.0),
            ("       j component = -(1*6 - 3*4) = -(6-12) = 6", GREEN, 1.2),
            ("       k component = 1*5 - 2*4 = 5-8 = -3", BLUE, 0.4),
            ("v x w = (-3, 6, -3)", YELL, -0.4),
            ("Check: v.(vxw) = 1*(-3)+2*6+3*(-3) = -3+12-9 = 0", GREEN, -1.2),
            ("And w.(vxw) = 4*(-3)+5*6+6*(-3) = 0  (perpendicular!)", GREEN, -2.0),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=24, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "Applications")
        ins = Text("Cross product powers 3D graphics:\n\n  Surface normals: n = v x w\n  (perpendicular to surface -> lighting calculations)\n\n  Physics: torque = r x F\n  Angular momentum: L = r x p\n  Magnetic force: F = q(v x B)\n\n  Computing area of triangle:\n  Area = 0.5 * |v x w|\n\n  Only defined in 3D (and 7D with octonions)", font_size=21, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        comp = Text("Dot vs Cross product:\n\n  Dot product:   v . w = scalar\n    -> measures alignment, projection\n    -> works in any dimension\n\n  Cross product: v x w = vector\n    -> gives perpendicular direction\n    -> measures area, rotation axis\n    -> only in 3D!\n\n  Together they completely describe 3D geometry.", font_size=22, color=YELL).move_to(ORIGIN)
        cb = self._box(comp, border=YELL, buff=0.38)
        self.play(FadeIn(cb), Write(comp), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        sm = Text("Cross Product  v x w\n\n  v x w = (vy*wz-vz*wy, vz*wx-vx*wz, vx*wy-vy*wx)\n  |v x w| = |v||w|sin(theta)\n\n  PERPENDICULAR to both v and w\n  Anti-commutative: w x v = -(v x w)\n  Magnitude = parallelogram area\n\n  Applications:\n  3D normals, torque, magnetic force,\n  triangle area, rotation axes", font_size=19, color=WHITE).move_to(ORIGIN)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
