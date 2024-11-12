import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import is_datetime64_any_dtype as is_datetime

sns.set(style="whitegrid")

class DataPlotter:
    def __init__(self, data_path , plot_name, plot_type, x_column=None, y_column=None, save_directory="plots", title="Data Plot"):
        self.data_path = data_path
        self.plot_name = plot_name
        self.plot_type = plot_type
        self.x_column = x_column
        self.y_column = y_column
        self.save_directory = save_directory
        self.title = title
        self.data = None

        if self.data_path is not None:
            self.load_data()

    def load_data(self):
        """Load and preprocess data from the CSV file, cleaning up column names."""
        try:
            self.data = pd.read_csv(self.data_path)
            self.data.columns = self.data.columns.str.strip()  # Remove any extra whitespace from column names
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")

    def determine_xlabel(self):
        """Determine an appropriate label for the x-axis based on the data's date granularity."""
        if is_datetime(self.data[self.x_column]):
            if self.data[self.x_column].dt.is_year_start.all():
                return 'Year'
            elif self.data[self.x_column].dt.is_month_start.all():
                return 'Month'
            else:
                return 'Date'
        return self.x_column

    def plot(self):
        """Generate and save the specified type of plot."""
        plt.figure(figsize=(20, 20))
        xlabel = self.determine_xlabel()
        
        if self.plot_type == "line":
            sns.lineplot(data=self.data, x=self.x_column, y=self.y_column, color='blue')
            plt.title(f"Line Plot - {self.title}")

        elif self.plot_type == "bar":
            sns.barplot(data=self.data, x=self.x_column, y=self.y_column)
            plt.title(f"Bar Plot - {self.title}")

        elif self.plot_type == "heatmap":
            # Assumes the data has 'year' and 'month' for heatmap pivot
            if self.x_column == "year" and self.y_column == "month":
                pivot_data = self.data.pivot(index="year", columns="month", values=self.y_column)
                sns.heatmap(pivot_data, cmap="coolwarm", annot=True)
                plt.title(f"Heatmap - {self.title}")
            else:
                print("For heatmaps, x_column should be 'year' and y_column should be 'month'.")
                return

        elif self.plot_type == "box":
            sns.boxplot(data=self.data, x=self.x_column, y=self.y_column)
            plt.title(f"Box Plot - {self.title}")

        elif self.plot_type == "histogram":
            sns.histplot(self.data[self.y_column], bins=20, kde=True)
            plt.title(f"Histogram - {self.title}")

        elif self.plot_type == "rolling_average":
            # Assuming x_column is time-based, calculate rolling average
            window_size = 12  # For example, a 12-month rolling average
            self.data['rolling_avg'] = self.data[self.y_column].rolling(window=window_size).mean()
            sns.lineplot(data=self.data, x=self.x_column, y='rolling_avg', color='green')
            plt.title(f"Rolling Average Plot - {self.title}")

        else:
            print(f"Plot type '{self.plot_type}' not recognized.")
            return
        
        plt.xlabel(xlabel)
        plt.ylabel(self.y_column.capitalize())
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        plot_path = os.path.join(self.save_directory, f"{self.plot_name}_{self.plot_type}.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"{self.plot_type.capitalize()} saved to {plot_path}")
