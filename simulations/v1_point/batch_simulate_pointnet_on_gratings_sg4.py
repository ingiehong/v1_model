import os
import json
import subprocess

# Base directory of your project
base_dir = os.path.abspath('.')

# Directories for inputs
lgn_base_dir = os.path.join(base_dir, '../lgn_stimulus')
bkg_base_dir = os.path.join(base_dir, '../bkg_inputs')

# Simulation parameters
orientations = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0]
trials = 10

# Template configuration
config_template = {
    "manifest": {
        "$BASE_DIR": base_dir,
        "$NETWORK_DIR": "$BASE_DIR/network",
        "$COMPONENTS_DIR": "$BASE_DIR/components",
        "$OUTPUT_DIR": "",  # Will be updated per simulation
        "$BKG_DIR": bkg_base_dir,
        "$LGN_DIR": lgn_base_dir
    },

    "run": {
        "duration": 12000.0,
        "dt": 0.25
    },

    "inputs": {
        "LGN_spikes": {
            "input_type": "spikes",
            "module": "h5",
            "input_file": "",  # Will be updated per simulation
            "node_set": "lgn"
        },
        "BKG_spikes": {
            "input_type": "spikes",
            "module": "csv",
            "input_file": "",  # Will be updated per simulation,
            "node_set": "bkg"
        }
    },

    "output": {
        "log_file": "log.txt",
        "spikes_file": "",  # Will be updated per simulation
        "spikes_file_csv": "",  # Will be updated per simulation
        "output_dir": "",  # Will be updated per simulation
        "overwrite_output_dir": True,
        "quiet_simulator": True
    },

    "target_simulator": "NEST",

    "components": {
        "point_neuron_models_dir": "$COMPONENTS_DIR/cell_models/nest_models",
        "synaptic_models_dir": "$COMPONENTS_DIR/synaptic_models"
    },

    "networks": {
        "nodes": [
            {
                "nodes_file": "$NETWORK_DIR/v1_nodes.h5",
                "node_types_file": "$NETWORK_DIR/v1_node_types_sg4.csv"
            },
            {
                "nodes_file": "$NETWORK_DIR/lgn_nodes.h5",
                "node_types_file": "$NETWORK_DIR/lgn_node_types.csv"
            },
            {
                "nodes_file": "$NETWORK_DIR/bkg_nodes.h5",
                "node_types_file": "$NETWORK_DIR/bkg_node_types.csv"
            }
        ],
        "edges": [
            {
                "edges_file": "$NETWORK_DIR/v1_v1_edges.h5",
                "edge_types_file": "$NETWORK_DIR/v1_v1_edge_types.csv"
            },
            {
                "edges_file": "$NETWORK_DIR/lgn_v1_edges.h5",
                "edge_types_file": "$NETWORK_DIR/lgn_v1_edge_types.csv"
            },
            {
                "edges_file": "$NETWORK_DIR/bkg_v1_edges.h5",
                "edge_types_file": "$NETWORK_DIR/bkg_v1_edge_types.csv"
            }
        ]
    }
}


# Function to run the simulation
def run_simulation(config_file, num_cores):
    result = subprocess.run(["mpirun", "-np", str(num_cores), "python", "run_pointnet.py", config_file], capture_output=True,
                            text=True)
    print(result.stdout)
    print(result.stderr)
    return result


# Generate and run simulations
for ori in orientations:
    for trial in range(trials):
        # Create unique output directory for each simulation
        output_dir = os.path.join(base_dir, 'output', f'sg4_12s_ori_{ori}_trial_{trial}')
        os.makedirs(output_dir, exist_ok=True)

        # Update the configuration
        config = config_template.copy()
        lgn_input_file = f"$LGN_DIR/results/12s_SF0.04_TF2.0_ori{ori}_c100.0_gs0.5/spikes.trial_{trial}.h5"
        bkg_input_file = f"$BKG_DIR/results/bkg_spikes_n1_fr1000_dt0.25_12s/spikes.trial_{trial}.csv"
        output_spikes_file = f"12s_SF0.04_TF2.0_ori{ori}_c100.0_gs0.5_spikes_trial_{trial}.h5"
        output_spikes_csv_file = f"12s_SF0.04_TF2.0_ori{ori}_c100.0_gs0.5_spikes_trial_{trial}.csv"

        config["manifest"]["$OUTPUT_DIR"] = output_dir
        config["inputs"]["LGN_spikes"]["input_file"] = lgn_input_file
        config["inputs"]["BKG_spikes"]["input_file"] = bkg_input_file
        config["output"]["spikes_file"] = output_spikes_file
        config["output"]["spikes_file_csv"] = output_spikes_csv_file
        config["output"]["output_dir"] = output_dir

        # Write the config file
        config_filename = os.path.join(output_dir, f"config_ori{ori}_trial{trial}.json")
        with open(config_filename, 'w') as f:
            json.dump(config, f, indent=2)

        # Run the simulation
        print(f"Running simulation for ori={ori}, trial={trial}")
        result = run_simulation(config_filename, 1)

        # Check if output files are created
        if not os.path.exists(os.path.join(output_dir, output_spikes_file)):
            print(f"Warning: Output spikes file {output_spikes_file} not found in {output_dir}.")
        if not os.path.exists(os.path.join(output_dir, output_spikes_csv_file)):
            print(f"Warning: Output spikes CSV file {output_spikes_csv_file} not found in {output_dir}.")

        # Check log file for errors
        log_file = os.path.join(output_dir, "log.txt")
        if os.path.exists(log_file):
            with open(log_file, 'r') as log:
                log_content = log.read()
                print(f"Log file content for ori={ori}, trial={trial}:\n{log_content}")
        else:
            print(f"Warning: Log file {log_file} not found in {output_dir}.")

