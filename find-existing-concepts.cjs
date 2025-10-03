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
      const relativePath = path.relative(dir, filepath);

      files.push({
        filename: basename,
        path: relativePath,
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
  variants.add(filename.replace(/\s+/g, '-').toLowerCase());
  variants.add(filename.replace(/-/g, ' ').toLowerCase());

  // Title case
  const titleCase = filename.replace(/\w\S*/g, (txt) =>
    txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  );
  variants.add(titleCase);
  variants.add(titleCase.replace(/\s+/g, '-'));

  // Parentheses handling
  variants.add(filename.replace(/\s*\([^)]*\)/g, ''));
  variants.add(filename.replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, '-'));

  // Plural/singular variants
  if (filename.endsWith('s') && filename.length > 3) {
    const singular = filename.slice(0, -1);
    variants.add(singular);
    variants.add(singular.replace(/\s+/g, '-'));
  }
  if (!filename.endsWith('s')) {
    variants.add(filename + 's');
    variants.add((filename + 's').replace(/\s+/g, '-'));
  }

  return Array.from(variants);
}

function findBrokenWikilinks(contentDir) {
  const files = getAllExistingFiles(contentDir);
  const brokenLinks = [];

  function scanFile(filepath) {
    try {
      const content = fs.readFileSync(filepath, 'utf8');
      const wikilinkRegex = /\[\[([^\]]+)\]\]/g;
      let match;

      while ((match = wikilinkRegex.exec(content)) !== null) {
        const target = match[1].trim();
        brokenLinks.push({
          target,
          file: path.relative(contentDir, filepath),
          line: content.substring(0, match.index).split('\n').length
        });
      }
    } catch (err) {
      // Skip files that can't be read
    }
  }

  function scanDirectory(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const filepath = path.join(dir, item);
      const stat = fs.statSync(filepath);

      if (stat.isDirectory()) {
        scanDirectory(filepath);
      } else if (item.endsWith('.md')) {
        scanFile(filepath);
      }
    }
  }

  scanDirectory(contentDir);
  return brokenLinks;
}

function analyzeExistingVsMissing(contentDir) {
  console.log('Analyzing existing files vs broken wikilinks...\n');

  const existingFiles = getAllExistingFiles(contentDir);
  const brokenLinks = findBrokenWikilinks(contentDir);

  // Create lookup maps
  const filenameToPath = new Map();
  const variantToFile = new Map();

  existingFiles.forEach(file => {
    filenameToPath.set(file.filename, file.path);
    file.variants.forEach(variant => {
      if (!variantToFile.has(variant.toLowerCase())) {
        variantToFile.set(variant.toLowerCase(), []);
      }
      variantToFile.get(variant.toLowerCase()).push(file);
    });
  });

  // Analyze broken links
  const linkCounts = new Map();
  brokenLinks.forEach(link => {
    const count = linkCounts.get(link.target) || 0;
    linkCounts.set(link.target, count + 1);
  });

  const sortedBrokenLinks = Array.from(linkCounts.entries())
    .sort((a, b) => b[1] - a[1]);

  // Find matches
  const existingMatches = [];
  const trulyMissing = [];

  sortedBrokenLinks.forEach(([target, count]) => {
    const targetLower = target.toLowerCase();
    const matches = variantToFile.get(targetLower) || [];

    if (matches.length > 0) {
      existingMatches.push({
        brokenLink: target,
        count,
        matches: matches.map(m => ({ filename: m.filename, path: m.path }))
      });
    } else {
      // Try partial matches
      const partialMatches = [];
      for (const [variant, files] of variantToFile) {
        if (variant.includes(targetLower) || targetLower.includes(variant)) {
          partialMatches.push(...files);
        }
      }

      if (partialMatches.length > 0) {
        existingMatches.push({
          brokenLink: target,
          count,
          matches: partialMatches.map(m => ({ filename: m.filename, path: m.path })),
          partial: true
        });
      } else {
        trulyMissing.push({ target, count });
      }
    }
  });

  return { existingMatches, trulyMissing, totalBroken: sortedBrokenLinks.length };
}

// Main execution
const contentDir = path.join(__dirname, 'content');

if (!fs.existsSync(contentDir)) {
  console.error('Content directory not found!');
  process.exit(1);
}

const { existingMatches, trulyMissing, totalBroken } = analyzeExistingVsMissing(contentDir);

console.log('📊 SUMMARY:');
console.log(`   Total broken wikilink targets: ${totalBroken}`);
console.log(`   Have existing files: ${existingMatches.length}`);
console.log(`   Truly missing: ${trulyMissing.length}`);

console.log('\n🎯 BROKEN LINKS TO EXISTING FILES (Top 30):');
existingMatches
  .sort((a, b) => b.count - a.count)
  .slice(0, 30)
  .forEach((item, index) => {
    const matchInfo = item.matches.length === 1
      ? item.matches[0].filename
      : `${item.matches.length} matches`;

    const partialNote = item.partial ? ' (partial match)' : '';
    console.log(`${(index + 1).toString().padStart(2)}. [[${item.brokenLink}]] (${item.count}x) → ${matchInfo}${partialNote}`);

    if (item.matches.length > 1) {
      item.matches.slice(0, 3).forEach(match => {
        console.log(`       - ${match.filename} (${match.path})`);
      });
      if (item.matches.length > 3) {
        console.log(`       ... and ${item.matches.length - 3} more`);
      }
    }
  });

console.log('\n❌ TRULY MISSING CONCEPTS (Top 20):');
trulyMissing
  .sort((a, b) => b.count - a.count)
  .slice(0, 20)
  .forEach((item, index) => {
    console.log(`${(index + 1).toString().padStart(2)}. [[${item.target}]] (${item.count}x)`);
  });

console.log(`\n💡 RECOMMENDATION:`);
console.log(`   1. First fix the ${existingMatches.length} broken links to existing files`);
console.log(`   2. Then create pages for the ${trulyMissing.length} truly missing concepts`);
console.log(`   3. This will resolve ${existingMatches.reduce((sum, item) => sum + item.count, 0)} broken wikilinks immediately!`);

console.log('\nDone!');