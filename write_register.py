import yaml
from pyModbusTCP.client import ModbusClient


class ModbusRegisterHandler:
    def __init__(self, config_file, host="192.168.1.120", port=502):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

        self.modbus_registers = self.config['modbus_registers']
        self.client = ModbusClient(host=host, port=port)
        self.client.open()

    def get_register_by_address(self, address):
        register = None
        for reg in self.modbus_registers:
            if reg['address'] == address:
                register = reg
                break

        if register is None:
            print(f"Address {address} not found in the configuration.")
            return None

        return register

    def write_register(self):
        for reg in self.modbus_registers:
            address = reg['address']
            data_type = reg['data_type']
            write_value = reg['write_value']

            if data_type == 'bool':
                value = int(write_value)
            elif data_type == 'real':
                import struct
                value = struct.unpack('>HH', struct.pack('>f', float(write_value)))
            else:
                value = [int(write_value)]

            result = self.client.write_multiple_registers(address, value)

            if result:
                print(f"Write successful to address {address}")
            else:
                print(f"Write error to address {address}")

    def close(self):
        self.client.close()


# Example usage
handler = ModbusRegisterHandler('write_modbus_config.yaml')

# Write the values defined in the configuration file to the registers
handler.write_register()

handler.close()
