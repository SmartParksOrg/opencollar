# Hardware

OpenCollar hardware is published as Altium projects (electronics), STEP, STL and DXF files (mechanics) and per-device documentation repositories with bills of materials and assembly instructions. Hardware source is intended to be licensed under CERN-OHL-W-2.0 (see [Licensing](../developers/licensing.md)).

## Electronics boards

| Board | Firmware name | Used by | Repository | Latest |
|---|---|---|---|---|
| RangerEdge | `rangeredge_nrf52840` | RangerEdge, TrapEdge, FenceEdge, WisentEdge, ElephantEdge, ScannerEdge | {{ repo_link('smartparks-rangeredge-hardware') }} | {{ latest_release('smartparks-rangeredge-hardware') }} |
| CollarEdge | `collaredge_nrf52840` | CollarEdge 38mm and 50mm | {{ repo_link('smartparks-collaredge-hardware') }} | {{ latest_release('smartparks-collaredge-hardware') }} |
| FreeEdge | `freeedge_nrf52840` | CollarEdge Free | {{ repo_link('smartparks-freeedge-hardware') }} | {{ latest_release('smartparks-freeedge-hardware') }} |
| RhinoEdge Cube | `rhinoedge_nrf52840` | RhinoEdge Cube, CollarEdge Pico and Nano, experimental trackers | {{ repo_link('smartparks-rhinoedge_cube-hardware') }} | {{ latest_release('smartparks-rhinoedge_cube-hardware') }} |
| RhinoEdge Puck 35 | `rhinopuck35_nrf52840` | RhinoEdge Puck 35 | {{ repo_link('smartparks-rhinoedge_puck35-hardware') }} | {{ latest_release('smartparks-rhinoedge_puck35-hardware') }} |
| RhinoEdge Puck 50 | `rhinopuck_nrf52840` | RhinoEdge Puck 50 | {{ repo_link('smartparks-rhinoedge_puck50-hardware') }} | {{ latest_release('smartparks-rhinoedge_puck50-hardware') }} |
| ElephantEdge battery pack | accessory | ElephantEdge | {{ repo_link('smartparks-elephantedge_battery_pack-hardware') }} | {{ latest_release('smartparks-elephantedge_battery_pack-hardware') }} |
| Fence monitor probe | accessory | FenceEdge | {{ repo_link('smartparks-fence_monitor-hardware') }} | {{ latest_release('smartparks-fence_monitor-hardware') }} |

Common to every board: nRF52840 MCU, Semtech LR11xx radio, u-blox GNSS, LIS2DW12 accelerometer, EN25 SPI flash, reed switch. RangerEdge adds charging, a microphone, an I2C port and connectors for external antennas; FreeEdge and RangerEdge have a RockBLOCK interface.

Each hardware repository keeps its changelog in the README and publishes fabrication (`FAB`), assembly (`PCBA`) and source (`SRC`) zip files per release. The Altium 365 viewer links in the READMEs require an account.

## Mechanics

{{ repo_table(category='mechanics', columns=('purpose','latest')) }}

## Documentation, bill of materials and assembly

One repository per device with `BOM.md`, `ASM.md`, a changelog and photographs of every assembly step.

{{ repo_table(category='device-docs', columns=('purpose','latest')) }}

## Manufacturing and provisioning

Devices are assembled by Smart Parks and provisioned on a test rack with the private provisioning software, which flashes the provisioning firmware, runs the operation tests and writes the device identity. The wiki describes [RangerEdge assembly](https://wiki.smartparks.org/devices/opencollar/rangeredge/production); the firmware README describes manual provisioning without a rack.
