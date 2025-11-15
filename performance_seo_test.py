#!/usr/bin/env python3
"""
Performance and SEO Test Suite for GitHub Homepage Enhancement
Tests page loading speed, SEO optimization, and mobile performance
"""

import os
import json
import yaml
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

class PerformanceSEOTest:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "performance_tests": {},
            "seo_tests": {},
            "mobile_tests": {},
            "summary": {}
        }
    
    def test_page_performance(self):
        """Test page performance optimization"""
        print("⚡ Testing Page Performance...")
        
        test_results = {}
        
        # Test 1: Check image optimization
        images_dir = self.base_path / "images"
        image_stats = {
            "total_images": 0,
            "optimized_formats": 0,
            "large_images": [],
            "unoptimized_images": []
        }
        
        if images_dir.exists():
            for img_file in images_dir.glob("*"):
                if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif']:
                    image_stats["total_images"] += 1
                    
                    # Check for modern formats
                    if img_file.suffix.lower() in ['.webp', '.avif']:
                        image_stats["optimized_formats"] += 1
                    
                    # Check file size (if > 500KB, consider large)
                    try:
                        file_size = img_file.stat().st_size
                        if file_size > 500 * 1024:  # 500KB
                            image_stats["large_images"].append({
                                "file": img_file.name,
                                "size_kb": round(file_size / 1024, 2)
                            })
                        
                        # Check for backup files (unoptimized)
                        if img_file.name.endswith('.backup'):
                            image_stats["unoptimized_images"].append(img_file.name)
                    
                    except Exception as e:
                        print(f"    ⚠️ Error checking {img_file.name}: {e}")
        
        test_results["image_optimization"] = {
            "stats": image_stats,
            "optimization_ratio": image_stats["optimized_formats"] / max(image_stats["total_images"], 1),
            "status": "PASS" if image_stats["optimized_formats"] > 0 else "WARN"
        }
        
        # Test 2: Check CSS/SASS optimization
        config_path = self.base_path / "_config.yml"
        css_optimization = {
            "sass_compression": False,
            "html_compression": False,
            "asset_optimization": False
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "style: compressed" in content:
                    css_optimization["sass_compression"] = True
                
                if "compress_html:" in content:
                    css_optimization["html_compression"] = True
                
                if "sass:" in content and "sourcemap: never" in content:
                    css_optimization["asset_optimization"] = True
            
            except Exception as e:
                print(f"    ⚠️ Error reading config: {e}")
        
        test_results["css_optimization"] = {
            "features": css_optimization,
            "status": "PASS" if any(css_optimization.values()) else "WARN"
        }
        
        # Test 3: Check for performance-impacting features
        performance_issues = []
        
        # Check for large CSS files
        sass_dir = self.base_path / "_sass"
        if sass_dir.exists():
            for sass_file in sass_dir.glob("*.scss"):
                try:
                    file_size = sass_file.stat().st_size
                    if file_size > 50 * 1024:  # 50KB
                        performance_issues.append(f"Large SASS file: {sass_file.name} ({round(file_size/1024, 2)}KB)")
                except Exception:
                    continue
        
        test_results["performance_issues"] = {
            "issues": performance_issues,
            "count": len(performance_issues),
            "status": "PASS" if len(performance_issues) == 0 else "WARN"
        }
        
        self.results["performance_tests"] = test_results
        
        print(f"    ✅ Image optimization: {image_stats['optimized_formats']}/{image_stats['total_images']} optimized")
        print(f"    ✅ CSS optimization: {sum(css_optimization.values())}/3 features enabled")
        print(f"    {'✅' if len(performance_issues) == 0 else '⚠️'} Performance issues: {len(performance_issues)} found")
        
        return len(performance_issues) == 0 and any(css_optimization.values())
    
    def test_seo_optimization(self):
        """Test SEO optimization features"""
        print("\n🔍 Testing SEO Optimization...")
        
        test_results = {}
        
        # Test 1: Check Jekyll SEO plugin configuration
        config_path = self.base_path / "_config.yml"
        seo_config = {
            "seo_plugin": False,
            "sitemap_plugin": False,
            "feed_plugin": False,
            "site_metadata": {}
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                plugins = config.get('plugins', [])
                
                if 'jekyll-seo-tag' in plugins:
                    seo_config["seo_plugin"] = True
                
                if 'jekyll-sitemap' in plugins:
                    seo_config["sitemap_plugin"] = True
                
                if 'jekyll-feed' in plugins:
                    seo_config["feed_plugin"] = True
                
                # Check site metadata
                metadata_fields = ['title', 'description', 'url', 'author']
                for field in metadata_fields:
                    if field in config:
                        seo_config["site_metadata"][field] = config[field]
            
            except Exception as e:
                print(f"    ⚠️ Error reading config: {e}")
        
        test_results["seo_config"] = {
            "features": seo_config,
            "metadata_completeness": len(seo_config["site_metadata"]) / 4,
            "status": "PASS" if seo_config["seo_plugin"] and len(seo_config["site_metadata"]) >= 3 else "WARN"
        }
        
        # Test 2: Check page-level SEO
        pages_dir = self.base_path / "_pages"
        page_seo_scores = {}
        
        if pages_dir.exists():
            for page_file in pages_dir.glob("*.md"):
                page_name = page_file.stem
                seo_score = {
                    "has_title": False,
                    "has_description": False,
                    "has_excerpt": False,
                    "title_length": 0,
                    "description_length": 0,
                    "has_headings": False,
                    "has_internal_links": False
                }
                
                try:
                    with open(page_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check front matter
                    if content.startswith('---'):
                        front_matter_end = content.find('---', 3)
                        if front_matter_end != -1:
                            front_matter = content[3:front_matter_end]
                            
                            # Check for SEO fields
                            if 'title:' in front_matter:
                                seo_score["has_title"] = True
                                title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', front_matter)
                                if title_match:
                                    seo_score["title_length"] = len(title_match.group(1))
                            
                            if 'description:' in front_matter or 'excerpt:' in front_matter:
                                seo_score["has_description"] = True
                                desc_match = re.search(r'(?:description|excerpt):\s*["\']?([^"\'\n]+)["\']?', front_matter)
                                if desc_match:
                                    seo_score["description_length"] = len(desc_match.group(1))
                            
                            if 'excerpt:' in front_matter:
                                seo_score["has_excerpt"] = True
                    
                    # Check content
                    content_body = content[front_matter_end + 3:] if front_matter_end != -1 else content
                    
                    # Check for headings
                    if re.search(r'^#+\s', content_body, re.MULTILINE):
                        seo_score["has_headings"] = True
                    
                    # Check for internal links
                    if re.search(r'\[.*?\]\(/.*?\)', content_body):
                        seo_score["has_internal_links"] = True
                
                except Exception as e:
                    print(f"    ⚠️ Error analyzing {page_file.name}: {e}")
                
                # Calculate SEO score (0-1)
                score_factors = [
                    seo_score["has_title"],
                    seo_score["has_description"],
                    seo_score["has_excerpt"],
                    30 <= seo_score["title_length"] <= 60,  # Optimal title length
                    120 <= seo_score["description_length"] <= 160,  # Optimal description length
                    seo_score["has_headings"],
                    seo_score["has_internal_links"]
                ]
                
                page_seo_scores[page_name] = {
                    "details": seo_score,
                    "score": sum(score_factors) / len(score_factors),
                    "status": "PASS" if sum(score_factors) >= 5 else "WARN"
                }
        
        test_results["page_seo"] = {
            "pages": page_seo_scores,
            "average_score": sum(p["score"] for p in page_seo_scores.values()) / max(len(page_seo_scores), 1),
            "status": "PASS" if all(p["status"] == "PASS" for p in page_seo_scores.values()) else "WARN"
        }
        
        # Test 3: Check for structured data
        structured_data = {
            "json_ld": False,
            "microdata": False,
            "open_graph": False,
            "twitter_cards": False
        }
        
        # Check layouts and includes for structured data
        for directory in [self.base_path / "_layouts", self.base_path / "_includes"]:
            if directory.exists():
                for html_file in directory.glob("*.html"):
                    try:
                        with open(html_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if 'application/ld+json' in content:
                            structured_data["json_ld"] = True
                        
                        if 'itemscope' in content or 'itemtype' in content:
                            structured_data["microdata"] = True
                        
                        if 'property="og:' in content:
                            structured_data["open_graph"] = True
                        
                        if 'name="twitter:' in content:
                            structured_data["twitter_cards"] = True
                    
                    except Exception:
                        continue
        
        test_results["structured_data"] = {
            "features": structured_data,
            "count": sum(structured_data.values()),
            "status": "PASS" if sum(structured_data.values()) >= 2 else "WARN"
        }
        
        self.results["seo_tests"] = test_results
        
        print(f"    ✅ SEO plugins: {sum([seo_config['seo_plugin'], seo_config['sitemap_plugin'], seo_config['feed_plugin']])}/3 enabled")
        print(f"    ✅ Page SEO average: {test_results['page_seo']['average_score']:.2f}/1.0")
        print(f"    ✅ Structured data: {sum(structured_data.values())}/4 types found")
        
        return (seo_config["seo_plugin"] and 
                test_results["page_seo"]["average_score"] > 0.7 and
                sum(structured_data.values()) >= 1)
    
    def test_mobile_performance(self):
        """Test mobile performance and user experience"""
        print("\n📱 Testing Mobile Performance...")
        
        test_results = {}
        
        # Test 1: Check responsive design implementation
        responsive_features = {
            "viewport_meta": False,
            "media_queries": 0,
            "flexible_images": False,
            "touch_friendly": False,
            "mobile_navigation": False
        }
        
        # Check for viewport meta tag
        for directory in [self.base_path / "_layouts", self.base_path / "_includes"]:
            if directory.exists():
                for html_file in directory.glob("*.html"):
                    try:
                        with open(html_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if 'name="viewport"' in content:
                            responsive_features["viewport_meta"] = True
                        
                        if 'mobile' in content.lower() or 'hamburger' in content.lower():
                            responsive_features["mobile_navigation"] = True
                    
                    except Exception:
                        continue
        
        # Check SASS files for responsive features
        sass_dir = self.base_path / "_sass"
        if sass_dir.exists():
            for sass_file in sass_dir.glob("*.scss"):
                try:
                    with open(sass_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count media queries
                    media_queries = len(re.findall(r'@media', content))
                    responsive_features["media_queries"] += media_queries
                    
                    # Check for flexible images
                    if any(prop in content for prop in ["max-width: 100%", "width: 100%", "height: auto"]):
                        responsive_features["flexible_images"] = True
                    
                    # Check for touch-friendly features
                    if any(prop in content for prop in ["touch-action", "min-height: 44px", "min-width: 44px"]):
                        responsive_features["touch_friendly"] = True
                
                except Exception:
                    continue
        
        test_results["responsive_design"] = {
            "features": responsive_features,
            "score": (
                responsive_features["viewport_meta"] +
                (responsive_features["media_queries"] > 0) +
                responsive_features["flexible_images"] +
                responsive_features["touch_friendly"] +
                responsive_features["mobile_navigation"]
            ) / 5,
            "status": "PASS" if responsive_features["viewport_meta"] and responsive_features["media_queries"] > 0 else "WARN"
        }
        
        # Test 2: Check mobile-specific optimizations
        mobile_optimizations = {
            "compressed_images": 0,
            "lazy_loading": False,
            "critical_css": False,
            "service_worker": False
        }
        
        # Check for compressed/optimized images
        images_dir = self.base_path / "images"
        if images_dir.exists():
            for img_file in images_dir.glob("*"):
                if img_file.suffix.lower() in ['.webp', '.avif']:
                    mobile_optimizations["compressed_images"] += 1
        
        # Check for lazy loading
        for directory in [self.base_path / "_layouts", self.base_path / "_includes"]:
            if directory.exists():
                for html_file in directory.glob("*.html"):
                    try:
                        with open(html_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if 'loading="lazy"' in content:
                            mobile_optimizations["lazy_loading"] = True
                    
                    except Exception:
                        continue
        
        test_results["mobile_optimizations"] = {
            "features": mobile_optimizations,
            "status": "PASS" if mobile_optimizations["compressed_images"] > 0 else "WARN"
        }
        
        self.results["mobile_tests"] = test_results
        
        print(f"    ✅ Responsive score: {test_results['responsive_design']['score']:.2f}/1.0")
        print(f"    ✅ Media queries: {responsive_features['media_queries']} found")
        print(f"    ✅ Optimized images: {mobile_optimizations['compressed_images']} found")
        
        return (test_results["responsive_design"]["score"] > 0.6 and
                mobile_optimizations["compressed_images"] > 0)
    
    def generate_performance_report(self):
        """Generate comprehensive performance and SEO report"""
        print("\n📊 Generating Performance & SEO Report...")
        
        # Calculate summary scores
        performance_score = 0
        seo_score = 0
        mobile_score = 0
        
        # Performance score
        perf_tests = self.results.get("performance_tests", {})
        if perf_tests:
            perf_factors = [
                perf_tests.get("image_optimization", {}).get("status") == "PASS",
                perf_tests.get("css_optimization", {}).get("status") == "PASS",
                perf_tests.get("performance_issues", {}).get("status") == "PASS"
            ]
            performance_score = sum(perf_factors) / len(perf_factors)
        
        # SEO score
        seo_tests = self.results.get("seo_tests", {})
        if seo_tests:
            seo_factors = [
                seo_tests.get("seo_config", {}).get("status") == "PASS",
                seo_tests.get("page_seo", {}).get("status") == "PASS",
                seo_tests.get("structured_data", {}).get("status") == "PASS"
            ]
            seo_score = sum(seo_factors) / len(seo_factors)
        
        # Mobile score
        mobile_tests = self.results.get("mobile_tests", {})
        if mobile_tests:
            mobile_factors = [
                mobile_tests.get("responsive_design", {}).get("status") == "PASS",
                mobile_tests.get("mobile_optimizations", {}).get("status") == "PASS"
            ]
            mobile_score = sum(mobile_factors) / len(mobile_factors)
        
        self.results["summary"] = {
            "performance_score": performance_score,
            "seo_score": seo_score,
            "mobile_score": mobile_score,
            "overall_score": (performance_score + seo_score + mobile_score) / 3,
            "overall_status": "PASS" if (performance_score + seo_score + mobile_score) / 3 > 0.7 else "WARN"
        }
        
        # Save report
        report_file = self.base_path / "performance_seo_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"    ✅ Performance & SEO report saved to: {report_file}")
        
        # Print summary
        print(f"\n🎯 Performance & SEO Summary:")
        print(f"  Performance Score: {performance_score:.2f}/1.0")
        print(f"  SEO Score: {seo_score:.2f}/1.0")
        print(f"  Mobile Score: {mobile_score:.2f}/1.0")
        print(f"  Overall Score: {self.results['summary']['overall_score']:.2f}/1.0")
        print(f"  Status: {self.results['summary']['overall_status']}")
        
        return self.results["summary"]["overall_status"] == "PASS"

def main():
    """Run performance and SEO tests"""
    print("🚀 Performance & SEO Test Suite")
    print("=" * 40)
    
    tester = PerformanceSEOTest()
    
    # Run all tests
    tests_passed = []
    
    tests_passed.append(tester.test_page_performance())
    tests_passed.append(tester.test_seo_optimization())
    tests_passed.append(tester.test_mobile_performance())
    
    # Generate report
    overall_success = tester.generate_performance_report()
    
    print("\n" + "=" * 40)
    if overall_success:
        print("🎉 Performance & SEO tests completed successfully!")
        return 0
    else:
        print("⚠️ Some performance/SEO issues detected. Check the report for details.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())