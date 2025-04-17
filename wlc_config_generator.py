import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import openai
from pydantic import BaseModel
import json
import sys

# Load environment variables
load_dotenv()

class WLCConfigRequest(BaseModel):
    topology: str  # p2p, pmp, mesh, mobility
    ap_model: str
    ap_mac: Optional[str] = None
    profile_name: Optional[str] = None
    country_code: Optional[str] = None
    channel: Optional[int] = None
    channel_width: Optional[int] = None
    passphrase: Optional[str] = None
    additional_requirements: Optional[str] = None

class WLCConfigGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        openai.api_key = api_key
        self.context = self._load_context()

    def _load_context(self) -> str:
        """Load the context from the configuration files."""
        context_files = []
        for root, _, files in os.walk("context"):
            for file in files:
                if file.endswith(".configwlc"):
                    with open(os.path.join(root, file), "r") as f:
                        context_files.append(f.read())
        return "\n\n".join(context_files)

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the OpenAI API."""
        return f"""You are a Cisco WLC configuration expert. Your task is to generate WLC configuration templates for uRWB (Ultra Reliable Wireless Backhaul) networks.
        
Available context from example configurations:
{self.context}

Generate configurations that follow Cisco's best practices and match the provided examples in style and format.
Use placeholders for variables that are not specified by the user.
"""

    def _create_user_prompt(self, request: WLCConfigRequest) -> str:
        """Create the user prompt based on the request."""
        prompt = f"""Generate a WLC configuration template for the following requirements:

Topology: {request.topology}
AP Model: {request.ap_model}
"""
        
        if request.ap_mac:
            prompt += f"AP MAC Address: {request.ap_mac}\n"
        if request.profile_name:
            prompt += f"Profile Name: {request.profile_name}\n"
        if request.country_code:
            prompt += f"Country Code: {request.country_code}\n"
        if request.channel:
            prompt += f"Channel: {request.channel}\n"
        if request.channel_width:
            prompt += f"Channel Width: {request.channel_width}\n"
        if request.passphrase:
            prompt += f"Passphrase: {request.passphrase}\n"
        if request.additional_requirements:
            prompt += f"Additional Requirements: {request.additional_requirements}\n"

        return prompt

    def generate_config(self, request: WLCConfigRequest) -> str:
        """Generate the WLC configuration based on the request."""
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": self._create_user_prompt(request)}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content

def get_user_input(prompt: str, required: bool = True) -> str:
    """Get user input with validation."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please enter a value.")

def create_config_from_user_input() -> WLCConfigRequest:
    """Create a configuration request from user input."""
    print("\n=== Cisco WLC Configuration Generator ===")
    print("Please provide the following information to generate your configuration:\n")

    # Required fields
    topology = get_user_input(
        "Enter network topology (p2p/p2mp/mesh/mobility): ",
        required=True
    ).lower()
    
    ap_model = get_user_input(
        "Enter AP model (e.g., 9124AXI, 9178AXD): ",
        required=True
    )

    # Optional fields
    print("\nOptional fields (press Enter to skip):")
    ap_mac = get_user_input("Enter AP MAC address (e.g., 60b9.c088.4f18): ", required=False)
    profile_name = get_user_input("Enter profile name: ", required=False)
    country_code = get_user_input("Enter country code (e.g., IT, US): ", required=False)
    
    channel = None
    channel_input = get_user_input("Enter channel number: ", required=False)
    if channel_input:
        try:
            channel = int(channel_input)
        except ValueError:
            print("Invalid channel number. Using default.")
    
    channel_width = None
    width_input = get_user_input("Enter channel width (20/40/80): ", required=False)
    if width_input:
        try:
            channel_width = int(width_input)
        except ValueError:
            print("Invalid channel width. Using default.")
    
    passphrase = get_user_input("Enter security passphrase: ", required=False)
    
    additional_requirements = get_user_input(
        "Enter any additional requirements (e.g., scanning, specific features): ",
        required=False
    )

    return WLCConfigRequest(
        topology=topology,
        ap_model=ap_model,
        ap_mac=ap_mac,
        profile_name=profile_name,
        country_code=country_code,
        channel=channel,
        channel_width=channel_width,
        passphrase=passphrase,
        additional_requirements=additional_requirements
    )

def main():
    try:
        # Create configuration from user input
        request = create_config_from_user_input()
        
        # Generate configuration
        print("\nGenerating configuration...")
        generator = WLCConfigGenerator()
        config = generator.generate_config(request)
        
        # Save configuration to file
        output_file = f"wlc_config_{request.topology}_{request.ap_model}.txt"
        with open(output_file, "w") as f:
            f.write(config)
        
        print(f"\nConfiguration generated successfully!")
        print(f"Configuration saved to: {output_file}")
        print("\nConfiguration content:")
        print("=" * 80)
        print(config)
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 