import math
import time

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation
import numpy as np

from triangle import Triangle
from settings import (ANIMATION_INTERVAL, PLOT_TITLE,
                      SPIRAL_OF_THEODORUS_AMOUNT, SHOW_CIRCLE, SHOW_TRIANGLES,
                      ANIMATE_PLOT, CONNECT_POINTS, PLOT_TRIANGLE_POINT,
                      SHOW_SPIRAL)


def rotate_points(origin, x_points, y_points, angle):
    """Rotate a list of points counterclockwise around an origin."""
    points = [(x_points[i], y_points[i]) for i in range(len(x_points))]
    for i, point in enumerate(points):
        points[i] = Triangle.rotate_point(origin, point, angle)
    x_points = [point[0] for point in points]
    y_points = [point[1] for point in points]
    
    return x_points, y_points


def plot_circle():
    """Plot a circle with a dot to mark the middle."""
    # What appears to be the circle edges.
    circle_edges = {
        "x": {
            "left": -2,
            "right": 0
        },
        "y": {
            "top": -1 * math.sqrt(2) + 2,
            "bottom": -1 * math.sqrt(2)
        }
    }
    # Plot what appears to be the circle center by taking the average of what
    # appears to be the circle edges.
    circle_center = [
        (circle_edges['x']['left'] + circle_edges['x']['right']) / 2,
        (circle_edges['y']['top'] + circle_edges['y']['bottom']) / 2
    ]
    
    ax = plt.gca()
    ax.add_patch(plt.Circle((circle_center[0], circle_center[1]), 1,
                            color=[1, 0.75, 0.8], alpha=0.5))
    
    # Center of circle.
    plt.plot(circle_center[0], circle_center[1],
             marker=".", markersize=10, color=[1, 0, 1])


def plot_points(points, show_circle=SHOW_CIRCLE, show_triangles=SHOW_TRIANGLES,
                animate_plot=ANIMATE_PLOT, connect=CONNECT_POINTS,
                plot_triangle_point=PLOT_TRIANGLE_POINT,
                show_spiral=SHOW_SPIRAL):
    """Plot the given points."""
    # Points is a list containing each triangle's data needed for plotting (as
    # a list).
    if plot_triangle_point == "outside left":
        point_index = 0
    elif plot_triangle_point == "outside right":
        point_index = 1
    else:
        # The inside point.
        point_index = 2
    
    fig = plt.figure()
    # Setup the view.
    if show_spiral:
        view_distance = 5.5
        ax = plt.axes(xlim=[-view_distance, view_distance],
                      ylim=[-view_distance, view_distance],
                      aspect="equal")
    else:
        view_circle_spacing = 1
        ax = plt.axes(xlim=[-2 - view_circle_spacing, view_circle_spacing],
                      ylim=[-1 * math.sqrt(2) - view_circle_spacing,
                            -1 * math.sqrt(2) + 2 + view_circle_spacing],
                      aspect="equal")
    ax.set_title(PLOT_TITLE)
    ax.grid()

    def plot_point(index, color_percent_done=False):
        """Animate the points being plot one by one."""
        point = points[index]

        # Color using a gradient based on the current progress.
        if color_percent_done:
            percent_done = (index + 1) / len(points)
            plot_color = [0, percent_done, 0]
        else:
            # plot_color = [0, 0.85, 1]
            plot_color = [0, 0, 0]
    
        if connect and index > 0:
            # Connect this point to the previous point with a straight line.
            ax.plot([points[index - 1][point_index][0], point[point_index][0]],
                    [points[index - 1][point_index][1], point[point_index][1]],
                    color=plot_color)
         
        # Plot either the entire current triangle or just its inside point.
        if show_triangles:
            ax.add_patch(Polygon(np.array(point[:3]), closed=True, fill=False,
                                 linewidth=2, color=plot_color))
        else:
            ax.plot(point[point_index][0], point[point_index][1], marker=".",
                    markersize=5, color=plot_color)
    
    if show_circle:
        plot_circle()
    
    # If the points should be periodically shown (animated), or shown all at
    # once (not animated).
    if animate_plot:
        animation = FuncAnimation(fig, plot_point, frames=len(points),
                                  interval=ANIMATION_INTERVAL, repeat=False)
    else:
        for i in range(len(points)):
            plot_point(i)
    
    # Do an animation showing how the Spiral of Theodorus overlaps with the
    # reverse Wurzelschnecke.
    if show_spiral:
        amount = SPIRAL_OF_THEODORUS_AMOUNT
        current_rotation = 0

        x_points = [1, 1]
        y_points = [0, 1]

        for n in range(2, amount + 1):
            current_point = (x_points[-1], y_points[-1] + 1)

            current_rotation += math.atan(1 / math.sqrt(n - 1))

            current_point = Triangle.rotate_point(
                (x_points[-1], y_points[-1]), current_point,
                -current_rotation)

            x_points.append(current_point[0])
            y_points.append(current_point[1])
        
        # Setup the rotation animation of the spiral.
        rotate_spiral_frames = 50
        # flip_spiral_frames = 1
        move_spiral_frames = 50
        x_distance = 2
        spiral_line, = ax.plot([], [], linewidth=2,
                               color=[1, 0, 0])
        
        def move_spiral(index, x_points, y_points):
            if index + 1 <= rotate_spiral_frames:
                if index == 1:
                    # Pause at the start.
                    move_spiral_animation.pause()
                    time.sleep(1)
                    move_spiral_animation.resume()
            
                x_points, y_points = rotate_points(
                    (1, 1), x_points, y_points,
                    -math.atan(1) * ((index + 1) / rotate_spiral_frames))
    
                spiral_line.set_data(x_points, y_points)
            else:
                if index == 50:
                    # Pause before flipping.
                    time.sleep(1)
                    move_spiral_animation.resume()
                
                current_x_points = spiral_line.get_xdata()
                new_x_points = [point - x_distance / move_spiral_frames for
                                point in current_x_points]
                spiral_line.set_xdata(new_x_points)
        
        # Create the animation.
        move_spiral_animation = FuncAnimation(
            fig, move_spiral, frames=rotate_spiral_frames + move_spiral_frames,
            interval=ANIMATION_INTERVAL, repeat=False,
            fargs=(x_points, y_points))
        
    plt.show()
