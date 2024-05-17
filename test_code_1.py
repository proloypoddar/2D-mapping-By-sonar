import pygame
import serial
import time
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Sonar Mapping ")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize serial port
ser = serial.Serial('COM8', 9600, timeout=1)  # Adjust 'COM3' to your Arduino port
time.sleep(2)  # Wait for the serial connection to initialize

# Center of the screen where the car is fixed
car_x = width // 2
car_y = height // 2

# Scale factor
scale = 10

# List to store sonar points
sonar_points = []

def get_sensor_data():
    line = ser.readline().decode('utf-8').rstrip()
    data = line.split(',')
    if len(data) == 5:
        try:
            left = int(data[0])
            front = int(data[1])
            right = int(data[2])
            direction = data[3]
            step = int(data[4])
            return left, front, right, direction, step
        except ValueError:
            pass
    return None, None, None, None, None

def update_position(x, y, direction, step):
    distance = step * 1  # Assuming each step is 1 cm
    if direction == 'N':
        y -= distance
    elif direction == 'S':
        y += distance
    elif direction == 'E':
        x += distance
    elif direction == 'W':
        x -= distance
    return x, y

def draw_point(screen, color, x, y):
    pygame.draw.circle(screen, color, (x, y), 2)

def main():
    running = True
    clock = pygame.time.Clock()

    global car_x, car_y

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get sensor data
        left, front, right, direction, step = get_sensor_data()

        if left is not None and front is not None and right is not None:
            # Update sonar points relative to the fixed car position
            # Convert steps to movement for updating the sonar points
            dx, dy = update_position(0, 0, direction, step)
            new_car_x = car_x + dx
            new_car_y = car_y + dy

            # Scale and limit the distances
            left = min(left, 30) * scale
            front = min(front, 30) * scale
            right = min(right, 30) * scale

            # Add sonar points relative to the fixed car position
            sonar_points.append((new_car_x - left, new_car_y))   # Left sonar
            sonar_points.append((new_car_x, new_car_y - front))  # Front sonar
            sonar_points.append((new_car_x + right, new_car_y))  # Right sonar

            # Clear the screen and set background to white
            screen.fill(WHITE)

            # Draw all sonar points
            for point in sonar_points:
                draw_point(screen, BLUE, *point)

            # Draw the car's fixed position
            pygame.draw.circle(screen, BLACK, (car_x, car_y), 5)

            # Update the display
            pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    ser.close()

if __name__ == "__main__":
    main()
