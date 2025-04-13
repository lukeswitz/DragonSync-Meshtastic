#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2025 CEMAXECUTER LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import logging
import socket
import struct
import json
import xmltodict
import re
import time

from cot_parser import parse_cot
import meshtastic.serial_interface

logging.basicConfig(level=logging.INFO)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Meshtastic CoT Multicast Listener"
    )
    parser.add_argument(
        "--port",
        type=str,
        default=None,
        help="Serial device to use (e.g., /dev/ttyACM0)."
    )
    return parser.parse_args()


def create_interface(port):
    """
    Create the Meshtastic interface.

    If a port is provided, use the devPath parameter;
    otherwise, use auto-detection.
    """
    if port:
        logging.info(f"Using specified serial device (devPath): {port}")
        return meshtastic.serial_interface.SerialInterface(devPath=port)
    else:
        logging.info("No device specified; using auto-detection.")
        return meshtastic.serial_interface.SerialInterface()


def setup_multicast_socket(multicast_grp, multicast_port):
    """
    Set up and return a UDP multicast socket.

    Args:
        multicast_grp (str): Multicast group IP address.
        multicast_port (int): Multicast port number.

    Returns:
        socket.socket: Configured UDP multicast socket.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                         socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((multicast_grp, multicast_port))
    mreq = struct.pack("4sl", socket.inet_aton(multicast_grp),
                       socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


def send_meshtastic(data):
    """
    Send JSON-formatted data through the Meshtastic interface.

    Args:
        data (dict): Data dictionary to send.
    """
    jdata = json.dumps(data)
    interface.sendText(jdata, wantAck=False)
    logging.info(f"Sent to Meshtastic: {jdata}")


def reconnect_interface(port):
    """
    Attempt to reinitialize the Meshtastic interface until successful.

    Args:
        port (str): Port to use for interface reinitialization.

    Returns:
        object: A new Meshtastic interface.
    """
    while True:
        try:
            logging.info("Attempting to reconnect the Meshtastic device...")
            new_iface = create_interface(port)
            # Optionally, you could send a test command here to confirm connectivity.
            logging.info("Reconnection successful.")
            return new_iface
        except Exception as reconnect_err:
            logging.error(f"Reconnection failed: {reconnect_err}")
            time.sleep(5)


def main():
    """Main function to run the multicast listener."""
    global interface  # Allow reassigning the global interface
    args = parse_arguments()
    interface = create_interface(args.port)

    MCAST_GRP = '239.2.3.1'
    MCAST_PORT = 6969
    sock = setup_multicast_socket(MCAST_GRP, MCAST_PORT)
    logging.info(f"Listening for CoT multicast on {MCAST_GRP}:{MCAST_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(8192)
            msgs = parse_cot(data.decode('utf-8'))
            for msg in msgs:
                try:
                    send_meshtastic(msg)
                except Exception as send_err:
                    logging.error(f"Error sending data: {send_err}")
                    # Attempt to reconnect if a send error occurs.
                    try:
                        if interface is not None:
                            interface.close()
                    except Exception as close_err:
                        logging.error(f"Error closing interface: {close_err}")
                    interface = reconnect_interface(args.port)
        except KeyboardInterrupt:
            logging.info("Stopping listener.")
            break
        except Exception as e:
            logging.error(f"General error: {e}")

    try:
        if interface is not None:
            interface.close()
    except Exception as e:
        logging.error(f"Error closing interface on exit: {e}")


if __name__ == "__main__":
    main()
