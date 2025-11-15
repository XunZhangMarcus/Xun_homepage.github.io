#!/usr/bin/env python3
"""
Navigation Link Verification Script
Verifies that all navigation links have corresponding pages with correct permalinks
"""

import os
import yaml
import re
from pathlib import Path

def extract_permalink_from_file(file_path):
    """Extract permalink from a markdown file's front matter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                front_matter = parts[1]
                try:
                    data = yaml.safe_load(front_matter)
                    return data.get('permalink', None)
                except yaml.YAMLError:
                    return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def verify_navigation():
    """Verify all navigation links have corresponding pages"""
    print("🔍 Verifying Navigation Links...")
    print("=" * 50)
    
    # Read navigation configuration
    nav_file = '_data/navigation.yml'
    if not os.path.exists(nav_file):
        print(f"❌ Navigation file {nav_file} not found!")
        return False
    
    with open(nav_file, 'r', encoding='utf-8') as f:
        nav_data = yaml.safe_load(f)
    
    main_nav = nav_data.get('main', [])
    all_valid = True
    
    print(f"Found {len(main_nav)} navigation items to verify:\n")
    
    for i, item in enumerate(main_nav, 1):
        title = item.get('title', 'Unknown')
        url = item.get('url', '')
        
        print(f"{i}. {title}")
        print(f"   URL: {url}")
        
        # Check if this is the home page
        if url == '/':
            # Home page should be _pages/about.md with permalink: /
            page_file = '_pages/about.md'
            if os.path.exists(page_file):
                permalink = extract_permalink_from_file(page_file)
                if permalink == '/':
                    print(f"   ✅ VALID - Found {page_file} with correct permalink")
                else:
                    print(f"   ❌ INVALID - {page_file} has permalink '{permalink}', expected '/'")
                    all_valid = False
            else:
                print(f"   ❌ INVALID - {page_file} not found")
                all_valid = False
        else:
            # For other pages, find corresponding file
            expected_permalink = url
            found_file = None
            found_permalink = None
            
            # Check all files in _pages directory
            pages_dir = '_pages'
            if os.path.exists(pages_dir):
                for filename in os.listdir(pages_dir):
                    if filename.endswith('.md'):
                        file_path = os.path.join(pages_dir, filename)
                        permalink = extract_permalink_from_file(file_path)
                        if permalink == expected_permalink:
                            found_file = file_path
                            found_permalink = permalink
                            break
            
            if found_file:
                print(f"   ✅ VALID - Found {found_file} with correct permalink")
            else:
                print(f"   ❌ INVALID - No page found with permalink '{expected_permalink}'")
                all_valid = False
        
        print()
    
    print("=" * 50)
    if all_valid:
        print("🎉 All navigation links are valid!")
        return True
    else:
        print("❌ Some navigation links have issues!")
        return False

def list_all_pages():
    """List all pages and their permalinks for reference"""
    print("\n📄 All Pages and Their Permalinks:")
    print("=" * 50)
    
    pages_dir = '_pages'
    if os.path.exists(pages_dir):
        for filename in sorted(os.listdir(pages_dir)):
            if filename.endswith('.md'):
                file_path = os.path.join(pages_dir, filename)
                permalink = extract_permalink_from_file(file_path)
                print(f"{filename:<20} → {permalink}")

if __name__ == "__main__":
    success = verify_navigation()
    list_all_pages()
    
    if success:
        print("\n✅ Navigation verification completed successfully!")
        exit(0)
    else:
        print("\n❌ Navigation verification failed!")
        exit(1)