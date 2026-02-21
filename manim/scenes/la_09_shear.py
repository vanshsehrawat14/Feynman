"""Feynman – Shear Transformation (Gold Standard) – 6-section, 3-5 min, Text/Cairo only."""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE, make_plane, vec
import numpy as np
AX_COLOR = "#888888"

class ShearScene(Scene):
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
        t = Text("Shear Transformations", font_size=44, color=WHITE).move_to(UP*0.5)
        t2 = Text("Tilting without scaling", font_size=26, color=BLUE).next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(t), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t), FadeOut(t2), run_time=0.5)
        q = Text("Imagine a stack of papers.\nPush the top sideways, bottom stays fixed.\nEach layer slides a little more than the one below.", font_size=26, color=WHITE).move_to(UP*1.0)
        ans = Text("This is a shear transformation.\nArea is preserved, but shape is distorted.", font_size=26, color=GREEN).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2.5); self.wait(2.3)
        self.play(Write(ans), run_time=2.0); self.wait(3.0)
        self.play(FadeOut(q), FadeOut(ans), run_time=0.5)
        intro = Text("Shear matrix (horizontal):\n\n  S = [[1, k],    applied to vector (x,y):\n       [0, 1]]    -> (x + k*y, y)\n\n  y-coordinates unchanged\n  x-coordinates shift by k*y", font_size=26, color=WHITE).move_to(ORIGIN)
        ib = self._box(intro, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(intro), run_time=2.5); self.wait(4.5)
    def s2_geometry(self):
        sec_label(self, "Visualizing Shear on a Grid")
        plane = make_plane()
        self.play(Create(plane), run_time=2.0); self.wait(0.8)
        r1 = Text("Before shear: unit square", font_size=24, color=WHITE)
        self._rp(r1, y=2.5); b1 = self._box(r1)
        self.play(FadeIn(b1), Write(r1), run_time=1.5)
        corners = [(-1,-1),(1,-1),(1,1),(-1,1)]
        square = Polygon(*[plane.c2p(x,y) for x,y in corners], color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
        self.play(Create(square), run_time=1.5); self.wait(1.8)
        k = 1.0
        sheared_corners = [(x + k*y, y) for x,y in corners]
        sheared = Polygon(*[plane.c2p(x,y) for x,y in sheared_corners], color=YELL, stroke_width=3, fill_color=YELL, fill_opacity=0.2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.3)
        r2 = Text("After shear (k=1):\nx -> x + y", font_size=24, color=YELL)
        self._rp(r2, y=2.5); b2 = self._box(r2, border=YELL)
        self.play(FadeIn(b2), Write(r2), Transform(square, sheared), run_time=2.5); self.wait(2.3)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3)
        r3 = Text("Area unchanged!\ndet([[1,k],[0,1]]) = 1", font_size=24, color=GREEN)
        self._rp(r3, y=2.5); b3 = self._box(r3, border=GREEN)
        self.play(FadeIn(b3), Write(r3), run_time=2.0); self.wait(4.0)
    def s3_notation(self):
        sec_label(self, "Shear Matrices")
        mats = Text("Horizontal shear (k):\n  S = [[1, k],  (x,y) -> (x+ky, y)\n       [0, 1]]\n\nVertical shear (k):\n  S = [[1, 0],  (x,y) -> (x, kx+y)\n       [k, 1]]\n\n3D shear (x by z):\n  S = [[1, 0, k],  (x,y,z) -> (x+kz, y, z)\n       [0, 1, 0],\n       [0, 0, 1]]", font_size=24, color=WHITE).move_to(UP*0.5)
        mb = self._box(mats, border=BLUE, buff=0.38)
        self.play(FadeIn(mb), Write(mats), run_time=2.5); self.wait(3.0)
        self.play(FadeOut(mb), FadeOut(mats), run_time=0.5)
        props = Text("Key properties of shear:\n\n  det(S) = 1  (area preserved in 2D)\n  Eigenvalues: both = 1\n  Not orthogonal (angles distorted)\n  Composition: S(k1) * S(k2) = S(k1+k2)\n  Inverse: S(-k) undoes shear", font_size=24, color=YELL).move_to(ORIGIN)
        pb = self._box(props, border=YELL, buff=0.38)
        self.play(FadeIn(pb), Write(props), run_time=2.5); self.wait(4.5)
    def s4_example(self):
        sec_label(self, "Example: Shear k=0.5 on (3, 2)")
        steps = [
            ("S = [[1, 0.5], [0, 1]],  v = (3, 2)", WHITE, 2.5),
            ("S * v = (1*3 + 0.5*2,  0*3 + 1*2)", BLUE, 1.7),
            ("      = (3 + 1.0,  2)", GREEN, 0.9),
            ("      = (4.0,  2)", YELL, 0.1),
            ("y unchanged: 2 -> 2", GREEN, -0.7),
            ("x shifted by k*y = 0.5*2 = 1.0", WHITE, -1.5),
            ("Area of unit square: still = 1", GREEN, -2.3),
        ]
        for txt, col, yp in steps:
            mob = Text(txt, font_size=26, color=col).move_to(UP*yp)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.8); self.wait(2.0)
        self.wait(3.5)
    def s5_insight(self):
        sec_label(self, "Where Shear Appears")
        ins = Text("Shear transforms appear everywhere:\n\n  Computer graphics: italicizing text!\n  (Fake italic = horizontal shear)\n\n  Stress/strain in materials:\n  (Material deforms under tangential force)\n\n  Image processing: perspective correction\n\n  LU decomposition: elimination steps are shears\n  (Row subtraction = shear transformation)\n\n  Crystal deformation in solid-state physics", font_size=22, color=WHITE).move_to(LEFT*0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        det_insight = Text("Deep insight: Shear has det=1.\n\nAll volume-preserving linear maps\nare products of shear matrices.\n\nSpecial Linear group SL(n):\n= all matrices with det=1\nGenerated entirely by elementary shears!\n\nThis makes shear the fundamental\nbuilding block of volume-preserving maps.", font_size=22, color=YELL).move_to(ORIGIN)
        db = self._box(det_insight, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(det_insight), run_time=2.5); self.wait(5.5)
    def s6_summary(self):
        sec_label(self, "Summary")
        plane = make_plane()
        corners = [(-1,-1),(1,-1),(1,1),(-1,1)]
        original = Polygon(*[plane.c2p(x,y) for x,y in corners], color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
        sheared_c = [(x+0.8*y,y) for x,y in corners]
        sheared = Polygon(*[plane.c2p(x,y) for x,y in sheared_c], color=YELL, stroke_width=3, fill_color=YELL, fill_opacity=0.2)
        self.play(Create(plane), Create(original), Create(sheared), run_time=2.0); self.wait(0.8)
        sm = Text("Shear  S = [[1,k],[0,1]]\n\n  (x,y) -> (x+ky, y)\n  Tilts shape, preserves area\n  det = 1 always\n\n  Found in: text italics,\n  LU decomposition, stress,\n  perspective correction\n\n  Builds all volume-preserving maps", font_size=19, color=WHITE)
        self._rp(sm, y=0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
