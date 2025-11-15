#!/usr/bin/env python3
"""
Performance optimization script for GitHub Pages.
This script analyzes and optimizes various aspects of the site for better performance.
"""

import os
import re
import gzip
import json
from pathlib import Path

def analyze_css_performance():
    """Analyze CSS files for performance issues."""
    print("🎨 Analyzing CSS Performance...")
    print("-" * 40)
    
    css_files = []
    for root, dirs, files in os.walk("_sass"):
        for file in files:
            if file.endswith('.scss'):
                css_files.append(os.path.join(root, file))
    
    # Add main CSS file
    if os.path.exists("assets/css/main.scss"):
        css_files.append("assets/css/main.scss")
    
    total_size = 0
    issues = []
    
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                file_size = len(content.encode('utf-8'))
                total_size += file_size
                
                # Check for performance issues
                if '!important' in content:
                    important_count = content.count('!important')
                    if important_count > 5:
                        issues.append(f"⚠️  {css_file}: {important_count} !important declarations (consider refactoring)")
                
                # Check for unused vendor prefixes
                old_prefixes = ['-moz-border-radius', '-webkit-border-radius', '-ms-filter']
                for prefix in old_prefixes:
                    if prefix in content:
                        issues.append(f"⚠️  {css_file}: Contains outdated prefix '{prefix}'")
                
                print(f"✓ {css_file}: {file_size//1024}KB")
                
        except Exception as e:
            print(f"✗ Error reading {css_file}: {str(e)}")
    
    print(f"\nTotal CSS size: {total_size//1024}KB")
    
    if issues:
        print("\n🔍 Performance Issues Found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ No major CSS performance issues found!")

def analyze_html_structure():
    """Analyze HTML structure for performance."""
    print("\n🏗️  Analyzing HTML Structure...")
    print("-" * 40)
    
    layout_files = []
    include_files = []
    
    # Find layout files
    if os.path.exists("_layouts"):
        for file in os.listdir("_layouts"):
            if file.endswith('.html'):
                layout_files.append(os.path.join("_layouts", file))
    
    # Find include files
    if os.path.exists("_includes"):
        for file in os.listdir("_includes"):
            if file.endswith('.html'):
                include_files.append(os.path.join("_includes", file))
    
    issues = []
    
    for html_file in layout_files + include_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for performance issues
                if 'document.write' in content:
                    issues.append(f"⚠️  {html_file}: Uses document.write (blocks parsing)")
                
                # Check for inline styles
                inline_styles = re.findall(r'style="[^"]*"', content)
                if len(inline_styles) > 3:
                    issues.append(f"⚠️  {html_file}: {len(inline_styles)} inline styles (consider moving to CSS)")
                
                # Check for missing alt attributes
                img_tags = re.findall(r'<img[^>]*>', content)
                for img in img_tags:
                    if 'alt=' not in img:
                        issues.append(f"⚠️  {html_file}: Image without alt attribute")
                        break
                
                print(f"✓ {html_file}: {len(content.encode('utf-8'))//1024}KB")
                
        except Exception as e:
            print(f"✗ Error reading {html_file}: {str(e)}")
    
    if issues:
        print("\n🔍 HTML Performance Issues Found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ No major HTML performance issues found!")

def check_image_optimization():
    """Check image optimization status."""
    print("\n🖼️  Checking Image Optimization...")
    print("-" * 40)
    
    if not os.path.exists("images"):
        print("No images directory found.")
        return
    
    image_files = []
    large_images = []
    unoptimized_images = []
    
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    
    for root, dirs, files in os.walk("images"):
        for file in files:
            if file.lower().endswith(supported_formats):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                image_files.append((file_path, file_size))
                
                # Check for large images
                if file_size > 500000:  # 500KB
                    large_images.append((file_path, file_size))
                
                # Check for unoptimized images
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    webp_path = os.path.splitext(file_path)[0] + '.webp'
                    if not os.path.exists(webp_path):
                        unoptimized_images.append(file_path)
    
    total_size = sum(size for _, size in image_files)
    print(f"Found {len(image_files)} images, total size: {total_size//1024}KB")
    
    if large_images:
        print(f"\n⚠️  Large images found ({len(large_images)}):")
        for img_path, size in large_images[:5]:  # Show first 5
            print(f"  • {os.path.basename(img_path)}: {size//1024}KB")
        if len(large_images) > 5:
            print(f"  ... and {len(large_images) - 5} more")
    
    if unoptimized_images:
        print(f"\n💡 Consider creating WebP versions for {len(unoptimized_images)} images")
    
    if not large_images and not unoptimized_images:
        print("\n✅ Images appear to be well optimized!")

def generate_performance_report():
    """Generate a comprehensive performance report."""
    print("\n📊 Generating Performance Report...")
    print("-" * 40)
    
    report = {
        "timestamp": "2024-11-15",
        "optimizations_applied": [
            "CSS compression enabled",
            "HTML compression enabled",
            "SASS compression enabled",
            "Enhanced typography and spacing",
            "Responsive design improvements",
            "Hardware acceleration for animations",
            "Optimized image loading",
            "Performance-focused CSS enhancements"
        ],
        "recommendations": [
            "Run image optimization script regularly",
            "Monitor Core Web Vitals",
            "Consider implementing service worker for caching",
            "Use WebP images for modern browsers",
            "Implement lazy loading for images",
            "Consider using a CDN for static assets"
        ]
    }
    
    # Save report
    with open("performance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Performance report saved to performance_report.json")
    
    # Display summary
    print(f"\n📈 Performance Optimizations Applied:")
    for opt in report["optimizations_applied"]:
        print(f"  ✓ {opt}")
    
    print(f"\n💡 Additional Recommendations:")
    for rec in report["recommendations"]:
        print(f"  • {rec}")

def create_htaccess_for_caching():
    """Create .htaccess file for better caching (if not using GitHub Pages)."""
    htaccess_content = """# Performance optimizations
<IfModule mod_expires.c>
    ExpiresActive on
    
    # Images
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/webp "access plus 1 month"
    ExpiresByType image/svg+xml "access plus 1 month"
    
    # CSS and JavaScript
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType text/javascript "access plus 1 month"
    
    # Fonts
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType application/font-woff "access plus 1 year"
    ExpiresByType application/font-woff2 "access plus 1 year"
    
    # HTML
    ExpiresByType text/html "access plus 1 hour"
</IfModule>

# Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
"""
    
    print("\n⚙️  Creating .htaccess for caching (for non-GitHub Pages hosting)...")
    with open(".htaccess", "w") as f:
        f.write(htaccess_content)
    print("✓ .htaccess file created")

def main():
    """Main function to run performance analysis and optimization."""
    print("🚀 GitHub Pages Performance Optimizer")
    print("=" * 50)
    
    # Run analyses
    analyze_css_performance()
    analyze_html_structure()
    check_image_optimization()
    
    # Generate report
    generate_performance_report()
    
    # Create additional optimization files
    create_htaccess_for_caching()
    
    print("\n" + "=" * 50)
    print("✅ Performance analysis complete!")
    print("\n🎯 Next steps:")
    print("   1. Run 'python optimize_images.py' to optimize images")
    print("   2. Test your site with Google PageSpeed Insights")
    print("   3. Monitor Core Web Vitals in Google Search Console")
    print("   4. Consider implementing lazy loading for images")

if __name__ == "__main__":
    main()