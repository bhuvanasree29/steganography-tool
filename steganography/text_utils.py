# Zero-width encoding for better reliability in web environments
def hide_in_text(input_text, secret_message):
    binary = ''.join(format(ord(c), '08b') for c in secret_message + '###END###')
    zwc_message = ''.join(['\u200B' if bit == '0' else '\u200C' for bit in binary])
    return input_text.rstrip() + '\n' + zwc_message

def extract_from_text(text):
    lines = text.strip().splitlines()
    if not lines:
        return "[!] No hidden message found."

    zwc_line = lines[-1]
    binary = ''.join(['0' if c == '\u200B' else '1' for c in zwc_line if c in ['\u200B', '\u200C']])

    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
        if ''.join(chars).endswith("###END###"):
            break

    return ''.join(chars).replace("###END###", "")
