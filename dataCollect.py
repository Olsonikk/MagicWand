import serial
import time
import csv
import os
import sys

port = "COM8"  # Change to your serial port
baudrate = 115200

if len(sys.argv) > 1:
    folder_name = sys.argv[1]
else:
    folder_name = input("Choose folder name: ")

# Create folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

fields = ['time', 'acc_X', 'acc_Y', 'acc_Z', 'gyro_X', 'gyro_Y', 'gyro_Z']

ser = serial.Serial(port, baudrate, timeout=1)
time.sleep(1)
count = 0

while(count < 30):
    data_rows = []
    
    while len(data_rows) == 0:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                rows_data = line.split(';')
                for row_str in rows_data:
                    row_str = row_str.strip()
                    if row_str:
                        row = eval(f"[{row_str}]")
                        data_rows.append(row)
        else:
            time.sleep(0.01)

    if len(data_rows) == 0:
        continue

    file_path = f"{folder_name}/{folder_name}{count:04d}.csv"

    with open(file_path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data_rows)
        
    print(f'New data appended to CSV file {file_path}')
    count += 1

ser.close()