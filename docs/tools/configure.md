# Configure your OpenCollar

Every setting of an OpenCollar Edge device can be read and changed over Bluetooth, and most can also be changed remotely over LoRaWAN or Iridium. Start with Bluetooth.

## Over Bluetooth

{{ tool_cards(task='configure', status=['current']) }}

### With the BLE web app

1. Open the [web app](https://smartparksorg.github.io/ble-settings-app/) in Chrome or Edge on a laptop, or Chrome on Android. Safari and Firefox do not support Web Bluetooth.
2. Press **Scan** and choose your device. Devices advertise the Smart Parks manufacturer id and the Nordic UART service; the browser shows only matching devices.
3. The app loads the settings schema that matches the firmware version reported by the device (schemas for firmware 4.4.2 to 8.0.x are bundled) and shows every setting grouped by family, with default and range.
4. Change a value and press **Update**. Use **Export settings** to save a profile as JSON and **Import settings** to apply it to another device.
5. Commands (reset, request position, request status, get logs) are in the Actions section; custom commands can be sent as hex.

The **HEX composer** on the same site builds the byte sequence of a settings or command message so you can paste it into a LoRaWAN downlink.

### With the Smart Parks Connect App

The Android app offers the same settings and commands, plus PIN handling, device lists and the automatic DFU mode for updating many devices. Instructions are on the [wiki](https://wiki.smartparks.org/devices/opencollar/connect-app).

## Over LoRaWAN

Settings are downlinks on FPort 3 and commands on FPort 32. Since firmware 8.0.0 a settings message is `family id length data` (little-endian integers); before 8.0.0 it was `id length data`. Commands are `id length data` in every version. The [Protocols](../protocols/index.md) section has the format; the wiki page [Settings and Commands](https://wiki.smartparks.org/devices/opencollar/settings-and-commands) has worked examples for the pre-8.0 format.

!!! warning "Firmware 8.0.0 changed the settings wire format"
    Tools and downlink scripts written for firmware 7.x send `id length data` and will be rejected by firmware 8.x, which expects `family id length data`. The BLE web app selects the right format automatically; check any custom integration.

## Over Iridium

Devices with a RockBLOCK accept the same settings and commands as mobile-terminated SBD messages. See the wiki page [Iridium Satellite](https://wiki.smartparks.org/devices/opencollar/satellite).
