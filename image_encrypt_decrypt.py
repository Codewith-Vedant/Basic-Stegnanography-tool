from PIL import Image
import numpy as np
import os

def message_to_binary(message):
    """Convert a string message to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary):
    """Convert a binary string to a string message."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def embed_message(image_path, output_path, message):
    """Embed a message into an image."""
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            binary_message = message_to_binary(message) + '1111111111111110'  # End of message delimiter
            binary_message = list(binary_message)
            pixels = np.array(img)

            if len(binary_message) > pixels.size * 3:
                raise ValueError("Message is too long to be embedded in the image.")

            for i in range(pixels.shape[0]):
                for j in range(pixels.shape[1]):
                    for k in range(3):  # R, G, B
                        if binary_message:
                            pixels[i, j, k] = (pixels[i, j, k] & ~1) | int(binary_message.pop(0))

            result_img = Image.fromarray(pixels)
            result_img.save(output_path)
            print(f"Message embedded and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_message(image_path):
    """Extract a message from an image."""
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            pixels = np.array(img)

            binary_message = ""
            for i in range(pixels.shape[0]):
                for j in range(pixels.shape[1]):
                    for k in range(3):  # R, G, B
                        binary_message += str(pixels[i, j, k] & 1)
                        if binary_message.endswith('1111111111111110'):  # End of message delimiter
                            return binary_to_message(binary_message[:-16])

        return binary_to_message(binary_message)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Image Steganography Tool")
    operation = input("Do you want to (e)mbed or (d)extract a message? ")
    if operation not in ['e', 'd']:
        print("Invalid operation. Please enter 'e' to embed or 'd' to extract.")
        return

    image_path = input("Enter the path to the image: ")
    if not os.path.isfile(image_path):
        print(f"File not found: {image_path}")
        return

    if operation == 'e':
        output_path = input("Enter the path to save the output image: ")
        message = input("Enter the message to embed: ")
        embed_message(image_path, output_path, message)
    elif operation == 'd':
        message = extract_message(image_path)
        print(f"Extracted message: {message}")

if __name__ == "__main__":
    main()
