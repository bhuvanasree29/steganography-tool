from PIL import Image

def encode_image(image_path, output_path, secret_message):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size

    max_capacity = width * height * 3 // 8  # each pixel can carry 3 bits, 8 bits per char
    full_message = secret_message + "###END###"

    if len(full_message) > max_capacity:
        raise ValueError("Message too large to hide in image.")

    binary_message = ''.join(format(ord(c), '08b') for c in full_message)
    pixels = list(image.getdata())
    new_pixels = []

    idx = 0
    for pixel in pixels:
        r, g, b = pixel
        if idx < len(binary_message):
            r = (r & ~1) | int(binary_message[idx])
            idx += 1
        if idx < len(binary_message):
            g = (g & ~1) | int(binary_message[idx])
            idx += 1
        if idx < len(binary_message):
            b = (b & ~1) | int(binary_message[idx])
            idx += 1
        new_pixels.append((r, g, b))

    new_pixels.extend(pixels[len(new_pixels):])
    encoded_img = Image.new("RGB", image.size)
    encoded_img.putdata(new_pixels)
    encoded_img.save(output_path)

def decode_image(image_path):
    image = Image.open(image_path).convert('RGB')
    pixels = list(image.getdata())

    binary = ''
    for pixel in pixels:
        for value in pixel[:3]:
            binary += str(value & 1)

    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
        if ''.join(chars).endswith("###END###"):
            break

    return ''.join(chars).replace("###END###", "")
