# Update firmware

Firmware is distributed as MCUboot images, one per hardware board and revision group, and installed over Bluetooth (DFU). The current release is {{ latest_release('smartparks-opencollar-edge-fw-public') }}.

## Before you start

- **Turn off the u-blox GPS interval** in the settings during the update. A GPS fix interrupts the transfer.
- **Check the migration path.** Devices on firmware 4.x must first install the 5.0.1 migration image and then a 6.x or later image. Firmware 8.0.0 migrates stored settings to a new format; export a settings profile first, because downgrading to 7.3 or earlier afterwards resets settings to defaults.
- **Use the image for your board and hardware revision group.** The file name encodes both, for example `open-collar-rangeredge_nrf52840-hv1.8.0-v8.0.1.bin` for RangerEdge boards 1.8.0 to 1.13.0. See [Supported hardware](../firmware/supported-hardware.md).

## Choose a tool

{{ tool_cards(task='update-firmware') }}

## With the BLE web app

1. Connect to the device as described in [Configure your OpenCollar](configure.md).
2. Press **DFU**. The app lists the bundled firmware images that match the connected hardware type and revision; you can also select a `.bin` file downloaded from the [releases](../firmware/releases.md) page.
3. Press **Start DFU upload** and keep the browser tab open until the device reboots. Then **Confirm active image**.

## With the Smart Parks Connect App

The Android app updates from a file on the phone (**Manual**) or downloads the latest bundle from the Smart Parks file server (**Automatic**). The automatic mode also supports updating many devices of one type in a row. The [wiki](https://wiki.smartparks.org/devices/opencollar/firmware) has the step-by-step instructions.

## Where to download

- GitHub: [firmware releases](https://github.com/SmartParksOrg/smartparks-opencollar-edge-fw-public/releases) for 7.3.0 and later. Each release has a production bundle, debug and provisioning bundles and the matching `settings-vX.json` and `ttn_decoder-vX.js`.
- Smart Parks file server: [files.smartparks.org/edge/dfu](https://files.smartparks.org/edge/dfu/) for older bundles (2.15.0, 4.4.3, 5.0.1, 6.15.1, 7.2.0) and the bundle used by the Connect App.

{{ release_assets('smartparks-opencollar-edge-fw-public') }}
