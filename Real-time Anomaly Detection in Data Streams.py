import numpy as np
import random
import matplotlib.pyplot as plt
import os
import time

# Step 1: Real-Time Data Stream Simulation
def generate_data_point(t):
    """
    Generates a single data point with seasonal patterns, random noise, 
    and occasional anomalies.
    
    :param t: Current time point
    :return: Single data point
    """
    seasonal = np.sin(0.1 * t)
    noise = np.random.normal(0, 0.5)
    data_point = seasonal + noise
    
    # Add a random anomaly occasionally
    if random.random() < 0.01:  # 1% chance of an anomaly
        data_point += random.choice([5, -5])  # Large spike or drop
    
    return data_point

# Step 2: Anomaly Detection (Z-Score method)
def detect_anomalies(data, threshold=3):
    """
    Detects anomalies in a data stream using Z-score method.
    
    :param data: List representing the data stream
    :param threshold: Z-score threshold for anomaly detection
    :return: List of detected anomalies as tuples (index, value)
    """
    mean = np.mean(data)
    std_dev = np.std(data)
    anomalies = []
    
    for i, point in enumerate(data):
        z_score = (point - mean) / std_dev
        if np.abs(z_score) > threshold:
            anomalies.append((i, point))
    
    return anomalies

# Step 3: Real-Time Visualization
def visualize_data_stream_realtime(data, anomalies):
    """
    Updates the real-time plot of the data stream and highlights detected anomalies.
    
    :param data: List representing the data stream
    :param anomalies: List of detected anomalies
    """
    plt.clf()  # Clear the plot
    plt.plot(data, label='Data Stream')
    if anomalies:
        anomaly_points = [x[1] for x in anomalies]
        anomaly_indices = [x[0] for x in anomalies]
        plt.scatter(anomaly_indices, anomaly_points, color='r', label='Anomalies')
    plt.legend()
    plt.pause(0.01)  # Pause to update the plot

# Main function to execute the real-time anomaly detection and logging
def main():
    data_stream = []
    anomalies_log = []
    
    # Set the log file path to the current directory
    log_file_path = "anomaly_log.txt"
    
    # Open the log file for appending anomalies
    with open(log_file_path, "w") as log_file:
        plt.ion()  # Enable interactive mode for real-time plotting
        t = 0
        try:
            while True:
                # Simulate real-time data point generation
                new_data_point = generate_data_point(t)
                data_stream.append(new_data_point)
                
                # Detect anomalies in real-time (using the last 100 data points for Z-score)
                if len(data_stream) > 100:
                    recent_data = data_stream[-100:]  # Sliding window of 100 data points
                    anomalies = detect_anomalies(recent_data, threshold=3)
                else:
                    anomalies = detect_anomalies(data_stream, threshold=3)
                
                # Log anomalies to file and print in console
                for idx, value in anomalies:
                    anomaly_idx = t - len(recent_data) + idx if len(data_stream) > 100 else idx
                    anomalies_log.append((anomaly_idx, value))
                    log_file.write(f"Anomaly at index {anomaly_idx} with value {value}\n")
                    log_file.flush()  # Ensure the log is written immediately
                
                # Visualize data stream in real-time
                visualize_data_stream_realtime(data_stream, anomalies_log)
                
                t += 1
                time.sleep(0.1)  # Simulate delay for real-time data (e.g., 100ms between data points)
        
        except KeyboardInterrupt:
            print(f"\nReal-time anomaly detection stopped. {len(anomalies_log)} anomalies logged.")
            plt.ioff()  # Disable interactive mode

# Run the script
if __name__ == "__main__":
    main()
