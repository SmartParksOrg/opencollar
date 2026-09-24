# Protocols

OpenCollar Edge devices speak one protocol over three transports: LoRaWAN uplinks and downlinks, Bluetooth (Nordic UART Service), and Iridium short-burst data. The message layouts are the same; only the framing differs.

!!! info "This section grows in the next phase"
    The complete reference (byte layouts per FPort, the settings families, the command table, Bluetooth framing, the raw log format and the Iridium buffer) will be generated from the released `settings.json` and the firmware source. Until then, the [Smart Parks Wiki](https://wiki.smartparks.org/devices/opencollar/lorawan_messages) documents the pre-8.0 formats with examples, and the firmware [settings README](https://github.com/SmartParksOrg/smartparks-opencollar-edge-fw-public/blob/main/scripts/settings/README.md) describes the 8.0 family structure.

## Framing

- **Uplink over LoRaWAN:** `[msg_id][len][data]` on an FPort that selects the message type. Integers are little-endian.
- **Over Bluetooth and in raw log files:** the FPort is prepended: `[port][msg_id][len][data]`.
- **Stored records (FPort 29 and the satellite buffer):** `[port][msg_id][len][data][store timestamp u32]`.
- **Settings downlink (FPort 3):** `family id length data` since firmware 8.0.0; `id length data` before.
- **Command downlink (FPort 32):** `id length data`.

## FPorts (firmware 8.0.1)

| FPort | Name | Direction | Content |
|---|---|---|---|
| 1 | `port_lr_gps` | uplink | LR11xx GNSS NAV message (needs a cloud solver) |
| 2 | `port_ublox_gps` | uplink | u-blox position with altitude, accuracy, satellites, fix type, PDOP |
| 3 | `port_settings` | both | Settings write (downlink) and readback (uplink) |
| 4 | `port_status` | uplink | Battery, charging, temperature, acceleration, uptime, reset reason, errors, firmware and hardware version |
| 5 | `port_lr_sat_data` | uplink | LR11xx satellite list |
| 6 / 10 | `port_wifi_scan_aggregated` / `port_wifi_scan` | uplink | Wi-Fi scan results |
| 7 / 11 | `port_ble_scan_aggregated` / `port_ble_scan` | uplink | BLE scan results (contact tracing) |
| 9 | `port_ublox_sat_data` | uplink | u-blox satellite list |
| 12 | `port_fence` | uplink | Electric fence measurement |
| 13 / 16 | `port_ublox_short_message` / `port_ublox_resend_location` | uplink | Short position and its periodic resend |
| 14 | `port_flash_status` | uplink | Flash usage and message count |
| 15 | `port_ble_cmdq` | uplink | Cardiac monitoring device (CMDQ) results |
| 18 | `port_timestamp` | uplink | Device clock |
| 19 / 20 | `port_external_switch_detection` / `_status` | uplink | External switch change and status |
| 21 | `port_air_quality` | uplink | Air quality (AirQ build) |
| 22 / 33 | `port_lp0_ping` / `port_lp0_commands` | both | LP0 discovery and commands (experimental) |
| 27 | `port_memfault` | uplink | Memfault diagnostic chunks |
| 28 | `port_lr_messaging` | both | Text messaging |
| 29 | `port_flash_log` | uplink | Stored records read from flash |
| 30 | `port_values` | uplink | Readable runtime values |
| 31 | `port_messages` | uplink | Command confirmation, BLE MAC, last position |
| 32 | `port_commands` | downlink | Commands |

Ports 8 and 17 (RF scan, open sky detection) existed up to firmware 6.16 and were removed in 7.1.0.

## Settings families (firmware 8.0.0 and later)

| Family | Id | Used for |
|---|---|---|
| `general` | 0x02 | Tracker type, status and diagnostic intervals, logging, device name and PIN, LEDs |
| `flags` | 0x03 | Which messages are sent over LoRa, stored in flash, sent over satellite |
| `ble` | 0x04 | Advertising, scanning, filters, connection, CMDQ |
| `lora` | 0x05 | LoRaWAN credentials and behaviour, LR GNSS, S-band, VHF, LP0 |
| `gps` | 0x06 | u-blox scheduling, retries, accuracy, constellations, motion trigger |
| `satellite` | 0x07 | Iridium enablement and schedules |
| `sensors` | 0x08 | Accelerometer, fence, outdoor detection, external switch, air quality |
| `values` | 0xA0 | Readable runtime values (not settings) |

Family `0x00` is reserved for pre-8.0 settings during migration and `0x01` for internal firmware records.

## Decoders

The reference implementation of the uplink layouts is the decoder released with each firmware version. See [LoRaWAN payload decoders](../tools/payload-decoders.md).
