#!/usr/bin/env python3
"""
Simple Broken Link Detector for Web3 Meta-Crisis Wiki
Uses only standard library - no external dependencies.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class SimpleLinkChecker:
    def __init__(self, content_dir="content"):
        self.content_dir = Path(content_dir)
        self.all_files = set()  # All markdown filenames (without .md)
        self.all_aliases = defaultdict(list)  # alias -> [files that define it]
        self.all_links = defaultdict(list)  # link_target -> [(file, line_num, full_link)]

    def scan_files(self):
        """Scan all markdown files and build file inventory."""
        print(f"Scanning files in {self.content_dir}...")

        for md_file in self.content_dir.rglob("*.md"):
            filename = md_file.stem
            self.all_files.add(filename)

            # Simple frontmatter parsing for aliases
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for aliases in frontmatter
                lines = content.split('\n')
                in_frontmatter = False
                in_aliases = False

                for line in lines[:20]:  # Only check first 20 lines for frontmatter
                    line = line.strip()
                    if line == '---':
                        if not in_frontmatter:
                            in_frontmatter = True
                        else:
                            break  # End of frontmatter
                    elif in_frontmatter:
                        if line.startswith('aliases:'):
                            in_aliases = True
                        elif in_aliases and line.startswith('- '):
                            alias = line[2:].strip().strip('"\'')
                            if alias:
                                self.all_aliases[alias].append(filename)
                        elif in_aliases and not line.startswith(' ') and line:
                            in_aliases = False

            except Exception as e:
                print(f"Error reading {md_file}: {e}")

        total_aliases = sum(len(files) for files in self.all_aliases.values())
        print(f"Found {len(self.all_files)} files with {total_aliases} alias definitions")

    def extract_links(self):
        """Extract all wikilinks from markdown files."""
        print("Extracting wikilinks...")

        # Simple regex for wikilinks
        link_pattern = r'\[\[([^\]]+)\]\]'

        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                rel_path = md_file.relative_to(self.content_dir)

                for line_num, line in enumerate(lines, 1):
                    # Skip frontmatter lines
                    if line_num <= 15 and ('---' in line or 'aliases:' in line or line.strip().startswith('- "')):
                        continue

                    matches = re.finditer(link_pattern, line)
                    for match in matches:
                        full_link = match.group(0)
                        link_content = match.group(1)

                        # Handle different link formats
                        if '|' in link_content:
                            # [[target|display text]]
                            link_target = link_content.split('|')[0].strip()
                        elif '#' in link_content:
                            # [[target#section]]
                            link_target = link_content.split('#')[0].strip()
                        else:
                            # [[target]]
                            link_target = link_content.strip()

                        if link_target:  # Skip empty targets
                            self.all_links[link_target].append((rel_path, line_num, full_link))

            except Exception as e:
                print(f"Error processing {md_file}: {e}")

        print(f"Found {len(self.all_links)} unique link targets")

    def analyze_broken_links(self):
        """Find and categorize broken links."""
        print("Analyzing broken links...")

        broken_links = {
            'missing': [],
            'case_mismatch': [],
            'could_be_alias': []
        }

        working_links = 0

        for link_target, occurrences in self.all_links.items():
            is_broken = True

            # Check exact match with filenames
            if link_target in self.all_files:
                is_broken = False
                working_links += 1

            # Check exact match with aliases
            elif link_target in self.all_aliases:
                is_broken = False
                working_links += 1

            # Check for case mismatches
            elif any(f.lower() == link_target.lower() for f in self.all_files):
                broken_links['case_mismatch'].append((link_target, occurrences))

            # Check if it could be an alias for existing files
            else:
                potential_targets = []
                for filename in self.all_files:
                    # Look for partial matches
                    if (link_target.lower() in filename.lower() or
                        filename.lower() in link_target.lower() or
                        any(word.lower() in filename.lower() for word in link_target.split() if len(word) > 3)):
                        potential_targets.append(filename)

                if potential_targets:
                    broken_links['could_be_alias'].append((link_target, occurrences, potential_targets[:3]))
                else:
                    broken_links['missing'].append((link_target, occurrences))

        return broken_links, working_links

    def generate_report(self):
        """Generate and display broken link report."""
        broken_links, working_links = self.analyze_broken_links()

        print("\n" + "="*80)
        print("BROKEN LINK ANALYSIS REPORT")
        print("="*80)

        total_links = sum(len(occs) for occs in self.all_links.values())
        total_targets = len(self.all_links)
        total_broken_targets = sum(len(category) for category in broken_links.values())

        print(f"\nSUMMARY:")
        print(f"Files scanned: {len(self.all_files)}")
        print(f"Total link instances: {total_links}")
        print(f"Unique link targets: {total_targets}")
        print(f"Working targets: {working_links}")
        print(f"Broken targets: {total_broken_targets}")
        print(f"Success rate: {working_links/total_targets*100:.1f}%")

        # Case mismatches (easy to fix)
        if broken_links['case_mismatch']:
            print(f"\n🔧 CASE MISMATCHES (Easy to fix: {len(broken_links['case_mismatch'])}):")
            print("-" * 50)
            for link_target, occurrences in broken_links['case_mismatch'][:10]:
                correct_case = next(f for f in self.all_files if f.lower() == link_target.lower())
                total_occs = len(occurrences)
                print(f"  '{link_target}' → '{correct_case}' ({total_occs} occurrences)")

        # Could be aliases (medium difficulty)
        if broken_links['could_be_alias']:
            print(f"\n📝 COULD ADD AS ALIASES ({len(broken_links['could_be_alias'])}):")
            print("-" * 40)
            for link_target, occurrences, potential_targets in broken_links['could_be_alias'][:10]:
                total_occs = len(occurrences)
                print(f"  '{link_target}' → {potential_targets} ({total_occs} occurrences)")

        # Missing completely
        if broken_links['missing']:
            print(f"\n❌ MISSING TARGETS (Need to create or remove: {len(broken_links['missing'])}):")
            print("-" * 60)
            for link_target, occurrences in broken_links['missing'][:15]:
                total_occs = len(occurrences)
                print(f"  '{link_target}' ({total_occs} occurrences)")
                # Show first few files that reference it
                files = list(set(str(occ[0]) for occ in occurrences[:3]))
                print(f"    Referenced in: {', '.join(files)}")

        return broken_links

    def generate_quick_fixes(self, broken_links):
        """Generate shell commands for quick fixes."""
        print(f"\n🛠️  QUICK FIXES:")
        print("="*40)

        if broken_links['case_mismatch']:
            print("\n# Case mismatch fixes (run these commands):")
            for link_target, occurrences in broken_links['case_mismatch']:
                correct_case = next(f for f in self.all_files if f.lower() == link_target.lower())
                print(f"find content -name '*.md' -exec sed -i '' 's/\\[\\[{re.escape(link_target)}\\]\\]/[[{correct_case}]]/g' {{}} \\;")

        if broken_links['could_be_alias']:
            print(f"\n# Suggested aliases to add to frontmatter:")
            alias_suggestions = defaultdict(list)
            for link_target, occurrences, potential_targets in broken_links['could_be_alias']:
                if len(potential_targets) == 1:  # Clear single match
                    alias_suggestions[potential_targets[0]].append(link_target)

            for filename, aliases in alias_suggestions.items():
                print(f"# Add to {filename}.md frontmatter: {aliases}")

def main():
    checker = SimpleLinkChecker()
    checker.scan_files()
    checker.extract_links()
    broken_links = checker.generate_report()
    checker.generate_quick_fixes(broken_links)

if __name__ == "__main__":
    main()