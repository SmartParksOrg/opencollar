# Accelerometer calculator

{{ tool_cards(task='plan', status=['experimental']) }}

The calculator models the LIS2DW12 accelerometer and the nRF52 duty cycle of an OpenCollar Edge device to estimate battery life, flash usage and payload size for a motion summary message. It is a design study: the summary message it builds is not implemented in the released firmware. Use it to reason about trade-offs before proposing firmware changes.

A related research tool, the [Arduino BLE accelerometer streamer](https://smartparksorg.github.io/arduino-ble-accelerometer/), streams live accelerometer data from an Arduino Nano 33 BLE Sense and applies movement statistics and a rhino behaviour classifier in the browser.
