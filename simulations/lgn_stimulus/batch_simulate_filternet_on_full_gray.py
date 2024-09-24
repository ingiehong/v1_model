import json
import os

"""
simulate the LGN network on full gray stimuli. To see/tweak parameters of the simulation, 
refer to/change the corresponding file in the configs folder.
"""
# Define the base configuration path
base_config_path = "./configs/config.filternet.full_gray.12s.json"
with open(base_config_path, 'r') as file:
    base_config = json.load(file)

# Ensure the ./configs directory exists
os.makedirs("./configs", exist_ok=True)

# Run 10 simulations
for trial in range(10):
    print(f"Trial {trial}")
    # Modify output file names for each trial
    base_config["output"]["spikes_csv"] = f"12s_full_gray/spikes.trial_{trial}.csv"
    base_config["output"]["spikes_h5"] = f"12s_full_gray/spikes.trial_{trial}.h5"

    # Save the modified JSON file for this trial
    trial_json_filename = f"config.filternet.full_gray.12s.trial_{trial}.json"
    trial_json_filepath = f"./configs/{trial_json_filename}"
    with open(trial_json_filepath, 'w') as trial_json_file:
        json.dump(base_config, trial_json_file, indent=4)

    # Run the simulation
    os.system(f"python run_filternet.py {trial_json_filepath}")
