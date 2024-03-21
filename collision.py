from mpu9250 import MPU9250
import utime
import math

# Assuming MPU9250, MPU6500, and AK8963 classes are defined elsewhere

class CollisionDetector:
    def __init__(self, i2c, soft_threshold=9.43800118535422, hard_threshold=9.737911225701378, gyro_threshold=0.2808514652826003, window_size=20, debounce_count=6):
        self.mpu9250 = MPU9250(i2c)
        self.soft_threshold = soft_threshold
        self.hard_threshold = hard_threshold
        self.gyro_threshold = gyro_threshold
        self.window_size = window_size
        self.debounce_count = debounce_count  # New attribute for debounce mechanism
        self.accel_window = []
        self.gyro_window = []
        self.collision_count = {'soft': 0, 'hard': 0, 'rotation': 0}  # Track consecutive collisions
        self.operational_noise_buffer = 0.0
        self.operational_gyro_noise_buffer = 0.0
        self.calculate_operational_noise_buffer()

    def calculate_operational_noise_buffer(self, measurement_duration=5000):
        start_time = utime.ticks_ms()
        accel_data = []
        gyro_data = []

        while utime.ticks_diff(utime.ticks_ms(), start_time) < measurement_duration:
            accel = self.mpu9250.acceleration
            gyro = self.mpu9250.gyro
            accel_data.append(accel)
            gyro_data.append(gyro)
            utime.sleep_ms(100)  # Short delay between readings

        # Calculate the standard deviation for each axis as operational noise
        axis_data = list(zip(*accel_data))
        gyro_axis_data = list(zip(*gyro_data))
        noise_levels = [math.sqrt(sum([(x - sum(axis) / len(axis)) ** 2 for x in axis]) / len(axis)) for axis in axis_data]
        gyro_noise_levels = [math.sqrt(sum([(x - sum(axis) / len(axis)) ** 2 for x in axis]) / len(axis)) for axis in gyro_axis_data]
        self.operational_noise_buffer = max(noise_levels)  # This is a simplistic approach
        self.operational_gyro_noise_buffer = max(gyro_noise_levels)

    def collision_detected(self):
        """
        Simplified method to detect any type of collision or significant rotation.
        
        :return: True if any collision or significant rotation is detected, False otherwise.
        """
        collision_type = self.detect_collision()
        if collision_type in ['hard', 'soft', 'rotation']:
            print(f"{collision_type} collision/rotation detected!")
            return True
        return False

    def update_windows(self, accel, gyro):
        """
        Updates the windows of acceleration and gyroscope readings for moving average calculation.
        """
        if len(self.accel_window) >= self.window_size:
            self.accel_window.pop(0)
            self.gyro_window.pop(0)
        
        self.accel_window.append(accel)
        self.gyro_window.append(gyro)

    def moving_average(self, data_window):
        """
        Calculates the moving average for a given window of readings.
        """
        if not data_window:
            return 0
        avg = [sum(x) / len(data_window) for x in zip(*data_window)]
        return math.sqrt(sum([x**2 for x in avg]))

    def detect_collision(self):
        """
        Detects collisions, including soft obstacles, using both acceleration and gyroscope data.
        
        :return: 'hard' if a hard collision is detected, 'soft' for a soft collision, 'rotation' for significant rotation, None otherwise.
        """
        current_accel = self.mpu9250.acceleration
        current_gyro = self.mpu9250.gyro
        self.update_windows(current_accel, current_gyro)
        
        avg_accel_change = self.moving_average(self.accel_window)
        avg_gyro_change = self.moving_average(self.gyro_window)
        
        detected_collision = None
        if avg_accel_change > self.hard_threshold + self.operational_noise_buffer:
            detected_collision = 'hard'
        elif avg_accel_change > self.soft_threshold + self.operational_noise_buffer:
            detected_collision = 'soft'
        elif avg_gyro_change > self.gyro_threshold + self.operational_gyro_noise_buffer:
            detected_collision = 'rotation'
        
        # Implement debounce mechanism
        if detected_collision:
            self.collision_count[detected_collision] += 1
            if self.collision_count[detected_collision] >= self.debounce_count:
                self.reset_collision_count()
                return detected_collision
        else:
            self.reset_collision_count()

        return None
    
    def reset_collision_count(self):
        for key in self.collision_count:
            self.collision_count[key] = 0

