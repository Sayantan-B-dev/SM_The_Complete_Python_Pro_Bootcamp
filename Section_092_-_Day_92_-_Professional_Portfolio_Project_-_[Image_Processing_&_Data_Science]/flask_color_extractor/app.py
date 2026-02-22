import os
import numpy as np
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image, ImageFile

# Increase PIL's maximum image pixel limit to avoid DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None
# Allow loading of truncated images (if any)
ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_colors(image_path):
    """
    Extract all distinct colors from the image by quantizing to a 32‑color palette.
    Returns a list of dicts: each with 'rgb', 'count', 'percentage', 'hex'.
    Sorted by frequency (most common first).
    """
    # Open image and ensure RGB mode
    img = Image.open(image_path).convert('RGB')
    
    # Quantize to 32 colors (P mode with palette)
    quantized = img.quantize(colors=32, method=Image.MEDIANCUT)
    
    # Get the palette (list of 768 integers: R,G,B repeated)
    palette = quantized.getpalette()
    colors_in_palette = len(palette) // 3
    
    # Build list of RGB tuples from the palette
    palette_colors = [
        (palette[i*3], palette[i*3+1], palette[i*3+2])
        for i in range(colors_in_palette)
    ]
    
    # Convert quantized image to numpy array of pixel indices
    pix = np.array(quantized)
    indices = pix.flatten()
    
    # Count frequency of each index
    counter = Counter(indices)
    total_pixels = len(indices)
    
    # Build result list for every index that appears (i.e., every color used)
    result = []
    for idx, count in counter.most_common():  # most_common() without argument returns all, sorted
        rgb = palette_colors[idx]
        percentage = (count / total_pixels) * 100
        hex_code = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        result.append({
            'rgb': rgb,
            'count': count,
            'percentage': round(percentage, 2),
            'hex': hex_code
        })
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                colors = get_colors(filepath)
                return render_template('index.html', colors=colors, uploaded_image=filename)
            except Exception as e:
                flash(f'Error processing image: {str(e)}')
                return redirect(request.url)
        else:
            flash('Allowed file types: png, jpg, jpeg, gif, bmp, tiff')
            return redirect(request.url)
    
    return render_template('index.html', colors=None)

if __name__ == '__main__':
    app.run(debug=True)