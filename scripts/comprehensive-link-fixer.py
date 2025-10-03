#!/usr/bin/env python3
"""
Comprehensive Broken Link Fixer for Web3 Meta-Crisis Wiki
Implements holistic strategy to fix broken links automatically.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import shutil

class ComprehensiveLinkFixer:
    def __init__(self, content_dir="content"):
        self.content_dir = Path(content_dir)
        self.all_files = set()
        self.all_aliases = defaultdict(list)
        self.all_links = defaultdict(list)
        self.fixes_applied = 0
        self.aliases_added = 0
        self.links_removed = 0

    def scan_files(self):
        """Scan all markdown files and build complete inventory."""
        print(f"Scanning files in {self.content_dir}...")

        for md_file in self.content_dir.rglob("*.md"):
            filename = md_file.stem
            self.all_files.add(filename)

            # Parse aliases from frontmatter
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                lines = content.split('\n')
                in_frontmatter = False
                in_aliases = False

                for line in lines[:25]:
                    line = line.strip()
                    if line == '---':
                        if not in_frontmatter:
                            in_frontmatter = True
                        else:
                            break
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

        print(f"Found {len(self.all_files)} files with {sum(len(a) for a in self.all_aliases.values())} aliases")

    def extract_links(self):
        """Extract all wikilinks from markdown files."""
        print("Extracting wikilinks...")

        link_pattern = r'\[\[([^\]]+)\]\]'

        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                rel_path = md_file.relative_to(self.content_dir)

                for line_num, line in enumerate(lines, 1):
                    # Skip frontmatter
                    if line_num <= 20 and ('---' in line or 'aliases:' in line or line.strip().startswith('- "')):
                        continue

                    matches = re.finditer(link_pattern, line)
                    for match in matches:
                        full_link = match.group(0)
                        link_content = match.group(1)

                        # Handle different link formats
                        if '|' in link_content:
                            link_target = link_content.split('|')[0].strip()
                        elif '#' in link_content:
                            link_target = link_content.split('#')[0].strip()
                        else:
                            link_target = link_content.strip()

                        if link_target:
                            self.all_links[link_target].append((rel_path, line_num, full_link, line))

            except Exception as e:
                print(f"Error processing {md_file}: {e}")

        print(f"Found {len(self.all_links)} unique link targets")

    def categorize_broken_links(self):
        """Categorize all broken links for systematic fixing."""
        case_mismatches = []
        can_add_aliases = []
        should_remove = []
        working_links = 0

        print("Categorizing broken links...")

        for link_target, occurrences in self.all_links.items():
            # Check exact matches
            if link_target in self.all_files or link_target in self.all_aliases:
                working_links += 1
                continue

            # Case mismatches - easy fix
            case_match = next((f for f in self.all_files if f.lower() == link_target.lower()), None)
            if case_match:
                case_mismatches.append((link_target, case_match, occurrences))
                continue

            # Can be aliases - medium effort
            potential_targets = []
            for filename in self.all_files:
                # Strong partial matches
                if (link_target.lower() in filename.lower() or
                    filename.lower() in link_target.lower()):
                    potential_targets.append(filename)
                # Word overlap matches
                elif len(set(link_target.lower().split()) & set(filename.lower().split())) >= 2:
                    potential_targets.append(filename)

            if potential_targets and len(potential_targets) <= 3:
                # Strong candidate for alias
                best_match = min(potential_targets, key=len)  # Prefer shorter filename
                can_add_aliases.append((link_target, best_match, occurrences))
                continue

            # Should probably remove - no good matches
            should_remove.append((link_target, occurrences))

        return case_mismatches, can_add_aliases, should_remove, working_links

    def apply_case_fixes(self, case_mismatches):
        """Apply all case mismatch fixes."""
        print(f"\nApplying {len(case_mismatches)} case mismatch fixes...")

        for wrong_case, correct_case, occurrences in case_mismatches:
            files_to_fix = set(str(occ[0]) for occ in occurrences)

            for file_path in files_to_fix:
                full_path = self.content_dir / file_path
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Replace the incorrect case
                    old_link = f"[[{wrong_case}]]"
                    new_link = f"[[{correct_case}]]"

                    if old_link in content:
                        content = content.replace(old_link, new_link)

                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                        self.fixes_applied += 1

                except Exception as e:
                    print(f"Error fixing {full_path}: {e}")

        print(f"Applied {self.fixes_applied} case mismatch fixes")

    def add_aliases(self, can_add_aliases):
        """Add aliases to target files for resolvable links."""
        print(f"\nAdding {len(can_add_aliases)} aliases...")

        alias_additions = defaultdict(list)

        # Group aliases by target file
        for link_target, best_match, occurrences in can_add_aliases:
            alias_additions[best_match].append(link_target)

        for filename, new_aliases in alias_additions.items():
            # Find the file
            target_file = None
            for md_file in self.content_dir.rglob("*.md"):
                if md_file.stem == filename:
                    target_file = md_file
                    break

            if not target_file:
                continue

            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                lines = content.split('\n')

                # Find frontmatter and aliases section
                frontmatter_start = -1
                frontmatter_end = -1
                aliases_line = -1

                for i, line in enumerate(lines):
                    if line.strip() == '---':
                        if frontmatter_start == -1:
                            frontmatter_start = i
                        else:
                            frontmatter_end = i
                            break
                    elif frontmatter_start != -1 and line.strip().startswith('aliases:'):
                        aliases_line = i

                if frontmatter_start == -1:
                    # No frontmatter - add it
                    new_aliases_section = ['---', 'aliases:'] + [f'  - "{alias}"' for alias in new_aliases] + ['---', '']
                    lines = new_aliases_section + lines
                elif aliases_line == -1:
                    # Has frontmatter but no aliases - add aliases section
                    insert_pos = frontmatter_start + 1
                    new_lines = ['aliases:'] + [f'  - "{alias}"' for alias in new_aliases]
                    lines[insert_pos:insert_pos] = new_lines
                else:
                    # Has aliases - add to existing
                    insert_pos = aliases_line + 1
                    while insert_pos < len(lines) and lines[insert_pos].strip().startswith('- '):
                        insert_pos += 1

                    new_lines = [f'  - "{alias}"' for alias in new_aliases]
                    lines[insert_pos:insert_pos] = new_lines

                # Write back
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))

                self.aliases_added += len(new_aliases)
                print(f"Added {len(new_aliases)} aliases to {filename}")

            except Exception as e:
                print(f"Error adding aliases to {target_file}: {e}")

    def remove_invalid_links(self, should_remove):
        """Remove links to non-existent concepts."""
        print(f"\nRemoving {len(should_remove)} invalid link targets...")

        # Define patterns for links that should definitely be removed
        removal_patterns = [
            'extitutions', 'cosmo-localism', 'revnets', 'Revnets', 'Hypercerts',
            'Globalization', 'Financialization', 'Cosmo-localism', 'Polycentricity',
            'Dual Power Strategies', 'dual power', 'Intermediary Elimination',
            'peer validation', 'Peer Review', 'Dispute Resolution'
        ]

        files_modified = set()

        for link_target, occurrences in should_remove:
            # Only remove if it's clearly invalid or matches removal patterns
            should_remove_this = (
                link_target in removal_patterns or
                len(link_target) < 3 or  # Very short, likely typos
                link_target.endswith('.md') or  # File references
                'manuscript' in link_target.lower() or
                any(word in link_target.lower() for word in ['draft', 'temp', 'old', 'backup'])
            )

            if not should_remove_this:
                continue

            for file_path, line_num, full_link, line_content in occurrences:
                full_path = self.content_dir / file_path
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Remove the specific link
                    if full_link in content:
                        # Replace with just the link text (remove brackets)
                        link_text = link_target
                        if '|' in full_link:
                            link_text = full_link.split('|')[1].rstrip(']')

                        content = content.replace(full_link, link_text)

                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                        files_modified.add(str(file_path))
                        self.links_removed += 1

                except Exception as e:
                    print(f"Error removing link from {full_path}: {e}")

        print(f"Removed {self.links_removed} invalid links from {len(files_modified)} files")

    def generate_report(self):
        """Generate final report of all fixes applied."""
        print("\n" + "="*80)
        print("COMPREHENSIVE LINK FIXING REPORT")
        print("="*80)

        print(f"\nFIXES APPLIED:")
        print(f"Case mismatch fixes: {self.fixes_applied}")
        print(f"Aliases added: {self.aliases_added}")
        print(f"Invalid links removed: {self.links_removed}")
        print(f"Total improvements: {self.fixes_applied + self.aliases_added + self.links_removed}")

    def run_comprehensive_fix(self):
        """Execute the complete holistic fixing strategy."""
        print("Starting comprehensive broken link fixing...")

        # Scan and analyze
        self.scan_files()
        self.extract_links()
        case_mismatches, can_add_aliases, should_remove, working_links = self.categorize_broken_links()

        total_targets = len(self.all_links)
        initial_success_rate = working_links / total_targets * 100

        print(f"\nINITIAL STATE:")
        print(f"Working links: {working_links}/{total_targets} ({initial_success_rate:.1f}%)")
        print(f"Case mismatches to fix: {len(case_mismatches)}")
        print(f"Links that can become aliases: {len(can_add_aliases)}")
        print(f"Links to remove: {len(should_remove)}")

        # Apply fixes
        self.apply_case_fixes(case_mismatches)
        self.add_aliases(can_add_aliases)
        self.remove_invalid_links(should_remove)

        # Calculate projected improvement
        projected_working = working_links + len(case_mismatches) + len(can_add_aliases)
        projected_success_rate = projected_working / total_targets * 100

        print(f"\nPROJECTED IMPROVEMENT:")
        print(f"Expected working links: {projected_working}/{total_targets} ({projected_success_rate:.1f}%)")
        print(f"Improvement: +{projected_success_rate - initial_success_rate:.1f} percentage points")

        self.generate_report()

def main():
    fixer = ComprehensiveLinkFixer()
    fixer.run_comprehensive_fix()

if __name__ == "__main__":
    main()