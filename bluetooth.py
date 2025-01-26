import asyncio
from bleak import BleakClient, BleakScanner

# UUID usługi i charakterystyki (dopasuj do tych, które masz w Arduino)
SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-abcdefabcdef"

# Nazwa urządzenia BLE
DEVICE_NAME = "Nano33BLE"

async def run():
    # Skanowanie urządzeń BLE w pobliżu
    print("Skanowanie urządzeń BLE...")
    devices = await BleakScanner.discover()

    # Szukanie urządzenia o nazwie DEVICE_NAME
    target_device = None
    for device in devices:
        if device.name == DEVICE_NAME:
            target_device = device
            break

    if not target_device:
        print(f"Nie znaleziono urządzenia o nazwie {DEVICE_NAME}.")
        return

    print(f"Połączono z urządzeniem: {target_device.name} ({target_device.address})")

    # Połączenie z urządzeniem
    async with BleakClient(target_device.address) as client:
        print("Połączono. Oczekiwanie na dane...")

        # Callback do obsługi danych odbieranych z charakterystyki
        def notification_handler(sender, data):
            print(f"Odebrano dane z charakterystyki {sender}: {data.decode('utf-8')}")

        # Subskrypcja charakterystyki
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        print("Naciśnij Ctrl+C, aby zakończyć...")
        try:
            while True:
                await asyncio.sleep(1)  # Czekaj na dane
        except KeyboardInterrupt:
            print("Rozłączanie...")
            await client.stop_notify(CHARACTERISTIC_UUID)

# Uruchomienie programu
asyncio.run(run())
