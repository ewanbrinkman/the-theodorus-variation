import math

import sympy

from utils import calculate_hypotenuse
from settings import (EXACT_VALUES, HEADERS, CUSTOM_HYPOTENUSE_FUNCTION,
                      OUTSIDE_LEG_LENGTH)


class NotRightTriangleError(Exception):
    def __init__(self, triangle_number):
        super().__init__(
            f"Can't create a right triangle for triangle #{triangle_number}.")


class Triangle:
    def __init__(self, outside_left, outside_right, inside, number, rotation):
        # The three points of the triangle.
        self.points = {
            "outside left": outside_left,
            "outside right": outside_right,
            "inside": inside
        }
        # The position of this triangle in the series of triangles.
        self.number = number
        # How much this triangle is rotated.
        self.rotation = rotation
        
    def save_triangle_data(self, triangle_data):
        """Save this triangle's data to a dictionary."""
        triangle_data[HEADERS[0]].append(self.number)
        triangle_data[HEADERS[1]].append(self.points['outside left'][0])
        triangle_data[HEADERS[2]].append(self.points['outside left'][1])
        triangle_data[HEADERS[3]].append(
            self.points['outside right'][0])
        triangle_data[HEADERS[4]].append(
            self.points['outside right'][1])
        triangle_data[HEADERS[5]].append(self.points['inside'][0])
        triangle_data[HEADERS[6]].append(self.points['inside'][1])
        triangle_data[HEADERS[7]].append(self.rotation)

    @staticmethod
    def rotate_point(origin, point, angle):
        """Rotate a point counterclockwise around an origin."""
        origin_x, origin_y = origin
        point_x, point_y = point
        
        if EXACT_VALUES:
            angle_cos = sympy.cos(angle)
            angle_sin = sympy.sin(angle)
        else:
            angle_cos = math.cos(angle)
            angle_sin = math.sin(angle)
        
        delta_x = point_x - origin_x
        delta_y = point_y - origin_y
        
        rotated_x = origin_x + angle_cos * delta_x - angle_sin * delta_y
        rotated_y = origin_y + angle_sin * delta_x + angle_cos * delta_y
        
        return rotated_x, rotated_y

    @classmethod
    def calculate_triangle(cls, triangle_number, current_rotation,
                           previous_outside_right_point):
        """Calculate a triangle and create a triangle object for it."""
        # The outside leg of the triangle.
        outside_leg = OUTSIDE_LEG_LENGTH
        
        # If a custom function should be used for calculating a triangle's
        # hypotenuse.
        if CUSTOM_HYPOTENUSE_FUNCTION:
            hypotenuse = calculate_hypotenuse(triangle_number)
        
            if hypotenuse <= outside_leg:
                raise NotRightTriangleError(triangle_number)

            if EXACT_VALUES:
                inside_leg = sympy.sqrt(hypotenuse ** 2 - outside_leg ** 2)
            else:
                inside_leg = math.sqrt(hypotenuse ** 2 - outside_leg ** 2)
        else:
            # The triangle's side lengths.
            if EXACT_VALUES:
                inside_leg = sympy.sqrt(triangle_number)
            else:
                inside_leg = math.sqrt(triangle_number)
        
        # Points are in the order: outside left, outside right, inside.
        if triangle_number == 1:
            return cls((-outside_leg, inside_leg), (0, inside_leg), (0, 0),
                       triangle_number, current_rotation)
        else:
            # The points before rotation.
            outside_right_point = (
                previous_outside_right_point[0] + outside_leg,
                previous_outside_right_point[1])
            inside_point = (
                previous_outside_right_point[0] + outside_leg,
                previous_outside_right_point[1] - inside_leg)
            
            # How much to rotate.
            if EXACT_VALUES:
                current_rotation += sympy.atan(outside_leg / inside_leg)
            else:
                current_rotation += math.atan(outside_leg / inside_leg)
            
            point_outside_right = cls.rotate_point(
                previous_outside_right_point, outside_right_point,
                -current_rotation)
            point_inside = cls.rotate_point(
                previous_outside_right_point, inside_point, -current_rotation)
            
            return cls(previous_outside_right_point, point_outside_right,
                       point_inside, triangle_number, current_rotation)
