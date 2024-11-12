import os
import streamlit as st
import pandas as pd
from plots.visualization import DataPlotter  # Ensure correct path to DataPlotter class
from io import BytesIO
from PIL import Image

# Streamlit App Title
st.title("NOAA Data Plotting Application")

# File Uploader for CSV data
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# If a file is uploaded
if uploaded_file:
    # Read CSV into DataFrame
    data = pd.read_csv(uploaded_file)
    data.columns = data.columns.str.strip() 
    st.write("Data Preview:")
    st.write(data.head())

    # Select X and Y Columns
    x_column = st.selectbox("Select the X-axis column", options=data.columns)
    y_column = st.selectbox("Select the Y-axis column", options=data.columns)

    # Select Plot Type
    plot_type = st.selectbox(
        "Select Plot Type",
        options=["line", "bar", "heatmap", "box", "histogram", "rolling_average"]
    )
    
    # Plot Title
    plot_title = st.text_input("Plot Title", value="Data Plot")

    # Specify Plot Name and Save Directory
    plot_name = st.text_input("Plot Name", value="my_plot")
    save_directory = "plots"
    
    # Create the plot
    if st.button("Generate Plot"):
        # Pass DataFrame directly to DataPlotter
        plotter = DataPlotter(
            data_path=None,  # Pass None as it's not used for file loading in this case
            plot_name=plot_name,
            plot_type=plot_type,
            x_column=x_column,
            y_column=y_column,
            save_directory=save_directory,
            title=plot_title
        )
        plotter.data = data  # Directly assign the DataFrame to the plotter

        # Generate and save the plot
        plotter.plot()

        # Display the saved plot image
        plot_path = os.path.join(save_directory, f"{plot_name}_{plot_type}.png")
        if os.path.exists(plot_path):
            image = Image.open(plot_path)
            st.image(image, caption=f"{plot_type.capitalize()} Plot", use_column_width=True)

            # Download Option for the Plot
            with open(plot_path, "rb") as file:
                btn = st.download_button(
                    label="Download Plot",
                    data=file,
                    file_name=f"{plot_name}_{plot_type}.png",
                    mime="image/png"
                )
