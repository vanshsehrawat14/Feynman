"""la_16_eigen.py — Eigenvalues & Eigenvectors  (Gold Standard)

6-section narrative structure, target ≈ 4–5 minutes.
Strict zone discipline: left half = visuals, right half = text.
All Manim Text() — no LaTeX.  Matrix M = [[3,1],[0,2]].
"""
from manim import *
from la_utils import *
import numpy as np


# ── helpers ──────────────────────────────────────────────────────────────────

def _mk_plane():
    """Left-zone plane: default range, scaled so right edge ≈ x=0."""
    return make_plane().scale(0.72).shift(LEFT * 2.6)


def _arr(plane, start, end, color=BLUE, sw=3, tr=0.18):
    """Safe arrow on plane; VMobject() guard for zero-length."""
    s = plane.c2p(*start)
    e = plane.c2p(*end)
    if np.linalg.norm(e - s) < 0.08:
        return VMobject()
    return Arrow(s, e, buff=0, color=color,
                 stroke_width=sw,
                 max_tip_length_to_length_ratio=tr)


# ── Scene ─────────────────────────────────────────────────────────────────────

class EigenScene(Scene):
    M = np.array([[3, 1], [0, 2]], dtype=float)

    # ── Lifecycle ────────────────────────────────────────────────────────
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

    # ── Utility ──────────────────────────────────────────────────────────
    def _fade_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)
        self.wait(0.3)

    def _sec(self, title):
        sec_label(self, title)

    def _box(self, mob, border=WHITE, buff=0.28):
        return text_box(mob, border=border, buff=buff)

    def _rp(self, mob, y=0.0, x=4.1):
        """Position mob in the right text panel."""
        mob.move_to(RIGHT * x + UP * y)
        return mob

    # ── Section 1 — Hook (~38 s) ─────────────────────────────────────────
    def s1_hook(self):
        # Title card
        t1 = Text("Eigenvalues & Eigenvectors", font_size=46, color=WHITE)
        t2 = Text("The Hidden Skeleton of Linear Transformations",
                  font_size=24, color=BLUE)
        t1.move_to(UP * 0.5)
        t2.next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1), run_time=1)
        self.wait(0.4)
        self.play(FadeIn(t2), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        self.wait(0.4)

        # Hook question
        q1 = Text("What if I told you...", font_size=44, color=WHITE)
        q2 = Text("when you transform space,", font_size=44, color=WHITE)
        q3 = Text("some vectors refuse to change direction?",
                  font_size=36, color=YELL)
        q1.move_to(UP * 1.5)
        q2.next_to(q1, DOWN, buff=0.5)
        q3.next_to(q2, DOWN, buff=0.5)
        self.play(FadeIn(q1), run_time=1.0);  self.wait(0.5)
        self.play(FadeIn(q2), run_time=1.0);  self.wait(0.5)
        self.play(Write(q3), run_time=1.5);   self.wait(2.5)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q3), run_time=0.5)
        self.wait(0.4)

        # Left-zone plane
        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5)
        self.wait(0.5)

        # Two vectors: one random (coral), one eigenvector (yellow)
        vn = _arr(plane, (0, 0), (0.7, 1.1), RED, sw=3)
        ve = _arr(plane, (0, 0), (1.4, 0.0), YELL, sw=5)

        ln = Text("A random vector", font_size=24, color=RED)
        le = Text("A mysterious one...", font_size=24, color=YELL)
        self._rp(ln, y=1.5)
        self._rp(le, y=0.1)
        bn = self._box(ln, border=RED,  buff=0.24)
        be = self._box(le, border=YELL, buff=0.24)

        self.play(GrowArrow(vn), run_time=0.8); self.wait(0.3)
        self.play(FadeIn(bn), Write(ln))
        self.wait(0.3)
        self.play(GrowArrow(ve), run_time=0.8); self.wait(0.3)
        self.play(FadeIn(be), Write(le))
        self.wait(0.8)

        # Fade right labels before transform (rule: fade text before grid transform)
        self.play(FadeOut(bn), FadeOut(ln), FadeOut(be), FadeOut(le), run_time=0.4)
        self.wait(0.3)

        tl = Text("Applying transformation M...", font_size=26, color=BLUE)
        self._rp(tl, y=0.5)
        tb = self._box(tl, border=BLUE, buff=0.24)
        self.play(FadeIn(tb), Write(tl)); self.wait(0.5)

        tn = self.M @ np.array([0.7, 1.1])
        te = self.M @ np.array([1.4, 0.0])
        vn2 = _arr(plane, (0, 0), tuple(tn.tolist()), RED,  sw=3)
        ve2 = _arr(plane, (0, 0), tuple(te.tolist()), YELL, sw=5)
        self.play(Transform(vn, vn2), Transform(ve, ve2), run_time=3)
        self.wait(1.5)
        self.play(FadeOut(tb), FadeOut(tl), run_time=0.3); self.wait(0.3)

        # Observations in right zone
        o1 = Text("Red vector changed direction.", font_size=24, color=RED)
        o2 = Text("Yellow vector only got longer!", font_size=24, color=YELL)
        self._rp(o1, y=1.4)
        self._rp(o2, y=0.0)
        b1 = self._box(o1, border=RED,  buff=0.22)
        b2 = self._box(o2, border=YELL, buff=0.22)
        self.play(FadeIn(b1), Write(o1)); self.wait(0.5)
        self.play(FadeIn(b2), Write(o2)); self.wait(3)

    # ── Section 2 — Geometric Intuition (~70 s) ──────────────────────────
    def s2_geometry(self):
        self._sec("Geometric Intuition")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.5); self.wait(0.5)

        # 8 unit vectors
        n = 8
        tips = [(np.cos(2 * PI * i / n), np.sin(2 * PI * i / n)) for i in range(n)]
        arrows = [a for a in [_arr(plane, (0, 0), t, BLUE, sw=2) for t in tips]
                  if isinstance(a, Arrow)]

        self.play(AnimationGroup(*[GrowArrow(a) for a in arrows], lag_ratio=0.1),
                  run_time=1.5); self.wait(0.5)

        r1 = Text("Many vectors.\nMany directions.", font_size=26, color=BLUE)
        self._rp(r1, y=1.5)
        b1 = self._box(r1, border=BLUE)
        self.play(FadeIn(b1), Write(r1)); self.wait(2)
        self.play(FadeOut(b1), FadeOut(r1), run_time=0.4); self.wait(0.3)

        # Apply transformation
        r2 = Text("Now apply\ntransformation M...", font_size=26, color=WHITE)
        self._rp(r2, y=1.5)
        b2 = self._box(r2, border=WHITE)
        self.play(FadeIn(b2), Write(r2)); self.wait(0.8)
        self.play(FadeOut(b2), FadeOut(r2), run_time=0.3); self.wait(0.2)

        trans_tips = [(self.M @ np.array(t)).tolist() for t in tips]
        arrows_t = [_arr(plane, (0, 0), tuple(tt), RED, sw=2)
                    for tt in trans_tips]
        pairs = [(arrows[i], arrows_t[i])
                 for i in range(min(len(arrows), len(arrows_t)))
                 if isinstance(arrows_t[i], Arrow)]
        self.play(*[Transform(a, b) for a, b in pairs], run_time=4)
        self.wait(1.5)

        r3 = Text("Every vector changed direction.\nThey all rotated.", font_size=26, color=RED)
        self._rp(r3, y=1.5)
        b3 = self._box(r3, border=RED)
        self.play(FadeIn(b3), Write(r3)); self.wait(2.5)
        self.play(*[FadeOut(a) for a in arrows], FadeOut(b3), FadeOut(r3),
                  run_time=0.5); self.wait(0.4)

        # The question
        q = Text("Is there any vector that\nkeeps its original direction?\nA vector that only scales?",
                 font_size=26, color=YELL)
        self._rp(q, y=0.8)
        qb = self._box(q, border=YELL)
        self.play(FadeIn(qb), Write(q), run_time=1.5); self.wait(3)
        self.play(FadeOut(qb), FadeOut(q), run_time=0.4); self.wait(0.3)

        # Test a non-eigenvector (builds suspense)
        rt = Text("Let's try this one...", font_size=26, color=WHITE)
        self._rp(rt, y=1.8)
        bt = self._box(rt, border=WHITE)
        self.play(FadeIn(bt), Write(rt)); self.wait(0.5)

        vtip = (0.5, 1.0)
        vtip_t = tuple((self.M @ np.array(vtip)).tolist())
        at = _arr(plane, (0, 0), vtip,   BLUE, sw=3)
        at2 = _arr(plane, (0, 0), vtip_t, RED,  sw=3)
        self.play(GrowArrow(at), run_time=0.8); self.wait(0.4)
        self.play(FadeOut(bt), FadeOut(rt), run_time=0.3); self.wait(0.2)

        rno = Text("After M...", font_size=26, color=WHITE)
        self._rp(rno, y=1.8)
        bno = self._box(rno, border=WHITE)
        self.play(FadeIn(bno), Write(rno)); self.wait(0.4)
        self.play(Transform(at, at2), run_time=2.5); self.wait(0.5)
        self.play(FadeOut(bno), FadeOut(rno), run_time=0.3); self.wait(0.2)

        rnope = Text("It rotated. Not this one.", font_size=26, color=RED)
        self._rp(rnope, y=1.8)
        bnope = self._box(rnope, border=RED)
        self.play(FadeIn(bnope), Write(rnope)); self.wait(2)
        self.play(FadeOut(bnope), FadeOut(rnope), FadeOut(at), run_time=0.4)
        self.wait(0.3)

        # Reveal eigenvectors
        rev = Text("But these two are different...", font_size=26, color=YELL)
        self._rp(rev, y=2.0)
        brev = self._box(rev, border=YELL)
        self.play(FadeIn(brev), Write(rev)); self.wait(0.5)

        e1 = _arr(plane, (0, 0), (1.3, 0.0), YELL, sw=5)
        e2 = _arr(plane, (0, 0), (1.0, -1.0), YELL, sw=5)
        self.play(GrowArrow(e1), run_time=1.0); self.wait(0.4)
        self.play(GrowArrow(e2), run_time=1.0); self.wait(1.5)

        watch = Text("Watch very carefully...", font_size=24, color=WHITE)
        self._rp(watch, y=0.9)
        bwatch = self._box(watch, border=WHITE, buff=0.24)
        self.play(FadeOut(brev), FadeOut(rev), FadeIn(bwatch), Write(watch))
        self.wait(1)

        # Transform eigenvectors (slow) — they only scale!
        te1 = self.M @ np.array([1.3, 0.0])   # → [3.9, 0.0]
        te2 = self.M @ np.array([1.0, -1.0])  # → [2.0, -2.0]
        e1t = _arr(plane, (0, 0), tuple(te1.tolist()), YELL, sw=5)
        e2t = _arr(plane, (0, 0), tuple(te2.tolist()), YELL, sw=5)

        self.play(FadeOut(bwatch), FadeOut(watch), run_time=0.3); self.wait(0.2)

        rscale = Text("ONLY SCALING.\nNo rotation at all.", font_size=28, color=YELL)
        self._rp(rscale, y=2.0)
        bscale = self._box(rscale, border=YELL)
        self.play(FadeIn(bscale), Write(rscale)); self.wait(0.5)

        self.play(Transform(e1, e1t), Transform(e2, e2t), run_time=4)
        self.wait(3)
        self.play(FadeOut(bscale), FadeOut(rscale), run_time=0.4); self.wait(0.3)

        # Label with eigenvalues — right zone only
        lam_lbl = Text(
            "These are EIGENVECTORS.\n\n"
            "v\u2081 = [1, 0]\n"
            "  \u2192 scaled by \u03bb\u2081 = 3\n\n"
            "v\u2082 = [1, \u22121]\n"
            "  \u2192 scaled by \u03bb\u2082 = 2\n\n"
            "The scale factors are EIGENVALUES.",
            font_size=21, color=YELL,
        )
        self._rp(lam_lbl, y=0.3)
        lb = self._box(lam_lbl, border=YELL)
        self.play(FadeIn(lb), Write(lam_lbl), run_time=2); self.wait(4)

    # ── Section 3 — Formal Notation (~55 s) ──────────────────────────────
    def s3_notation(self):
        self._sec("The Formal Definition")

        # Main equation — top zone, centered
        eq = Text("A v  =  \u03bb v", font_size=72, color=GREEN)
        eq.move_to(UP * 2.3)
        self.play(Write(eq), run_time=2.5); self.wait(1)

        # Three symbol boxes explaining each symbol
        sA   = Text("A",  font_size=52, color=BLUE)
        sv   = Text("v",  font_size=52, color=YELL)
        slam = Text("\u03bb", font_size=52, color=GREEN)
        sA.move_to(LEFT  * 3.8 + UP * 0.3)
        sv.move_to(ORIGIN        + UP * 0.3)
        slam.move_to(RIGHT * 3.8 + UP * 0.3)

        dA   = Text("the matrix\n(the transformation)", font_size=21, color=BLUE)
        dv   = Text("the eigenvector\n(special direction)",  font_size=21, color=YELL)
        dlam = Text("the eigenvalue\n(scaling factor)",      font_size=21, color=GREEN)
        dA.next_to(sA,   DOWN, buff=0.28)
        dv.next_to(sv,   DOWN, buff=0.28)
        dlam.next_to(slam, DOWN, buff=0.28)

        gA   = VGroup(sA,   dA)
        gv   = VGroup(sv,   dv)
        glam = VGroup(slam, dlam)

        bA   = self._box(gA,   border=BLUE,  buff=0.28)
        bv   = self._box(gv,   border=YELL,  buff=0.28)
        blam = self._box(glam, border=GREEN, buff=0.28)

        self.play(FadeIn(bA),   FadeIn(sA),   Write(dA));   self.wait(0.6)
        self.play(FadeIn(bv),   FadeIn(sv),   Write(dv));   self.wait(0.6)
        self.play(FadeIn(blam), FadeIn(slam), Write(dlam)); self.wait(2.5)

        self.play(
            FadeOut(bA),  FadeOut(sA),   FadeOut(dA),
            FadeOut(bv),  FadeOut(sv),   FadeOut(dv),
            FadeOut(blam), FadeOut(slam), FadeOut(dlam),
            run_time=0.5,
        )
        self.wait(0.3)

        # Key insight
        insight = Text(
            '"Applying A to v only scales it.\n'
            ' It never rotates."',
            font_size=32, color=WHITE,
        )
        insight.move_to(DOWN * 0.2)
        ib = self._box(insight, border=WHITE, buff=0.35)
        self.play(FadeIn(ib), Write(insight), run_time=1.5); self.wait(3)
        self.play(FadeOut(ib), FadeOut(insight), FadeOut(eq), run_time=0.5)
        self.wait(0.4)

        # Characteristic equation
        cq = Text("How do we FIND the eigenvalues?", font_size=34, color=BLUE)
        cq.move_to(UP * 2.3)
        self.play(Write(cq), run_time=1); self.wait(0.5)

        ce = Text("det( A  \u2212  \u03bbI )  =  0", font_size=56, color=GREEN)
        ce.move_to(UP * 0.7)
        self.play(Write(ce), run_time=2); self.wait(0.5)

        cn = Text("The Characteristic Equation", font_size=28, color=WHITE)
        cn.move_to(DOWN * 0.9)
        cnb = self._box(cn, border=WHITE, buff=0.28)
        self.play(FadeIn(cnb), Write(cn)); self.wait(2.5)

    # ── Section 4 — Worked Example (~70 s) ───────────────────────────────
    def s4_example(self):
        self._sec("Worked Example")

        # Right zone: matrix display
        mh = Text("Given matrix A:", font_size=28, color=WHITE)
        mv = Text("[ 3   1 ]\n[ 0   2 ]", font_size=38, color=BLUE)
        mh.move_to(RIGHT * 3.5 + UP * 2.9)
        mv.move_to(RIGHT * 3.5 + UP * 1.8)
        mb = self._box(mv, border=BLUE, buff=0.30)
        self.play(Write(mh));                        self.wait(0.3)
        self.play(FadeIn(mb), Write(mv));            self.wait(0.8)

        # Left zone: characteristic equation steps
        def L(y): return LEFT * 3.2 + UP * y

        items = []

        def step(mob, y, animate=Write):
            mob.move_to(L(y))
            self.play(animate(mob)); self.wait(0.5)
            items.append(mob)

        s1 = Text("Step 1: det(A \u2212 \u03bbI) = 0", font_size=24, color=WHITE)
        step(s1, 2.6, FadeIn)

        l1 = Text("det(A \u2212 \u03bbI) = 0", font_size=28, color=GREEN)
        step(l1, 1.7)

        l2 = Text("(3 \u2212 \u03bb)(2 \u2212 \u03bb) = 0", font_size=26, color=WHITE)
        step(l2, 0.8)

        l3 = Text("\u03bb\u00b2 \u2212 5\u03bb + 6 = 0", font_size=26, color=WHITE)
        step(l3, -0.1)

        l4 = Text("(\u03bb \u2212 3)(\u03bb \u2212 2) = 0", font_size=28, color=GREEN)
        step(l4, -1.0)

        ev_txt = Text("\u03bb\u2081 = 3     \u03bb\u2082 = 2", font_size=30, color=YELL)
        ev_txt.move_to(L(-2.0))
        evb = self._box(ev_txt, border=YELL, buff=0.24)
        self.play(FadeIn(evb), Write(ev_txt)); self.wait(2.5)
        items += [evb, ev_txt]

        # Fade left zone, keep matrix
        self.play(*[FadeOut(x) for x in items], run_time=0.5); self.wait(0.3)
        items = []

        # Eigenvectors
        s2 = Text("Step 2: Find Eigenvectors", font_size=24, color=WHITE)
        step(s2, 2.6, FadeIn)

        h1 = Text("For \u03bb\u2081 = 3:", font_size=26, color=YELL)
        step(h1, 1.7, FadeIn)

        r1 = Text("(A \u2212 3I)v = 0", font_size=24, color=WHITE)
        step(r1, 0.9)

        v1s = Text("\u2192   v\u2081 = [ 1,  0 ]", font_size=26, color=YELL)
        v1s.move_to(L(0.1))
        v1b = self._box(v1s, border=YELL, buff=0.22)
        self.play(FadeIn(v1b), Write(v1s)); self.wait(1)
        items += [v1b, v1s]

        h2 = Text("For \u03bb\u2082 = 2:", font_size=26, color=RED)
        step(h2, -1.0, FadeIn)

        r2 = Text("(A \u2212 2I)v = 0", font_size=24, color=WHITE)
        step(r2, -1.8)

        v2s = Text("\u2192   v\u2082 = [ 1, \u22121 ]", font_size=26, color=RED)
        v2s.move_to(L(-2.6))
        v2b = self._box(v2s, border=RED, buff=0.22)
        self.play(FadeIn(v2b), Write(v2s)); self.wait(2.5)
        items += [v2b, v2s]

        # Visual confirmation — show both eigenvectors on a clean plane
        all_items = items + [s1, h1, r1, h2, r2, mh, mb, mv]
        self.play(*[FadeOut(x) for x in all_items if x in self.mobjects],
                  run_time=0.5); self.wait(0.3)

        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)

        ea = _arr(plane, (0, 0), (2.5, 0.0),  YELL, sw=5)
        eb = _arr(plane, (0, 0), (1.8, -1.8),  RED,  sw=5)
        self.play(GrowArrow(ea), GrowArrow(eb)); self.wait(0.5)

        conf = Text(
            "v\u2081 = [1, 0]    \u03bb = 3\n"
            "v\u2082 = [1,\u22121]   \u03bb = 2",
            font_size=28, color=WHITE,
        )
        self._rp(conf, y=0.5)
        cb = self._box(conf, border=WHITE, buff=0.30)
        self.play(FadeIn(cb), Write(conf)); self.wait(3)

    # ── Section 5 — Deeper Insight (~55 s) ───────────────────────────────
    def s5_insight(self):
        self._sec("The Deeper Insight")

        plane = _mk_plane()
        self.play(Create(plane), run_time=1.2); self.wait(0.5)

        v = np.array([0.6, 1.1])
        a = _arr(plane, (0, 0), tuple(v.tolist()), RED, sw=4)
        self.play(GrowArrow(a), run_time=0.8); self.wait(0.5)

        lbl = Text("Apply M again\nand again...", font_size=26, color=WHITE)
        self._rp(lbl, y=1.8)
        lb = self._box(lbl, border=WHITE)
        self.play(FadeIn(lb), Write(lbl)); self.wait(0.5)

        # Power iteration — direction converges to dominant eigenvector [1,0]
        for _ in range(7):
            v = self.M @ v
            vd = v / np.linalg.norm(v) * 2.0
            an = _arr(plane, (0, 0), tuple(vd.tolist()), RED, sw=4)
            self.play(Transform(a, an), run_time=0.9); self.wait(0.2)

        self.wait(1)
        self.play(FadeOut(lb), FadeOut(lbl), run_time=0.4); self.wait(0.3)

        # Arrow becomes dominant eigenvector (yellow)
        vd_final = v / np.linalg.norm(v) * 2.5
        a_dom = _arr(plane, (0, 0), tuple(vd_final.tolist()), YELL, sw=6)
        self.play(Transform(a, a_dom), run_time=1.2); self.wait(1)

        ins = Text(
            "After many applications,\nevery vector converges to\nthe dominant eigenvector!",
            font_size=26, color=YELL,
        )
        self._rp(ins, y=1.5)
        ib = self._box(ins, border=YELL)
        self.play(FadeIn(ib), Write(ins)); self.wait(2.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.4); self.wait(0.3)

        # Real-world applications
        apps = Text(
            "Why eigenvalues matter:\n\n"
            "Google PageRank\n"
            "  Pages ranked by the dominant\n"
            "  eigenvector of the link matrix.\n\n"
            "Principal Component Analysis\n"
            "  Eigenvectors = directions\n"
            "  of maximum data spread.\n\n"
            "Quantum Mechanics\n"
            "  Energy levels = eigenvalues.",
            font_size=19, color=WHITE,
        )
        self._rp(apps, y=0.0)
        ab = self._box(apps, border=BLUE, buff=0.30)
        self.play(FadeIn(ab), Write(apps), run_time=1.5); self.wait(4)

    # ── Section 6 — Summary (~28 s) ──────────────────────────────────────
    def s6_summary(self):
        self._sec("Summary")

        # Left: clean eigenvector visualization
        plane = _mk_plane()
        self.play(Create(plane), run_time=1); self.wait(0.3)

        e1 = _arr(plane, (0, 0), (2.5, 0.0),  YELL, sw=5)
        e2 = _arr(plane, (0, 0), (1.8, -1.8),  RED,  sw=5)
        self.play(GrowArrow(e1), GrowArrow(e2)); self.wait(0.5)

        # Right: summary box
        sm = Text(
            "Eigenvalues & Eigenvectors\n\n"
            "  Av = \u03bbv\n\n"
            "  v  \u2192  the special direction\n"
            "  \u03bb  \u2192  the scaling factor\n\n"
            "They reveal the deep structure\n"
            "of any linear transformation.",
            font_size=24, color=WHITE,
        )
        self._rp(sm, y=0.0)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2); self.wait(3.5)
