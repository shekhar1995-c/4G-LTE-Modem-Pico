from machine import UART, ADC, Pin
import utime
import math

# UART for EC200 module
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
print("UART initialized")

# Thermistor configuration
BETA = 3950
R0 = 10000
T0 = 298.15  # 25°C in Kelvin
adc = ADC(26)  # ADC pin connected to thermistor voltage divider

# Set your actual APN here (replace 'jionet' if needed)
APN = "jionet"

def wait_resp_info(timeout=3000):
    pr = b""
    ts = utime.ticks_ms()
    while (utime.ticks_ms() - ts) < timeout:
        if uart.any():
            pr += uart.read()
    print(pr)
    return pr.decode(errors="ignore")

def send_command(cmd, expected="OK", timeout=2000):
    uart.write(cmd.encode())
    response = wait_resp_info(timeout)
    return expected in response

def read_temperature():
    raw = adc.read_u16()
    voltage = raw * 3.3 / 65535
    resistance = 10000 * (3.3 / voltage - 1)
    temperature = 1 / (1/T0 + (1/BETA) * math.log(resistance / R0)) - 273.15
    return round(temperature, 2)

def get_gps_location():
    send_command('AT+QGPSLOC=2\r\n')
    resp = wait_resp_info()
    if "+QGPSLOC:" in resp:
        try:
            parts = resp.split(":")[1].strip().split(",")
            lat = parts[1]
            lon = parts[2]
            return lat, lon
        except:
            return None, None
    return None, None

def initialize_modem():
    send_command('AT\r\n')
    send_command('ATE0\r\n')
    send_command('AT+CPIN?\r\n')
    send_command('AT+CSQ\r\n')
    send_command('AT+CGREG?\r\n')
    send_command('AT+QIFGCNT=0\r\n')
    send_command(f'AT+QICSGP=1,1,"{APN}","","",1\r\n')
    send_command('AT+QGPS=1\r\n')
    send_command('AT+QIDEACT=1\r\n')
    send_command('AT+QIACT=1\r\n')
    send_command('AT+QIACT?\r\n')

def connect_tcp(server_ip, port):
    send_command('AT+QICLOSE=0\r\n')
    send_command(f'AT+QIOPEN=1,0,"TCP","{server_ip}",{port},0,0\r\n', 'OK', timeout=5000)
    utime.sleep(2)
    return send_command('AT+QISTATE=1,0\r\n')

def send_tcp_data(data):
    send_command('AT+QISEND=0\r\n', '>')
    uart.write(data.encode())
    uart.write(b'\x1A')  # Ctrl+Z
    utime.sleep(2)
    print("Data sent.")

def main():
    initialize_modem()
    if not connect_tcp("192.168.1.100", 5000):
        print("TCP connection failed")
        return

    while True:
        temp = read_temperature()
        lat, lon = get_gps_location()
        tcp_payload = f"{temp},{lat},{lon}*"
        print(f"Sending: {tcp_payload}")
        send_tcp_data(tcp_payload)
        utime.sleep(10)

main()
