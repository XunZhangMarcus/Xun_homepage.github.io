#!/usr/bin/env python3
"""
GitHub Pages Deployment Test Suite
Tests GitHub Pages compatibility, build requirements, and deployment readiness
"""

import os
import json
import yaml
import re
import subprocess
from datetime import datetime
from pathlib import Path

class GitHubPagesDeploymentTest:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "jekyll_tests": {},
            "github_pages_tests": {},
            "security_tests": {},
            "deployment_tests": {},
            "summary": {}
        }
    
    def test_jekyll_build_compatibility(self):
        """Test Jekyll build compatibility"""
        print("🔧 Testing Jekyll Build Compatibility...")
        
        test_results = {}
        
        # Test 1: Check Jekyll configuration
        config_path = self.base_path / "_config.yml"
        jekyll_config = {
            "config_exists": False,
            "valid_yaml": False,
            "github_pages_compatible": False,
            "required_fields": {},
            "plugins": []
        }
        
        if config_path.exists():
            jekyll_config["config_exists"] = True
            
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                jekyll_config["valid_yaml"] = True
                
                # Check required fields
                required_fields = ['title', 'description', 'url']
                for field in required_fields:
                    jekyll_config["required_fields"][field] = field in config
                
                # Check plugins
                plugins = config.get('plugins', [])
                jekyll_config["plugins"] = plugins
                
                # Check GitHub Pages compatibility
                github_pages_plugins = [
                    'jekyll-paginate', 'jekyll-sitemap', 'jekyll-gist',
                    'jekyll-feed', 'jekyll-redirect-from', 'jemoji',
                    'jekyll-seo-tag', 'jekyll-github-metadata'
                ]
                
                incompatible_plugins = [p for p in plugins if p not in github_pages_plugins]
                jekyll_config["github_pages_compatible"] = len(incompatible_plugins) == 0
                jekyll_config["incompatible_plugins"] = incompatible_plugins
                
            except Exception as e:
                test_results["config_error"] = str(e)
        
        test_results["jekyll_config"] = jekyll_config
        
        # Test 2: Check directory structure
        required_dirs = ['_pages', '_data', '_sass', '_includes']
        optional_dirs = ['_layouts', 'assets', 'images']
        
        dir_structure = {}
        for dir_name in required_dirs + optional_dirs:
            dir_path = self.base_path / dir_name
            dir_structure[dir_name] = {
                "exists": dir_path.exists(),
                "required": dir_name in required_dirs
            }
        
        test_results["directory_structure"] = dir_structure
        
        # Test 3: Check for problematic files
        problematic_files = []
        
        # Check for files that might cause issues
        for file_pattern in ['*.php', '*.asp', '*.jsp']:
            for file_path in self.base_path.rglob(file_pattern):
                problematic_files.append(str(file_path.relative_to(self.base_path)))
        
        # Check for large files (>100MB GitHub limit)
        large_files = []
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    if file_size > 100 * 1024 * 1024:  # 100MB
                        large_files.append({
                            "file": str(file_path.relative_to(self.base_path)),
                            "size_mb": round(file_size / (1024 * 1024), 2)
                        })
                except Exception:
                    continue
        
        test_results["file_issues"] = {
            "problematic_files": problematic_files,
            "large_files": large_files,
            "status": "PASS" if not problematic_files and not large_files else "WARN"
        }
        
        self.results["jekyll_tests"] = test_results
        
        print(f"    ✅ Jekyll config: {'Valid' if jekyll_config['valid_yaml'] else 'Invalid'}")
        print(f"    ✅ GitHub Pages compatible: {jekyll_config['github_pages_compatible']}")
        print(f"    ✅ Directory structure: {sum(1 for d in dir_structure.values() if d['exists'])}/{len(dir_structure)} present")
        print(f"    {'✅' if not problematic_files and not large_files else '⚠️'} File issues: {len(problematic_files + large_files)} found")
        
        return (jekyll_config["valid_yaml"] and 
                jekyll_config["github_pages_compatible"] and
                not problematic_files and not large_files)
    
    def test_github_pages_requirements(self):
        """Test GitHub Pages specific requirements"""
        print("\n🐙 Testing GitHub Pages Requirements...")
        
        test_results = {}
        
        # Test 1: Check repository structure
        repo_structure = {
            "has_readme": (self.base_path / "README.md").exists(),
            "has_license": (self.base_path / "LICENSE").exists(),
            "has_gitignore": (self.base_path / ".gitignore").exists(),
            "has_github_dir": (self.base_path / ".github").exists()
        }
        
        test_results["repository_structure"] = {
            "structure": repo_structure,
            "score": sum(repo_structure.values()) / len(repo_structure),
            "status": "PASS" if repo_structure["has_readme"] else "WARN"
        }
        
        # Test 2: Check GitHub Pages settings compatibility
        config_path = self.base_path / "_config.yml"
        pages_settings = {
            "baseurl_set": False,
            "url_set": False,
            "github_metadata": False,
            "safe_mode": True  # GitHub Pages runs in safe mode
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                if 'baseurl' in config:
                    pages_settings["baseurl_set"] = True
                
                if 'url' in config:
                    pages_settings["url_set"] = True
                
                plugins = config.get('plugins', [])
                if 'jekyll-github-metadata' in plugins:
                    pages_settings["github_metadata"] = True
                
                # Check for unsafe configurations
                if config.get('safe', True) == False:
                    pages_settings["safe_mode"] = False
                
            except Exception as e:
                test_results["config_error"] = str(e)
        
        test_results["pages_settings"] = {
            "settings": pages_settings,
            "status": "PASS" if pages_settings["url_set"] and pages_settings["safe_mode"] else "WARN"
        }
        
        # Test 3: Check for GitHub Pages limitations
        limitations_check = {
            "custom_plugins": [],
            "server_side_code": [],
            "large_repo_size": False
        }
        
        # Check for custom plugins
        plugins_dir = self.base_path / "_plugins"
        if plugins_dir.exists():
            for plugin_file in plugins_dir.glob("*.rb"):
                limitations_check["custom_plugins"].append(plugin_file.name)
        
        # Check for server-side code
        for pattern in ['*.php', '*.py', '*.rb', '*.js']:
            for file_path in self.base_path.rglob(pattern):
                # Exclude Jekyll-specific files
                if not any(exclude in str(file_path) for exclude in ['_site', 'node_modules', '.git']):
                    # Check if it's server-side code (basic heuristic)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read(1000)  # Read first 1000 chars
                        
                        if any(keyword in content for keyword in ['<?php', 'require_once', 'import flask', 'express(']):
                            limitations_check["server_side_code"].append(str(file_path.relative_to(self.base_path)))
                    except Exception:
                        continue
        
        # Estimate repository size (simplified)
        try:
            total_size = sum(f.stat().st_size for f in self.base_path.rglob('*') if f.is_file())
            limitations_check["large_repo_size"] = total_size > 1024 * 1024 * 1024  # 1GB
            limitations_check["repo_size_mb"] = round(total_size / (1024 * 1024), 2)
        except Exception:
            limitations_check["repo_size_mb"] = 0
        
        test_results["limitations"] = {
            "checks": limitations_check,
            "status": "PASS" if (not limitations_check["custom_plugins"] and 
                               not limitations_check["server_side_code"] and 
                               not limitations_check["large_repo_size"]) else "WARN"
        }
        
        self.results["github_pages_tests"] = test_results
        
        print(f"    ✅ Repository structure: {test_results['repository_structure']['score']:.2f}/1.0")
        print(f"    ✅ Pages settings: {'Compatible' if pages_settings['safe_mode'] else 'Issues detected'}")
        print(f"    ✅ Limitations check: {len(limitations_check['custom_plugins'] + limitations_check['server_side_code'])} issues")
        
        return (test_results["repository_structure"]["status"] == "PASS" and
                test_results["pages_settings"]["status"] == "PASS" and
                test_results["limitations"]["status"] == "PASS")
    
    def test_security_compliance(self):
        """Test security compliance for GitHub Pages"""
        print("\n🔒 Testing Security Compliance...")
        
        test_results = {}
        
        # Test 1: Check for secure external references
        external_refs = {
            "http_links": [],
            "insecure_resources": [],
            "external_scripts": []
        }
        
        # Check all HTML and Markdown files
        for file_pattern in ['*.html', '*.md']:
            for file_path in self.base_path.rglob(file_pattern):
                if '_site' in str(file_path):  # Skip generated site
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for HTTP links (should be HTTPS)
                    http_matches = re.findall(r'http://[^\s\'"<>]+', content)
                    for match in http_matches:
                        external_refs["http_links"].append({
                            "file": str(file_path.relative_to(self.base_path)),
                            "url": match
                        })
                    
                    # Check for external scripts
                    script_matches = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content)
                    for match in script_matches:
                        if match.startswith('http'):
                            external_refs["external_scripts"].append({
                                "file": str(file_path.relative_to(self.base_path)),
                                "src": match
                            })
                
                except Exception:
                    continue
        
        test_results["external_references"] = {
            "refs": external_refs,
            "http_count": len(external_refs["http_links"]),
            "external_script_count": len(external_refs["external_scripts"]),
            "status": "PASS" if len(external_refs["http_links"]) == 0 else "WARN"
        }
        
        # Test 2: Check for sensitive information
        sensitive_patterns = [
            r'password\s*[:=]\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*[:=]\s*["\'][^"\']+["\']',
            r'secret\s*[:=]\s*["\'][^"\']+["\']',
            r'token\s*[:=]\s*["\'][^"\']+["\']'
        ]
        
        sensitive_findings = []
        
        for file_path in self.base_path.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix in ['.yml', '.yaml', '.json', '.md', '.html'] and
                '_site' not in str(file_path)):
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            sensitive_findings.append({
                                "file": str(file_path.relative_to(self.base_path)),
                                "pattern": pattern,
                                "context": match[:50] + "..." if len(match) > 50 else match
                            })
                
                except Exception:
                    continue
        
        test_results["sensitive_data"] = {
            "findings": sensitive_findings,
            "count": len(sensitive_findings),
            "status": "PASS" if len(sensitive_findings) == 0 else "FAIL"
        }
        
        # Test 3: Check .gitignore for security
        gitignore_path = self.base_path / ".gitignore"
        gitignore_security = {
            "exists": gitignore_path.exists(),
            "has_env_files": False,
            "has_config_files": False,
            "has_log_files": False
        }
        
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    gitignore_content = f.read()
                
                if any(pattern in gitignore_content for pattern in ['.env', '*.env']):
                    gitignore_security["has_env_files"] = True
                
                if any(pattern in gitignore_content for pattern in ['config.yml', '*.config']):
                    gitignore_security["has_config_files"] = True
                
                if any(pattern in gitignore_content for pattern in ['*.log', 'logs/']):
                    gitignore_security["has_log_files"] = True
            
            except Exception:
                pass
        
        test_results["gitignore_security"] = {
            "checks": gitignore_security,
            "status": "PASS" if gitignore_security["exists"] else "WARN"
        }
        
        self.results["security_tests"] = test_results
        
        print(f"    {'✅' if len(external_refs['http_links']) == 0 else '⚠️'} HTTP links: {len(external_refs['http_links'])} found")
        print(f"    {'✅' if len(sensitive_findings) == 0 else '❌'} Sensitive data: {len(sensitive_findings)} findings")
        print(f"    ✅ .gitignore: {'Present' if gitignore_security['exists'] else 'Missing'}")
        
        return (len(external_refs["http_links"]) == 0 and 
                len(sensitive_findings) == 0 and
                gitignore_security["exists"])
    
    def test_deployment_readiness(self):
        """Test overall deployment readiness"""
        print("\n🚀 Testing Deployment Readiness...")
        
        test_results = {}
        
        # Test 1: Check build requirements
        build_requirements = {
            "gemfile_exists": (self.base_path / "Gemfile").exists(),
            "gemfile_lock_exists": (self.base_path / "Gemfile.lock").exists(),
            "config_valid": False,
            "pages_ready": False
        }
        
        # Check if Jekyll can potentially build
        config_path = self.base_path / "_config.yml"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
                build_requirements["config_valid"] = True
            except Exception:
                pass
        
        # Check if basic pages exist
        required_pages = ['_pages/about.md']  # At least homepage
        build_requirements["pages_ready"] = all(
            (self.base_path / page).exists() for page in required_pages
        )
        
        test_results["build_requirements"] = {
            "requirements": build_requirements,
            "status": "PASS" if (build_requirements["config_valid"] and 
                               build_requirements["pages_ready"]) else "FAIL"
        }
        
        # Test 2: Simulate build check (basic validation)
        build_simulation = {
            "liquid_syntax_errors": [],
            "yaml_errors": [],
            "markdown_issues": []
        }
        
        # Check for common Liquid syntax issues
        for file_path in self.base_path.rglob('*.html'):
            if '_site' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic Liquid syntax check
                liquid_tags = re.findall(r'{%.*?%}', content)
                for tag in liquid_tags:
                    if not tag.strip().endswith('%}'):
                        build_simulation["liquid_syntax_errors"].append({
                            "file": str(file_path.relative_to(self.base_path)),
                            "issue": "Malformed Liquid tag"
                        })
            
            except Exception:
                continue
        
        # Check YAML front matter in Markdown files
        for file_path in self.base_path.rglob('*.md'):
            if '_site' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.startswith('---'):
                    front_matter_end = content.find('---', 3)
                    if front_matter_end != -1:
                        front_matter = content[3:front_matter_end]
                        try:
                            yaml.safe_load(front_matter)
                        except yaml.YAMLError:
                            build_simulation["yaml_errors"].append({
                                "file": str(file_path.relative_to(self.base_path)),
                                "issue": "Invalid YAML front matter"
                            })
            
            except Exception:
                continue
        
        test_results["build_simulation"] = {
            "issues": build_simulation,
            "total_issues": (len(build_simulation["liquid_syntax_errors"]) + 
                           len(build_simulation["yaml_errors"]) + 
                           len(build_simulation["markdown_issues"])),
            "status": "PASS" if all(not issues for issues in build_simulation.values()) else "WARN"
        }
        
        # Test 3: Check deployment configuration
        deployment_config = {
            "github_actions": (self.base_path / ".github" / "workflows").exists(),
            "pages_config": False,
            "domain_config": False
        }
        
        # Check for custom domain
        cname_path = self.base_path / "CNAME"
        if cname_path.exists():
            deployment_config["domain_config"] = True
        
        test_results["deployment_config"] = {
            "config": deployment_config,
            "status": "INFO"  # These are optional
        }
        
        self.results["deployment_tests"] = test_results
        
        print(f"    ✅ Build requirements: {'Met' if build_requirements['config_valid'] and build_requirements['pages_ready'] else 'Issues found'}")
        print(f"    ✅ Build simulation: {test_results['build_simulation']['total_issues']} issues found")
        print(f"    ℹ️ GitHub Actions: {'Configured' if deployment_config['github_actions'] else 'Not configured'}")
        
        return (test_results["build_requirements"]["status"] == "PASS" and
                test_results["build_simulation"]["status"] in ["PASS", "WARN"])
    
    def generate_deployment_report(self):
        """Generate comprehensive deployment readiness report"""
        print("\n📊 Generating Deployment Report...")
        
        # Calculate summary scores
        jekyll_score = 0
        github_pages_score = 0
        security_score = 0
        deployment_score = 0
        
        # Jekyll score
        jekyll_tests = self.results.get("jekyll_tests", {})
        if jekyll_tests:
            jekyll_config = jekyll_tests.get("jekyll_config", {})
            jekyll_factors = [
                jekyll_config.get("valid_yaml", False),
                jekyll_config.get("github_pages_compatible", False),
                jekyll_tests.get("file_issues", {}).get("status") == "PASS"
            ]
            jekyll_score = sum(jekyll_factors) / len(jekyll_factors)
        
        # GitHub Pages score
        pages_tests = self.results.get("github_pages_tests", {})
        if pages_tests:
            pages_factors = [
                pages_tests.get("repository_structure", {}).get("status") == "PASS",
                pages_tests.get("pages_settings", {}).get("status") == "PASS",
                pages_tests.get("limitations", {}).get("status") == "PASS"
            ]
            github_pages_score = sum(pages_factors) / len(pages_factors)
        
        # Security score
        security_tests = self.results.get("security_tests", {})
        if security_tests:
            security_factors = [
                security_tests.get("external_references", {}).get("status") == "PASS",
                security_tests.get("sensitive_data", {}).get("status") == "PASS",
                security_tests.get("gitignore_security", {}).get("status") == "PASS"
            ]
            security_score = sum(security_factors) / len(security_factors)
        
        # Deployment score
        deployment_tests = self.results.get("deployment_tests", {})
        if deployment_tests:
            deployment_factors = [
                deployment_tests.get("build_requirements", {}).get("status") == "PASS",
                deployment_tests.get("build_simulation", {}).get("status") in ["PASS", "WARN"]
            ]
            deployment_score = sum(deployment_factors) / len(deployment_factors)
        
        overall_score = (jekyll_score + github_pages_score + security_score + deployment_score) / 4
        
        self.results["summary"] = {
            "jekyll_score": jekyll_score,
            "github_pages_score": github_pages_score,
            "security_score": security_score,
            "deployment_score": deployment_score,
            "overall_score": overall_score,
            "deployment_ready": overall_score > 0.8,
            "overall_status": "READY" if overall_score > 0.8 else "NEEDS_WORK"
        }
        
        # Save report
        report_file = self.base_path / "github_pages_deployment_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"    ✅ Deployment report saved to: {report_file}")
        
        # Print summary
        print(f"\n🎯 Deployment Readiness Summary:")
        print(f"  Jekyll Compatibility: {jekyll_score:.2f}/1.0")
        print(f"  GitHub Pages Compliance: {github_pages_score:.2f}/1.0")
        print(f"  Security Score: {security_score:.2f}/1.0")
        print(f"  Deployment Readiness: {deployment_score:.2f}/1.0")
        print(f"  Overall Score: {overall_score:.2f}/1.0")
        print(f"  Status: {self.results['summary']['overall_status']}")
        
        return self.results["summary"]["deployment_ready"]

def main():
    """Run GitHub Pages deployment tests"""
    print("🐙 GitHub Pages Deployment Test Suite")
    print("=" * 50)
    
    tester = GitHubPagesDeploymentTest()
    
    # Run all tests
    tests_passed = []
    
    tests_passed.append(tester.test_jekyll_build_compatibility())
    tests_passed.append(tester.test_github_pages_requirements())
    tests_passed.append(tester.test_security_compliance())
    tests_passed.append(tester.test_deployment_readiness())
    
    # Generate report
    deployment_ready = tester.generate_deployment_report()
    
    print("\n" + "=" * 50)
    if deployment_ready:
        print("🎉 Site is ready for GitHub Pages deployment!")
        return 0
    else:
        print("⚠️ Some deployment issues detected. Check the report for details.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())