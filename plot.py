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


def pause_plot_animation(plot_animation, seconds=1):
    # Pause the animation.
    plot_animation.pause()
    time.sleep(seconds)
    plot_animation.resume()


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
    if show_spiral:
        ax.set_title("The Spiral of Theodorus and the Reverse Wurzelschnecke")
    else:
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
        # How many triangles to calculate for the Spiral of Theodorus.
        amount = SPIRAL_OF_THEODORUS_AMOUNT
        # Start the rotation at 0 radians.
        current_rotation = 0
        
        # The starting points of the Spiral of Theodorus.
        x_points = [1, 1]
        y_points = [0, 1]
    
        # Create the points for the Spiral of Theodorus.
        for n in range(2, amount + 1):
            # Use the previous point to calculate the next point.
            current_point = (x_points[-1], y_points[-1] + 1)
            
            # Find the rotation.
            current_rotation += math.atan(1 / math.sqrt(n - 1))
            
            # Rotate the point.
            current_point = Triangle.rotate_point(
                (x_points[-1], y_points[-1]), current_point,
                current_rotation)
            
            # Add the new point to the list of points.
            x_points.append(current_point[0])
            y_points.append(current_point[1])
        
        # Setup the rotation animation of the spiral.
        flip_spiral_frames = 1
        rotate_spiral_frames = 50
        move_spiral_frames = 50
        x_distance = 2
        spiral_line, = ax.plot([], [], linewidth=2,
                               color=[1, 0, 0])

        def move_spiral(index, x_points, y_points):
            if index == 0:
                # Set the starting coordinates for the Spiral of Theodorus.
                spiral_line.set_data(x_points, y_points)
            elif index <= flip_spiral_frames:
                pause_plot_animation(move_spiral_animation)
                
                # Flip the x coordinates about the line x=1. The Spiral of
                # Theodorus will then be rotated, followed by being translated,
                # in order to overlap with the reverse Wurzelschnecke.
                current_x_points = spiral_line.get_xdata()
                flipped_x_points = [-p + 2 for p in current_x_points]
                spiral_line.set_xdata(flipped_x_points)
                
            elif index <= flip_spiral_frames + rotate_spiral_frames:
                if index == flip_spiral_frames + 1:
                    pause_plot_animation(move_spiral_animation)
                
                # Rotate the Spiral of Theodorus until it is lined up
                # correctly. It will be rotated by by arctan(1) radians
                # clockwise.
                current_x_points = spiral_line.get_xdata()
                current_y_points = spiral_line.get_ydata()
                rotated_x_points, rotated_y_points = rotate_points(
                    (1, 1), current_x_points, current_y_points,
                    -math.atan(1) / rotate_spiral_frames)
                spiral_line.set_data(rotated_x_points, rotated_y_points)
            else:
                if index == flip_spiral_frames + rotate_spiral_frames + 1:
                    pause_plot_animation(move_spiral_animation)

                # Translate the Spiral of Theodorus until it overlaps. It will
                # be translated 2 units to the left.
                current_x_points = spiral_line.get_xdata()
                moved_x_points = [point - x_distance / move_spiral_frames for
                                  point in current_x_points]
                spiral_line.set_xdata(moved_x_points)
        
        # Create the animation. Add 1 to the number of frames, since the first
        # one is used as a setup.
        move_spiral_animation = FuncAnimation(
            fig, move_spiral, frames=(flip_spiral_frames + rotate_spiral_frames
                                      + move_spiral_frames + 1),
            interval=ANIMATION_INTERVAL, repeat=False,
            fargs=(x_points, y_points))
            
        # Save the animation.
        # move_spiral_animation.save("data/animation.gif", fps=15)
        
    plt.show()
