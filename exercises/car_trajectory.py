# Exercise: the Car class
#
# We already wrote the parts that are hard to guess:
#   - the equations that compute the car's new positions
#   - the matplotlib setup that draws the trajectory
#   - the loop that asks the user for a steering angle
#
# Your job is to fill in the two TODO parts below.

import math
import matplotlib.pyplot as plt

POINTS_PER_MOVE = 20        # how many new points compute_new_position gives us
MAX_TRAJECTORY_POINTS = 100  # how many past positions we remember, always


class Car:

    def __init__(self, speed=1.0):
        self.x = 0.0                    # current x position (float)
        self.y = 0.0                    # current y position (float)
        self.angle = 0.0                # current heading, in degrees (float)
        self.speed = speed              # how far the car moves on each step (float)
        self.is_moving = True           # is the car currently moving (bool)

        self.trajectory = []            # list of past [x, y] positions
        for i in range(MAX_TRAJECTORY_POINTS):
            self.trajectory.append([0.0, 0.0])

        # This is given: create the plot window once, here, so we can
        # keep updating the same window instead of opening a new one
        # every time.
        plt.ion()
        self.figure, self.axis = plt.subplots()

    def compute_new_position(self, angle):
        # This is given: "angle" is how many degrees to steer by, not
        # the new direction itself. We start from the car's current
        # orientation (self.angle) and turn a little more at every one
        # of the POINTS_PER_MOVE steps, so the path curves smoothly.
        # This is also why steering the same angle again and again
        # keeps turning the car further and further, instead of
        # driving straight in a fixed direction.
        turn_per_point = angle / POINTS_PER_MOVE
        step_length = self.speed / POINTS_PER_MOVE

        new_points = []
        x = self.x
        y = self.y
        heading = self.angle
        for i in range(POINTS_PER_MOVE):
            heading = heading + turn_per_point
            heading_in_radians = math.radians(heading)
            x = x + step_length * math.cos(heading_in_radians)
            y = y + step_length * math.sin(heading_in_radians)
            new_points.append([x, y])

        return new_points

    def plot_trajectory(self):
        # TODO (your part, 1 of 2):
        # self.trajectory is a list of [x, y] points. Build two
        # separate lists from it: one with all the x's, one with all
        # the y's. x_values and y_values must end up the same length
        # as self.trajectory.
        x_values = []
        y_values = []
        # <- your loop goes here

        # This part is given: it draws x_values against y_values.
        self.axis.clear()
        self.axis.plot(x_values, y_values, marker="o")
        self.axis.set_xlabel("x")
        self.axis.set_ylabel("y")
        self.axis.set_title("Car trajectory")
        self.axis.axis("equal")
        plt.pause(0.001)

    def stir(self, angle):
        # TODO (your part, 2 of 2):
        # 1. Call self.compute_new_position(angle). It returns a list
        #    of POINTS_PER_MOVE new [x, y] points.
        # 2. Remove the oldest POINTS_PER_MOVE points from
        #    self.trajectory (the ones at the start of the list).
        # 3. Add the new points to the end of self.trajectory, so it
        #    always keeps exactly MAX_TRAJECTORY_POINTS points.
        # 4. Update self.x and self.y with the last new point.
        # 5. Update self.angle by ADDING angle to it (self.angle =
        #    self.angle + angle), not by replacing it. This way the
        #    car remembers how much it has already turned.
        pass  # <- remove this line once you add your code

    def close_plot(self):
        # This is given: closes the plot window.
        plt.close(self.figure)


def main():
    speed = float(input("Enter the car's speed: "))
    car = Car(speed)

    while True:
        user_input = input("Enter a steering angle in degrees (or 'q' to quit): ")

        if user_input == "q":
            break

        angle = float(user_input)
        car.stir(angle)
        car.plot_trajectory()

    car.close_plot()


if __name__ == "__main__":
    main()
