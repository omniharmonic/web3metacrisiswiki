#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function fixMalformedWikilinks(contentDir) {
  console.log('Finding and fixing malformed wikilinks...\n');

  let totalFixed = 0;
  const fixes = [];

  function processFile(filepath) {
    try {
      const content = fs.readFileSync(filepath, 'utf8');
      const relativePath = path.relative(contentDir, filepath);

      // Find wikilinks with full paths
      const malformedRegex = /\[\[content\/[^|\]]+\|?([^\]]*)\]\]/g;
      let hasChanges = false;
      let newContent = content;

      let match;
      while ((match = malformedRegex.exec(content)) !== null) {
        const fullMatch = match[0];
        const pathPart = match[0].match(/\[\[content\/([^|\]]+)/)[1];
        const displayText = match[1] || '';

        // Extract just the filename without extension
        const fileName = path.basename(pathPart, '.md');

        // Create proper wikilink
        const properLink = displayText ? `[[${fileName}|${displayText}]]` : `[[${fileName}]]`;

        // Replace in content
        newContent = newContent.replace(fullMatch, properLink);
        hasChanges = true;

        fixes.push({
          file: relativePath,
          original: fullMatch,
          fixed: properLink,
          concept: fileName
        });

        totalFixed++;
      }

      // Also fix simple content/ path references without pipes
      const simplePathRegex = /\[\[content\/([^|\]]+)\]\]/g;
      newContent = newContent.replace(simplePathRegex, (match, pathPart) => {
        const fileName = path.basename(pathPart, '.md');
        const properLink = `[[${fileName}]]`;

        if (match !== properLink) {
          fixes.push({
            file: relativePath,
            original: match,
            fixed: properLink,
            concept: fileName
          });
          totalFixed++;
          hasChanges = true;
        }

        return properLink;
      });

      if (hasChanges) {
        fs.writeFileSync(filepath, newContent);
        console.log(`✅ Fixed ${relativePath}`);
      }

    } catch (err) {
      console.error(`Error processing ${filepath}:`, err.message);
    }
  }

  function scanDirectory(dir) {
    const files = fs.readdirSync(dir);

    for (const file of files) {
      const filepath = path.join(dir, file);
      const stat = fs.statSync(filepath);

      if (stat.isDirectory()) {
        scanDirectory(filepath);
      } else if (file.endsWith('.md')) {
        processFile(filepath);
      }
    }
  }

  scanDirectory(contentDir);

  console.log(`\n📊 SUMMARY:`);
  console.log(`   Total malformed wikilinks fixed: ${totalFixed}`);

  if (fixes.length > 0) {
    console.log(`\n🔧 FIXES APPLIED:`);

    // Group by concept
    const conceptGroups = {};
    fixes.forEach(fix => {
      if (!conceptGroups[fix.concept]) {
        conceptGroups[fix.concept] = [];
      }
      conceptGroups[fix.concept].push(fix);
    });

    Object.keys(conceptGroups).forEach(concept => {
      const conceptFixes = conceptGroups[concept];
      console.log(`\n   [[${concept}]] (${conceptFixes.length} fixes):`);
      conceptFixes.slice(0, 3).forEach(fix => {
        console.log(`     ${fix.file}: ${fix.original} → ${fix.fixed}`);
      });
      if (conceptFixes.length > 3) {
        console.log(`     ... and ${conceptFixes.length - 3} more`);
      }
    });
  }

  return totalFixed;
}

// Main execution
const contentDir = path.join(__dirname, 'content');

if (!fs.existsSync(contentDir)) {
  console.error('Content directory not found!');
  process.exit(1);
}

const totalFixed = fixMalformedWikilinks(contentDir);

if (totalFixed > 0) {
  console.log('\n✅ Malformed wikilinks have been fixed!');
  console.log('💡 Run the broken links analysis again to see the updated results.');
} else {
  console.log('\n✅ No malformed wikilinks found.');
}

console.log('\nDone!');