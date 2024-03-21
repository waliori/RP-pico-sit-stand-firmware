from machine import I2C
import ustruct
import math
class SMAFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.data = []

    def add(self, value):
        self.data.append(value)
        if len(self.data) > self.window_size:
            self.data.pop(0)

    def get(self):
        return sum(self.data) / len(self.data) if self.data else None

    def get_std(self):
        if not self.data:
            return None
        mean = self.get()
        variance = sum((x - mean) ** 2 for x in self.data) / len(self.data)
        return variance ** 0.5


class Accelerometer:
    # Constants
    ADXL345_ADDRESS = 0x53
    ADXL345_POWER_CTL = 0x2D
    ADXL345_DATA_FORMAT = 0x31
    ADXL345_DATAX0 = 0x32

    # Initialization with configurable thresholds
    def __init__(self, sda, scl, freq, collision_threshold=2, obstacle_threshold_factor=1.5, debounce_count=1):
        # Initialize I2C
        self.i2c = I2C(1, sda=sda, scl=scl, freq=freq)

        # Initialize ADXL345
        self.i2c.writeto_mem(self.ADXL345_ADDRESS, self.ADXL345_POWER_CTL, bytearray([0x08]))  # Measurement mode
        self.i2c.writeto_mem(self.ADXL345_ADDRESS, self.ADXL345_DATA_FORMAT, bytearray([0x0B]))  # Full resolution, +/- 16g

        # Configurable parameters
        self.COLLISION_THRESHOLD = collision_threshold
        self.OBSTACLE_THRESHOLD_FACTOR = obstacle_threshold_factor
        self.DEBOUNCE_COUNT = debounce_count

        # Initialize filters
        self.x_filter = SMAFilter(5)
        self.y_filter = SMAFilter(5)
        self.z_filter = SMAFilter(5)

        # Store the last readings for comparison
        self.last_x, self.last_y, self.last_z = self.read_accel_data()
        self.collision_count = 0
        self.obstacle_count = 0            

    def read_accel_data(self):
        data = self.i2c.readfrom_mem(self.ADXL345_ADDRESS, self.ADXL345_DATAX0, 6)
        x, y, z = ustruct.unpack('<3h', data)
        self.x_filter.add(x)
        self.y_filter.add(y)
        self.z_filter.add(z)
        return self.x_filter.get(), self.y_filter.get(), self.z_filter.get()

    def low_pass_filter(self, current, last, alpha=0.5):
        return last * alpha + current * (1 - alpha)

    def detect_change(self, x, y, z):
        # Using dynamic threshold based on standard deviation
        std_x, std_y, std_z = self.x_filter.get_std(), self.y_filter.get_std(), self.z_filter.get_std()

        # In case std_x, std_y, or std_z is None, set a default value
        std_x = std_x if std_x is not None else 1
        std_y = std_y if std_y is not None else 1
        std_z = std_z if std_z is not None else 1

        dynamic_threshold = self.OBSTACLE_THRESHOLD_FACTOR * max(std_x, std_y, std_z)

        x = self.low_pass_filter(x, self.last_x)
        y = self.low_pass_filter(y, self.last_y)
        z = self.low_pass_filter(z, self.last_z)

        dx = abs(x - self.last_x)
        dy = abs(y - self.last_y)
        dz = abs(z - self.last_z)
        return dx > dynamic_threshold or dy > dynamic_threshold or dz > dynamic_threshold

    def detect_collision(self, x, y, z):
        x = self.low_pass_filter(x, self.last_x)
        y = self.low_pass_filter(y, self.last_y)
        z = self.low_pass_filter(z, self.last_z)

        dx = abs(x - self.last_x)
        dy = abs(y - self.last_y)
        dz = abs(z - self.last_z)
        return dx > self.COLLISION_THRESHOLD or dy > self.COLLISION_THRESHOLD or dz > self.COLLISION_THRESHOLD

    def debounce_detection(self, detection_func, x, y, z, count_var):
        if detection_func(x, y, z):
            setattr(self, count_var, getattr(self, count_var) + 1)
            if getattr(self, count_var) >= self.DEBOUNCE_COUNT:
                setattr(self, count_var, 0)
                return True
        else:
            setattr(self, count_var, 0)
        return False

    def show_accel(self):
        x, y, z = self.read_accel_data()
        #print(f"X: {x}, Y: {y}, Z: {z}")        
#         if self.debounce_detection(self.detect_collision, x, y, z, 'collision_count'):
#             print("Collision detected!")
#         if self.debounce_detection(self.detect_change, x, y, z, 'obstacle_count'):
#             print("Obstacle detected!")

        self.last_x, self.last_y, self.last_z = x, y, z