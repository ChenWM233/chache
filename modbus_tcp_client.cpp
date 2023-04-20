#include <iostream>
#include <modbus/modbus.h>

int main() {
    // 设置客户端连接
    const char *host = "192.168.1.120";
    int port = 502;
    modbus_t *client = modbus_new_tcp(host, port);

    if (client == NULL) {
        std::cerr << "Unable to create modbus client" << std::endl;
        return -1;
    }

    // 打开连接
    if (modbus_connect(client) == -1) {
        std::cerr << "Connection failed: " << modbus_strerror(errno) << std::endl;
        modbus_free(client);
        return -1;
    }

    // 读取寄存器
    uint16_t address = 830;
    int num_registers = 5;
    uint16_t result[5];

    int read_result = modbus_read_registers(client, address, num_registers, result);
    if (read_result != -1) {
        std::cout << "Value: " << result[0] << std::endl;
    } else {
        std::cerr << "Read error" << std::endl;
    }

    // 关闭连接
    modbus_close(client);
    modbus_free(client);

    return 0;
}
