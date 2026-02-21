"""
Feynman – Quicksort (Gold Standard)
6-section narrative, 3-5 minutes. Text/Cairo only, no LaTeX.
"""
from manim import *
from la_utils import text_box, sec_label, BG, BLUE, YELL, RED, GREEN, WHITE
import numpy as np

AX_COLOR = "#888888"

class QuicksortScene(Scene):
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
        t1 = Text("Quicksort", font_size=52, color=WHITE)
        t2 = Text("Divide, Conquer, Sort", font_size=26, color=BLUE)
        t1.move_to(UP * 0.5); t2.next_to(t1, DOWN, buff=0.5)
        self.play(FadeIn(t1), run_time=1.5); self.wait(0.8)
        self.play(FadeIn(t2), run_time=1.0); self.wait(3.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)
        q1 = Text("You have 8 unsorted numbers.", font_size=28, color=WHITE)
        q2 = Text("What is the fastest way to sort them?", font_size=28, color=YELL)
        q1.move_to(UP * 1.2); q2.next_to(q1, DOWN, buff=0.5)
        self.play(Write(q1), run_time=2.0); self.wait(1.8)
        self.play(Write(q2), run_time=1.5); self.wait(3.5)
        self.play(FadeOut(q1), FadeOut(q2), run_time=0.5)
        ans = Text(
            "Quicksort: pick a pivot, partition around it,\n"
            "then recursively sort each half.\n\n"
            "Average time: O(n log n)\n"
            "Used in Python, C++, Java standard libraries.",
            font_size=26, color=WHITE)
        ans.move_to(ORIGIN)
        ab = self._box(ans, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(ans), run_time=2.5); self.wait(4.5)

    def _draw_array(self, arr, colors=None, y=-1.0):
        mobs = VGroup()
        if colors is None: colors = [BLUE]*len(arr)
        for i, (val, col) in enumerate(zip(arr, colors)):
            x = -3.5 + i * 0.85
            box = Rectangle(width=0.75, height=0.75, color=col, fill_color=col, fill_opacity=0.4, stroke_width=2)
            box.move_to(RIGHT*x + UP*y)
            lbl = Text(str(val), font_size=22, color=WHITE).move_to(box.get_center())
            mobs.add(box, lbl)
        return mobs

    def s2_geometry(self):
        sec_label(self, "Quicksort in Action")
        arr = [5, 3, 8, 1, 9, 2, 7, 4]
        cols = [BLUE]*8
        mobs = self._draw_array(arr, cols)
        title = Text("Unsorted array:", font_size=24, color=WHITE).move_to(UP * 2.5)
        self.play(FadeIn(title), FadeIn(mobs), run_time=2.0); self.wait(2.3)

        # Show pivot = 5
        pivot_lbl = Text("Pivot = 5 (first element)", font_size=22, color=YELL).move_to(UP * 1.5)
        self.play(Write(pivot_lbl), run_time=1.5); self.wait(1.8)

        # Partition visualization
        less_label = Text("< 5: [3, 1, 2, 4]", font_size=22, color=GREEN).move_to(UP * 0.5 + LEFT * 2.5)
        pivot_show = Text("pivot: [5]", font_size=22, color=YELL).move_to(UP * 0.5)
        more_label = Text("> 5: [8, 9, 7]", font_size=22, color=RED).move_to(UP * 0.5 + RIGHT * 2.5)
        self.play(Write(less_label), Write(pivot_show), Write(more_label), run_time=2.5); self.wait(3.0)

        step2 = Text("Recursively sort [3,1,2,4] and [8,9,7]", font_size=22, color=WHITE).move_to(DOWN * 0.3)
        self.play(Write(step2), run_time=2.0); self.wait(2.3)

        sorted_arr = [1, 2, 3, 4, 5, 7, 8, 9]
        sorted_cols = [GREEN]*8
        sorted_mobs = self._draw_array(sorted_arr, sorted_cols, y=-1.8)
        sorted_title = Text("Result: sorted!", font_size=22, color=GREEN).move_to(DOWN * 1.0)
        self.play(Write(sorted_title), FadeIn(sorted_mobs), run_time=2.0); self.wait(4.0)

    def s3_notation(self):
        sec_label(self, "The Algorithm")
        algo = Text(
            "quicksort(arr, low, high):\n"
            "  if low >= high: return\n"
            "  pivot = arr[high]\n"
            "  i = low - 1\n"
            "  for j from low to high-1:\n"
            "    if arr[j] <= pivot:\n"
            "      i += 1\n"
            "      swap arr[i], arr[j]\n"
            "  swap arr[i+1], arr[high]\n"
            "  p = i + 1\n"
            "  quicksort(arr, low, p-1)\n"
            "  quicksort(arr, p+1, high)",
            font_size=22, color=BLUE)
        algo.move_to(ORIGIN)
        ab = self._box(algo, border=BLUE, buff=0.38)
        self.play(FadeIn(ab), Write(algo), run_time=3.0); self.wait(4.5)
        self.play(FadeOut(ab), FadeOut(algo), run_time=0.5)

        complexity = Text(
            "Time complexity:\n\n"
            "  Average case: O(n log n)\n"
            "  Best case:    O(n log n)\n"
            "  Worst case:   O(n^2)  (already sorted + bad pivot)\n\n"
            "  Space: O(log n) for recursion stack\n\n"
            "  Pivot strategies to avoid worst case:\n"
            "  Median-of-three, random pivot, Sedgewick",
            font_size=23, color=WHITE)
        complexity.move_to(ORIGIN)
        cb = self._box(complexity, border=YELL, buff=0.38)
        self.play(FadeIn(cb), Write(complexity), run_time=2.5); self.wait(4.5)

    def s4_example(self):
        sec_label(self, "Step-by-Step: [3, 1, 2]")
        steps = [
            ("Array: [3, 1, 2]", WHITE),
            ("Pivot = 2 (last element)", YELL),
            ("Compare 3 > 2: stays right", RED),
            ("Compare 1 < 2: move left -> [1, 3, 2]", GREEN),
            ("Swap pivot: [1, 2, 3]", YELL),
            ("Left partition [1]: already sorted", GREEN),
            ("Right partition [3]: already sorted", GREEN),
            ("Final: [1, 2, 3] -- sorted!", BLUE),
        ]
        y = 3.0
        for txt, col in steps:
            mob = Text(txt, font_size=26, color=col).move_to(UP * y)
            b = self._box(mob, border=col)
            self.play(FadeIn(b), Write(mob), run_time=1.5); self.wait(2.0)
            y -= 0.9
        self.wait(3.0)

    def s5_insight(self):
        sec_label(self, "The Deeper Insight")
        ins = Text(
            "Why quicksort is fast in practice:\n\n"
            "  Cache-friendly: works in place on array\n"
            "  Low overhead: minimal extra memory\n"
            "  Average O(n log n): most inputs behave well\n\n"
            "  Comparison: Merge sort always O(n log n)\n"
            "  but requires O(n) extra space\n\n"
            "  Python uses Timsort (hybrid merge + insertion)\n"
            "  C++ std::sort: introsort (quicksort + heapsort)\n\n"
            "  Random pivot eliminates pathological worst-case",
            font_size=21, color=WHITE)
        ins.move_to(LEFT * 0.5)
        ib = self._box(ins, border=BLUE, buff=0.38)
        self.play(FadeIn(ib), Write(ins), run_time=3.0); self.wait(5.5)
        self.play(FadeOut(ib), FadeOut(ins), run_time=0.5)
        dc = Text(
            "Divide and conquer strategy:\n\n"
            "  Split problem into smaller subproblems\n"
            "  Solve each subproblem independently\n"
            "  Combine solutions\n\n"
            "  The PIVOT is the key creative insight!\n"
            "  After partitioning, pivot is in FINAL position.\n"
            "  Reduces problem size by half each time on average.",
            font_size=22, color=WHITE)
        dc.move_to(ORIGIN)
        db = self._box(dc, border=YELL, buff=0.38)
        self.play(FadeIn(db), Write(dc), run_time=2.5); self.wait(5.5)

    def s6_summary(self):
        sec_label(self, "Summary")
        arr_sorted = [1, 2, 3, 4, 5, 6, 7, 8]
        mobs = self._draw_array(arr_sorted, [GREEN]*8)
        self.play(FadeIn(mobs), run_time=1.5); self.wait(0.8)
        sm = Text(
            "Quicksort\n\n"
            "  1. Pick a pivot\n"
            "  2. Partition: smaller left, larger right\n"
            "  3. Pivot is now in final sorted position\n"
            "  4. Recurse on both halves\n\n"
            "  Average: O(n log n)\n"
            "  Worst case: O(n^2) -- avoid with random pivot\n"
            "  In-place, cache-friendly -- fast in practice\n"
            "  Used in C++, Java standard libraries",
            font_size=20, color=WHITE)
        sm.move_to(RIGHT * 3.0 + UP * 0.2)
        sb = self._box(sm, border=BLUE, buff=0.35)
        self.play(FadeIn(sb), Write(sm), run_time=2.5); self.wait(6.0)
