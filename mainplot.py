import argparse
from plots.visualization  import DataPlotter

def main():
    parser = argparse.ArgumentParser(description="Generate various types of plots from CSV data.")
    parser.add_argument("data_path",  help="Path to the CSV data file")
    parser.add_argument("plot_name", help="Name for the output plot file")
    parser.add_argument("plot_type", choices=["line", "bar", "heatmap", "box", "histogram", "rolling_average"], help="Type of plot to generate")
    parser.add_argument("x_column", help="Column name for x-axis data")
    parser.add_argument("y_column", help="Column name for y-axis data")
    parser.add_argument("save_directory", default="plots", help="Directory to save the plot")
    parser.add_argument("title", default="Data Plot", help="Title for the plot")

    args = parser.parse_args()
    plotter = DataPlotter(args.data_path, args.plot_name, args.plot_type, args.x_column, args.y_column, args.save_directory, args.title)
    plotter.plot()


if __name__ == "__main__":
    main()
