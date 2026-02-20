import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Your Images")
        self.root.geometry("800x600")

        # Variables to store images and paths
        self.main_image = None          # PIL Image object (original)
        self.main_image_tk = None       # ImageTk for display
        self.logo_image = None           # PIL Image object (logo)
        self.watermarked_image = None    # PIL Image after watermarking
        self.current_preview = None       # ImageTk for preview

        self.watermark_pos = (0.8, 0.9)  # default relative position (bottom-right)
        self.watermark_text = tk.StringVar()
        self.watermark_text.set("© YourWebsite.com")

        # Watermark type: "text", "logo", or "both"
        self.watermark_type = tk.StringVar(value="text")

        # Font settings
        self.font_path = None
        self.font_size = 36
        self.font_color = (255, 255, 255, 128)  # white with 50% opacity

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Buttons for loading images
        tk.Button(control_frame, text="Load Main Image", command=self.load_main_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Load Logo", command=self.load_logo).pack(side=tk.LEFT, padx=5)

        # Watermark text entry
        tk.Label(control_frame, text="Watermark Text:").pack(side=tk.LEFT, padx=5)
        tk.Entry(control_frame, textvariable=self.watermark_text, width=30).pack(side=tk.LEFT, padx=5)

        # Watermark type selection
        tk.Radiobutton(control_frame, text="Text", variable=self.watermark_type, value="text").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Logo", variable=self.watermark_type, value="logo").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Both", variable=self.watermark_type, value="both").pack(side=tk.LEFT)

        # Buttons for actions
        tk.Button(control_frame, text="Add Watermark", command=self.add_watermark).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)

        # Font customization (optional)
        tk.Button(control_frame, text="Choose Font", command=self.choose_font).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Font Color", command=self.choose_color).pack(side=tk.LEFT, padx=5)

        # Canvas for image preview
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.set_watermark_position)

        # Status bar
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def load_main_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Main Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                self.main_image = Image.open(file_path).convert("RGBA")
                self.show_image_on_canvas(self.main_image)
                self.status.config(text=f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

    def load_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                self.logo_image = Image.open(file_path).convert("RGBA")
                self.status.config(text=f"Logo loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open logo: {e}")

    def show_image_on_canvas(self, pil_image):
        """Resize image to fit canvas and display it."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1:  # canvas not yet realized
            canvas_width, canvas_height = 700, 400

        # Maintain aspect ratio
        pil_image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.current_preview = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.current_preview, anchor=tk.CENTER)

    def set_watermark_position(self, event):
        """Capture click position on canvas for watermark placement."""
        if self.current_preview and self.main_image:
            # Convert canvas coordinates to image coordinates
            canvas_bbox = self.canvas.bbox("all")
            if canvas_bbox:
                img_x, img_y = event.x - canvas_bbox[0], event.y - canvas_bbox[1]
                # Map to original image size
                orig_w, orig_h = self.main_image.size
                disp_w, disp_h = self.current_preview.width(), self.current_preview.height()
                if disp_w > 0 and disp_h > 0:
                    x = int(img_x * orig_w / disp_w)
                    y = int(img_y * orig_h / disp_h)
                    self.watermark_pos = (x, y)
                    self.status.config(text=f"Watermark position set to ({x}, {y})")

    def choose_font(self):
        file_path = filedialog.askopenfilename(
            title="Select TrueType Font",
            filetypes=[("Font files", "*.ttf *.otf")]
        )
        if file_path:
            self.font_path = file_path
            self.status.config(text=f"Font selected: {os.path.basename(file_path)}")

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose font color", color='white')
        if color[0]:
            # color[0] is RGB tuple, add alpha (e.g., 255 for opaque)
            self.font_color = (int(color[0][0]), int(color[0][1]), int(color[0][2]), 255)
            self.status.config(text=f"Font color set")

    def add_watermark(self):
        if not self.main_image:
            messagebox.showwarning("No Image", "Please load a main image first.")
            return

        # Work on a copy of the main image
        img = self.main_image.copy()
        draw_type = self.watermark_type.get()

        # Add logo if selected
        if draw_type in ("logo", "both") and self.logo_image:
            img = self.add_logo_watermark(img)

        # Add text if selected
        if draw_type in ("text", "both") and self.watermark_text.get().strip():
            img = self.add_text_watermark(img)

        # Update preview and store watermarked image
        self.watermarked_image = img
        self.show_image_on_canvas(img)
        self.status.config(text="Watermark applied. You can save the image now.")

    def add_text_watermark(self, img):
        """Draw text onto the image at self.watermark_pos."""
        draw = ImageDraw.Draw(img, "RGBA")
        text = self.watermark_text.get().strip()

        # Try to load font, fallback to default
        try:
            if self.font_path:
                font = ImageFont.truetype(self.font_path, self.font_size)
            else:
                # Use default font; size can be approximated
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Use textbbox to get text size (new in Pillow 8.0.0)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Determine position (absolute or relative)
        if isinstance(self.watermark_pos[0], float):
            # relative coordinates (0-1)
            x = int((img.width - text_width) * self.watermark_pos[0])
            y = int((img.height - text_height) * self.watermark_pos[1])
        else:
            # absolute coordinates from click
            x, y = self.watermark_pos
            # Adjust so that the click point is at the top-left of the text?
            # For simplicity, we'll use the click as top-left corner.
            # Alternatively, you could center the text around the click.
            pass

        # Draw the text
        draw.text((x, y), text, font=font, fill=self.font_color)
        return img

    def add_logo_watermark(self, img):
        """Overlay logo image with transparency."""
        if not self.logo_image:
            return img

        # Resize logo to be a reasonable size (e.g., 20% of main image width)
        base_width = int(img.width * 0.2)
        w_percent = base_width / float(self.logo_image.width)
        new_height = int(self.logo_image.height * w_percent)
        logo_resized = self.logo_image.resize((base_width, new_height), Image.Resampling.LANCZOS)

        # Determine position
        if isinstance(self.watermark_pos[0], float):
            # relative
            x = int((img.width - logo_resized.width) * self.watermark_pos[0])
            y = int((img.height - logo_resized.height) * self.watermark_pos[1])
        else:
            x, y = self.watermark_pos

        # Paste using alpha channel as mask if available
        if logo_resized.mode == 'RGBA':
            # Create a transparent layer the size of the main image
            transparent = Image.new('RGBA', img.size, (0,0,0,0))
            transparent.paste(logo_resized, (x, y), logo_resized)
            img = Image.alpha_composite(img, transparent)
        else:
            # If logo has no alpha, just paste (may lose transparency)
            img.paste(logo_resized, (x, y))

        return img

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showwarning("No Watermarked Image", "Please add a watermark first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                # Convert to RGB if saving as JPEG
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    self.watermarked_image.convert("RGB").save(file_path)
                else:
                    self.watermarked_image.save(file_path)
                self.status.config(text=f"Saved to: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()