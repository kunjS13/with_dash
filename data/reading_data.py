import os
import pandas as pd

def read_xbee_data(folder_path):
    header_data = {}
    
    for filename in os.listdir(folder_path):
        if filename.startswith("xbee_data_"):
            packet_count = int(filename.split('_')[-1].split('.')[0])
            
            # Read the CSV file
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            
            # Store the data for each header
            for header in df.columns:
                if header != 'TEAM_ID':
                    if header not in header_data:
                        header_data[header] = []
                    header_data[header].append(df[header][0])  # Assuming second row is the corresponding values

    return header_data

if __name__ == "__main__":
    folder_path = 'data/each_second'
    data = read_xbee_data(folder_path)
    for header, values in data.items():
        print(header, values)
