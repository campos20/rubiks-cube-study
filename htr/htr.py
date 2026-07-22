import numpy as np
from manim import *

OFFSET = 0.2
ZOOM_FACTOR = 1.5


# manim -ql htr.py HTR
class HTR(Scene):
    def construct(self):
        title = Text("HTR Maze", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Create(title))

        points = [
            (1, 3, 0),
            (2, 3, 0),
            (0, 2, 0),
            (1, 2, 0),
            (2, 2, 0),
            (3, 2, 0),
            (0, 1, 0),
            (1, 1, 0),
            (2, 1, 0),
            (3, 1, 0),
            (1, 0, 0),
            (2, 0, 0),
            (3, 0, 0),
        ]

        # Center the grid on the origin using its bounding-box midpoint
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        center_x = (max(xs) + min(xs)) / 2
        center_y = (max(ys) + min(ys)) / 2

        def centered(x, y, z=0):
            return (x - center_x, y - center_y, z)

        points = [centered(*p) for p in points]
        additional_points = [
            centered(1 + OFFSET, 2),
            centered(2 + OFFSET, 1),
            centered(3 + OFFSET, 0),
        ]
        final_points = [centered(2 + 2 * OFFSET, 1)]

        self.fade_in_dots(points)
        self.wait(1)
        self.fade_in_dots(additional_points)
        self.wait(1)
        self.fade_in_dots(final_points)
        self.wait(1)

        # First polygon
        self.draw_path(
            [points[11], points[9], points[4], points[0], points[2], points[7]],
            GREEN,
            closed=True,
        )
        self.wait(1)

        # Second polygon
        self.draw_path(
            [
                points[10],
                final_points[0],
                points[5],
                points[1],
                additional_points[0],
                points[6],
            ],
            BLUE,
            closed=True,
        )
        self.wait(1)

        self.draw_path(
            [points[10], points[11], points[12], points[9], points[5]], YELLOW
        )
        self.wait(1)

        self.draw_path([points[0], points[3], points[2]], RED)
        self.draw_path([points[7], additional_points[0], points[4]], RED)
        self.wait(1)

        # Draw diagonals
        self.draw_path([points[3], points[8], points[12]], PURPLE)

        self.draw_path(
            [additional_points[0], additional_points[1], additional_points[2]], PURPLE
        )
        self.wait(1)

        # Draw additional diagonals
        self.draw_path([additional_points[2], final_points[0]], PURPLE)
        self.draw_path([points[8], additional_points[0]], PURPLE)
        self.wait(1)

        # Draw a circle touching each point, extending in the given direction
        radius = 0.2
        self_arc_points = [
            (points[10], DOWN),
            (additional_points[2], RIGHT),
            (points[5], RIGHT),
        ]
        for point, direction in self_arc_points:
            circle = Circle(radius=radius, color=ORANGE).move_to(
                np.array(point) + radius * direction
            )
            self.play(Create(circle), run_time=0.5)
        self.wait(1)

        arc = ArcBetweenPoints(
            start=points[12],
            end=additional_points[2],
            angle=3 * PI / 2,
            color=ORANGE,
        )
        self.play(Create(arc), run_time=0.5)
        self.wait(1)

        v_labels = [
            (0, 3, "SL", LEFT),
            (0, 2, "S", LEFT),
            (0, 1, "B", LEFT),
            (0, 0, "B/S", LEFT),
        ]

        h_labels = [
            (0, 3, "S", UP),
            (1, 3, "OF", UP),
            (2, 3, "B", UP),
            (3, 3, "OB", UP),
        ]
        self.fade_in_labels(v_labels, centered)
        self.fade_in_labels(h_labels, centered)

        self.wait(3)

    def fade_in_dots(self, dot_points):
        for point in dot_points:
            dot = Dot(point=point, color=WHITE)
            self.play(FadeIn(dot), run_time=0.1)

    def draw_path(self, path_points, color, closed=False):
        segments = len(path_points) if closed else len(path_points) - 1
        for i in range(segments):
            start_point = path_points[i]
            end_point = path_points[(i + 1) % len(path_points)]
            line = Line(start=start_point, end=end_point, color=color)
            self.play(Create(line), run_time=0.5)

    def fade_in_labels(self, labels, centered):
        for x, y, text, direction in labels:
            label = Text(text, font_size=24).next_to(centered(x, y), direction)
            self.play(FadeIn(label), run_time=0.1)
