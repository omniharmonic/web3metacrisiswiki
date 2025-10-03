#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function getAllExistingFiles(dir, files = []) {
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const filepath = path.join(dir, item);
    const stat = fs.statSync(filepath);

    if (stat.isDirectory()) {
      getAllExistingFiles(filepath, files);
    } else if (item.endsWith('.md')) {
      const basename = path.basename(item, '.md');
      files.push({
        filename: basename,
        path: filepath,
        variants: generateVariants(basename)
      });
    }
  }

  return files;
}

function generateVariants(filename) {
  const variants = new Set();

  // Original
  variants.add(filename);

  // Case variants
  variants.add(filename.toLowerCase());
  variants.add(filename.toUpperCase());

  // Space/hyphen variants
  variants.add(filename.replace(/\s+/g, '-'));
  variants.add(filename.replace(/-/g, ' '));

  // Title case
  const titleCase = filename.replace(/\w\S*/g, (txt) =>
    txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  );
  variants.add(titleCase);

  // Remove parentheses content
  variants.add(filename.replace(/\s*\([^)]*\)/g, ''));

  // Plural/singular
  if (filename.endsWith('s') && filename.length > 3) {
    variants.add(filename.slice(0, -1));
  }
  if (!filename.endsWith('s')) {
    variants.add(filename + 's');
  }

  return Array.from(variants);
}

function createWikilinkMappings(existingFiles) {
  const mappings = new Map();

  existingFiles.forEach(file => {
    file.variants.forEach(variant => {
      const key = variant.toLowerCase().trim();
      if (!mappings.has(key)) {
        mappings.set(key, file.filename);
      }
    });
  });

  return mappings;
}

function fixWikilinksInFile(filepath, mappings, contentDir) {
  try {
    const content = fs.readFileSync(filepath, 'utf8');
    const relativePath = path.relative(contentDir, filepath);

    let newContent = content;
    let changesMade = 0;
    const fixes = [];

    // Find all wikilinks
    const wikilinkRegex = /\[\[([^\]]+)\]\]/g;

    newContent = newContent.replace(wikilinkRegex, (match, target) => {
      const cleanTarget = target.trim();
      const targetKey = cleanTarget.toLowerCase();

      // Check if this wikilink has a mapping to an existing file
      if (mappings.has(targetKey)) {
        const correctFilename = mappings.get(targetKey);

        // Only fix if it's different from the target
        if (correctFilename !== cleanTarget) {
          const newLink = `[[${correctFilename}]]`;
          fixes.push({
            original: match,
            fixed: newLink,
            target: cleanTarget,
            correctFilename
          });
          changesMade++;
          return newLink;
        }
      }

      return match;
    });

    if (changesMade > 0) {
      fs.writeFileSync(filepath, newContent);
      return { file: relativePath, fixes, changesMade };
    }

    return null;
  } catch (err) {
    console.error(`Error processing ${filepath}:`, err.message);
    return null;
  }
}

function fixAllExistingWikilinks(contentDir) {
  console.log('Fixing broken wikilinks to existing files...\n');

  const existingFiles = getAllExistingFiles(contentDir);
  const mappings = createWikilinkMappings(existingFiles);

  console.log(`Found ${existingFiles.length} existing files`);
  console.log(`Created ${mappings.size} mapping variants\n`);

  let totalFilesFixed = 0;
  let totalLinksFixed = 0;
  const allFixes = [];

  function processDirectory(dir) {
    const items = fs.readdirSync(dir);

    for (const item of items) {
      const filepath = path.join(dir, item);
      const stat = fs.statSync(filepath);

      if (stat.isDirectory()) {
        processDirectory(filepath);
      } else if (item.endsWith('.md')) {
        const result = fixWikilinksInFile(filepath, mappings, contentDir);
        if (result) {
          console.log(`✅ Fixed ${result.file} (${result.changesMade} links)`);
          totalFilesFixed++;
          totalLinksFixed += result.changesMade;
          allFixes.push(result);
        }
      }
    }
  }

  processDirectory(contentDir);

  console.log(`\n📊 SUMMARY:`);
  console.log(`   Files updated: ${totalFilesFixed}`);
  console.log(`   Total wikilinks fixed: ${totalLinksFixed}`);

  if (allFixes.length > 0) {
    console.log(`\n🔧 TOP FIXES APPLIED:`);

    // Group fixes by target concept
    const conceptFixes = new Map();
    allFixes.forEach(fileResult => {
      fileResult.fixes.forEach(fix => {
        const key = fix.correctFilename;
        if (!conceptFixes.has(key)) {
          conceptFixes.set(key, 0);
        }
        conceptFixes.set(key, conceptFixes.get(key) + 1);
      });
    });

    // Show top fixed concepts
    const sortedConcepts = Array.from(conceptFixes.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);

    sortedConcepts.forEach(([concept, count], index) => {
      console.log(`   ${index + 1}. [[${concept}]]: ${count} links fixed`);
    });
  }

  return totalLinksFixed;
}

// Main execution
const contentDir = path.join(__dirname, 'content');

if (!fs.existsSync(contentDir)) {
  console.error('Content directory not found!');
  process.exit(1);
}

const totalFixed = fixAllExistingWikilinks(contentDir);

if (totalFixed > 0) {
  console.log('\n✅ Wikilink fixes complete!');
  console.log('💡 Run the broken links analysis again to see remaining missing concepts.');
} else {
  console.log('\n✅ No wikilink fixes needed.');
}

console.log('\nDone!');