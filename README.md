# Swiss Pollen integration for Home Assistant

[![hacs_badge][hacs-shield]][hacs]
![Project Maintenance][maintenance-shield]
[![License][license-shield]][license]

![Downloads][downloads-shield]
![Downloads][downloads-latest-shield]


[![Build Status][build-status-shield]][build-status]
[![Deploy Status][deploy-status-shield]][deploy-status]

A Home Assistant integration that provides pollen data for Switzerland from [MeteoSchweiz][MeteoSchweiz].
Data integration is done via [swiss-pollen][swiss-pollen].

This integration is not officially developed, supported or endorsed by MeteoSchweiz.

## Features

- Provides pollen concentration data for various plant types in Switzerland
- Data is sourced from [MeteoSchweiz][MeteoSchweiz]
- Supports multiple measurement stations across Switzerland
- Provides both numeric values (No/m³) and categorical levels (None, Low, Medium, Strong, Very Strong)

## Installation

### HACS (recommended)

You can install this component through [HACS](https://hacs.xyz/) to easily receive updates. Once HACS is installed, click this link:
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=frimtec&repository=hass-swiss-pollen)

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/frimtec/hass-swiss-pollen/releases)
2. Unpack the release and copy the `custom_components/swiss_pollen` directory into your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Swiss Pollen"
4. Follow the configuration flow to set up a service for a specific plant:
   - Select a plant of interest
   - Select one or more measurement stations to get sensors for these stations
5. You can repeat step 4) to set up multiple services, one for each plant you are interested in

## Available Sensors

For each selected station and plant type combination, the integration creates two sensors:

1. **Numeric Sensor**: Shows the pollen concentration in No/m³ (number per cubic meter)
   - Entity ID format: `sensor.[station_code]_[plant_name]`
   - Icon: mdi:flower-pollen

2. **Level Sensor**: Shows the categorical level of pollen concentration
   - Entity ID format: `sensor.[station_code]_[plant_name]_2`
   - Possible values: None, Low, Medium, Strong, Very Strong
   - Icon: mdi:flag

## Example Dashboard
![dashboard-example.png](images/dashboard-example.png)
<details>

<summary>YAML-Code</summary>

```
- type: grid
  cards:
    - type: heading
      heading: 🌳Pollen
      heading_style: title
    - type: markdown
      content: >-
        <img
        src="https://github.com/frimtec/hass-swiss-pollen/blob/main/images/grass.png?raw=true"
        alt="Gräser" width="55" height="70">

        &nbsp;&nbsp;&nbsp;Gräser
      grid_options:
        columns: 3
        rows: 2
    - type: horizontal-stack
      cards:
        - type: tile
          name: ' Zürich'
          entity: sensor.grasses_zurich
          features_position: bottom
          vertical: false
          hide_state: false
        - type: tile
          name: ' Zürich'
          entity: sensor.grasses_zurich_2
          features_position: bottom
          vertical: false
      grid_options:
        columns: 9
        rows: auto
    - type: horizontal-stack
      cards:
        - type: tile
          name: ' Bern'
          entity: sensor.grasses_bern
          features_position: bottom
          vertical: false
        - type: tile
          name: '  Bern'
          entity: sensor.grasses_bern_2
          features_position: bottom
          vertical: false
      grid_options:
        columns: 9
        rows: auto
    - type: markdown
      content: >-
        <img
        src="https://github.com/frimtec/hass-swiss-pollen/blob/main/images/birch.png?raw=true"
        alt="Birke" width="55" height="70">

        &nbsp;&nbsp;&nbsp;Birke
      grid_options:
        columns: 3
        rows: 2
    - type: horizontal-stack
      cards:
        - type: tile
          name: ' Zürich'
          entity: sensor.birch_zurich
          features_position: bottom
          vertical: false
        - type: tile
          name: '  Zürich'
          entity: sensor.birch_zurich_2
          features_position: bottom
          vertical: false
      grid_options:
        columns: 9
        rows: auto
    - type: horizontal-stack
      cards:
        - type: tile
          name: '  Bern'
          entity: sensor.birch_bern
          features_position: bottom
          vertical: false
        - type: tile
          name: '  Bern'
          entity: sensor.birch_bern_2
          features_position: bottom
          vertical: false
      grid_options:
        columns: 9
        rows: auto
```
</details>

## Credits
- [izacus](https://github.com/izacus): For his great integration [hass-swissweather](https://github.com/izacus/hass-swissweather) that was the insperation for this integration.

---

[hacs-shield]: https://img.shields.io/badge/HACS-Default-blue.svg
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
[MeteoSchweiz]: https://www.meteoschweiz.admin.ch/service-und-publikationen/applikationen/pollenprognose.html
[swiss-pollen]: https://github.com/frimtec/swiss-pollen
