from PIL import Image
import os

# ----------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------
STOP_SIGNAL = 0 

# ----------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------

def message_to_numbers(message):
    numbers = [ord(char) for char in message]
    numbers.append(STOP_SIGNAL)
    return numbers

def numbers_to_message(numbers):
    # Converts list of ASCII numbers back into a string
    return "".join(chr(num) for num in numbers)

def encode_image(image_file, message, output_file):
    if not all(ord(c) < 128 for c in message):
        print("ERROR: Message contains non-ASCII characters (no emoji or special characters).")
        return

    if not output_file.lower().endswith('.png'):
        print("ERROR: Output file must be a .png file.")
        return


    image_file = os.path.expanduser(image_file)
    try:
        img = Image.open(image_file).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    width, height = img.size
    total_pixels = width * height
    secret_numbers = message_to_numbers(message)

    if len(secret_numbers) > total_pixels:
        print("ERROR: Your message is too long for this image!")
        return

    index = 0
    # Create a copy to modify
    encoded_img = img.copy()

    for y in range(height):
        for x in range(width):
            if index < len(secret_numbers):
                r, g, b = encoded_img.getpixel((x, y))
                # Overwrite Red channel
                encoded_img.putpixel((x, y), (secret_numbers[index], g, b))
                index += 1
            else:
                break
        if index >= len(secret_numbers):
            break

    encoded_img.save(output_file)
    print(f"\nSuccess! Encoded image saved as: '{output_file}'")

def decode_image(image_file):
    image_file = os.path.expanduser(image_file)
    try:
        img = Image.open(image_file).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return
        
    collected_numbers = []

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            if r == STOP_SIGNAL:
                if not collected_numbers:
                    print("No hidden message was found.")
                    return ""
                secret_message = numbers_to_message(collected_numbers)
                print(f"\nHidden message revealed: '{secret_message}'")
                return secret_message
            collected_numbers.append(r)

    print("Warning: No stop signal found.")
    return ""

def main():
    print("================================")
    print("   Image Steganography Project  ")
    print("================================")
    print("1 - Hide a secret message (Encode)")
    print("2 - Reveal a secret message (Decode)")

    choice = input("\nEnter 1 or 2: ").strip()
    if choice == "1":
        img_path = input("Original image path: ").strip()
        msg = input("Message to hide: ").strip()
        out_path = input("Save as (e.g., secret.png): ").strip()
        encode_image(img_path, msg, out_path)
    elif choice == "2":
        img_path = input("Encoded image path: ").strip()
        decode_image(img_path)

if __name__ == "__main__":
    main()
