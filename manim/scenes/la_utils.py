"""Shared utilities for linear-algebra Manim scenes.

Colour palette, plane factory, arrow helper, text-box helpers.
All scenes import * from here.
"""
from manim import *
import numpy as np

# ── Colour palette (spec-exact) ──────────────────────────────────────────────
BG    = "#0F0E17"   # background
BLUE  = "#58C4DD"   # primary objects
YELL  = "#FFFF00"   # eigenvectors / highlights
RED   = "#FF6B6B"   # coral — secondary contrast
GREEN = "#00FF88"   # equation highlights
GREY  = "#333333"   # dark grid lines (never bright)
WHITE = "#FFFFFE"   # near-white text

# Aliases
CORAL = RED
AXIS_C = "#555555"

# ── NumberPlane factory ──────────────────────────────────────────────────────
def make_plane(x_range=(-5, 5, 1), y_range=(-4, 4, 1)):
    """Dark-themed NumberPlane — no axis numbers, #333333 grid."""
    return NumberPlane(
        x_range=x_range,
        y_range=y_range,
        background_line_style={"stroke_color": GREY, "stroke_width": 1},
        axis_config={
            "stroke_color": AXIS_C,
            "stroke_width": 1.5,
            "include_numbers": False,
            "include_tip": False,
        },
    )

# ── Arrow helper ─────────────────────────────────────────────────────────────
def vec(plane, tip, color=BLUE, base=(0, 0), stroke_width=3, tip_ratio=0.18):
    """Arrow from plane-coords *base* to *tip*; returns VMobject() if zero-length."""
    s = plane.c2p(*base)
    e = plane.c2p(*tip)
    if np.linalg.norm(e - s) < 0.08:
        return VMobject()
    return Arrow(s, e, buff=0, color=color,
                 stroke_width=stroke_width,
                 max_tip_length_to_length_ratio=tip_ratio)

# ── Text helpers ─────────────────────────────────────────────────────────────
def header(text, size=44, color=WHITE):
    return Text(text, font_size=size, color=color).to_edge(UP, buff=0.35)

def label(text, point, direction=UP, color=BLUE, size=28):
    return Text(text, font_size=size, color=color).next_to(point, direction, buff=0.15)

def text_box(mob, bg=BG, border=WHITE, buff=0.28):
    """Wrap *mob* in a filled SurroundingRectangle (clean text box)."""
    return SurroundingRectangle(
        mob, color=border, buff=buff,
        fill_color=bg, fill_opacity=0.92,
        corner_radius=0.06,
    )

def sec_label(scene, title, color=BLUE, size=38):
    """Flash a section title on screen, then fade it away."""
    lbl = Text(title, font_size=size, color=color)
    scene.play(FadeIn(lbl), run_time=0.6)
    scene.wait(1.2)
    scene.play(FadeOut(lbl), run_time=0.4)
    scene.wait(0.3)
