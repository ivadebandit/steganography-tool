"""
==========================================================
  IMAGE STEGANOGRAPHY PROJECT
==========================================================

Hide a secret message inside a normal-looking image,
then decode it back out.

HOW IT WORKS:
  Every pixel has a Red, Green, and Blue (RGB) value (0-255).
  We secretly overwrite the Red channel of successive pixels
  with the ASCII number of each character in our message.
  The change is invisible to the human eye, but Python can
  read it back.

  Example:  'H' -> ord('H') -> 72  -> stored in pixel (0,0) Red
            'I' -> ord('I') -> 73  -> stored in pixel (1,0) Red
             0  (stop signal)      -> stored in pixel (2,0) Red

IMPORTANT — USE PNG IMAGES ONLY

"""

from PIL import Image


# ----------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------

STOP_SIGNAL = 0 # A Red value of 0 signals "message ends here"


# ----------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------

def message_to_numbers(message):
    """
    Converts a text message into a list of ASCII numbers,
    then appends the stop signal (0) at the end.

    Example:
        message_to_numbers("HI")  ->  [72, 73, 0]
    """
    numbers = []
    for char in message:
        numbers.append(ord(char))  # 'H' -> 72, 'I' -> 73, etc.
    numbers.append(STOP_SIGNAL)    # Mark the end of the message
    return numbers


def numbers_to_message(numbers):
    """
    Converts a list of ASCII numbers back into a text string.

    Example:
        numbers_to_message([72, 73])  ->  "HI"
    """
    message = ""
    for num in numbers:
        message += chr(num)   # 72 -> 'H', 73 -> 'I', etc.
    return message


# ----------------------------------------------------------
# ENCODER  —  Hide the message inside the image
# ----------------------------------------------------------

def encode_image(image_file, message, output_file):
    img = Image.open(image_file).convert('RGB')
    width, height = img.size
    total_pixels = width * height

    # Safety check
    if len(message) + 1 > total_pixels:
        print("ERROR: Your message is too long for this image!")
        return

    secret_numbers = message_to_numbers(message)
    index = 0

    for y in range(height):
        for x in range(width):
            if index < len(secret_numbers):
                r, g, b = img.getpixel((x, y))
                img.putpixel((x, y), (secret_numbers[index], g, b))
                index += 1
            else:
                break
        if index >= len(secret_numbers):
            break

    img.save(output_file)
    print(f"\nSuccess! Encoded image saved as: '{output_file}'")

    # -- Convert message to numbers -----------------------
    secret_numbers = message_to_numbers(message)

    print("Encoding message: '" + message + "'")
    print("As ASCII numbers: " + str(secret_numbers))

    # -- Inject numbers into the image, pixel by pixel ----
    
    # We scan row by row (y first, then x) — same order used in decoding.
    index = 0   # tracks which secret number we are writing next

    for y in range(img.height):
        for x in range(img.width):

            if index < len(secret_numbers):
                r, g, b = img.getpixel((x, y))
                img.putpixel((x, y), (secret_numbers[index], g, b))
                index += 1
            else:
                break   # All data has been written; leave rest of image alone

        if index >= len(secret_numbers):
            break       # Break out of the outer loop too

    # -- Save the encoded image ---------------------------
    img.save(output_file)
    print("\nSuccess! Encoded image saved as: '" + output_file + "'")
    print("To a human viewer it looks completely normal.")
    print("Send it to a friend and have them run the decoder!")


# ----------------------------------------------------------
# DECODER  -  Reveal the hidden message from an image
# ----------------------------------------------------------

def decode_image(image_file):
    img = Image.open(image_file).convert('RGB')
    collected_numbers = []

    print(f"Scanning image: '{image_file}'")
    print("Reading hidden data from pixels...")

    # -- Scan pixels in the same order as the encoder -----
    for y in range(img.height):
        for x in range(img.width):
            # Get the pixel data using Pillow
            r, g, b = img.getpixel((x, y))
            red_value = r

            # Did we hit the stop signal?
            if red_value == STOP_SIGNAL:
                if len(collected_numbers) == 0:
                    print("No hidden message was found in this image.")
                    return ""

                # Convert the collected numbers back to text
                secret_message = numbers_to_message(collected_numbers)
                print(f"\nHidden message revealed: '{secret_message}'")
                return secret_message

            # Not a stop signal, keep collecting
            collected_numbers.append(red_value)

    # We scanned the whole image and never found a stop signal
    print("Warning: No stop signal found.")
    print("This image may not contain a hidden message.")
    return ""

# ----------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------

def main():
    print("================================")
    print("   Image Steganography Project  ")
    print("================================")
    print("1 - Hide a secret message (Encode)")
    print("2 - Reveal a secret message (Decode)")

    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        print("\n--- ENCODER ---")
        print("Make sure you use a .png image file!")
        image_file  = input("Path to your original image (e.g. photo.png): ").strip()
        message     = input("Secret message to hide: ").strip()
        output_file = input("Save encoded image as (e.g. secret.png): ").strip()
        encode_image(image_file, message, output_file)

    elif choice == "2":
        print("\n--- DECODER ---")
        image_file = input("Path to the encoded image (e.g. secret.png): ").strip()
        decode_image(image_file)

    else:
        print("Invalid choice — please enter 1 or 2.")


# ----------------------------------------------------------
# Run the program
# ----------------------------------------------------------
if __name__ == "__main__":
    main()

# thats it