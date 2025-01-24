import serial  # Teraz nie ma konfliktu z nazwą pliku
import time
import csv

# Ustawienia portu szeregowego
port = "COM5"  # Ustaw odpowiedni port szeregowy (dla systemu Windows COMx, dla Linux /dev/ttyUSBx)
baudrate = 9600  # Prędkość transmisji


fields = ['time', 'acc_X', 'acc_Y', 'acc_Z', 'gyro_X', 'gyro_Y', 'gyro_Z']

# Otwieramy port szeregowy
ser = serial.Serial(port, baudrate, timeout=1)
time.sleep(1)
count=0

while(count < 30):
    received_data = []
    # Wysłanie znaku "x"

    # Czekamy chwilę, aby odbiorca miał czas na odpowiedź

    # Odczytanie danych z portu szeregowego
    if ser.in_waiting > 0:
        received_data = ser.readline().decode('utf-8').strip()  # Odczytujemy dane i dekodujemy je
        received_data = eval(f"[{received_data}]")
        #print(f"Odczytano: {received_data}")
    if len(received_data) == 0:
        continue

    count += 1
    file_path = f"avada2/avada{count:03}.csv"

    with open(file_path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(received_data)
        
    print(f'New data appended to CSV file {file_path}')

ser.close()