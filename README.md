# WLC Configuration Generator

This application generates Cisco Wireless LAN Controller (WLC) configuration templates for uRWB (Ultra Reliable Wireless Backhaul) networks using OpenAI's GPT-4 model.

## Features

- Generate WLC configuration templates for different topologies (P2P, P2MP, Mesh, Mobility)
- Support for various AP models
- Customizable parameters (channels, country codes, passphrases, etc.)
- Uses example configurations as context for accurate template generation

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the `.env.example` file to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file and add your OpenAI API key

## Usage

The application can be used in two ways:

1. Run the example configuration:
   ```bash
   python wlc_config_generator.py
   ```

2. Import and use in your own code:
   ```python
   from wlc_config_generator import WLCConfigGenerator, WLCConfigRequest

   generator = WLCConfigGenerator()
   request = WLCConfigRequest(
       topology="p2mp",
       ap_model="9124AXI",
       country_code="IT",
       channel=136,
       channel_width=20,
       passphrase="your_passphrase",
       additional_requirements="Include scanning functionality"
   )
   
   config = generator.generate_config(request)
   print(config)
   ```

## Configuration Parameters

The `WLCConfigRequest` class accepts the following parameters:

- `topology`: Network topology (p2p, pmp, mesh, mobility)
- `ap_model`: AP model number
- `ap_mac`: AP MAC address (optional)
- `profile_name`: Profile name (optional)
- `country_code`: Country code (optional)
- `channel`: Channel number (optional)
- `channel_width`: Channel width (optional)
- `passphrase`: Security passphrase (optional)
- `additional_requirements`: Any additional requirements (optional)

## Example Output

The generated configuration will follow Cisco's WLC configuration format and will include placeholders for any unspecified parameters.

## Contributing

Feel free to submit issues and enhancement requests. 