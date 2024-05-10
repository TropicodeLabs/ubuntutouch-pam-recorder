import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import librosa as lr

def inspect_device(device_folder, color = "blue"):
    # Step 1: Read and process log file
    device_log_path = os.path.join(device_folder, "pam_output", "pam_recorder_log.txt")
    with open(device_log_path) as f:
        lines = [line.rstrip() for line in f if line[0].isdigit()]
    df = pd.DataFrame(lines, columns=["line"])
    df = df["line"].str.split(",", expand=True)
    df.columns = ["timestamp", "file", "state"]
    df["basename"] = [os.path.basename(x) for x in df["file"]]
    basename_id = df["basename"].str.replace(".flac", "").str.replace("recording_", "")
    df["date"] = basename_id.str[:8]
    df["time"] = basename_id.str[8:]
    df["datetime"] = pd.to_datetime(df["date"] + df["time"], format="%Y%m%d%H%M%S")
    df["duration"] = [lr.get_duration(filename=os.path.join(device_folder, "pam_output", x)) for x in df["basename"]]

    # Step 2: Plot duration histogram
    plt.figure(figsize=(10, 5))
    duration_histplot = df.duration.plot.hist(bins=100, color=color)  # Set color here
    duration_histplot.set_xlabel("Duration (s)")
    duration_histplot.set_ylabel("Count")
    duration_histplot.set_title("Histogram of file durations")

    # Step 3: Plot number of files per day
    plt.figure(figsize=(10, 5))
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d").dt.date
    number_of_files_per_day = df["date"].value_counts().plot.bar(color=color)  # Set color here
    number_of_files_per_day.set_title("Number of files per day")
    number_of_files_per_day.set_xlabel("Date")
    number_of_files_per_day.set_ylabel("Count")

    # Step 4: Plot number of files per hour
    plt.figure(figsize=(10, 5))
    df["hour"] = df["datetime"].dt.hour
    number_of_files_per_hour_plot = df["hour"].value_counts().sort_index().plot.bar(color=color)  # Set color here
    number_of_files_per_hour_plot.set_title("Number of files per hour")
    number_of_files_per_hour_plot.set_xlabel("Hour")
    number_of_files_per_hour_plot.set_ylabel("Count")

    # Step 5: Calendar line of points plot
    plt.figure(figsize=(20, 5))
    calendar_line_of_points_plot = plt.scatter(df["datetime"], np.zeros(len(df)), s=1, color=color)  # Set color here
    plt.title("Calendar line of points")
    plt.xlabel("Datetime")
    plt.ylabel("Y-axis Label")

    # Step 6: Duration vs datetime plot
    df["datetime"] = pd.to_datetime(df["datetime"])
    duration_vs_datetime_plot = df.plot(x="datetime", y="duration", style=".", color=color)  # Set color here
    duration_vs_datetime_plot.set_title("Duration vs datetime")

    # Step 7: Get total hours information
    first_datetime = df["datetime"].iloc[0]
    last_datetime = df["datetime"].iloc[-1]
    total_hours = (last_datetime - first_datetime).total_seconds() / 3600
    total_hours_recordings = df["duration"].sum() / 3600
    percentage_of_time = total_hours_recordings / total_hours * 100

    print(f"Total hours: {total_hours}")
    print(f"Total hours of recordings: {total_hours_recordings}")
    print(f"Percentage of time covered: {percentage_of_time}%")

    # Return plot objects
    return (
        duration_histplot,
        number_of_files_per_day,
        number_of_files_per_hour_plot,
        calendar_line_of_points_plot,
        duration_vs_datetime_plot,
        df
    )
