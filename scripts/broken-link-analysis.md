# Comprehensive Broken Link Detection and Fixing Plan

## Overview
This plan outlines a systematic approach to find and fix broken links across the entire Web3 Meta-Crisis Wiki knowledge base.

## Phase 1: Automated Link Detection

### 1.1 Identify All Wikilinks
- Scan all `.md` files in `content/` directory
- Extract patterns: `[[link]]`, `[[link|display text]]`, `[[link#section]]`
- Create comprehensive inventory of all links used

### 1.2 Identify All File Targets
- Scan all `.md` files to create complete inventory of existing pages
- Include aliases from frontmatter as valid targets
- Account for different path structures (nested folders, etc.)

### 1.3 Cross-Reference Analysis
- Compare links against existing files
- Account for alias resolution (aliases in frontmatter should resolve)
- Identify case sensitivity issues
- Check for broken section links (`#` anchors)

## Phase 2: Categorize Broken Links

### 2.1 Missing Files
- Links to pages that don't exist at all
- Priority: Create missing high-impact pages or remove invalid links

### 2.2 Case Mismatches
- Links where filename exists but case doesn't match exactly
- Priority: Fix case to match actual filenames

### 2.3 Path Issues
- Links where target exists but path is incorrect
- Priority: Update paths to correct locations

### 2.4 Alias Issues
- Links to valid concepts but using non-standard alias
- Priority: Update to use canonical filename or add missing aliases

### 2.5 Section Links
- Links to sections that don't exist in target pages
- Priority: Fix section references or remove invalid anchors

## Phase 3: Automated Fixing Strategy

### 3.1 High-Confidence Fixes
- Case mismatches: Auto-fix to match existing files
- Path corrections: Auto-fix when target clearly exists elsewhere
- Simple typos: Auto-fix obvious misspellings

### 3.2 Alias Additions
- Add missing aliases to frontmatter when links use valid alternative names
- Standardize alias patterns for consistency

### 3.3 Manual Review Required
- Links to concepts that should exist but don't (create vs. remove decision)
- Ambiguous references where multiple targets possible
- Complex reorganization decisions

## Phase 4: Implementation Tools

### 4.1 Link Scanner Script
```bash
# Extract all wikilinks from all markdown files
find content -name "*.md" -exec grep -H -o '\[\[[^]]*\]\]' {} \;

# Extract all filenames and aliases
find content -name "*.md" -exec basename {} .md \;
grep -r "aliases:" content --include="*.md"
```

### 4.2 Cross-Reference Analysis
- Python script to parse markdown files
- Build comprehensive link->target mapping
- Generate broken link report with categorization

### 4.3 Automated Fixing
- Script to apply high-confidence fixes
- Backup system before making changes
- Batch processing with validation

## Phase 5: Quality Assurance

### 5.1 Build Validation
- Run Quartz build after fixes to ensure no new issues
- Check for any build warnings or errors

### 5.2 Spot Checking
- Manual verification of sample fixes
- Test that aliases work correctly
- Verify wikilink resolution in frontend

### 5.3 Continuous Monitoring
- Script to run periodic broken link checks
- Integration with content creation workflow

## Implementation Priority

1. **Phase 1**: Complete link inventory (immediate)
2. **Phase 2**: Categorize all broken links (immediate)
3. **Phase 3.1**: Implement high-confidence auto-fixes (immediate)
4. **Phase 3.2**: Add missing aliases (immediate)
5. **Phase 3.3**: Manual review of remaining issues (ongoing)
6. **Phase 4**: Build comprehensive tooling (as needed)
7. **Phase 5**: Quality assurance and monitoring (ongoing)

## Expected Outcomes

- Zero broken wikilinks in the knowledge base
- Consistent alias patterns across all pages
- Improved navigation and discoverability
- Robust system for preventing future broken links
- Better integration between related concepts

## Tools Needed

1. **Link Extraction**: grep, find, custom parsing script
2. **File Inventory**: filesystem scanning, frontmatter parsing
3. **Cross-Reference**: Python/Node.js script for analysis
4. **Batch Fixing**: sed, awk, custom replacement scripts
5. **Validation**: Quartz build process, custom verification

## Success Metrics

- Number of broken links reduced to zero
- All aliases properly configured
- Build process runs without link warnings
- Improved user navigation experience
- Faster content creation with reliable link infrastructure