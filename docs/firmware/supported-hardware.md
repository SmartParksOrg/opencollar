# Supported hardware

The firmware is built per **board** and per **hardware revision group**. When building or choosing a DFU image, use the revision group that contains the revision printed on your board, not the printed revision itself.

## Boards and revision groups (firmware 8.0.1)

| Board | Devices | Hardware revisions (marked on board) | Revision group to use |
|---|---|---|---|
| `rangeredge_nrf52840` | RangerEdge, TrapEdge, FenceEdge, WisentEdge, ElephantEdge, ScannerEdge | 1.4.0 to 1.5.0 | `1.4.0` |
| | | 1.6.0 | `1.6.0` |
| | | 1.7.0 | `1.7.0` |
| | | 1.8.0 to 1.13.0 | `1.8.0` |
| `rangeredge_airq_nrf52840` | RangerEdge AirQ (special build) | 1.4.0 to 1.13.0 | as rangeredge |
| `collaredge_nrf52840` | CollarEdge 38mm and 50mm | 1.0.0 | `1.0.0` |
| | | 1.1.0 to 1.3.0 | `1.1.0` |
| | | 1.4.0 to 1.7.0 | `1.4.0` (1.5.0 board files also exist) |
| `freeedge_nrf52840` | CollarEdge Free | 1.0.0 to 1.2.0 | `1.0.0` |
| | | 1.3.0 to 1.5.0 | `1.3.0` |
| | | 1.6.0 | `1.6.0` |
| | | 1.7.0 | `1.7.0` |
| `rhinoedge_nrf52840` | RhinoEdge Cube, CollarEdge Pico, CollarEdge Nano, BaboonEdge, PangolinEdge, HorseEdge | 1.4.0 to 1.6.0 | `1.4.0` |
| `rhinopuck_nrf52840` | RhinoEdge Puck 50 | 1.3.0 | `1.3.0` |
| `rhinopuck35_nrf52840` | RhinoEdge Puck 35 | 1.2.0 | `1.2.0` |

Firmware 5.0.0 and later dropped support for older RangerEdge revisions (1.0 to 1.3). Early boards `elephantedge_nrf52840`, `wisentedge_nrf52840` and `cattracker_nrf52840` existed only in firmware 0.2 to 1.9 (2021); those products moved to the RangerEdge board.

## Tracker types

The setting `tracker_type` (family `general`, id 0x00) selects the device personality. The hardware default is derived from the board; other values are allowed only on the boards listed.

| Value | Tracker type | Allowed boards |
|---|---|---|
| 0 | `default_tracker` (hardware default) | all |
| 1 | `rhinoedge_tracker` | rhinoedge |
| 2 | `elephantedge_tracker` | rangeredge |
| 3 | `wisentedge_tracker` | rangeredge |
| 4 | `cattracker_tracker` | (obsolete) |
| 5 | `rangeredge_tracker` | rangeredge |
| 6 | `rhinopuck_tracker` | rhinopuck, rhinopuck35 |
| 7 | `scanneredge_tracker` | rangeredge |
| 8 | `collaredge_tracker` | collaredge |
| 9 | `freeedge_tracker` | freeedge |
| 10 | `fenceedge_tracker` | rangeredge |
| 11 | `horseedge_tracker` | rhinoedge |
| 12 | `collaredgepico_tracker` | rhinoedge |
| 13 | `collaredgenano_tracker` | rhinoedge |
| 14 | `baboonedge_tracker` | rhinoedge |
| 15 | `pangolinedge_tracker` | rhinoedge |

The status message carries the hardware type in the low nibble and the tracker type in the high nibble of one byte, so apps and platforms can tell them apart.

## Release image names

`open-collar-<board>-hv<revision group>-v<firmware>[-dbg|-prov].bin`, for example `open-collar-collaredge_nrf52840-hv1.4.0-v8.0.1.bin`. The `-prov` images are provisioning builds used on the test rack; `-dbg` builds have logging enabled and MCUboot disabled.
