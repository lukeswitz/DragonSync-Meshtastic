# WIP The necessary cot_parser will be uploaded once fully tested

# DragonSync-Meshtastic

DragonSync-Meshtastic is a Python-based application designed to bridge data between multicast network messages and Meshtastic devices. It listens for Cursor-on-Target (CoT) messages transmitted via a multicast group, parses these messages, and relays them as JSON-formatted text to connected Meshtastic devices. This tool is particularly useful for integrating various data sources (such as system messages, drone telemetry, and electromagnetic spectrum alerts) into a single, robust communication system.

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

DragonSync-Meshtastic serves as a middleware application that links multicast data streams to Meshtastic devices. This integration allows users to:

- Receive real-time system and drone messages.
- Support future expansion to include a variety of electromagnetic (EM) spectrum events.
- Enhance situational awareness in applications like field operations, emergency services, and distributed sensor networks.

## Features

- **Multicast Listening:** Listens on a configurable multicast IP and port for CoT messages.
- **Meshtastic Integration:** Relays parsed CoT messages to Meshtastic devices using their serial interface.
- **Error Handling and Reconnection:** Automatically attempts to reconnect to the Meshtastic device if errors occur.
- **Configurable Multicast Settings:** Users can specify the multicast group and port via command-line arguments, providing flexible network configuration.
- **Extensible Design:** The code structure makes it easy to integrate additional data sources such as EM spectrum event alerts.

## How It Works

1. **Initialization:**  
   The application starts by parsing command-line arguments for the serial port and multicast settings. If a serial device is provided, it establishes a connection to the Meshtastic device. Otherwise, it auto-detects the device.

2. **Socket Setup:**  
   A UDP multicast socket is created and bound to the specified multicast group and port. The application uses `INADDR_ANY` to join the multicast group on all available interfaces by default.

3. **Message Processing:**  
   The listener receives data packets from the multicast network, decodes them, and uses a CoT parser to generate message dictionaries.

4. **Data Relay:**  
   Each parsed message is serialized into JSON and sent to the Meshtastic device. The application includes robust error handling to manage connection issues, including automatic reconnection attempts.

5. **Extensibility:**  
   While the current implementation focuses on system and drone messages, it is designed to be extended to incorporate additional alerts (e.g., EM spectrum events) as the project evolves.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/alphafox02/DragonSync-Meshtastic.git
   cd DragonSync-Meshtastic
   ```

2. **Install Dependencies:**

   Ensure you have Python 3 installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: The requirements include packages such as `xmltodict` and any libraries needed by `meshtastic.serial_interface` and `cot_parser`.*

## Usage

Run the application from the command line:

```bash
./dragonsync_meshtastic.py --port /dev/ttyACM0 --mcast-ip 239.2.3.1 --mcast-port 6969
```

- **--port:** Serial device to use (e.g., `/dev/ttyACM0`).
- **--mcast-ip:** Multicast group IP address. Default is `239.2.3.1`.
- **--mcast-port:** Multicast port number. Default is `6969`.

If the serial device or multicast settings are not specified, the application will use auto-detection and default settings.

## Configuration

The application allows configuration via command-line arguments. This makes it flexible to adapt to various network environments and serial device settings without modifying the source code:

- **Multicast Group:** Choose a multicast IP that suits your network setup.
- **Multicast Port:** Specify a port to avoid conflicts with other applications.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements. Ensure your changes adhere to PEP8 guidelines and include proper documentation.

## Contact

cemaxecuter.com

*DragonSync_Meshtastic - Bridging the gap between multicast networks and Meshtastic devices to enhance situational awareness and real-time data integration.*
