from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(
    port='/dev/tty.usbserial-0001',  # verify your CP2102 port in /dev/
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1
)

client.connect()

# Read current address first to confirm comms are working
# result = client.read_holding_registers(0x0002, count=1, slave=0x01)
# print(f"Current address: {result.registers[0]}")

# # Write new address — run this for 0x01 first, then 0x02 on the second module
# client.write_register(0x0002, 0x01, slave=0x01)
# print("Address set to 0x01")

result = client.read_holding_registers(0x0002, count=1, slave=0x01)

client.write_register(0x0002, 0x02, slave=0x01)
print("Address set to 0x02")

client.close()