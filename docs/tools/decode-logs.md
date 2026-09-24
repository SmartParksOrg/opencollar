# Download and decode logs

Every message an OpenCollar Edge device sends is also stored in its external flash: positions, status, scans, fence and switch events. The stored history can be read remotely in small batches over LoRaWAN (FPort 29) or downloaded in full over Bluetooth.

## Download the raw log

{{ tool_cards(task='download-logs') }}

In the BLE web app, open the **Logs** section and press **Download all logs** (or download one message type). The result is a text file with one frame per line, base64 encoded, exactly as the device sent it over Bluetooth: `[port][msg_id][len][data]`, with stored records carrying their own timestamp.

## Decode it

{{ tool_cards(task='decode-logs') }}

1. Open the [raw logs decoder](https://smartparksorg.github.io/raw_logs_decoder/).
2. Choose the built-in decoder that matches the firmware version the device was running when it stored the data (the decoder versions follow the firmware versions), or upload a `ttn_decoder-vX.js` from a [firmware release](../firmware/releases.md).
3. Select the log file and press **Decode**. Filter by port, chart any field over time, view positions on the map and export CSV, JSON or Excel.

Nothing is uploaded; the decoder runs in your browser.

## Which decoder version

| Device firmware | Decoder |
|---|---|
| 8.0.x, 7.1.0 to 7.3.0 | `ttn_decoder-v7.2.0.js` (identical to the 7.3.0 firmware script; 8.0 changed settings, not the uplink layouts) |
| 6.15.0 to 6.16.3 | `ttn_decoder-v6.15.1.js` |
| 6.9.0 to 6.14.3 | `ttn_decoder-v6.11.2.js` |
| 6.1 to 6.8 | ChirpStack v4 decoder 6.5.0 from the [legacy toolset](legacy.md) |
| 4.x | decoder 4.4.3 from the legacy toolset |

The mapping comes from a comparison of the decoder files across repositories; it will be maintained on the [payload decoders](payload-decoders.md) page.

## Alternatives

Smart Parks Protect imports raw log files and Bluetooth reads directly into its device history, deduplicating records that already arrived over LoRaWAN. See [Integrations](../integrations/index.md).
