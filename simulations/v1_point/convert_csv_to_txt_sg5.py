import os
import pandas as pd

# Task 1: Convert CSV files to .txt files
def convert_csv_to_txt(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for ori in range(0, 360, 30):
        for trial in range(10):
            print("ori = ", ori, "trial =", trial)
            subfolder_name = f"sg5_12s_ori_{ori}.0_trial_{trial}"

            csv_file_name = f"12s_SF0.04_TF2.0_ori{ori}.0_c100.0_gs0.5_spikes_trial_{trial}.csv"
            csv_path = os.path.join(input_folder, subfolder_name, csv_file_name)
            txt_file_name = f"12s_SF0.04_TF2.0_ori{ori}.0_c100.0_gs0.5_spikes_trial_{trial}.txt"
            txt_path = os.path.join(output_folder, txt_file_name)

            if os.path.exists(os.path.join(output_folder, txt_file_name)):
                print(f"Output spikes CSV file {txt_file_name} already exists in {output_folder}, skipping....")
            else:
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
    simulation_folder = os.path.join(base_folder, "syngap simulation 5")
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
