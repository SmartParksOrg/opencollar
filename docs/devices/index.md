# Devices

OpenCollar devices are built from a small set of electronics boards that all run the same firmware. The table lists every device known to the firmware, the repositories and the Smart Parks catalog. Entries marked with a verification badge could not be fully confirmed against source or documentation; see the notes on each page.

## All devices

{{ device_matrix() }}

## RangerEdge family

Rechargeable or primary-battery trackers around the RangerEdge board (`rangeredge_nrf52840`).

{{ device_cards('rangeredge') }}

## CollarEdge family

Collar trackers on BioThane belting, from a 5 g Pico unit to the three-cell Iridium CollarEdge Free.

{{ device_cards('collaredge') }}

## RhinoEdge family

Potted horn implants for rhinos. The RhinoEdge Cube board is also the electronics of the CollarEdge Pico and Nano.

{{ device_cards('rhinoedge') }}

## Experimental

Research and development devices. Some are sold on request; specifications and repositories are incomplete.

{{ device_cards('experimental') }}

## Legacy

{{ device_cards('legacy') }}
