# Releases

Release information on this page is synchronised from GitHub (last run: {{ releases_generated_at }}). Older firmware bundles are on [files.smartparks.org/edge/dfu](https://files.smartparks.org/edge/dfu/).

## Latest firmware

{{ release_assets('smartparks-opencollar-edge-fw-public') }}

Each release contains:

| Asset | Content |
|---|---|
| `open-collar-vX.zip` | Production images for every board and revision group (`.bin` for DFU, `.hex` for programming) |
| `open-collar-vX-debug.zip`, `-prov.zip` | Debug and provisioning builds |
| `air-quality-vX.zip` | RangerEdge AirQ special build |
| `samples-vX.zip` | Sample applications, including the LR11xx transceiver update |
| `settings-vX.json` | The settings, commands, values, messages and ports of this version; used by the apps |
| `ttn_decoder-vX.js` | LoRaWAN payload decoder for this version |

Read the [CHANGELOG](https://github.com/SmartParksOrg/smartparks-opencollar-edge-fw-public/blob/main/CHANGELOG.md) before updating. Notable migration steps: 4.x to 6.x requires the 5.0.1 image first; 8.0.0 migrates settings to a family-based format and downgrading afterwards resets settings.

## All tracked repositories

{{ releases_table() }}
