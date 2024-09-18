# Real-time Anomaly Detection in Data Streams

## Introduction

This Python script simulates a real-time data stream, detects anomalies in the data using the Z-Score method, and logs those anomalies to a file while visualizing the data and anomalies in real-time. This is useful for scenarios where continuous monitoring of metrics (e.g., financial transactions, system metrics) is required, and anomalies such as sudden spikes or deviations need to be identified on the fly.

## Libraries Used

- **NumPy**: For numerical computations, generating data, and calculating statistics (mean, standard deviation).
- **Random**: To add randomness and introduce anomalies in the data stream.
- **Matplotlib**: For real-time visualization of the data stream and detected anomalies.
- **OS**: For handling file operations (optional if logging in a specific directory).
- **Time**: To simulate real-time data stream processing with delays.

### Installation

Ensure you have Python 3.x installed. Then, install the required libraries:

```
pip install numpy matplotlib
```

---

## Code Breakdown

### 1. **Importing Libraries**

```python
import numpy as np
import random
import matplotlib.pyplot as plt
import os
import time
```

- `numpy`: Used for generating numerical data, calculating mean, standard deviation, and handling arrays.
- `random`: Generates random values for noise and simulates anomalies in the data.
- `matplotlib.pyplot`: For plotting the data stream and anomalies in real-time.
- `os`: Optional, if you need to manage file paths, such as logging to a specific location.
- `time`: Used to simulate real-time data processing with delays.

---

### 2. **Simulating the Data Stream**

```python
def generate_data_point(t):
    seasonal = np.sin(0.1 * t)
    noise = np.random.normal(0, 0.5)
    data_point = seasonal + noise

    if random.random() < 0.01:  # 1% chance of an anomaly
        data_point += random.choice([5, -5])

    return data_point
```

- This function generates a single data point that combines:
  - **Seasonal component** (using a sine function).
  - **Random noise** to simulate real-world data behavior.
  - **Anomalies**: A 1% chance to add a large spike or drop to simulate an anomaly.
- It returns the generated data point at each time step `t`.

---

### 3. **Anomaly Detection Using Z-Score**

```python
def detect_anomalies(data, threshold=3):
    mean = np.mean(data)
    std_dev = np.std(data)
    anomalies = []

    for i, point in enumerate(data):
        z_score = (point - mean) / std_dev
        if np.abs(z_score) > threshold:
            anomalies.append((i, point))

    return anomalies
```

- **Z-Score Method**: This function calculates the Z-score for each data point, which is a measure of how many standard deviations away the point is from the mean.
- If a point’s Z-score exceeds a given threshold (default is 3), it is flagged as an anomaly.
- The function returns a list of anomalies in the form of tuples `(index, value)`.

---

### 4. **Real-Time Data Visualization**

```python
def visualize_data_stream_realtime(data, anomalies):
    plt.clf()
    plt.plot(data, label='Data Stream')

    if anomalies:
        anomaly_points = [x[1] for x in anomalies]
        anomaly_indices = [x[0] for x in anomalies]
        plt.scatter(anomaly_indices, anomaly_points, color='r', label='Anomalies')

    plt.legend()
    plt.pause(0.01)
```

- **Clear the Plot (`plt.clf()`)**: This ensures that each frame is updated, creating a smooth real-time plotting effect.
- The current data stream is plotted, and anomalies (if detected) are highlighted as red scatter points.
- **`plt.pause(0.01)`**: Used to briefly pause and update the plot in real-time.

---

### 5. **Main Function**

```python
def main():
    data_stream = []
    anomalies_log = []
    log_file_path = "anomaly_log.txt"

    with open(log_file_path, "w") as log_file:
        plt.ion()  # Enable interactive mode
        t = 0
        try:
            while True:
                new_data_point = generate_data_point(t)
                data_stream.append(new_data_point)

                if len(data_stream) > 100:
                    recent_data = data_stream[-100:]
                    anomalies = detect_anomalies(recent_data, threshold=3)
                else:
                    anomalies = detect_anomalies(data_stream, threshold=3)

                for idx, value in anomalies:
                    anomaly_idx = t - len(recent_data) + idx if len(data_stream) > 100 else idx
                    anomalies_log.append((anomaly_idx, value))
                    log_file.write(f"Anomaly at index {anomaly_idx} with value {value}
")
                    log_file.flush()

                visualize_data_stream_realtime(data_stream, anomalies_log)

                t += 1
                time.sleep(0.1)

        except KeyboardInterrupt:
            print(f"
Real-time anomaly detection stopped. {len(anomalies_log)} anomalies logged.")
            plt.ioff()
```

- **Data Stream**: A list (`data_stream`) that holds the generated data points.
- **Logging**: The file `anomaly_log.txt` is created and anomalies are logged in real-time. Each detected anomaly’s index and value are written to the file.
- **Interactive Mode**: `plt.ion()` enables real-time interactive plotting with `matplotlib`.
- **Real-time Detection and Visualization**:
  - The script continuously generates data points and detects anomalies using a sliding window of 100 data points (if available).
  - It updates the plot and logs anomalies in real-time.

- **Stopping the Script**: The script runs indefinitely until manually stopped by pressing `Ctrl+C`, at which point the loop is interrupted with `KeyboardInterrupt`.

---

## How to Run the Script

1. **Install Required Libraries**:
   Run the following command in your terminal to install necessary packages:

```
pip install numpy matplotlib
```

2. **Save the Script**:
   Save the script as `real_time_anomaly_detection.py`.

3. **Run the Script**:
   Open your terminal or command prompt and run:

```
python real_time_anomaly_detection.py
```

4. **View the Output**:
   - A real-time plot of the data stream and anomalies will be displayed.
   - Anomalies are logged to the file `anomaly_log.txt` in the current working directory.

5. **Stop the Script**:
   To stop the real-time processing, press `Ctrl+C` in the terminal.

---

## Customization

1. **Threshold Adjustment**:
   You can adjust the anomaly detection sensitivity by changing the threshold value in the `detect_anomalies` function.

```python
anomalies = detect_anomalies(data_stream, threshold=2.5)
```

2. **Window Size for Anomaly Detection**:
   The sliding window size for detecting anomalies is set to 100 data points. You can modify this to fit your needs:

```python
recent_data = data_stream[-200:]  # Use the last 200 data points
```

3. **Real-time Delay**:
   You can adjust the speed of real-time data generation by modifying the delay in the `time.sleep()` function.

```python
time.sleep(0.05)  # Faster, with 50ms delay between points
```

---

## Conclusion

This script offers a simple yet powerful approach to real-time anomaly detection and logging. By using a combination of a sliding window for Z-Score detection and real-time visualization with `matplotlib`, you can continuously monitor data streams and quickly identify deviations from the norm.
