# Swiss Pollen integration for Home Assistant

[![hacs_badge][hacs-shield]][hacs]
![Project Maintenance][maintenance-shield]
[![License][license-shield]][license]

![Downloads][downloads-shield]
![Downloads][downloads-latest-shield]


[![Build Status][build-status-shield]][build-status]
[![Deploy Status][deploy-status-shield]][deploy-status]

A Home Assistant integration that provides pollen data for Switzerland from MeteoSwiss.

## Features

- Provides pollen concentration data for various plant types in Switzerland
- Data is sourced from MeteoSwiss
- Supports multiple measurement stations across Switzerland
- Provides both numeric values (No/m³) and categorical levels (None, Low, Medium, Strong, Very Strong)

## Installation

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Add this repository as a custom repository in HACS:
   - Go to HACS > Integrations
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add `https://github.com/frimtec/hass-swiss-pollen` with category "Integration"
3. Click "Install" on the "Swiss Pollen" integration
4. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/frimtec/hass-swiss-pollen/releases)
2. Unpack the release and copy the `custom_components/swiss_pollen` directory into your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Swiss Pollen"
4. Follow the configuration flow:
   - Select the plant type you want to monitor
   - Select one or more measurement stations

## Available Sensors

For each selected station and plant type combination, the integration creates two sensors:

1. **Numeric Sensor**: Shows the pollen concentration in No/m³ (number per cubic meter)
   - Entity ID format: `sensor.[station_code]_[plant_name]`
   - Icon: mdi:flower-pollen

2. **Level Sensor**: Shows the categorical level of pollen concentration
   - Entity ID format: `sensor.[station_code]_[plant_name]_level`
   - Possible values: None, Low, Medium, Strong, Very Strong
   - Icon: mdi:flag

---

[hacs-shield]: https://img.shields.io/badge/HACS-Default-41BDF5.svg
[hacs]: https://github.com/hacs/integration
[downloads-latest-shield]:https://img.shields.io/github/downloads/frimtec/hass-swiss-pollen/latest/total
[downloads-shield]:https://img.shields.io/github/downloads/frimtec/hass-swiss-pollen/total
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[license-shield]: https://img.shields.io/github/license/frimtec/hass-swiss-pollen.svg
[license]: https://opensource.org/licenses/Apache-2.0
[build-status-shield]: https://github.com/frimtec/hass-swiss-pollen/actions/workflows/build.yml/badge.svg
[build-status]: https://github.com/frimtec/hass-swiss-pollen/actions/workflows/build.yml
[deploy-status-shield]: https://github.com/frimtec/hass-swiss-pollen/actions/workflows/deploy_release.yml/badge.svg
[deploy-status]: https://github.com/frimtec/hass-swiss-pollen/actions/workflows/deploy_release.yml
[latest-release]: https://github.com/frimtec/hass-swiss-pollen/releases/latest

