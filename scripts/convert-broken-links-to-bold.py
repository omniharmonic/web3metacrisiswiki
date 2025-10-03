#!/usr/bin/env python3
"""
Convert all remaining broken wikilinks to bold text.
This removes broken links while preserving the concept names for readability.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class BrokenLinkConverter:
    def __init__(self, content_dir="content"):
        self.content_dir = Path(content_dir)
        self.files_modified = 0
        self.links_converted = 0

    def find_all_files_and_aliases(self):
        """Get all markdown files and their aliases."""
        files_with_aliases = {}

        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract aliases from frontmatter
                aliases = set()
                lines = content.split('\n')
                in_frontmatter = False
                in_aliases = False

                for line in lines:
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
                            aliases.add(alias)
                        elif not line.startswith('-') and not line.startswith(' '):
                            in_aliases = False

                # Add filename as alias
                aliases.add(md_file.stem)
                files_with_aliases[md_file.stem] = aliases

            except Exception as e:
                print(f"Error reading {md_file}: {e}")

        return files_with_aliases

    def extract_wikilinks(self, content):
        """Extract all wikilinks from content."""
        # Pattern for [[link]] or [[link|display text]]
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        return re.findall(pattern, content)

    def is_link_broken(self, link_target, all_aliases):
        """Check if a wikilink target is broken."""
        # Check if any file has this as filename or alias
        for filename, aliases in all_aliases.items():
            if link_target in aliases or link_target == filename:
                return False
        return True

    def convert_broken_links_in_file(self, file_path, all_aliases):
        """Convert broken wikilinks to bold text in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Find all wikilinks
            wikilinks = self.extract_wikilinks(content)
            converted_count = 0

            for link_target in wikilinks:
                if self.is_link_broken(link_target, all_aliases):
                    # Convert [[broken link]] to **broken link**
                    # Handle both [[link]] and [[link|display]] formats
                    pattern1 = rf'\[\[{re.escape(link_target)}\]\]'
                    pattern2 = rf'\[\[{re.escape(link_target)}\|([^\]]+)\]\]'

                    # Replace [[link|display]] with **display**
                    def replace_with_display(match):
                        return f"**{match.group(1)}**"

                    new_content = re.sub(pattern2, replace_with_display, content)

                    # Replace remaining [[link]] with **link**
                    new_content = re.sub(pattern1, f"**{link_target}**", new_content)

                    if new_content != content:
                        content = new_content
                        converted_count += 1

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_modified += 1
                self.links_converted += converted_count
                print(f"Converted {converted_count} broken links in {file_path.name}")
                return True

            return False

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False

    def convert_all_broken_links(self):
        """Convert all broken wikilinks to bold text."""
        print("Finding all files and aliases...")
        all_aliases = self.find_all_files_and_aliases()

        print(f"Converting broken links in all markdown files...")

        for md_file in self.content_dir.rglob("*.md"):
            self.convert_broken_links_in_file(md_file, all_aliases)

    def generate_report(self):
        """Generate conversion report."""
        print(f"\n{'='*60}")
        print("BROKEN LINK CONVERSION REPORT")
        print(f"{'='*60}")
        print(f"Files modified: {self.files_modified}")
        print(f"Total links converted to bold: {self.links_converted}")
        print("All remaining broken wikilinks have been converted to bold text.")

def main():
    converter = BrokenLinkConverter()
    converter.convert_all_broken_links()
    converter.generate_report()

if __name__ == "__main__":
    main()