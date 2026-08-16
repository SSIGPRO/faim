# Solution: the Car class
#
# Same as car_trajectory.py, but with both TODO parts filled in.

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
        # Build the two lists, x's and y's, from self.trajectory.
        x_values = []
        y_values = []
        for point in self.trajectory:
            x_values.append(point[0])
            y_values.append(point[1])

        # This part is given: it draws x_values against y_values.
        self.axis.clear()
        self.axis.plot(x_values, y_values, marker="o")
        self.axis.set_xlabel("x")
        self.axis.set_ylabel("y")
        self.axis.set_title("Car trajectory")
        self.axis.axis("equal")
        plt.pause(0.001)

    def stir(self, angle):
        new_points = self.compute_new_position(angle)

        # drop the oldest POINTS_PER_MOVE points
        self.trajectory = self.trajectory[POINTS_PER_MOVE:]

        # add the new points at the end
        for point in new_points:
            self.trajectory.append(point)

        last_point = new_points[-1]
        self.x = last_point[0]
        self.y = last_point[1]
        self.angle = self.angle + angle

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
