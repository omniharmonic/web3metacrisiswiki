#!/usr/bin/env python3
"""
Comprehensive Broken Link Detector for Web3 Meta-Crisis Wiki
Scans all markdown files and identifies broken wikilinks.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
import argparse

class WikiLinkAnalyzer:
    def __init__(self, content_dir="content"):
        self.content_dir = Path(content_dir)
        self.all_files = {}  # filename -> file_path mapping
        self.all_aliases = {}  # alias -> file_path mapping
        self.all_links = defaultdict(list)  # link -> [(file, line_num, full_link)]
        self.broken_links = defaultdict(list)

    def scan_files(self):
        """Scan all markdown files and build file inventory."""
        print(f"Scanning files in {self.content_dir}...")

        for md_file in self.content_dir.rglob("*.md"):
            # Store relative path from content directory
            rel_path = md_file.relative_to(self.content_dir)
            filename = md_file.stem

            # Add filename mapping
            self.all_files[filename] = rel_path

            # Extract aliases from frontmatter
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        try:
                            fm_data = yaml.safe_load(frontmatter)
                            if fm_data and 'aliases' in fm_data:
                                aliases = fm_data['aliases']
                                if isinstance(aliases, list):
                                    for alias in aliases:
                                        self.all_aliases[alias] = rel_path
                        except yaml.YAMLError:
                            pass
            except Exception as e:
                print(f"Error processing {md_file}: {e}")

        print(f"Found {len(self.all_files)} files with {len(self.all_aliases)} aliases")

    def extract_links(self):
        """Extract all wikilinks from all markdown files."""
        print("Extracting wikilinks...")

        # Regex patterns for different wikilink formats
        patterns = [
            r'\[\[([^|\]]+)\|([^\]]+)\]\]',  # [[link|display text]]
            r'\[\[([^|\]#]+)(#[^\]]+)?\]\]'   # [[link]] or [[link#section]]
        ]

        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    # Skip frontmatter
                    if line_num <= 10 and ('---' in line or 'aliases:' in line):
                        continue

                    for pattern in patterns:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            if '|' in match.group(0):
                                # Format: [[link|display]]
                                link_target = match.group(1).strip()
                                full_match = match.group(0)
                            else:
                                # Format: [[link]] or [[link#section]]
                                full_group = match.group(1)
                                if '#' in full_group:
                                    link_target = full_group.split('#')[0].strip()
                                else:
                                    link_target = full_group.strip()
                                full_match = match.group(0)

                            # Store the link
                            rel_path = md_file.relative_to(self.content_dir)
                            self.all_links[link_target].append((rel_path, line_num, full_match.strip()))

            except Exception as e:
                print(f"Error processing {md_file}: {e}")

        print(f"Found {len(self.all_links)} unique link targets across all files")

    def analyze_broken_links(self):
        """Analyze which links are broken and categorize them."""
        print("Analyzing broken links...")

        for link_target, occurrences in self.all_links.items():
            is_broken = True
            broken_reason = ""

            # Check if target exists as filename
            if link_target in self.all_files:
                is_broken = False

            # Check if target exists as alias
            elif link_target in self.all_aliases:
                is_broken = False

            # Check for case-insensitive matches
            elif any(f.lower() == link_target.lower() for f in self.all_files.keys()):
                is_broken = True
                broken_reason = "case_mismatch"

            # Check for partial matches (might be typos)
            elif any(link_target.lower() in f.lower() or f.lower() in link_target.lower()
                    for f in self.all_files.keys() if len(f) > 3):
                is_broken = True
                broken_reason = "possible_typo"

            else:
                is_broken = True
                broken_reason = "missing_target"

            if is_broken:
                self.broken_links[broken_reason].extend([(link_target, occurrences)])

    def generate_report(self):
        """Generate comprehensive broken link report."""
        print("\n" + "="*80)
        print("BROKEN LINK ANALYSIS REPORT")
        print("="*80)

        total_broken = sum(len(links) for links in self.broken_links.values())
        total_unique_broken = len([link for category in self.broken_links.values() for link, _ in category])

        print(f"\nSUMMARY:")
        print(f"Total files scanned: {len(self.all_files)}")
        print(f"Total unique link targets: {len(self.all_links)}")
        print(f"Total broken link categories: {len(self.broken_links)}")
        print(f"Total unique broken targets: {total_unique_broken}")

        for category, broken_list in self.broken_links.items():
            print(f"\n{category.upper().replace('_', ' ')} ({len(broken_list)} targets):")
            print("-" * 60)

            for link_target, occurrences in broken_list[:10]:  # Show first 10
                print(f"\nTarget: '{link_target}'")
                print(f"Occurrences: {len(occurrences)}")
                for file_path, line_num, full_link in occurrences[:3]:  # Show first 3 occurrences
                    print(f"  - {file_path}:{line_num} -> {full_link}")
                if len(occurrences) > 3:
                    print(f"  ... and {len(occurrences) - 3} more")

            if len(broken_list) > 10:
                print(f"\n... and {len(broken_list) - 10} more broken targets in this category")

    def suggest_fixes(self):
        """Suggest automatic fixes for broken links."""
        print(f"\n{'='*80}")
        print("SUGGESTED FIXES")
        print("="*80)

        # Case mismatch fixes
        if "case_mismatch" in self.broken_links:
            print(f"\nCASE MISMATCH FIXES:")
            print("-" * 30)

            for link_target, occurrences in self.broken_links["case_mismatch"]:
                # Find the correct case version
                correct_case = None
                for filename in self.all_files.keys():
                    if filename.lower() == link_target.lower():
                        correct_case = filename
                        break

                if correct_case:
                    print(f"'{link_target}' -> '{correct_case}' ({len(occurrences)} occurrences)")

        # Missing targets that could be aliases
        if "missing_target" in self.broken_links:
            print(f"\nMISSING TARGETS THAT COULD BE ALIASES:")
            print("-" * 45)

            for link_target, occurrences in self.broken_links["missing_target"][:20]:
                # Look for similar existing files
                similar_files = []
                for filename in self.all_files.keys():
                    if (link_target.lower() in filename.lower() or
                        filename.lower() in link_target.lower() or
                        any(word in filename.lower() for word in link_target.lower().split() if len(word) > 3)):
                        similar_files.append(filename)

                if similar_files:
                    print(f"'{link_target}' -> could be alias for: {similar_files[:3]} ({len(occurrences)} occurrences)")

    def generate_fix_script(self, output_file="fix-broken-links.sh"):
        """Generate shell script to fix high-confidence broken links."""
        fixes = []

        # Case mismatch fixes
        if "case_mismatch" in self.broken_links:
            for link_target, occurrences in self.broken_links["case_mismatch"]:
                correct_case = None
                for filename in self.all_files.keys():
                    if filename.lower() == link_target.lower():
                        correct_case = filename
                        break

                if correct_case:
                    for file_path, line_num, full_link in occurrences:
                        old_link = f"[[{link_target}]]"
                        new_link = f"[[{correct_case}]]"
                        fixes.append(f'sed -i "" "s/{re.escape(old_link)}/{re.escape(new_link)}/g" "content/{file_path}"')

        if fixes:
            with open(output_file, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("# Auto-generated script to fix broken links\n")
                f.write("# BACKUP YOUR FILES BEFORE RUNNING THIS SCRIPT\n\n")
                f.write("set -e\n\n")
                for fix in fixes:
                    f.write(fix + "\n")

            print(f"\nGenerated fix script: {output_file}")
            print("Review carefully before running!")

def main():
    parser = argparse.ArgumentParser(description="Analyze broken wikilinks in markdown files")
    parser.add_argument("--content-dir", default="content", help="Content directory to scan")
    parser.add_argument("--fix-script", action="store_true", help="Generate fix script")
    args = parser.parse_args()

    analyzer = WikiLinkAnalyzer(args.content_dir)
    analyzer.scan_files()
    analyzer.extract_links()
    analyzer.analyze_broken_links()
    analyzer.generate_report()
    analyzer.suggest_fixes()

    if args.fix_script:
        analyzer.generate_fix_script()

if __name__ == "__main__":
    main()