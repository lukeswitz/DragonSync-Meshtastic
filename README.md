# DragonSync‑Meshtastic

DragonSync‑Meshtastic is a Python asyncio application that bridges Meshtastic devices with remote‑ID and system telemetry feeds over ZeroMQ. It listens on two ZMQ ports—one for drone bursts, one for system status—and relays each unique transmitter’s position and telemetry as compact TAK PLI and GeoChat packets via the Meshtastic serial interface.

> **Note:** This version no longer uses CoT multicast. FPV message processing has been removed to a separate future module.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [How It Works](#how-it-works)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Configuration](#configuration)  
7. [License](#license)  
8. [Contributing](#contributing)  
9. [Contact](#contact)  

---

## Overview

DragonSync‑Meshtastic listens on two ZeroMQ subscriptions:

- **Drone feed**: raw Remote‑ID bursts (Serial or CAA IDs, location, RSSI, MAC)  
- **System feed**: system status (CPU, temperatures, GPS)  

It deduplicates by transmitter (buffers CAA until matching serial/MAC seen), throttles PLI and GeoChat packets per‑UID, and sends them over a Meshtastic radio for TAK integration.

---

## Features

- **ZMQ → Meshtastic bridge**  
- **Asyncio‑powered**: non‑blocking ZMQ receive + periodic flusher  
- **Throttling**: configurable PLI & GeoChat intervals per device type  
- **Stale cleanup**: drops transmitters after timeout  
- **CAA buffering**: ignore pure CAA bursts until serial/MAC known  
- **Full & short callsigns**: full IDs for drones, short for system  
- **Separate Meshtastic debug flag** to control library verbosity  

---

## How It Works

1. **Startup & CLI**  
   Parses arguments (`--port`, `--zmq-host`, `--zmq-drone-port`, `--zmq-system-port`, `-d`, `--meshtastic-debug`).  
2. **ZMQ Listeners**  
   - **Drone listener**: parses Remote‑ID JSON list/dict, extracts Serial vs. CAA, MAC, RSSI, location, pilot/home.  
   - **System listener**: parses system JSON, builds CPU/Temp/SDR remarks.  
3. **CAA buffering**  
   - On “Serial Number” bursts: register MAC→serial, release any pending CAA.  
   - On “CAA Assigned” bursts: if serial known, append CAA to remarks; otherwise ignore until next serial.  
4. **Flush loop**  
   Every second:  
   - Drop stale UIDs.  
   - For each pending drone/pilot/home update, send PLI if ≥PLI interval, GeoChat if ≥Geo interval.  
5. **Thread‑safe TX**  
   An `asyncio.Lock` ensures only one serial send at a time.

---

## Installation

Clone & install dependencies:

    git clone https://github.com/alphafox02/DragonSync-Meshtastic.git
    cd DragonSync-Meshtastic
    pip install -r requirements.txt

---

## Usage

Run with your Meshtastic port and ZMQ endpoints:

    ./dragonsync_meshtastic.py \
      --port /dev/ttyACM0 \
      --zmq-host 127.0.0.1 \
      --zmq-drone-port 4224 \
      --zmq-system-port 4225 \
      -d \
      --meshtastic-debug

**Options:**

- `--port`             Meshtastic serial port (e.g. `/dev/ttyUSB0`)  
- `--zmq-host`         Host for both ZMQ feeds (default: `127.0.0.1`)  
- `--zmq-drone-port`   ZMQ port for Remote‑ID bursts (default: `4224`)  
- `--zmq-system-port`  ZMQ port for system status (default: `4225`)  
- `-d`, `--debug`      Show full PLI/GeoChat proto dumps  
- `--meshtastic-debug` Enable internal Meshtastic library logging  

---

## Configuration

All behavior is driven by command‑line flags; no additional config file is required. Adjust intervals and timeouts in the script’s constants if desired.

---

## License

This project is MIT‑licensed. See [LICENSE](./LICENSE) for details.

---

## Contributing

Contributions welcome! Please:

1. Fork & branch  
2. Adhere to PEP8  
3. Run existing tests & add new ones  
4. Submit a PR with a clear description  

---

## Contact

For questions or support, visit [cemaxecuter.com](https://www.cemaxecuter.com).  
