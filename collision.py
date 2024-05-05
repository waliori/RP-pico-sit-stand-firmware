class Collision:
    def __init__(self, calibrationO):
        self.calibration_data = calibrationO.calib
        self.distance_window_up = []
        self.distance_window_down = []
        self.window_size = 10
        self.sensitivity_up = 8.0  # Sensitivity for upward movement
        self.sensitivity_down = 10.0  # Sensitivity for downward movement

    def detect_obstacle(self, direction, sensor_data):
        # Normalize the sensor data
        normalized_data = self.normalize_data(sensor_data)

        # Set the calibration data and distance window based on the direction
        if direction == 1:  # Going up
            principal_components = self.calibration_data["principal_components_up"]
            projected_mean = self.calibration_data["projected_mean_up"]
            distance_window = self.distance_window_up
            sensitivity = self.sensitivity_up
        else:  # Going down
            principal_components = self.calibration_data["principal_components_down"]
            projected_mean = self.calibration_data["projected_mean_down"]
            distance_window = self.distance_window_down
            sensitivity = self.sensitivity_down

        # Project the normalized sensor data onto the principal components
        projected_data = [
            sum(normalized_data[i] * principal_components[j][i] for i in range(len(principal_components[0]))) - projected_mean[j]
            for j in range(len(principal_components))
        ]

        # Calculate the distance between the projected normalized sensor data and the projected mean
        distance = sum(x ** 2 for x in projected_data) ** 0.5
        print(f"direction:{direction}, distance: {distance}")

        # Update the sliding window with the new distance value
        distance_window.append(distance)
        if len(distance_window) > self.window_size:
            distance_window.pop(0)

        # Calculate the mean and standard deviation of the distances in the sliding window
        mean_distance = sum(distance_window) / len(distance_window)
        std_dev_distance = (sum((x - mean_distance) ** 2 for x in distance_window) / len(distance_window)) ** 0.5

        # Set the adaptive threshold distance
        threshold_distance = mean_distance + sensitivity * std_dev_distance
        print(f"threshold_distance:{threshold_distance}")

        # Check if the distance exceeds the adaptive threshold
        if distance > threshold_distance:
            print("Distance exceeds the adaptive threshold")
            return True
        else:
            return False
        
    def normalize_data(self, data):
        # Extract acceleration, RPM, and current values from the data
        accel_x, accel_y, accel_z, rpm, current = data

        # Normalize acceleration values
        min_accel = self.calibration_data["accel_down"]
        max_accel = self.calibration_data["accel_up"]
        normalized_accel_x = (accel_x - min_accel[0]) / (max_accel[0] - min_accel[0])
        normalized_accel_y = (accel_y - min_accel[1]) / (max_accel[1] - min_accel[1])
        normalized_accel_z = (accel_z - min_accel[2]) / (max_accel[2] - min_accel[2])

        # Normalize RPM value
        min_rpm = self.calibration_data["rpm_down"]
        max_rpm = self.calibration_data["rpm_up"]
        normalized_rpm = (rpm - min_rpm) / (max_rpm - min_rpm)

        # Normalize current value
        min_current = self.calibration_data["current_down"]
        max_current = self.calibration_data["current_up"]
        normalized_current = (current - min_current) / (max_current - min_current)

        # Return the normalized data as a list
        return [normalized_accel_x, normalized_accel_y, normalized_accel_z, normalized_rpm, normalized_current]