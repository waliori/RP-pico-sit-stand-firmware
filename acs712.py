from machine import ADC, Pin

class ACS712:
    def __init__(self, adc_pin, sensitivity=66, aref=3.3, default_output_voltage=2.29, error=0.12):
        self.adc = ADC(Pin(adc_pin))  # Initialize ADC with the given pin
        self.sensitivity = sensitivity  # mV/A, sensitivity of the sensor
        self.aref = aref  # Reference voltage for ADC
        self.default_output_voltage = default_output_voltage  # Default output voltage from sensor (V)
        self.error = error  # Calibration error to adjust
        self.conversion_factor = self.aref / 65535.0  # Conversion factor for ADC reading

    def read_current(self):
        # Read raw ADC value
        analog_value = self.adc.read_u16()
        # Convert ADC value to voltage
        sensor_voltage = (analog_value * self.conversion_factor)
        # Adjust for sensor's default output voltage and convert to millivolts
        sensor_voltage_mv = (sensor_voltage - self.default_output_voltage) * 1000
        # Calculate current from sensor voltage
        dc_current = (sensor_voltage_mv / self.sensitivity) - self.error
        return dc_current
