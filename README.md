 # SteganoHide

A Python CLI utility that hides secret text messages inside the Red channel of PNG images using Least Significant Bit (LSB) steganography.

## Quick Start
1. Clone this repository:
```bash
   git clone [https://github.com/ivadebandit/steganography-tool.git](https://github.com/ivadebandit/steganography-tool.git)
   cd steganography

   Features
Encodes text messages into standard PNG files without visible quality loss.

Decodes hidden messages by scanning the exact pixel path used during encoding.

Stop-Signal Logic: Uses a 0 signal to automatically detect the end of a message.

Safety Checks: Prevents encoding if the message is too long for the image size.

How it works
This tool modifies the Red channel of pixels. The decoder scans the image in the exact same order (nested loops) as the encoder. It collects numerical values until it encounters the STOP_SIGNAL (0), at which point it converts the collected numbers back into text using ASCII mapping.

**Push the update:**
    ```bash
git push

