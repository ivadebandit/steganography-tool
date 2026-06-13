SteganoHide

A Python CLI tool for hiding secret text in PNG images using LSB (Least Significant Bit) steganography.

## Demo

![SteganoHide in Action](demo.gif)

<br>

Features
Encodes secret messages into any standard .png image file.
Decodes hidden messages from processed images to reveal the original text.
Uses LSB steganography for invisible data embedding that preserves image quality.
Simple CLI menu to guide the user through the process.
Immediate feedback provided directly in your terminal.
Quick Start
1. Installation

The easiest way to install this tool is using pip:

# Clone the repository
git clone https://github.com/ivadebandit/steganography-tool.git
cd steganography-tool

# Install the tool and its dependencies
pip install .
2. Usage

Once installed, you can run the tool from anywhere in your terminal by simply typing:

steg-tool
Technical Details

This tool uses LSB steganography to modify the Red channel of pixels. The decoder scans the image in the exact sequence as the encoder, gathering values until it hits the STOP_SIGNAL (0), then maps the integers back to text via ASCII.