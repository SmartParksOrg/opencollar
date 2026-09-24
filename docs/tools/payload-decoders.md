# LoRaWAN payload decoders

OpenCollar Edge devices send binary payloads on numbered FPorts. A JavaScript decoder turns them into JSON on the network server. There is one decoder family for all Edge devices; it lives in the firmware repository as `scripts/ttn_decoder.js` and is released with every firmware version as `ttn_decoder-vX.js`.

{{ tool_cards(task='decode-uplinks', status=['current']) }}

## Get the decoder

- **Firmware 7.3.0 and later:** download `ttn_decoder-vX.js` from the [firmware release](https://github.com/SmartParksOrg/smartparks-opencollar-edge-fw-public/releases) that matches the device firmware.
- **Older firmware:** [files.smartparks.org/edge/decoder](https://files.smartparks.org/edge/decoder/) has TTN, ChirpStack v3 and ChirpStack v4 flavours up to 6.15.1, and the [legacy toolset](legacy.md) repository has ChirpStack v4 decoders for 4.4.3, 6.1.2 and 6.5.0.

{{ release_assets('smartparks-opencollar-edge-fw-public', 'ttn_decoder') }}

## Install it

=== "The Things Network (v3)"

    The file defines `Decoder(bytes, port)`. Wrap it for the v3 payload formatter:

    ```javascript
    function decodeUplink(input) {
      return { data: Decoder(input.bytes, input.fPort) };
    }
    ```

=== "ChirpStack v4"

    Same wrapper as TTN v3, or use the `CSv4_*` files from the file server, which already contain `decodeUplink(input)`.

=== "ChirpStack v3"

    Use the `chirpstack-v3` files from the file server, which define `Decode(fPort, bytes, variables)`.

## Which version for which firmware

| Device firmware | Decoder file | Notes |
|---|---|---|
| 8.0.x, 7.1.0 to 7.3.0 | `ttn_decoder-v7.2.0.js` / `ttn_decoder-v8.0.x.js` | Adds FPort 21 (air quality); drops FPorts 8 and 17 |
| 6.15.0 to 6.16.3 | `ttn_decoder-v6.15.1.js` | Adds FPorts 18, 19, 20 |
| 6.9.0 to 6.14.3 | `ttn_decoder-v6.11.2.js` | 15-byte CMDQ records |
| 6.1 to 6.8 | `CSv4_Decoder_OpenCollar_Edge_v6.5.0.js` | 13-byte CMDQ records |
| 4.x | `CSv4_Decoder_OpenCollar_Edge_v4.4.3.js` | No CMDQ |
| First generation (pre-Edge) | `d_opencollar_*.js` in the toolset | Different protocol |

The uplink layouts are backward compatible within these ranges; a newer decoder decodes older firmware for all ports it knows.
