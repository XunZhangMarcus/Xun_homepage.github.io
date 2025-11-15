#!/usr/bin/env python3
"""
Resource Path Validation Script
Validates that all referenced images, CSS, and JS files exist
"""

import os
import re
import yaml
from pathlib import Path

def validate_config_resources():
    """Validate resources referenced in _config.yml"""
    issues = []
    
    if not os.path.exists('_config.yml'):
        return ["ERROR: _config.yml not found"]
    
    with open('_config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Check avatar image
    if 'author' in config and 'avatar' in config['author']:
        avatar_path = config['author']['avatar']
        if not os.path.exists(avatar_path):
            issues.append(f"ERROR: Avatar image not found: {avatar_path}")
        else:
            print(f"✅ Avatar image found: {avatar_path}")
    
    return issues

def validate_css_resources():
    """Validate CSS file references"""
    issues = []
    
    # Check main CSS file reference in head.html
    head_file = '_includes/head.html'
    if os.path.exists(head_file):
        with open(head_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for CSS references
        css_refs = re.findall(r'href="([^"]*\.css)"', content)
        for css_ref in css_refs:
            # For Jekyll, main.css is compiled from main.scss
            if css_ref == 'assets/css/main.css':
                scss_path = 'assets/css/main.scss'
                if os.path.exists(scss_path):
                    print(f"✅ SCSS source found: {scss_path}")
                else:
                    issues.append(f"ERROR: SCSS source not found: {scss_path}")
            elif not os.path.exists(css_ref):
                issues.append(f"ERROR: CSS file not found: {css_ref}")
            else:
                print(f"✅ CSS file found: {css_ref}")
    
    return issues

def validate_js_resources():
    """Validate JavaScript file references"""
    issues = []
    
    # Check main JS file reference in scripts.html
    scripts_file = '_includes/scripts.html'
    if os.path.exists(scripts_file):
        with open(scripts_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for JS references
        js_refs = re.findall(r'src="([^"]*\.js)"', content)
        for js_ref in js_refs:
            if not os.path.exists(js_ref):
                issues.append(f"ERROR: JavaScript file not found: {js_ref}")
            else:
                print(f"✅ JavaScript file found: {js_ref}")
    
    return issues

def validate_image_references():
    """Validate image references in markdown files"""
    issues = []
    
    # Check images in pages
    pages_dir = Path('_pages')
    if pages_dir.exists():
        for page_file in pages_dir.glob('*.md'):
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for image references
            img_refs = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
            img_refs.extend(re.findall(r'<img[^>]+src="([^"]+)"', content))
            
            for img_ref in img_refs:
                # Skip external URLs
                if img_ref.startswith('http'):
                    continue
                    
                if not os.path.exists(img_ref):
                    issues.append(f"ERROR: Image not found in {page_file}: {img_ref}")
                else:
                    print(f"✅ Image found: {img_ref}")
    
    return issues

def validate_font_resources():
    """Check for font resources"""
    issues = []
    
    # Check if Font Awesome is properly configured
    fa_scss = Path('_sass/vendor/font-awesome')
    if fa_scss.exists():
        print("✅ Font Awesome SCSS files found")
    else:
        issues.append("WARNING: Font Awesome SCSS files not found")
    
    return issues

def main():
    """Run all resource validations"""
    print("Resource Path Validation")
    print("=" * 40)
    
    all_issues = []
    
    print("\n1. Validating _config.yml resources...")
    config_issues = validate_config_resources()
    all_issues.extend(config_issues)
    
    print("\n2. Validating CSS resources...")
    css_issues = validate_css_resources()
    all_issues.extend(css_issues)
    
    print("\n3. Validating JavaScript resources...")
    js_issues = validate_js_resources()
    all_issues.extend(js_issues)
    
    print("\n4. Validating image references...")
    img_issues = validate_image_references()
    all_issues.extend(img_issues)
    
    print("\n5. Validating font resources...")
    font_issues = validate_font_resources()
    all_issues.extend(font_issues)
    
    print("\n" + "=" * 40)
    print("RESULTS:")
    
    if not all_issues:
        print("✅ All resource paths are valid!")
    else:
        errors = [issue for issue in all_issues if issue.startswith('ERROR')]
        warnings = [issue for issue in all_issues if issue.startswith('WARNING')]
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for error in errors:
                print(f"  {error}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"  {warning}")
    
    print(f"\nTotal issues found: {len(all_issues)}")
    return len([issue for issue in all_issues if issue.startswith('ERROR')])

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)