from flask import Flask, render_template, request, send_file
import os
from steganography.image_utils import encode_image, decode_image
from steganography.text_utils import hide_in_text, extract_from_text

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return """
    <div style='display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;'>
        <h1>🕵️ Steganography Tool</h1>
        <p><a href='/image'>Image Steganography</a> | <a href='/text'>Text Steganography</a></p>
    </div>
    """

@app.route("/image", methods=["GET", "POST"])
def image_steg():
    message = ""
    if request.method == "POST":
        if "image" in request.files and request.form.get("secret_text"):
            image = request.files["image"]
            secret = request.form.get("secret_text")
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)
            output_path = os.path.join(UPLOAD_FOLDER, "stego_" + image.filename)
            encode_image(image_path, output_path, secret)
            if os.path.exists(output_path):
                return send_file(output_path, as_attachment=True)
            else:
                return f"<p><strong>[!] Failed to create output file:</strong> {output_path}</p>"
        elif "decode_image" in request.files:
            stego = request.files["decode_image"]
            stego_path = os.path.join(UPLOAD_FOLDER, stego.filename)
            stego.save(stego_path)
            message = decode_image(stego_path)
    return f"""
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 20px;'>
            <h2>🖼️ Image Steganography</h2>
            <form method="post" enctype="multipart/form-data" style="margin-bottom: 20px;">
                <h3>Hide Message in Image</h3>
                <input type="file" name="image" required><br><br>
                <textarea name="secret_text" rows="4" cols="50" placeholder="Enter secret message" required></textarea><br><br>
                <input type="submit" value="Encode"><br><br>
            </form>
            <hr style='width: 60%; border: 1px solid #ccc;'>
            <form method="post" enctype="multipart/form-data">
                <h3>Decode Message from Image</h3>
                <input type="file" name="decode_image" required><br><br>
                <input type="submit" value="Decode"><br><br>
            </form>
            <p><strong>Decoded:</strong> {message}</p>
        </div>
    """

@app.route("/text", methods=["GET", "POST"])
def text_steg():
    message = ""
    if request.method == "POST":
        if "textfile" in request.files and request.form.get("secret_text"):
            text_file = request.files["textfile"]
            secret = request.form.get("secret_text")
            content = text_file.read().decode('utf-8', errors='ignore')
            stego_text = hide_in_text(content, secret)
            out_path = os.path.join(UPLOAD_FOLDER, "stego_text.txt")
            with open(out_path, "w", encoding='utf-8') as f:
                f.write(stego_text)
            if os.path.exists(out_path):
                return send_file(out_path, as_attachment=True)
            else:
                return f"<p><strong>[!] Failed to create output file:</strong> {out_path}</p>"
        elif "decode_textfile" in request.files:
            decode_file = request.files["decode_textfile"]
            content = decode_file.read().decode('utf-8', errors='ignore')
            message = extract_from_text(content)
    return f"""
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 20px;'>
            <h2>📄 Text Steganography</h2>
            <form method="post" enctype="multipart/form-data" style="margin-bottom: 20px;">
                <h3>Hide Message in Text</h3>
                <input type="file" name="textfile" required><br><br>
                <textarea name="secret_text" rows="4" cols="50" placeholder="Enter secret message" required></textarea><br><br>
                <input type="submit" value="Encode"><br><br>
            </form>
            <hr style='width: 60%; border: 1px solid #ccc;'>
            <form method="post" enctype="multipart/form-data">
                <h3>Decode Message from Text</h3>
                <input type="file" name="decode_textfile" required><br><br>
                <input type="submit" value="Decode"><br><br>
            </form>
            <p><strong>Decoded:</strong> {message}</p>
        </div>
    """

if __name__ == "__main__":
    app.run(debug=True)

