# Getting started

This page walks a new user from an unboxed device to decoded data. Each step links to the tool or page that does the work.

## 1. Identify your device

Every OpenCollar Edge device has a hardware type and revision printed on the board or in the device status, and runs the shared OpenCollar Edge firmware. Find your product in [Devices](../devices/index.md) to learn which board it uses, which firmware revision group applies and where its hardware files are.

## 2. Connect over Bluetooth

Devices advertise over Bluetooth Low Energy when they are awake. Use one of:

- [Configure your OpenCollar](../tools/configure.md) with the BLE web app in Chrome or Edge on a laptop or Android phone.
- The [Smart Parks Connect App](https://play.google.com/store/apps/details?id=com.smartparks_connect_app) on Android.

The device shows its firmware version, hardware type, battery, temperature and last position as soon as you connect. Devices with a PIN set answer nothing until they are unlocked.

## 3. Check and update the firmware

Always run the latest firmware. The current release is {{ latest_release('smartparks-opencollar-edge-fw-public') }}. Follow [Update firmware](../tools/update-firmware.md). Two things to know before you start:

- Devices on firmware 4.x must first be updated to the 5.0.1 migration image, then to 6.x or later.
- Firmware 8.0.0 changed the settings storage format. Export your settings with the web app before updating and read the [release notes](../firmware/releases.md).

## 4. Configure the device

Settings control how often the device looks for a GPS fix, how often it sends status, which LoRaWAN region it uses and which data it stores. The web app and the Connect App show every setting with its default and range; the same settings can be sent as LoRaWAN downlinks. See [Configure your OpenCollar](../tools/configure.md) and the [Protocols](../protocols/index.md) overview for the wire format.

## 5. Join a LoRaWAN network

The device joins with OTAA using the DevEUI and AppKey provisioned by Smart Parks. Register it on your network server (The Things Network, ChirpStack, ThingPark or another) and install the payload decoder that matches its firmware version from [LoRaWAN payload decoders](../tools/payload-decoders.md).

## 6. Read the data

- Uplinks arrive on numbered FPorts; the decoder turns them into JSON with position, status and sensor fields.
- Everything the device sends is also stored in its flash. Download the log over Bluetooth and decode it with the [raw logs decoder](../tools/decode-logs.md) to get the full history as CSV or Excel.
- To put the data on a map, forward the uplinks to a platform such as [Smart Parks Protect](../integrations/index.md) or EarthRanger.

## Where to get help

- [Smart Parks Wiki](https://wiki.smartparks.org/devices/opencollar) for field procedures, datasheets and feature descriptions.
- GitHub issues on the tool repositories listed under [Developers](../developers/repositories.md).
- Smart Parks directly for devices bought through the [catalog](https://www.smartparks.org/catalog/).
