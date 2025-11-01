import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark Tool")
        self.root.geometry("800x600")
        
        # Variables
        self.original_image = None
        self.watermarked_image = None
        self.preview_image = None
        
        # Watermark settings
        self.watermark_text = tk.StringVar(value="WATERMARK")
        self.watermark_opacity = tk.IntVar(value=128)
        self.watermark_size = tk.IntVar(value=36)
        self.watermark_color = "#FFFFFF"
        self.watermark_position = tk.StringVar(value="bottom-right")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Select Image", command=self.select_image).pack(side=tk.LEFT, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="No image selected")
        self.file_label.pack(side=tk.LEFT)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Watermark Settings", padding="5")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Text input
        ttk.Label(settings_frame, text="Watermark Text:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_frame, textvariable=self.watermark_text, width=20).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Opacity slider
        ttk.Label(settings_frame, text="Opacity:").grid(row=1, column=0, sticky=tk.W, pady=2)
        opacity_frame = ttk.Frame(settings_frame)
        opacity_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Scale(opacity_frame, from_=0, to=255, variable=self.watermark_opacity, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(opacity_frame, textvariable=self.watermark_opacity, width=4).pack(side=tk.RIGHT)
        
        # Font size slider
        ttk.Label(settings_frame, text="Font Size:").grid(row=2, column=0, sticky=tk.W, pady=2)
        size_frame = ttk.Frame(settings_frame)
        size_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Scale(size_frame, from_=12, to=100, variable=self.watermark_size, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(size_frame, textvariable=self.watermark_size, width=4).pack(side=tk.RIGHT)
        
        # Color selection
        ttk.Label(settings_frame, text="Color:").grid(row=3, column=0, sticky=tk.W, pady=2)
        color_frame = ttk.Frame(settings_frame)
        color_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(color_frame, text="Choose Color", command=self.choose_color).pack(side=tk.LEFT)
        self.color_preview = tk.Label(color_frame, bg=self.watermark_color, width=3, relief=tk.RAISED)
        self.color_preview.pack(side=tk.LEFT, padx=(10, 0))
        
        # Position selection
        ttk.Label(settings_frame, text="Position:").grid(row=4, column=0, sticky=tk.W, pady=2)
        position_combo = ttk.Combobox(settings_frame, textvariable=self.watermark_position, 
                                    values=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                                    state="readonly", width=18)
        position_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Preview", command=self.preview_watermark).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT)
        
        # Configure settings frame grid
        settings_frame.columnconfigure(1, weight=1)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="5")
        preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas for image preview
        self.canvas = tk.Canvas(preview_frame, bg="white", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars for canvas
        v_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)   
 
    def select_image(self):
        """Open file dialog to select an image"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=file_types
        )
        
        if filename:
            try:
                self.original_image = Image.open(filename)
                self.file_label.config(text=os.path.basename(filename))
                self.display_original_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def display_original_image(self):
        """Display the original image in the canvas"""
        if self.original_image:
            # Calculate display size while maintaining aspect ratio
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 400, 400
            
            img_width, img_height = self.original_image.size
            
            # Calculate scaling factor
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            scale = min(scale_x, scale_y, 1.0)  # Don't upscale
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image for display
            display_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(display_image)
            
            # Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.preview_image)
    
    def choose_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose watermark color")
        if color[1]:  # color[1] is the hex value
            self.watermark_color = color[1]
            self.color_preview.config(bg=self.watermark_color)
    
    def get_watermark_position(self, img_width, img_height, text_width, text_height):
        """Calculate watermark position based on selection"""
        margin = 20
        position = self.watermark_position.get()
        
        if position == "top-left":
            return (margin, margin)
        elif position == "top-right":
            return (img_width - text_width - margin, margin)
        elif position == "bottom-left":
            return (margin, img_height - text_height - margin)
        elif position == "bottom-right":
            return (img_width - text_width - margin, img_height - text_height - margin)
        elif position == "center":
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        else:
            return (img_width - text_width - margin, img_height - text_height - margin)
    
    def create_watermarked_image(self):
        """Create watermarked version of the image"""
        if not self.original_image:
            messagebox.showwarning("Warning", "Please select an image first.")
            return None
        
        # Create a copy of the original image
        watermarked = self.original_image.copy().convert("RGBA")
        
        # Create a transparent overlay
        overlay = Image.new("RGBA", watermarked.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Try to use a better font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", self.watermark_size.get())
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", self.watermark_size.get())
            except:
                font = ImageFont.load_default()
        
        # Get text dimensions
        text = self.watermark_text.get()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Get position
        x, y = self.get_watermark_position(watermarked.width, watermarked.height, text_width, text_height)
        
        # Convert hex color to RGB and add alpha
        color_rgb = tuple(int(self.watermark_color[i:i+2], 16) for i in (1, 3, 5))
        color_rgba = color_rgb + (self.watermark_opacity.get(),)
        
        # Draw text on overlay
        draw.text((x, y), text, font=font, fill=color_rgba)
        
        # Composite the overlay onto the original image
        watermarked = Image.alpha_composite(watermarked, overlay)
        
        return watermarked.convert("RGB")
    
    def preview_watermark(self):
        """Preview the watermarked image"""
        self.watermarked_image = self.create_watermarked_image()
        if self.watermarked_image:
            # Display watermarked image
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 400, 400
            
            img_width, img_height = self.watermarked_image.size
            
            # Calculate scaling factor
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            scale = min(scale_x, scale_y, 1.0)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image for display
            display_image = self.watermarked_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(display_image)
            
            # Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.preview_image)
    
    def save_image(self):
        """Save the watermarked image"""
        if not self.watermarked_image:
            messagebox.showwarning("Warning", "Please preview the watermark first.")
            return
        
        file_types = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Save watermarked image",
            defaultextension=".jpg",
            filetypes=file_types
        )
        
        if filename:
            try:
                # Determine format based on file extension
                if filename.lower().endswith('.png'):
                    self.watermarked_image.save(filename, "PNG")
                else:
                    self.watermarked_image.save(filename, "JPEG", quality=95)
                messagebox.showinfo("Success", f"Image saved successfully as {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()