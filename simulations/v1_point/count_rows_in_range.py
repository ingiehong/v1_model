import pandas as pd


def count_rows_in_range(file_path, column_name, start, end):
    """
    Counts the number of rows in the CSV file where the column values are within the specified range.
    """
    # Load the CSV file
    df = pd.read_csv(file_path, sep=' ')

    # Count rows with timestamps in the specified range
    count = df[(df[column_name] >= start) & (df[column_name] <= end)].shape[0]

    return count


# Parameters
file_path = '../lgn_stimulus/results/full3_GScorrected_PScorrected_3.0sec_SF0.04_TF2.0_ori0.0_c80.0_gs0.5/spikes.trial_0.csv'
column_name = 'timestamps'
start = 500.0
end = 3000.0

# Count the rows and print the result
count = count_rows_in_range(file_path, column_name, start, end)
print(f'Number of rows with {column_name} between {start} and {end}: {count}')
