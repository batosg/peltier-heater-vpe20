import serial
import time

def calculate_bcc(command: str) -> str:
    bcc = 0
    for char in command:
        bcc ^= ord(char)
    return f"{command}{bcc:02X}\r"

def send_command(ser: serial.Serial, command_body: str, delay=0.5):
    full_command = calculate_bcc(command_body)
    print(f"Sending: {repr(full_command)}")
    ser.write(full_command.encode('ascii'))
    time.sleep(delay)
    response = ser.read_all().decode(errors='ignore').strip()
    print("Response:", response)
    return response

def set_temperature(ser: serial.Serial, temp_celsius: int):
    if not (-20 <= temp_celsius <= 110):
        raise ValueError("Temperature must be between -20 and 110 °C")

    # Pad temperature to 5 digits (e.g., 30°C → 00030)
    temp_str = f"{temp_celsius:05d}"
    send_command(ser, f"@00TS{temp_str}")
    run(ser)

def run(ser: serial.Serial):
    send_command(ser, "@01OP0000FF")
def stop(ser: serial.Serial):
    send_command(ser, "@01OP000100")
if __name__ == "__main__":
    COM_PORT = 'COM6'
    BAUDRATE = 9600
    temperatures = [30, 40, 50, 60, 70]

    try:
        with serial.Serial(port=COM_PORT, baudrate=BAUDRATE, timeout=1) as ser:
            for temp in temperatures:
                print(f"\nSetting temperature to {temp} °C")
                set_temperature(ser, temp)
                run(ser)
                print("Waiting 1 minute...\n")
                time.sleep(60)
                stop(ser)

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
