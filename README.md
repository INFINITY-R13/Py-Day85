# Py-Day85: Image Watermarking Desktop App

A desktop application built with Python that allows users to upload images and add customizable watermarks.

## Features

- **Image Upload**: Support for common image formats (JPEG, PNG, BMP, GIF, TIFF)
- **Customizable Watermarks**: 
  - Custom text watermarks
  - Adjustable opacity (0-255)
  - Variable font size (12-100)
  - Color picker for watermark color
  - Multiple positioning options (corners, center)
- **Live Preview**: See watermark changes in real-time
- **Save Options**: Export as JPEG or PNG with high quality

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Click "Select Image" to choose your image file
3. Customize your watermark:
   - Enter watermark text
   - Adjust opacity with the slider
   - Change font size
   - Pick a color
   - Choose position
4. Click "Preview" to see the result
5. Click "Save Image" to export the watermarked image

## Requirements

- Python 3.7+
- Pillow (PIL) for image processing
- tkinter (included with Python)

## Screenshots

The application provides an intuitive interface with:
- Image selection panel
- Watermark customization controls
- Live preview canvas
- Easy save functionality
