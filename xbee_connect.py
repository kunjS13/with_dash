import serial
import csv

ser = serial.Serial('COM8', 9600) 

# Open the CSV file
with open('data/xbee_stream/data.csv', 'a', newline='') as f:
    writer = csv.writer(f)

    while True:
        try:
            line = ser.readline().decode('Ascii').strip()
            packets = line.split(',')
            writer.writerow(packets)

        except KeyboardInterrupt:
            break

# Close the serial port
ser.close()