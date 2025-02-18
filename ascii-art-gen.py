from PIL import Image
import argparse

# ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image_path, width=100):
    # Open image and convert to grayscale
    image = Image.open(image_path).convert("L")
    
    # Calculate new height to maintain aspect ratio
    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio * 0.55)  # Adjusting for character height
    
    # Resize the image
    image = image.resize((width, new_height))
    
    # Convert pixels to ASCII
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    
    # Format ASCII string into image shape
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join(ascii_str[i:i+width] for i in range(0, ascii_str_len, width))
    
    return ascii_img

def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("-w", "--width", type=int, default=100, help="Width of ASCII output")
    
    args = parser.parse_args()
    ascii_art = image_to_ascii(args.image, args.width)
    
    # Print ASCII Art
    print(ascii_art)
    
    # Save output to a file
    with open("ascii_art_output.txt", "w") as f:
        f.write(ascii_art)
    print("ASCII art saved to ascii_art_output.txt")

if __name__ == "__main__":
    main()
