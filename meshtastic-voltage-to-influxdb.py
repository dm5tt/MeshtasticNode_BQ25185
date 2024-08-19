import subprocess
import re
from influxdb import InfluxDBClient
import time

def execute_meshtastic_command(device_id):
    command = f"/home/had/bin/meshtastic --host 192.168.1.4 --request-telemetry --dest \\!{device_id}"
    output = subprocess.getoutput(command)
    return output

def parse_output(output):
    voltage_pattern = r"Voltage:\s+(\d+\.\d+)\s+V"
    device_id_pattern = r"Sending telemetry request to \!(\w+)"

    voltage_match = re.search(voltage_pattern, output)
    device_id_match = re.search(device_id_pattern, output)

    if voltage_match and device_id_match:
        voltage = voltage_match.group(1)
        device_id = device_id_match.group(1)
        return device_id, voltage
    else:
        raise ValueError("Could not parse output. Check if the command output is correct.")

def send_to_influxdb(device_id, voltage):
    client = InfluxDBClient(host='localhost', port=8086, database='meshtastic', username='meshuser', password='')
    json_body = [
        {
            "measurement": "telemetry",
            "tags": {
                "device_id": device_id,
            },
            "fields": {
                "voltage": float(voltage)
            }
        }
    ]
    client.write_points(json_body)
    print(f"Data sent to InfluxDB: {json_body}")

def main(device_ids):
    max_attempts = 4

    for device_id in device_ids:
        attempts = 0

        while attempts < max_attempts:
            output = execute_meshtastic_command(device_id)
            try:
                parsed_device_id, voltage = parse_output(output)
                send_to_influxdb(parsed_device_id, voltage)
                break
            except ValueError as e:
                print(f"Error processing device {device_id}: {e}")
                attempts += 1
                time.sleep(1)

        if attempts == max_attempts:
            print(f"Failed to process device {device_id} after {max_attempts} attempts.")

device_ids = ['bdc1842c']

if __name__ == "__main__":
    main(device_ids)
