"""
Manim scene: pi = lim (n -> inf) n * sin(360 deg / 2n)

Render with:
    manim -qh pi_limit.py PiLimit
"""
import math
from manim import *


R = 2.2  # visual radius of the circle on screen (math uses r = 1)


def polygon_points(n, radius=R):
    return [
        radius * np.array([math.cos(2 * PI * k / n + PI / 2),
                           math.sin(2 * PI * k / n + PI / 2), 0])
        for k in range(n)
    ]


class PiLimit(Scene):
    def construct(self):
        self.camera.background_color = "#0e0e14"
        self.intro()
        self.slices()
        self.derivation()
        self.converge()
        self.outro()

    # ---------------------------------------------------------- 1. intro
    def intro(self):
        formula = MathTex(
            r"\pi", r"=", r"\lim_{n \to \infty}", r"\, n \cdot \sin\!\left(\frac{360^\circ}{2n}\right)",
            font_size=72,
        )
        formula[0].set_color(YELLOW)
        sub = Text("A circle as a polygon with infinitely many sides",
                   font_size=30, color=GREY_B).next_to(formula, DOWN, buff=0.6)
        self.play(Write(formula), run_time=2)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(2)
        self.play(FadeOut(sub), formula.animate.scale(0.45).to_corner(UR, buff=0.3))
        self.formula_corner = formula

    # --------------------------------------------------------- 2. slices
    def slices(self):
        n = 6
        circle = Circle(radius=R, color=BLUE_B, stroke_width=3).shift(LEFT * 3)
        center = circle.get_center()
        dot = Dot(center, color=WHITE, radius=0.05)
        radius_label = MathTex("r = 1", font_size=36, color=BLUE_B)
        radius_line = Line(center, center + R * RIGHT, color=BLUE_B, stroke_width=2)
        radius_label.next_to(radius_line, DOWN, buff=0.1)

        self.play(Create(circle), FadeIn(dot))
        self.play(Create(radius_line), FadeIn(radius_label))
        self.wait(0.5)
        self.play(FadeOut(radius_line), FadeOut(radius_label))

        pts = [center + p for p in polygon_points(n)]
        spokes = VGroup(*[Line(center, p, color=GREY_B, stroke_width=2) for p in pts])
        poly = Polygon(*pts, color=YELLOW, stroke_width=4)

        caption = Text("Cut the circle into n equal slices", font_size=30).to_edge(DOWN, buff=0.5)
        self.play(Create(spokes), Write(caption))
        self.wait(0.5)
        self.play(Create(poly))
        self.wait(0.5)

        # highlight one slice: vertices pts[0] (top) and pts[1]
        a, b = pts[0], pts[1]
        slice_tri = Polygon(center, a, b, color=ORANGE, fill_opacity=0.35, stroke_width=0)
        self.play(FadeIn(slice_tri))

        # central angle arc + label 360/n
        ang = Angle(Line(center, b), Line(center, a), radius=0.6, color=ORANGE)
        ang_label = MathTex(r"\frac{360^\circ}{n}", font_size=36, color=ORANGE)
        ang_label.move_to(center + 1.05 * (a + b - 2 * center) / np.linalg.norm(a + b - 2 * center))
        new_caption = Text("Each slice has a central angle of 360° / n", font_size=30).to_edge(DOWN, buff=0.5)
        self.play(Create(ang), FadeIn(ang_label), Transform(caption, new_caption))
        self.wait(1.5)

        # split with the bisector -> half angle 360/(2n)
        mid = (a + b) / 2
        bisector = DashedLine(center, mid, color=WHITE, stroke_width=2)
        half_ang = Angle(Line(center, mid), Line(center, a), radius=0.9, color=GREEN)
        half_label = MathTex(r"\frac{360^\circ}{2n}", font_size=34, color=GREEN)
        half_dir = (a + mid) / 2 - center
        half_label.move_to(center + 1.45 * half_dir / np.linalg.norm(half_dir))
        right_angle = RightAngle(Line(mid, center), Line(mid, a), length=0.2, color=WHITE)
        new_caption = Text("Bisect it: two right triangles with angle 360° / 2n", font_size=30).to_edge(DOWN, buff=0.5)
        self.play(Create(bisector), Create(right_angle), FadeOut(ang), FadeOut(ang_label))
        self.play(Create(half_ang), FadeIn(half_label), Transform(caption, new_caption))
        self.wait(1.5)

        # half side = sin(360/2n)
        half_side = Line(mid, a, color=RED, stroke_width=6)
        hs_label = MathTex(r"\sin\!\left(\frac{360^\circ}{2n}\right)", font_size=32, color=RED)
        hs_label.next_to(half_side, UP, buff=0.15)
        new_caption = Text("Opposite side = r · sin(360° / 2n) = sin(360° / 2n)", font_size=30).to_edge(DOWN, buff=0.5)
        self.play(Create(half_side), FadeIn(hs_label), Transform(caption, new_caption))
        self.wait(1.5)

        full_side = Line(b, a, color=RED, stroke_width=6)
        fs_label = MathTex(r"\text{side} = 2\sin\!\left(\frac{360^\circ}{2n}\right)", font_size=32, color=RED)
        fs_label.next_to(full_side, UP, buff=0.15).shift(RIGHT * 0.6)
        new_caption = Text("So one full side is 2 · sin(360° / 2n)", font_size=30).to_edge(DOWN, buff=0.5)
        self.play(Transform(half_side, full_side), Transform(hs_label, fs_label),
                  Transform(caption, new_caption))
        self.wait(1.5)

        self.geo = VGroup(circle, dot, spokes, poly, slice_tri, bisector, half_ang,
                          half_label, right_angle, half_side, hs_label)
        self.caption = caption
        self.circle_center = center

    # ------------------------------------------------------ 3. derivation
    def derivation(self):
        lines = VGroup(
            MathTex(r"\text{perimeter} = n \cdot 2\sin\!\left(\frac{360^\circ}{2n}\right)", font_size=40),
            MathTex(r"\text{diameter} = 2", font_size=40),
            MathTex(r"\frac{\text{perimeter}}{\text{diameter}} = n \cdot \sin\!\left(\frac{360^\circ}{2n}\right)", font_size=40),
            MathTex(r"\xrightarrow{\;n\to\infty\;}\ \frac{\text{circumference}}{\text{diameter}} = \pi", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.6)
        lines[3][0][-1].set_color(YELLOW)

        self.play(FadeOut(self.caption))
        for ln in lines:
            self.play(Write(ln))
            self.wait(1.2)
        self.wait(1)
        self.play(FadeOut(lines), FadeOut(self.geo))

    # -------------------------------------------------------- 4. converge
    def converge(self):
        circle = Circle(radius=R, color=BLUE_B, stroke_width=3).shift(LEFT * 3)
        center = circle.get_center()
        n_tracker = ValueTracker(3)

        def make_poly():
            n = int(round(n_tracker.get_value()))
            pts = [center + p for p in polygon_points(n)]
            poly = Polygon(*pts, color=YELLOW, stroke_width=3)
            spokes = VGroup(*[Line(center, p, color=GREY_D, stroke_width=1) for p in pts])
            return VGroup(spokes, poly)

        poly = always_redraw(make_poly)

        n_txt = VGroup(MathTex("n = ", font_size=48),
                       Integer(3, font_size=48)).arrange(RIGHT)
        n_txt[1].add_updater(lambda m: m.set_value(int(round(n_tracker.get_value()))))

        val_lbl = MathTex(r"n \cdot \sin\!\left(\frac{360^\circ}{2n}\right) =", font_size=44)
        val_num = DecimalNumber(0, num_decimal_places=5, font_size=44, color=YELLOW)
        val_num.add_updater(lambda m: m.set_value(
            (lambda n: n * math.sin(math.radians(360 / (2 * n))))(int(round(n_tracker.get_value())))))
        val_row = VGroup(val_lbl, val_num).arrange(RIGHT, buff=0.25)

        pi_row = VGroup(MathTex(r"\pi =", font_size=44),
                        MathTex("3.14159", font_size=44, color=GREEN)).arrange(RIGHT, buff=0.25)

        panel = VGroup(n_txt, val_row, pi_row).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        panel.to_edge(RIGHT, buff=0.8)

        self.play(Create(circle), FadeIn(poly), FadeIn(panel))
        self.wait(1)

        for target in [4, 5, 6, 8, 12, 24, 48, 96]:
            self.play(n_tracker.animate.set_value(target), run_time=1.0, rate_func=linear)
            self.wait(0.6 if target < 96 else 2.5)

        note = Text("The polygon becomes the circle", font_size=30, color=GREY_B).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)

        val_num.clear_updaters()
        n_txt[1].clear_updaters()
        self.play(FadeOut(VGroup(circle, poly, panel, note)))

    # ----------------------------------------------------------- 5. outro
    def outro(self):
        formula = MathTex(
            r"\pi", r"=", r"\lim_{n \to \infty}", r"\, n \cdot \sin\!\left(\frac{360^\circ}{2n}\right)",
            font_size=80,
        )
        formula[0].set_color(YELLOW)
        self.play(FadeOut(self.formula_corner), Write(formula), run_time=2)
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.4)
        self.play(Create(box))
        self.wait(3)
