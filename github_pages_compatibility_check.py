#!/usr/bin/env python3
"""
GitHub Pages Compatibility Checker
Validates Jekyll configuration and files for GitHub Pages compatibility
"""

import os
import yaml
import re
from pathlib import Path

def check_config_yml():
    """Check _config.yml for GitHub Pages compatibility"""
    issues = []
    
    if not os.path.exists('_config.yml'):
        issues.append("ERROR: _config.yml not found")
        return issues
    
    with open('_config.yml', 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            issues.append(f"ERROR: Invalid YAML in _config.yml: {e}")
            return issues
    
    # Check required fields
    required_fields = ['title', 'description']
    for field in required_fields:
        if field not in config:
            issues.append(f"WARNING: Missing required field '{field}' in _config.yml")
    
    # Check GitHub Pages supported plugins
    github_pages_plugins = [
        'jekyll-coffeescript',
        'jekyll-default-layout',
        'jekyll-gist',
        'jekyll-github-metadata',
        'jekyll-optional-front-matter',
        'jekyll-paginate',
        'jekyll-readme-index',
        'jekyll-redirect-from',
        'jekyll-relative-links',
        'jekyll-sass-converter',
        'jekyll-sitemap',
        'jekyll-feed',
        'jekyll-seo-tag',
        'jemoji'
    ]
    
    if 'plugins' in config:
        for plugin in config['plugins']:
            if plugin not in github_pages_plugins:
                issues.append(f"WARNING: Plugin '{plugin}' may not be supported by GitHub Pages")
    
    # Check for proper URL configuration
    if 'url' not in config:
        issues.append("WARNING: 'url' field missing - recommended for GitHub Pages")
    
    if 'baseurl' not in config:
        issues.append("INFO: 'baseurl' field missing - should be empty string for user pages")
    
    return issues

def check_gemfile():
    """Check Gemfile for GitHub Pages compatibility"""
    issues = []
    
    if not os.path.exists('Gemfile'):
        issues.append("WARNING: Gemfile not found")
        return issues
    
    with open('Gemfile', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for github-pages gem
    if 'github-pages' not in content:
        issues.append("WARNING: 'github-pages' gem not found in Gemfile")
    
    # Check for unsupported gems
    unsupported_patterns = [
        r'gem\s+["\']jekyll-archives["\']',
        r'gem\s+["\']jekyll-admin["\']',
    ]
    
    for pattern in unsupported_patterns:
        if re.search(pattern, content):
            issues.append(f"WARNING: Unsupported gem found matching pattern: {pattern}")
    
    return issues

def check_pages_structure():
    """Check pages structure and permalinks"""
    issues = []
    
    pages_dir = Path('_pages')
    if not pages_dir.exists():
        issues.append("WARNING: _pages directory not found")
        return issues
    
    # Check for required pages based on navigation
    nav_file = Path('_data/navigation.yml')
    if nav_file.exists():
        with open(nav_file, 'r', encoding='utf-8') as f:
            try:
                nav_data = yaml.safe_load(f)
                if 'main' in nav_data:
                    for item in nav_data['main']:
                        url = item.get('url', '')
                        if url.startswith('/') and url != '/':
                            # Check if corresponding page exists
                            page_name = url.strip('/') + '.md'
                            page_path = pages_dir / page_name
                            if not page_path.exists():
                                issues.append(f"ERROR: Navigation item '{item.get('title')}' points to '{url}' but no corresponding page found at {page_path}")
            except yaml.YAMLError as e:
                issues.append(f"ERROR: Invalid YAML in navigation.yml: {e}")
    
    return issues

def check_external_resources():
    """Check for HTTPS external resources"""
    issues = []
    
    # Check HTML files for external resources
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['_site', 'node_modules']]
        for file in files:
            if file.endswith(('.html', '.md')):
                html_files.append(os.path.join(root, file))
    
    http_pattern = re.compile(r'http://(?!localhost|127\.0\.0\.1)')
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = http_pattern.findall(content)
                if matches:
                    issues.append(f"WARNING: Non-HTTPS external resources found in {file_path}")
        except UnicodeDecodeError:
            continue  # Skip binary files
    
    return issues

def main():
    """Run all compatibility checks"""
    print("GitHub Pages Compatibility Check")
    print("=" * 40)
    
    all_issues = []
    
    print("\n1. Checking _config.yml...")
    config_issues = check_config_yml()
    all_issues.extend(config_issues)
    
    print("\n2. Checking Gemfile...")
    gemfile_issues = check_gemfile()
    all_issues.extend(gemfile_issues)
    
    print("\n3. Checking pages structure...")
    pages_issues = check_pages_structure()
    all_issues.extend(pages_issues)
    
    print("\n4. Checking external resources...")
    resource_issues = check_external_resources()
    all_issues.extend(resource_issues)
    
    print("\n" + "=" * 40)
    print("RESULTS:")
    
    if not all_issues:
        print("✅ No compatibility issues found!")
    else:
        errors = [issue for issue in all_issues if issue.startswith('ERROR')]
        warnings = [issue for issue in all_issues if issue.startswith('WARNING')]
        infos = [issue for issue in all_issues if issue.startswith('INFO')]
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for error in errors:
                print(f"  {error}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"  {warning}")
        
        if infos:
            print(f"\n💡 INFO ({len(infos)}):")
            for info in infos:
                print(f"  {info}")
    
    print(f"\nTotal issues found: {len(all_issues)}")
    return len([issue for issue in all_issues if issue.startswith('ERROR')])

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)