# WLC Configuration Generator

This application generates Cisco Wireless LAN Controller (WLC) configuration templates for uRWB (Ultra Reliable Wireless Backhaul) networks using OpenAI's GPT-4 model. It provides an interactive interface for specifying configuration requirements in natural language.

## Features

- Interactive command-line interface for specifying configuration requirements
- Support for different network topologies (P2P, P2MP, Mesh, Mobility)
- Support for various AP models
- Customizable parameters (channels, country codes, passphrases, etc.)
- Uses example configurations as context for accurate template generation
- Automatic configuration file generation
- Input validation and error handling

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
4. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```bash
python wlc_config_generator.py
```

The application will guide you through the configuration process with the following prompts:

### Required Fields
- Network topology (p2p/p2mp/mesh/mobility)
- AP model (e.g., 9124AXI, 9178AXD)

### Optional Fields
- AP MAC address (e.g., 60b9.c088.4f18)
- Profile name
- Country code (e.g., IT, US)
- Channel number
- Channel width (20/40/80)
- Security passphrase
- Additional requirements (e.g., scanning, specific features)

After providing the required information, the application will:
1. Generate the configuration
2. Save it to a file named `wlc_config_{topology}_{ap_model}.txt`
3. Display the configuration on screen

## Example Usage

```
=== Cisco WLC Configuration Generator ===
Please provide the following information to generate your configuration:

Enter network topology (p2p/p2mp/mesh/mobility): p2mp
Enter AP model (e.g., 9124AXI, 9178AXD): 9124AXI

Optional fields (press Enter to skip):
Enter AP MAC address (e.g., 60b9.c088.4f18): 
Enter profile name: 
Enter country code (e.g., IT, US): IT
Enter channel number: 136
Enter channel width (20/40/80): 20
Enter security passphrase: 
Enter any additional requirements (e.g., scanning, specific features): Include scanning functionality

Generating configuration...
Configuration generated successfully!
Configuration saved to: wlc_config_p2mp_9124AXI.txt
```

## Configuration Parameters

The application supports the following parameters:

- `topology`: Network topology (p2p, pmp, mesh, mobility)
- `ap_model`: AP model number
- `ap_mac`: AP MAC address (optional)
- `profile_name`: Profile name (optional)
- `country_code`: Country code (optional)
- `channel`: Channel number (optional)
- `channel_width`: Channel width (optional)
- `passphrase`: Security passphrase (optional)
- `additional_requirements`: Any additional requirements (optional)

## Error Handling

The application includes error handling for:
- Missing API key
- Invalid input values
- File system errors
- API communication errors

## Contributing

Feel free to submit issues and enhancement requests. 