# Building from source

The firmware builds with IRNAS's `east` tool on top of `west` and the nRF Connect SDK. The full procedure is in the [firmware README](https://github.com/SmartParksOrg/smartparks-opencollar-edge-fw-public#readme); this page summarises it and lists what you need.

## Requirements

- Linux or macOS with Python 3, `west`, and [east](https://github.com/IRNAS/irnas-east-software).
- The nRF Connect SDK 2.2 toolchain (installed by `east install toolchain`).
- A J-Link programmer for flashing and RTT logs, or the BLE DFU path for installing built images.
- The west manifest pulls the SDK plus ten IRNAS modules (drivers for the EN25 flash, LIS2DW12, voltage divider, peripheral power, version info, Semtech SWDR001/SWL2001 Zephyr ports, T5838 microphone, BMV080 and BME690 air-quality sensors). All are public on GitHub; the air-quality drivers need Bosch licences to be built.

## Steps

```bash
east init -m https://github.com/SmartParksOrg/smartparks-opencollar-edge-fw-public smartparks-opencollar-edge-fw
cd smartparks-opencollar-edge-fw
east install nrfutil-toolchain-manager
east install toolchain
east update
cd project/app
python ../scripts/settings/py2h.py          # regenerate settings from settings.json
east build -b rangeredge_nrf52840@1.8.0     # board@revision group, see Supported hardware
east flash
```

Build types: `-u debug` (logging, no MCUboot), `-u prov` (provisioning tests). `east release` builds every board and type into `release/`.

## Contributing to the firmware

The public repository is a release mirror; pull requests should be discussed with Smart Parks first. Firmware issues are best raised on the [ble-settings-app](https://github.com/SmartParksOrg/ble-settings-app/issues) or [opencollar](https://github.com/SmartParksOrg/opencollar/issues) issue trackers until issues are enabled on the firmware repository. See [Contributing](../developers/contributing.md).
