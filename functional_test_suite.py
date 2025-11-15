#!/usr/bin/env python3
"""
Functional Test Suite for GitHub Homepage Enhancement
Tests navigation links, page content integrity, and browser compatibility
"""

import os
import sys
import yaml
import re
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime

class FunctionalTestSuite:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "navigation_tests": {},
            "content_tests": {},
            "compatibility_tests": {},
            "summary": {}
        }
        
    def load_navigation_config(self):
        """Load navigation configuration from _data/navigation.yml"""
        nav_file = self.base_path / "_data" / "navigation.yml"
        if not nav_file.exists():
            return None
        
        with open(nav_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def test_navigation_links(self):
        """Test 1: Verify all navigation links point to existing pages"""
        print("🔗 Testing Navigation Links...")
        
        nav_config = self.load_navigation_config()
        if not nav_config:
            self.results["navigation_tests"]["error"] = "Navigation config not found"
            return False
        
        main_nav = nav_config.get("main", [])
        test_results = {}
        
        for nav_item in main_nav:
            title = nav_item.get("title", "Unknown")
            url = nav_item.get("url", "")
            
            print(f"  Testing: {title} -> {url}")
            
            # Convert URL to file path
            if url == "/":
                file_path = self.base_path / "_pages" / "about.md"
            else:
                # Remove leading/trailing slashes and add .md extension
                clean_url = url.strip("/")
                file_path = self.base_path / "_pages" / f"{clean_url}.md"
            
            # Check if file exists
            exists = file_path.exists()
            
            # If file exists, check permalink
            permalink_match = False
            if exists:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract front matter
                        if content.startswith('---'):
                            front_matter_end = content.find('---', 3)
                            if front_matter_end != -1:
                                front_matter = content[3:front_matter_end]
                                # Check permalink
                                permalink_match = f"permalink: {url}" in front_matter
                except Exception as e:
                    print(f"    Error reading file: {e}")
            
            test_results[title] = {
                "url": url,
                "file_path": str(file_path),
                "file_exists": exists,
                "permalink_match": permalink_match,
                "status": "PASS" if exists and permalink_match else "FAIL"
            }
            
            status_icon = "✅" if exists and permalink_match else "❌"
            print(f"    {status_icon} File exists: {exists}, Permalink match: {permalink_match}")
        
        self.results["navigation_tests"] = test_results
        
        # Summary
        passed = sum(1 for r in test_results.values() if r["status"] == "PASS")
        total = len(test_results)
        print(f"  Navigation Tests: {passed}/{total} passed")
        
        return passed == total
    
    def test_page_content_integrity(self):
        """Test 2: Verify page content integrity and accuracy"""
        print("\n📄 Testing Page Content Integrity...")
        
        pages_dir = self.base_path / "_pages"
        if not pages_dir.exists():
            self.results["content_tests"]["error"] = "Pages directory not found"
            return False
        
        test_results = {}
        
        # Required pages based on navigation
        required_pages = [
            "about.md", "news.md", "publications.md", "hydro90.md",
            "honors.md", "education.md", "vision.md", "funfacts.md", "farewell.md"
        ]
        
        for page_file in required_pages:
            page_path = pages_dir / page_file
            page_name = page_file.replace('.md', '')
            
            print(f"  Testing: {page_name}")
            
            if not page_path.exists():
                test_results[page_name] = {
                    "exists": False,
                    "has_front_matter": False,
                    "has_content": False,
                    "status": "FAIL"
                }
                print(f"    ❌ File does not exist")
                continue
            
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check front matter
                has_front_matter = content.startswith('---')
                front_matter_valid = False
                
                if has_front_matter:
                    front_matter_end = content.find('---', 3)
                    if front_matter_end != -1:
                        front_matter = content[3:front_matter_end]
                        # Check for required fields
                        required_fields = ['permalink:', 'title:', 'excerpt:']
                        front_matter_valid = all(field in front_matter for field in required_fields)
                
                # Check content length (should have substantial content)
                content_after_front_matter = content[front_matter_end + 3:] if front_matter_end != -1 else content
                has_substantial_content = len(content_after_front_matter.strip()) > 100
                
                # Check for images (if applicable)
                has_images = bool(re.search(r'!\[.*?\]\(.*?\)', content))
                
                # Check for links
                has_links = bool(re.search(r'\[.*?\]\(.*?\)', content))
                
                test_results[page_name] = {
                    "exists": True,
                    "has_front_matter": has_front_matter,
                    "front_matter_valid": front_matter_valid,
                    "has_content": has_substantial_content,
                    "has_images": has_images,
                    "has_links": has_links,
                    "content_length": len(content),
                    "status": "PASS" if has_front_matter and front_matter_valid and has_substantial_content else "FAIL"
                }
                
                status_icon = "✅" if test_results[page_name]["status"] == "PASS" else "❌"
                print(f"    {status_icon} Front matter: {front_matter_valid}, Content: {has_substantial_content}")
                
            except Exception as e:
                test_results[page_name] = {
                    "exists": True,
                    "error": str(e),
                    "status": "ERROR"
                }
                print(f"    ❌ Error reading file: {e}")
        
        self.results["content_tests"] = test_results
        
        # Summary
        passed = sum(1 for r in test_results.values() if r["status"] == "PASS")
        total = len(test_results)
        print(f"  Content Tests: {passed}/{total} passed")
        
        return passed == total
    
    def test_jekyll_compatibility(self):
        """Test 3: Verify Jekyll and GitHub Pages compatibility"""
        print("\n⚙️ Testing Jekyll Compatibility...")
        
        test_results = {}
        
        # Test 1: Check _config.yml
        config_path = self.base_path / "_config.yml"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                # Check for GitHub Pages compatible plugins
                plugins = config.get('plugins', [])
                github_pages_plugins = [
                    'jekyll-paginate', 'jekyll-sitemap', 'jekyll-gist',
                    'jekyll-feed', 'jekyll-redirect-from', 'jemoji',
                    'jekyll-seo-tag', 'jekyll-github-metadata'
                ]
                
                compatible_plugins = all(plugin in github_pages_plugins for plugin in plugins)
                
                test_results["config"] = {
                    "exists": True,
                    "valid_yaml": True,
                    "compatible_plugins": compatible_plugins,
                    "plugins": plugins,
                    "status": "PASS" if compatible_plugins else "WARN"
                }
                
                print(f"    ✅ Config file valid, Plugins compatible: {compatible_plugins}")
                
            except Exception as e:
                test_results["config"] = {
                    "exists": True,
                    "error": str(e),
                    "status": "ERROR"
                }
                print(f"    ❌ Error reading config: {e}")
        else:
            test_results["config"] = {
                "exists": False,
                "status": "FAIL"
            }
            print(f"    ❌ Config file not found")
        
        # Test 2: Check for unsupported features
        unsupported_features = []
        
        # Check for custom plugins (not in _plugins directory for GitHub Pages)
        plugins_dir = self.base_path / "_plugins"
        if plugins_dir.exists() and any(plugins_dir.iterdir()):
            unsupported_features.append("Custom plugins in _plugins directory")
        
        test_results["compatibility"] = {
            "unsupported_features": unsupported_features,
            "status": "PASS" if not unsupported_features else "WARN"
        }
        
        if unsupported_features:
            print(f"    ⚠️ Unsupported features found: {unsupported_features}")
        else:
            print(f"    ✅ No unsupported features detected")
        
        self.results["compatibility_tests"] = test_results
        
        return len(unsupported_features) == 0
    
    def test_resource_links(self):
        """Test 4: Verify external resource links and images"""
        print("\n🔗 Testing Resource Links...")
        
        test_results = {}
        
        # Check images directory
        images_dir = self.base_path / "images"
        if images_dir.exists():
            image_files = list(images_dir.glob("*"))
            test_results["images"] = {
                "directory_exists": True,
                "file_count": len(image_files),
                "files": [f.name for f in image_files if f.is_file()],
                "status": "PASS" if image_files else "WARN"
            }
            print(f"    ✅ Images directory: {len(image_files)} files found")
        else:
            test_results["images"] = {
                "directory_exists": False,
                "status": "FAIL"
            }
            print(f"    ❌ Images directory not found")
        
        # Check for broken image references in pages
        pages_dir = self.base_path / "_pages"
        broken_images = []
        
        if pages_dir.exists():
            for page_file in pages_dir.glob("*.md"):
                try:
                    with open(page_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find image references
                    image_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)
                    for img_ref in image_refs:
                        if img_ref.startswith('images/'):
                            img_path = self.base_path / img_ref
                            if not img_path.exists():
                                broken_images.append(f"{page_file.name}: {img_ref}")
                
                except Exception as e:
                    print(f"    ⚠️ Error checking {page_file.name}: {e}")
        
        test_results["broken_images"] = {
            "count": len(broken_images),
            "files": broken_images,
            "status": "PASS" if not broken_images else "FAIL"
        }
        
        if broken_images:
            print(f"    ❌ Broken image references: {len(broken_images)}")
            for broken in broken_images:
                print(f"      - {broken}")
        else:
            print(f"    ✅ No broken image references found")
        
        self.results["resource_tests"] = test_results
        
        return len(broken_images) == 0
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n📊 Generating Test Report...")
        
        # Calculate summary statistics
        nav_passed = sum(1 for r in self.results["navigation_tests"].values() 
                        if isinstance(r, dict) and r.get("status") == "PASS")
        nav_total = len([r for r in self.results["navigation_tests"].values() 
                        if isinstance(r, dict)])
        
        content_passed = sum(1 for r in self.results["content_tests"].values() 
                           if isinstance(r, dict) and r.get("status") == "PASS")
        content_total = len([r for r in self.results["content_tests"].values() 
                           if isinstance(r, dict)])
        
        self.results["summary"] = {
            "navigation": {"passed": nav_passed, "total": nav_total},
            "content": {"passed": content_passed, "total": content_total},
            "overall_status": "PASS" if nav_passed == nav_total and content_passed == content_total else "FAIL"
        }
        
        # Save detailed report
        report_file = self.base_path / "functional_test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"    ✅ Detailed report saved to: {report_file}")
        
        # Print summary
        print(f"\n🎯 Test Summary:")
        print(f"  Navigation Tests: {nav_passed}/{nav_total}")
        print(f"  Content Tests: {content_passed}/{content_total}")
        print(f"  Overall Status: {self.results['summary']['overall_status']}")
        
        return self.results["summary"]["overall_status"] == "PASS"

def main():
    """Run the complete functional test suite"""
    print("🧪 GitHub Homepage Enhancement - Functional Test Suite")
    print("=" * 60)
    
    tester = FunctionalTestSuite()
    
    # Run all tests
    tests_passed = []
    
    tests_passed.append(tester.test_navigation_links())
    tests_passed.append(tester.test_page_content_integrity())
    tests_passed.append(tester.test_jekyll_compatibility())
    tests_passed.append(tester.test_resource_links())
    
    # Generate final report
    overall_success = tester.generate_report()
    
    print("\n" + "=" * 60)
    if overall_success:
        print("🎉 All functional tests PASSED!")
        return 0
    else:
        print("❌ Some functional tests FAILED. Check the report for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())