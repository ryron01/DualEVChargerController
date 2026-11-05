from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(
    port='/dev/tty.usbserial-0001',
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1
)
client.connect()

result = client.read_holding_registers(0x0002, count=1, slave=0x02)
print(f"PZEM2 responded at address: {result.registers[0]}")

client.close()