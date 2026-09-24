# Integrations

OpenCollar devices are the hardware side of a Smart Parks deployment. Data leaves the device over LoRaWAN, Bluetooth or Iridium and is decoded and stored by a platform of your choice.

## LoRaWAN network servers

Any LoRaWAN 1.0.x network server works: The Things Network, ChirpStack, ThingPark and commercial operators have all been used. Install the [payload decoder](../tools/payload-decoders.md) that matches the firmware and forward the decoded JSON to your application. Downlinks (settings and commands) are sent through the same server.

## Smart Parks Protect

[Smart Parks Protect](https://github.com/SmartParksOrg/smartparks-protect) is Smart Parks' self-hosted operational data platform: devices and entities on one live map, analysis and export, a rules engine for events and alerts, device control and integrations such as EarthRanger. It has a native OpenCollar driver that decodes every FPort, imports raw log files, talks to nearby devices over Web Bluetooth and deduplicates records that arrive over several paths. Protect is a separate project with its own documentation; it is not part of the OpenCollar repositories.

## EarthRanger, Node-RED and others

- Node-RED nodes for [ChirpStack](https://github.com/SmartParksOrg/node-red-contrib-chirpstack) and [EarthRanger](https://github.com/SmartParksOrg/node-red-contrib-earthranger) support custom flows.
- The Smart Parks Wiki documents integrations with [EarthRanger](https://wiki.smartparks.org/stack/applications/earthranger), Movebank, Grafana, Gundi and FME under *Stack*.

## Iridium (RockBLOCK)

Devices with a RockBLOCK 9603 module send the satellite buffer as Iridium SBD messages and accept settings and commands as mobile-terminated messages via the RockBLOCK management system or Cloudloop. See the wiki page [Iridium Satellite](https://wiki.smartparks.org/devices/opencollar/satellite).
