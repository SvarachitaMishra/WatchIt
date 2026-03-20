import numpy as np
import pandas as pd
import time
from scipy.signal import find_peaks

class StressCalculator:
    def __init__(self, heart_rate_data, accelerometer_data):
        self.heart_rate_data = heart_rate_data  # Heart rate data as a list
        self.accelerometer_data = accelerometer_data  # Accelerometer data as a DataFrame

    def calculate_hrv(self):
        # Calculate heart rate variability using RR intervals
        rr_intervals = np.diff(self.heart_rate_data)
        mean_rr = np.mean(rr_intervals)
        std_rr = np.std(rr_intervals)
        return std_rr  # Return the standard deviation of RR intervals as HRV

    def process_accelerometer_data(self):
        # Process accelerometer data
        # Let's assume we calculate the magnitude of acceleration
        self.accelerometer_data['magnitude'] = np.sqrt(
            self.accelerometer_data['x'] ** 2 + 
            self.accelerometer_data['y'] ** 2 + 
            self.accelerometer_data['z'] ** 2
        )
        return self.accelerometer_data['magnitude']

    def score_stress(self, hrv, acc_data):
        # Score stress based on HRV and accelerometer magnitude
        avg_acc = np.mean(acc_data)
        if hrv < 50 and avg_acc > 1.5:
            return 'High Stress'
        elif hrv < 100 and avg_acc <= 1.5:
            return 'Medium Stress'
        else:
            return 'Low Stress'

    def calculate_stress(self):
        start_time = time.time()
        hrv = self.calculate_hrv()
        acc_data = self.process_accelerometer_data()
        stress_score = self.score_stress(hrv, acc_data)
        duration = time.time() - start_time

        if duration > 5:
            raise ValueError('Calculation took too long!')
        return stress_score

# Example usage
if __name__ == '__main__':
    # Simulated data for testing
    heart_rate_data = [60, 62, 58, 61, 59, 63]  # Simulated RR intervals
    accelerometer_data = pd.DataFrame({
        'x': [0.0, 0.1, -0.1, 0.2, -0.2],
        'y': [0.0, 0.05, -0.05, 0.1, -0.1],
        'z': [1.0, 1.1, 0.9, 1.2, 0.8]
    })
    stress_calculator = StressCalculator(heart_rate_data, accelerometer_data)
    print(stress_calculator.calculate_stress())
