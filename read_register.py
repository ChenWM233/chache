from pyModbusTCP.client import ModbusClient
import time
import yaml
import struct

# Function to convert raw Modbus register data to the desired data type
def convert_data(data, data_type):
    if data_type == "word":
        return data[0]
    elif data_type == "int":
        return struct.unpack('>h', struct.pack('>H', data[0]))[0]
    elif data_type == "bool":
        return bool(data[0])
    elif data_type == "real":
        return struct.unpack('>f', struct.pack('>HH', data[0], data[1]))[0]
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

# Read configuration from YAML file
with open('read_modbus_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

modbus_registers = config['modbus_registers']

# set up client connection
client = ModbusClient(host="192.168.1.120", port=502)

# open connection if not already open
if not client.is_open:
    client.open()

while True:
    for register in modbus_registers:
        address = register['address']
        description = register['description']
        data_type = register['data_type']

        # read holding register
        num_registers = 2 if data_type == "real" else 1
        raw_data = client.read_holding_registers(address, num_registers)

        # convert raw data to the specified data type
        if raw_data:
            value = convert_data(raw_data, data_type)
            print(f"Address: {address}, Description: {description}, Value: {value}")
        else:
            print(f"Read error at address {address}")

    # wait for 10ms before the next iteration
    time.sleep(1)

# close connection
client.close()
