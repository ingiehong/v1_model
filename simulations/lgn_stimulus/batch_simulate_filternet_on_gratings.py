import json
import os

"""
simulate the LGN network on gratings. To see/tweak parameters of the simulation, 
refer to/change the base_config defined within the code.
"""
# Define the base JSON content
base_config = {
    "run": {
        "tstop": 12000.0,
        "dt": 1.0
    },
    "target_simulator": "LGNModel",
    "inputs": {
        "LGN_spikes": {
            "input_type": "movie",
            "module": "graiting",
            "row_size": 120,
            "col_size": 240,
            "gray_screen_dur": 4000.0,
            "theta": 0.0,
            "cpd": 0.05,
            "temporal_f": 1.0,
            "contrast": 1.0,
            "evaluation_options": {
                "downsample": 1,
                "separable": True
            }
        }
    },
    "output": {
        "log_file": "../log.txt",
        "output_dir": "./results/12s_SF0.04_TF2.0_ori0.0_c100.0_gs0.5",
        "spikes_csv": "spikes.csv",
        "spikes_h5": "spikes.h5",
        "rates_h5": "rates.h5",
        "overwrite_output_dir": False,
        "log_level": "DEBUG"
    },
    "components": {
        "filter_models_dir": "./filter_components/model_templates"
    },
    "networks": {
        "nodes": [
            {
                "nodes_file": "./network/lgn_nodes.h5",
                "node_types_file": "./network/lgn_node_types.csv"
            }
        ]
    },
    "config_path": "",
    "config_dir": "/Users/owensong/Desktop/Huganir Lab/V1 model/Models/simulations/lgn_stimulus/configs"
}

# Ensure the ./configs directory exists
os.makedirs("./configs", exist_ok=True)

# Theta values
theta_values = [i * 30.0 for i in range(12)]

# Create and run simulations
for theta in theta_values:
    # Update theta and output_dir in the base config
    base_config["inputs"]["LGN_spikes"]["theta"] = theta
    base_config["output"]["output_dir"] = f"./results/12s_SF0.04_TF2.0_ori{theta}_c100.0_gs0.5"
    config_filename = f"config.filternet.dg.2Hz.{theta}deg.4s.json"
    base_config["config_path"] = f"/Users/owensong/Desktop/Huganir Lab/V1 model/Models/simulations/lgn_stimulus/configs/{config_filename}"

    # Generate the JSON file
    json_filepath = f"./configs/{config_filename}"
    with open(json_filepath, 'w') as json_file:
        json.dump(base_config, json_file, indent=4)

    # Run 10 simulations for each JSON file
    for trial in range(10):
        print(f"Starting trial {trial}, theta = {theta}")
        # Modify output file names for each trial
        base_config["output"]["spikes_csv"] = f"spikes.trial_{trial}.csv"
        base_config["output"]["spikes_h5"] = f"spikes.trial_{trial}.h5"
        base_config["output"]["rates_h5"] = f"rates.trial_{trial}.h5"

        # Save the modified JSON file for this trial
        trial_json_filename = f"config.filternet.dg.2Hz.{theta}deg.4s.trial_{trial}.json"
        trial_json_filepath = f"./configs/{trial_json_filename}"
        with open(trial_json_filepath, 'w') as trial_json_file:
            json.dump(base_config, trial_json_file, indent=4)

        # Run the simulation
        os.system(f"python run_filternet.py {trial_json_filepath}")
