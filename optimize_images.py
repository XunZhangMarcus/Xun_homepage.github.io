#!/usr/bin/env python3
"""
Image optimization script for GitHub Pages performance enhancement.
This script optimizes images in the images directory for better web performance.
"""

import os
import sys
from PIL import Image
import subprocess

def optimize_image(image_path, output_path=None, quality=85, max_width=1200):
    """
    Optimize a single image for web performance.
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path for the optimized image (optional)
        quality (int): JPEG quality (1-100)
        max_width (int): Maximum width for resizing
    """
    if output_path is None:
        output_path = image_path
    
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if image is too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Optimize and save
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            # Get file sizes
            original_size = os.path.getsize(image_path) if image_path != output_path else 0
            optimized_size = os.path.getsize(output_path)
            
            if original_size > 0:
                savings = ((original_size - optimized_size) / original_size) * 100
                print(f"✓ Optimized {os.path.basename(image_path)}: {original_size//1024}KB → {optimized_size//1024}KB ({savings:.1f}% savings)")
            else:
                print(f"✓ Optimized {os.path.basename(image_path)}: {optimized_size//1024}KB")
                
    except Exception as e:
        print(f"✗ Error optimizing {image_path}: {str(e)}")

def optimize_images_in_directory(directory="images"):
    """
    Optimize all images in the specified directory.
    
    Args:
        directory (str): Directory containing images to optimize
    """
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return
    
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_files.append(os.path.join(root, file))
    
    if not image_files:
        print(f"No images found in '{directory}' directory.")
        return
    
    print(f"Found {len(image_files)} images to optimize...")
    print("-" * 50)
    
    total_original_size = 0
    total_optimized_size = 0
    
    for image_path in image_files:
        original_size = os.path.getsize(image_path)
        total_original_size += original_size
        
        # Skip very small images (likely icons)
        if original_size < 5000:  # 5KB
            print(f"⏭ Skipping {os.path.basename(image_path)} (too small)")
            total_optimized_size += original_size
            continue
        
        # Create backup
        backup_path = image_path + '.backup'
        if not os.path.exists(backup_path):
            os.rename(image_path, backup_path)
            optimize_image(backup_path, image_path)
        else:
            optimize_image(image_path)
        
        total_optimized_size += os.path.getsize(image_path)
    
    print("-" * 50)
    total_savings = ((total_original_size - total_optimized_size) / total_original_size) * 100
    print(f"Total optimization: {total_original_size//1024}KB → {total_optimized_size//1024}KB ({total_savings:.1f}% savings)")

def create_webp_versions(directory="images"):
    """
    Create WebP versions of images for modern browsers.
    
    Args:
        directory (str): Directory containing images
    """
    if not os.path.exists(directory):
        return
    
    supported_formats = ('.jpg', '.jpeg', '.png')
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_path = os.path.join(root, file)
                webp_path = os.path.splitext(image_path)[0] + '.webp'
                
                if not os.path.exists(webp_path):
                    try:
                        with Image.open(image_path) as img:
                            img.save(webp_path, 'WEBP', quality=80, optimize=True)
                            print(f"✓ Created WebP version: {os.path.basename(webp_path)}")
                    except Exception as e:
                        print(f"✗ Error creating WebP for {file}: {str(e)}")

def main():
    """Main function to run image optimization."""
    print("🖼️  GitHub Pages Image Optimization Tool")
    print("=" * 50)
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow (PIL) is required for image optimization.")
        print("Install it with: pip install Pillow")
        sys.exit(1)
    
    # Optimize images
    optimize_images_in_directory("images")
    
    # Create WebP versions for modern browsers
    print("\n🚀 Creating WebP versions for modern browsers...")
    create_webp_versions("images")
    
    print("\n✅ Image optimization complete!")
    print("\n💡 Tips for better performance:")
    print("   • Use WebP images when possible")
    print("   • Implement lazy loading for images")
    print("   • Use appropriate image sizes for different screen sizes")
    print("   • Consider using a CDN for image delivery")

if __name__ == "__main__":
    main()