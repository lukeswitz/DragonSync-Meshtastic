# DragonSync-Meshtastic

DragonSync-Meshtastic is a Python-based application designed to bridge data between multicast network messages and Meshtastic devices. The application runs in duplex mode—listening for Cursor-on-Target (CoT) messages via a multicast group and relaying them as TAK packets (PLI and GeoChat) over a Meshtastic serial connection, while also optionally receiving FPV (First Person View) messages through a dedicated serial interface. FPV messages are enriched with GPS data (either from gpsd for live data or a static coordinate for stationary setups) and published via a ZMQ PUB socket.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

DragonSync-Meshtastic acts as a middleware solution that integrates multiple data sources into a unified communication stream. The application:
- Listens for multicast CoT messages containing system and drone telemetry.
- Parses these messages and transmits them as compact TAK PLI packets (with additional GeoChat packets) via the Meshtastic serial interface.
- Optionally receives FPV messages from a dedicated serial port, enriches them with GPS data (either live or static), and publishes them via a ZMQ PUB socket.
- Is built using asynchronous Python (asyncio) to ensure robust, non-blocking operations.

## Features

- **Duplex Communication:**
  - **Transmitting:**  
    Receives CoT messages via UDP multicast, parses them, and sends TAK PLI packets (with throttled GeoChat packets) via the Meshtastic serial interface.
  - **Receiving (Optional FPV):**  
    Listens for FPV messages on a separate serial port. FPV messages are enriched with GPS data and published via a ZMQ PUB socket.
- **Asynchronous Processing:**  
  Uses asyncio to decouple message reception, periodic update flushing, and FPV message processing.
- **Configurable Settings:**  
  Command-line arguments allow you to specify:
  - Meshtastic serial port.
  - Multicast IP address and port.
  - ZMQ port for FPV message publication.
  - FPV serial port and baud rate.
  - Whether GPS data is static (stationary) or dynamic.
  - Enable/disable FPV functionality with the `--fpv` flag.
- **Extensible & Modular:**  
  The clear, documented function structure allows for future expansion, such as adding new data sources or customized message processing.

## How It Works

1. **Initialization:**  
   The application parses command-line arguments for serial ports, multicast settings, ZMQ publishing, and FPV options. It then initializes the Meshtastic interface (or auto-detects it) and, if enabled, establishes a separate FPV serial connection.

2. **CoT Reception & Processing:**  
   A UDP multicast socket listens for CoT messages. Incoming XML messages are parsed into dictionaries, categorized by type (e.g. "drone," "wardragon," "pilot," "home") based on the UID prefix, and the most recent update for each unique transmitter (identified by a shortened callsign) is maintained in a dictionary.

3. **Message Transmission:**  
   A periodic flusher task sends the latest update for each transmitter as a TAK PLI packet via the Meshtastic interface. For system (and optionally pilot/home) messages, an additional GeoChat packet carrying key telemetry details is sent in a throttled manner.

4. **FPV Reception & Enrichment (Optional):**  
   When enabled with the `--fpv` flag and a corresponding serial port is provided, an asynchronous task reads FPV messages from the serial port. These FPV messages (in JSON) are enriched with GPS coordinates (using a persistent gpsd connection or static coordinates, based on the `--stationary` flag) and then published via a ZMQ PUB socket.

5. **Concurrency & Locking:**  
   All tasks run concurrently in the asyncio event loop. An asyncio lock serializes transmissions to ensure that the Meshtastic interface is not accessed concurrently.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/DragonSync-Meshtastic.git
   cd DragonSync-Meshtastic
   ```

2. **Install Dependencies:**

   Ensure you have Python 3 installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   *Dependencies include modules such as `xmltodict`, `gps3`, `pyserial`, `zmq`, and libraries required by Meshtastic.*

## Usage

Run the application from the command line. For example:

```bash
./dragonsync_meshtastic.py --port /dev/ttyACM0 --mcast 239.2.3.1 --mcast-port 6969 \
    --zmq-port 4020 --fpv --fpv-port /dev/ttyUSB0 --fpv-baud 115200
```

**Command-line options:**

- **--port:** Serial device for Meshtastic (e.g., `/dev/ttyACM0`).
- **--mcast:** Multicast group IP address (default: `239.2.3.1`).
- **--mcast-port:** Multicast port (default: `6969`).
- **--zmq-port:** ZMQ port for publishing FPV messages (default: `4020`).
- **--fpv:** Enable FPV reception features.
- **--fpv-port:** Serial port for FPV messages (e.g., `/dev/ttyUSB0`).
- **--fpv-baud:** Baud rate for FPV messages (default: `115200`).
- **--stationary:** If set, use static GPS coordinates (obtained once at startup).

If the FPV options are not specified or `--fpv` is not set, the script will run only the CoT processing and transmission tasks.

## Configuration

The application is fully configurable via command-line arguments, enabling you to:
- Adjust multicast settings to match your network environment.
- Specify different serial ports for Meshtastic and FPV functionalities.
- Set the ZMQ publishing port for external consumption of FPV data.
- Choose between dynamic and static GPS data, depending on the node’s mobility.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for full details.

## Contributing

Contributions are welcome! Fork this repository, make your improvements, and submit a pull request. Please follow PEP8 guidelines and include proper documentation and tests with your code.

## Contact

For more information or inquiries, visit [cemaxecuter.com](https://www.cemaxecuter.com).

---

*DragonSync-Meshtastic – Bridging multicast networks, Meshtastic devices, and FPV data for comprehensive, real-time situational awareness.*
