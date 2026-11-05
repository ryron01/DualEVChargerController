from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(
    port='/dev/tty.usbserial-0001',
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1
)
client.connect()

for addr in [0x01, 0x02]:
    try:
        result = client.read_holding_registers(0x0002, count=1, slave=addr)
        print(f"Address {addr}: responded with {result.registers[0]}")
    except Exception as e:
        print(f"Address {addr}: no response ({e})")

client.close()