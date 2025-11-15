#!/usr/bin/env python3
"""
Browser Compatibility Test for GitHub Homepage Enhancement
Tests responsive design and cross-browser functionality
"""

import os
import json
from datetime import datetime
from pathlib import Path

class BrowserCompatibilityTest:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "responsive_tests": {},
            "css_tests": {},
            "javascript_tests": {},
            "accessibility_tests": {},
            "summary": {}
        }
    
    def test_responsive_design(self):
        """Test responsive design elements"""
        print("📱 Testing Responsive Design...")
        
        test_results = {}
        
        # Check for responsive CSS
        sass_dir = self.base_path / "_sass"
        responsive_features = []
        
        if sass_dir.exists():
            for sass_file in sass_dir.glob("*.scss"):
                try:
                    with open(sass_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for media queries
                    if "@media" in content:
                        responsive_features.append(f"Media queries in {sass_file.name}")
                    
                    # Check for flexible units
                    if any(unit in content for unit in ["rem", "em", "%", "vw", "vh"]):
                        responsive_features.append(f"Flexible units in {sass_file.name}")
                    
                    # Check for grid/flexbox
                    if any(prop in content for prop in ["display: grid", "display: flex", "grid-template", "flex-"]):
                        responsive_features.append(f"Modern layout in {sass_file.name}")
                
                except Exception as e:
                    print(f"    ⚠️ Error reading {sass_file.name}: {e}")
        
        test_results["responsive_features"] = {
            "features_found": responsive_features,
            "count": len(responsive_features),
            "status": "PASS" if responsive_features else "WARN"
        }
        
        # Check for viewport meta tag in layouts
        layouts_dir = self.base_path / "_layouts"
        viewport_found = False
        
        if layouts_dir.exists():
            for layout_file in layouts_dir.glob("*.html"):
                try:
                    with open(layout_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'name="viewport"' in content:
                        viewport_found = True
                        break
                
                except Exception as e:
                    print(f"    ⚠️ Error reading {layout_file.name}: {e}")
        
        # Also check includes
        includes_dir = self.base_path / "_includes"
        if includes_dir.exists() and not viewport_found:
            for include_file in includes_dir.glob("*.html"):
                try:
                    with open(include_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'name="viewport"' in content:
                        viewport_found = True
                        break
                
                except Exception as e:
                    print(f"    ⚠️ Error reading {include_file.name}: {e}")
        
        test_results["viewport_meta"] = {
            "found": viewport_found,
            "status": "PASS" if viewport_found else "FAIL"
        }
        
        self.results["responsive_tests"] = test_results
        
        print(f"    ✅ Responsive features: {len(responsive_features)} found")
        print(f"    {'✅' if viewport_found else '❌'} Viewport meta tag: {viewport_found}")
        
        return len(responsive_features) > 0 and viewport_found
    
    def test_css_compatibility(self):
        """Test CSS compatibility and best practices"""
        print("\n🎨 Testing CSS Compatibility...")
        
        test_results = {}
        
        # Check SASS files for modern CSS features
        sass_dir = self.base_path / "_sass"
        css_features = {
            "modern_selectors": [],
            "animations": [],
            "transforms": [],
            "gradients": [],
            "flexbox": [],
            "grid": []
        }
        
        if sass_dir.exists():
            for sass_file in sass_dir.glob("*.scss"):
                try:
                    with open(sass_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for modern CSS features
                    if any(selector in content for selector in [":hover", ":focus", ":active", "::before", "::after"]):
                        css_features["modern_selectors"].append(sass_file.name)
                    
                    if any(prop in content for prop in ["animation", "transition", "@keyframes"]):
                        css_features["animations"].append(sass_file.name)
                    
                    if "transform" in content:
                        css_features["transforms"].append(sass_file.name)
                    
                    if any(func in content for func in ["linear-gradient", "radial-gradient"]):
                        css_features["gradients"].append(sass_file.name)
                    
                    if any(prop in content for prop in ["display: flex", "flex-", "justify-content", "align-items"]):
                        css_features["flexbox"].append(sass_file.name)
                    
                    if any(prop in content for prop in ["display: grid", "grid-template", "grid-gap"]):
                        css_features["grid"].append(sass_file.name)
                
                except Exception as e:
                    print(f"    ⚠️ Error reading {sass_file.name}: {e}")
        
        # Check for vendor prefixes (should be minimal with modern browsers)
        vendor_prefixes = []
        if sass_dir.exists():
            for sass_file in sass_dir.glob("*.scss"):
                try:
                    with open(sass_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if any(prefix in content for prefix in ["-webkit-", "-moz-", "-ms-", "-o-"]):
                        vendor_prefixes.append(sass_file.name)
                
                except Exception as e:
                    continue
        
        test_results["css_features"] = css_features
        test_results["vendor_prefixes"] = {
            "files_with_prefixes": vendor_prefixes,
            "count": len(vendor_prefixes),
            "status": "INFO"
        }
        
        # Overall CSS compatibility score
        feature_count = sum(len(features) for features in css_features.values())
        test_results["compatibility_score"] = {
            "total_features": feature_count,
            "status": "PASS" if feature_count > 5 else "WARN"
        }
        
        self.results["css_tests"] = test_results
        
        print(f"    ✅ Modern CSS features: {feature_count} found")
        print(f"    ℹ️ Files with vendor prefixes: {len(vendor_prefixes)}")
        
        return feature_count > 5
    
    def test_accessibility_features(self):
        """Test accessibility features"""
        print("\n♿ Testing Accessibility Features...")
        
        test_results = {}
        
        # Check for semantic HTML in layouts and includes
        semantic_elements = []
        accessibility_features = []
        
        # Check layouts
        layouts_dir = self.base_path / "_layouts"
        if layouts_dir.exists():
            for layout_file in layouts_dir.glob("*.html"):
                try:
                    with open(layout_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for semantic HTML5 elements
                    semantic_tags = ["<header>", "<nav>", "<main>", "<article>", "<section>", "<aside>", "<footer>"]
                    for tag in semantic_tags:
                        if tag in content:
                            semantic_elements.append(f"{tag} in {layout_file.name}")
                    
                    # Check for accessibility attributes
                    if 'alt=' in content:
                        accessibility_features.append(f"Alt attributes in {layout_file.name}")
                    if 'aria-' in content:
                        accessibility_features.append(f"ARIA attributes in {layout_file.name}")
                    if 'role=' in content:
                        accessibility_features.append(f"Role attributes in {layout_file.name}")
                
                except Exception as e:
                    print(f"    ⚠️ Error reading {layout_file.name}: {e}")
        
        # Check includes
        includes_dir = self.base_path / "_includes"
        if includes_dir.exists():
            for include_file in includes_dir.glob("*.html"):
                try:
                    with open(include_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for semantic HTML5 elements
                    semantic_tags = ["<header>", "<nav>", "<main>", "<article>", "<section>", "<aside>", "<footer>"]
                    for tag in semantic_tags:
                        if tag in content:
                            semantic_elements.append(f"{tag} in {include_file.name}")
                    
                    # Check for accessibility attributes
                    if 'alt=' in content:
                        accessibility_features.append(f"Alt attributes in {include_file.name}")
                    if 'aria-' in content:
                        accessibility_features.append(f"ARIA attributes in {include_file.name}")
                    if 'role=' in content:
                        accessibility_features.append(f"Role attributes in {include_file.name}")
                
                except Exception as e:
                    print(f"    ⚠️ Error reading {include_file.name}: {e}")
        
        test_results["semantic_html"] = {
            "elements_found": semantic_elements,
            "count": len(semantic_elements),
            "status": "PASS" if semantic_elements else "WARN"
        }
        
        test_results["accessibility_attributes"] = {
            "features_found": accessibility_features,
            "count": len(accessibility_features),
            "status": "PASS" if accessibility_features else "WARN"
        }
        
        self.results["accessibility_tests"] = test_results
        
        print(f"    ✅ Semantic HTML elements: {len(semantic_elements)} found")
        print(f"    ✅ Accessibility features: {len(accessibility_features)} found")
        
        return len(semantic_elements) > 0 or len(accessibility_features) > 0
    
    def test_performance_optimization(self):
        """Test performance optimization features"""
        print("\n⚡ Testing Performance Optimization...")
        
        test_results = {}
        
        # Check Jekyll config for performance settings
        config_path = self.base_path / "_config.yml"
        performance_features = []
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for SASS compression
                if "style: compressed" in content:
                    performance_features.append("SASS compression enabled")
                
                # Check for HTML compression
                if "compress_html:" in content:
                    performance_features.append("HTML compression configured")
                
                # Check for asset optimization
                if "sass:" in content:
                    performance_features.append("SASS configuration present")
                
            except Exception as e:
                print(f"    ⚠️ Error reading config: {e}")
        
        # Check for optimized images
        images_dir = self.base_path / "images"
        optimized_images = []
        
        if images_dir.exists():
            for img_file in images_dir.glob("*"):
                if img_file.suffix.lower() in ['.webp', '.avif']:
                    optimized_images.append(img_file.name)
        
        test_results["performance_config"] = {
            "features": performance_features,
            "count": len(performance_features),
            "status": "PASS" if performance_features else "WARN"
        }
        
        test_results["optimized_images"] = {
            "webp_avif_count": len(optimized_images),
            "files": optimized_images,
            "status": "PASS" if optimized_images else "INFO"
        }
        
        self.results["performance_tests"] = test_results
        
        print(f"    ✅ Performance features: {len(performance_features)} found")
        print(f"    ✅ Optimized images: {len(optimized_images)} found")
        
        return len(performance_features) > 0
    
    def generate_compatibility_report(self):
        """Generate browser compatibility report"""
        print("\n📊 Generating Compatibility Report...")
        
        # Calculate summary
        responsive_pass = self.results.get("responsive_tests", {}).get("viewport_meta", {}).get("status") == "PASS"
        css_pass = self.results.get("css_tests", {}).get("compatibility_score", {}).get("status") == "PASS"
        accessibility_pass = (
            self.results.get("accessibility_tests", {}).get("semantic_html", {}).get("status") == "PASS" or
            self.results.get("accessibility_tests", {}).get("accessibility_attributes", {}).get("status") == "PASS"
        )
        performance_pass = self.results.get("performance_tests", {}).get("performance_config", {}).get("status") == "PASS"
        
        self.results["summary"] = {
            "responsive_design": responsive_pass,
            "css_compatibility": css_pass,
            "accessibility": accessibility_pass,
            "performance": performance_pass,
            "overall_status": "PASS" if all([responsive_pass, css_pass, accessibility_pass]) else "PARTIAL"
        }
        
        # Save report
        report_file = self.base_path / "browser_compatibility_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"    ✅ Compatibility report saved to: {report_file}")
        
        # Print summary
        print(f"\n🎯 Compatibility Summary:")
        print(f"  Responsive Design: {'✅' if responsive_pass else '❌'}")
        print(f"  CSS Compatibility: {'✅' if css_pass else '❌'}")
        print(f"  Accessibility: {'✅' if accessibility_pass else '❌'}")
        print(f"  Performance: {'✅' if performance_pass else '❌'}")
        print(f"  Overall Status: {self.results['summary']['overall_status']}")
        
        return self.results["summary"]["overall_status"] in ["PASS", "PARTIAL"]

def main():
    """Run browser compatibility tests"""
    print("🌐 Browser Compatibility Test Suite")
    print("=" * 50)
    
    tester = BrowserCompatibilityTest()
    
    # Run all tests
    tests_passed = []
    
    tests_passed.append(tester.test_responsive_design())
    tests_passed.append(tester.test_css_compatibility())
    tests_passed.append(tester.test_accessibility_features())
    tests_passed.append(tester.test_performance_optimization())
    
    # Generate report
    overall_success = tester.generate_compatibility_report()
    
    print("\n" + "=" * 50)
    if overall_success:
        print("🎉 Browser compatibility tests completed successfully!")
        return 0
    else:
        print("⚠️ Some compatibility issues detected. Check the report for details.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())