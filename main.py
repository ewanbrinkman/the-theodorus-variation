import pandas as pd

from plot import plot_points
from triangle import Triangle
from utils import (read_last_triangle, read_triangle_points, get_input,
                   write_triangle_data)
from settings import HEADERS, DATA_FILE, EXACT_VALUES


def plot_data():
    """Plot saved triangle data using Matplotlib."""
    # Try to read a data file to get triangle data to plot. The constant
    # DATA_FILE can be changed to the data file name in "settings.py". The
    # program looks for the file in the "data" folder.
    points = read_triangle_points(DATA_FILE)
    
    if points:
        # If data was found, plot the data. There are some plotting options
        # which can be set in the "settings.py" file.
        plot_points(points)


def create_data():
    """Calculate a range of triangles and save the data to a file."""
    # Only save every "n" triangles.
    save_every_n_triangles = get_input(
        "Save every n triangles: ", int, default=1)
    # How many triangles to calculate. A value of -1 will continue forever.
    amount = get_input("Amount of triangles: ", int, default=15)
    
    # If exact values will be used. Warn the user how it could take a while.
    if EXACT_VALUES:
        print("\nNote: exact values are being used. This could take a while.")
    
    # Check if triangle data already exists. The constant DATA_FILE can be
    # changed to the data file name in "settings.py". The program looks for the
    # file in the "data" folder.
    last_triangle_dataframe = read_last_triangle(DATA_FILE)
    
    if last_triangle_dataframe is not None:
        # Data has been found that already exists. Get the data from the last
        # triangle calculated, in order to calculate the next triangle.
        current_triangle_number = last_triangle_dataframe[
                                      'number'].tolist()[0] + 1
        previous_outside_right_point = (
            last_triangle_dataframe['outside right x'].tolist()[0],
            last_triangle_dataframe['outside right y'].tolist()[0])
        current_rotation = last_triangle_dataframe['rotation'].tolist()[0]
        
        # When saving the new data, it will be added to the current data file,
        # instead of creating a new file.
        create_new_file = False
    else:
        # No data exists yet, or no data was found. Start calculating
        # triangles, starting at the first triangle.
        current_triangle_number = 1
        previous_outside_right_point = None
        current_rotation = 0

        # When saving the new data, a new data file will be created (since a
        # data file doesn't exist yet, or none was found).
        create_new_file = True

    # Create the dictionary to store the triangle data.
    triangle_data = {key: [] for key in HEADERS}
    
    if amount < 0:
        # If the amount of triangles to calculate is a negative number, such as
        # -1, then keep counting triangles forever (until the program is
        # interrupted).
        triangle_number = current_triangle_number
        
        # Create a data file if there is none. The calculated data will be
        # continually stored here as more triangles are calculated.
        if create_new_file:
            write_triangle_data(pd.DataFrame({key: [] for key in HEADERS}),
                                DATA_FILE, create_new_file)
            create_new_file = False

        print("\nCalculating triangles forever (until the program is "
              "interrupted)...")
        
        while True:
            current_triangle = Triangle.calculate_triangle(
                triangle_number, current_rotation,
                previous_outside_right_point)

            # Update the current rotation.
            current_rotation = current_triangle.rotation
            # Update the current outside right point, needed for creating the
            # next triangle.
            previous_outside_right_point = current_triangle.points[
                'outside right']
            
            # Save the data.
            if triangle_number % save_every_n_triangles == 0:
                # Add this triangle's data to the dictionary used to create a
                # pandas dataframe.
                triangle_data = {key: [] for key in HEADERS}
                current_triangle.save_triangle_data(triangle_data)
                print("\nCreating dataframe...")
                # Create the data frame for the triangle data.
                triangle_dataframe = pd.DataFrame(triangle_data)
                print("Done.")
                write_triangle_data(triangle_dataframe, DATA_FILE,
                                    create_new_file)

            triangle_number += 1
    else:
        # Calculate a set amount of triangles.
        start = current_triangle_number
        end = current_triangle_number + amount - 1
    
        print(f"\nCalculating triangles from {start} to {end}...")
        
        for triangle_number in range(start, end + 1):
            current_triangle = Triangle.calculate_triangle(
                triangle_number, current_rotation,
                previous_outside_right_point)
            
            # Update the current rotation.
            current_rotation = current_triangle.rotation
            # Update the current outside right point, needed for creating the
            # next triangle.
            previous_outside_right_point = current_triangle.points[
                'outside right']
            
            # Save the data.
            if triangle_number % save_every_n_triangles == 0:
                # Add this triangle's data to the dictionary used to create a
                # pandas dataframe.
                current_triangle.save_triangle_data(triangle_data)
    
        print("Done.")
    
        print("\nCreating dataframe...")
        # Create the data frame for the triangle data.
        triangle_dataframe = pd.DataFrame(triangle_data)
        print("Done.")
        
        write_triangle_data(triangle_dataframe, DATA_FILE, create_new_file)


def main():
    # If either data should be plotted, or new data should be created.
    choice = get_input(
        "\nOptions:\n\t[1] Plot data.\n\t[2] Create data.\nChoice: ",
        int, default=1, valid_inputs=(1, 2))
    
    if choice == 1:
        # Plot triangle data saved in a data file. The constant DATA_FILE can
        # be changed to the data file name in "settings.py". The program looks
        # for the file in the "data" folder.
        plot_data()
    elif choice == 2:
        # Calculate triangle data and output it into a data file (in csv
        # format). The constant DATA_FILE can be changed to the data file name
        # in "settings.py". If a data file with that name already exists, the
        # new data will be added on to the end of the csv file. If not, a new
        # file with the given name will be created (in the "data" folder).
        create_data()


if __name__ == "__main__":
    main()
