import os
import pandas as pd

# Task 1: Convert CSV files to .txt files
def convert_csv_to_txt(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    for trial in range(10):
        print("trial =", trial)
        subfolder_name = f"sg7_12s_full_gray_trial_{trial}"

        csv_file_name = f"12s_full_gray_spikes_trial_{trial}.csv"
        csv_path = os.path.join(input_folder, subfolder_name, csv_file_name)
        txt_file_name = f"12s_full_gray_spikes_trial_{trial}.txt"
        txt_path = os.path.join(output_folder, txt_file_name)

        # Read the CSV file
        df = pd.read_csv(csv_path, sep=' ')

        # Sort by "timestamps" in ascending order
        df_sorted = df.sort_values(by="timestamps")

        # Drop the "population" column
        df_sorted = df_sorted.drop(columns=["population"])

                # Save to .txt file
        df_sorted.to_csv(txt_path, sep=' ', index=False, header=False)


# Task 2: Create "simulation 1" folder and move .txt files
def create_simulation_folder(base_folder):
    simulation_folder = os.path.join(base_folder, "syngap simulation 7")
    if not os.path.exists(simulation_folder):
        os.makedirs(simulation_folder)
    return simulation_folder

def main():
    input_folder = "output"
    output_folder = "simulation_results_and_analysis"
    simulation_folder = create_simulation_folder(output_folder)
    convert_csv_to_txt(input_folder, simulation_folder)

if __name__ == "__main__":
    main()
