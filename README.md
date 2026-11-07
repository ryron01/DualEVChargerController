# Dual EV Charger Controller

An ESP32 controller that lets two Level 1 EV chargers share one 20 A garage circuit. Two relays switch two outlets, and a PZEM-004T energy meter on each outlet reports voltage, current, power, energy and power factor to Home Assistant over ESPHome. An interlock keeps both cars from drawing current at the same time, and a schedule hands charging from car 1 to car 2 overnight.

> [!WARNING]
> This project switches and measures 120 VAC mains. Build it only if you are qualified to work on mains wiring, keep the AC side in an enclosure, and feed the bench setup from a GFCI-protected circuit. Nothing here is a listed or certified product.

## Status

Bench rebuild in progress, November 2026.

- The first deployment could not hold a Wi-Fi connection from inside the enclosure. The controller now uses an ESP32 with an external u.FL antenna (WROOM-32U).
- Both PZEMs share one UART, and earlier attempts saw bus contention between the two TX lines. The bench build is for working that out. See [Shared UART](#shared-uart-between-the-two-pzems).

## Features

- Two outlets with relay control, exposed to Home Assistant as `Car 1 Switch` and `Car 2 Switch`.
- Two-layer interlock. Turning one relay on turns the other off, and if both outlets draw more than 0.5 A anyway, relay 2 is cut.
- Scheduled charging from Home Assistant `input_datetime` helpers: car 1 starts, car 2 takes over at its start time, then stops.
- Automatic handoff when the active car finishes charging early (current stays under 0.5 A for 60 s).
- 16×2 LCD with per-outlet current, charging animation, a done indicator and an interlock warning.
- Two panel switches for manual control without Home Assistant.

## Bench wiring

![Bench wiring diagram](docs/bench-wiring.svg)

An interactive version with the pre-power checklist and pin map is in [`docs/bench-wiring.html`](docs/bench-wiring.html). A PNG is at [`docs/bench-wiring.png`](docs/bench-wiring.png).

### AC side

![AC-side overview](docs/ac-side-overview.svg)

- **Buses.** The GFCI feed lands on Wago 221 buses for L, N and ground. Feed, buses, relay contacts and outlets carry the charging load, so use 12 AWG to match the 20 A circuit.
- **Relays.** Each relay's COM takes L from the bus, and its NO contact feeds the outlet. NO keeps the outlets off when the ESP32 reboots or loses power.
- **CTs.** The CTs are solid-core toroids. Thread each outlet's hot through its CT before landing either end, and run only the hot through it, never L and N together. Keep the CT leads connected to the PZEM whenever load current can flow. The PZEM-004T doesn't report power direction, so CT orientation doesn't change the readings. Wire both channels the same way anyway (red to terminal 3).
- **PZEM voltage inputs.** Both PZEMs take L and N from a tap behind a 1 A fuse, upstream of the relays, so they keep measuring and answering on Modbus with the relays open.
- **PZEM terminal order.** The V4.0 boards have no rear silkscreen. Counting from the `VCC=3.3-5.0V` edge, terminal 1 is N, 2 is L, and 3–4 take the CT leads. Confirm with a meter before applying power: with power off, terminals 3–4 read low ohms through the CT burden resistor.
- **Power for the measurement side.** The PZEM's metering chip runs off the AC voltage terminals. With no mains on terminals 1–2 the module never answers on Modbus, including when you set its address.

### Low-voltage side

The HLK-PM01 supplies 5 V for the ESP32, the relay coils and the LCD. The ESP32's 3V3 pin powers both PZEM interface sides, so their TX lines idle at 3.3 V. The LCD runs at 5 V and connects to the ESP32 through a BSS138 level shifter.

| ESP32 pin | Connects to | Notes |
| --- | --- | --- |
| `GPIO16` | Both PZEM TX | UART2 RX |
| `GPIO17` | Both PZEM RX | UART2 TX |
| `GPIO25` | Relay A `IN` | Car 1 |
| `GPIO26` | Relay B `IN` | Car 2 |
| `GPIO22` | Level shifter `LV1` → LCD `SDA` | PCF8574 backpack at 0x27 |
| `GPIO23` | Level shifter `LV2` → LCD `SCL` | |
| `GPIO32` | Panel switch, car 1 | Input pull-up, switch to GND |
| `GPIO33` | Panel switch, car 2 | Input pull-up, switch to GND |
| `5V` | +5 V rail | From HLK-PM01 |
| `3V3` | +3.3 V rail | PZEM `VCC`, level shifter `LV` |

- **LCD level shifter.** The PCF8574 backpack pulls SDA and SCL up to its own 5 V supply, which is above the ESP32's 3.6 V absolute maximum. Running the backpack at 3.3 V instead leaves the display too faint, and a 3.3 V high is below the PCF8574's 0.7 × VCC (3.5 V) input threshold at 5 V. A BSS138 shifter keeps each side at its own level:

  | Shifter | Connects to |
  | --- | --- |
  | `LV` | 3V3 |
  | `HV` | +5 V |
  | `GND` | GND |
  | `LV1` / `LV2` | `GPIO22` / `GPIO23` |
  | `HV1` / `HV2` | Backpack `SDA` / `SCL` |

  Power down before moving any I2C wire. An unpowered PCF8574 holds the bus low, which crashes the ESP32's I2C recovery (`SCL is held LOW`).
- **Relay trigger.** Set the relay module's trigger jumper to H and confirm it switches from a 3.3 V GPIO.
- **5 V budget.** The HLK-PM01 is rated 600 mA. ESP32 Wi-Fi peaks (about 250 mA), two relay coils (about 90 mA each) and the LCD backlight total roughly 460 mA.

### Shared UART between the two PZEMs

Both PZEMs sit on one Modbus RTU bus at different addresses, 0x01 and 0x02. Every module ships at 0x01, so set the addresses one module at a time, with AC live and only that module connected. See [`tools/pzem`](tools/pzem).

Whether the two TX lines can be tied directly depends on how the PZEM drives TX:

- **Open-collector output.** If an idle TX line sits high through a pull-up of several kΩ, the two lines can be tied together.
- **Push-pull output.** If TX actively drives high, use a diode-OR: one diode per PZEM, cathode toward the PZEM TX, anodes joined at GPIO16, with a 10 kΩ pull-up to 3.3 V. A Schottky (BAT54 or BAT43) leaves more low-level margin than a 1N4148.

## Bill of materials

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | ESP32 DevKitC, WROOM-32U | External u.FL antenna |
| 2 | Peacefair PZEM-004T-100A V4.0 | With solid-core 100 A CT |
| 2 | 1-channel relay module, SONGLE SLA-05VDC-SL-C | 30 A contacts, 5 V coil |
| 1 | HLK-PM01 | 120 VAC to 5 V, 600 mA |
| 1 | 1602 LCD with PCF8574 I2C backpack | Address 0x27, 5 V |
| 1 | BSS138 bidirectional level shifter, 4-channel | Adafruit 757, SparkFun BOB-12009 or generic; 2 channels used |
| 2 | 15 A or 20 A receptacle | One per car |
| 2 | Toggle (maintained) panel switch | On while closed, off when opened |
| 1 | Inline fuse holder, 1 A fuse | For the PZEM and HLK-PM01 tap |
| 5 | Wago 221-415 | L bus, L tap, N bus, N tap |
| 1 | Wago 221-413 | Ground bus |

## Firmware

The ESPHome configuration is [`ev-charger.yaml`](ev-charger.yaml). It was built with ESPHome 2025.5.2.

1. Copy `secrets.example.yaml` to `secrets.yaml` and fill in your values. `secrets.yaml` is git-ignored.
2. Create these Home Assistant helpers, each as a time-only `input_datetime`: `car1_charge_start`, `car1_charge_stop`, `car2_charge_start`, `car2_charge_stop`.
3. Flash:

   ```sh
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   esphome run ev-charger.yaml
   ```

## PZEM tools

Python scripts in [`tools/pzem`](tools/pzem) talk to a PZEM through a USB-to-TTL adapter (CP2102), for setting and checking Modbus addresses off the ESP32. Edit the serial port at the top of each script first.

- `modbus-addr.py` changes the module at address 0x01 to 0x02. Run it with only the second module connected.
- `modbus-trble.py` polls 0x01 and 0x02 and reports which answer.
- `modbus-trble1.py` reads the address register from the module at 0x02.

## Regenerating the diagram

The bench wiring diagram is generated from code, so wire changes stay in sync with the drawing:

```sh
python tools/diagram/build.py
```

PNG output needs `rsvg-convert` (`brew install librsvg`).

## License

[MIT](LICENSE)
