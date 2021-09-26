# If the entire triangle should be drawn. If not, just a point of the triangles
# is drawn (which can be set with the constant PLOT_TRIANGLE_POINT).
SHOW_TRIANGLES = True
# Which triangle's points to plot. Options are: "outside left",
# "outside right", or "inside".
PLOT_TRIANGLE_POINT = "inside"
# Do an animation showing how the Spiral of Theodorus overlaps with the reverse
# Wurzelschnecke.
SHOW_SPIRAL = True
# How many spiral of theodorus triangles to plot when doing the animation
# showing how the Spiral of Theodorus overlaps with the reverse Wurzelschnecke.
SPIRAL_OF_THEODORUS_AMOUNT = 16
# If triangle values should be exact instead of decimal approximations.
EXACT_VALUES = False
# Show the circle the triangles go around.
SHOW_CIRCLE = False
# Show points one by one with a pause between them (the pause length is set by
# the constant ANIMATION_INTERVAL).
ANIMATE_PLOT = False
# If points on the plot should be connected by a straight line, from one point
# to the next.
CONNECT_POINTS = False
# The pause between animation frames.
ANIMATION_INTERVAL = 100
# The title of the plot.
PLOT_TITLE = "Two Spirals"
# The file to save the triangle data to.
DATA_FILE = "triangles.csv"
# The header names in the csv data file. The first one, the index of the csv
# data file, is the triangle number.
HEADERS = ["number", "outside left x", "outside left y", "outside right x",
           "outside right y", "inside x", "inside y", "rotation"]
# The length of the outside leg of the triangle.
OUTSIDE_LEG_LENGTH = 1
# If a custom function for calculating the hypotenuse of the triangles should
# be used. The function is called "calculate_hypotenuse" and can be found in
# "utils.py".
CUSTOM_HYPOTENUSE_FUNCTION = False
