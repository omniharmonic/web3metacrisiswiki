#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function getAllPageSlugs(dir, slugs = new Set()) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const filepath = path.join(dir, file);
    const stat = fs.statSync(filepath);

    if (stat.isDirectory()) {
      getAllPageSlugs(filepath, slugs);
    } else if (file.endsWith('.md')) {
      const basename = path.basename(file, '.md');

      // Add various slug variants
      slugs.add(basename);
      slugs.add(basename.toLowerCase());
      slugs.add(basename.toLowerCase().replace(/\s+/g, '-'));

      // Also check for aliases in frontmatter
      try {
        const content = fs.readFileSync(filepath, 'utf8');
        if (content.startsWith('---')) {
          const frontmatterEnd = content.indexOf('---', 3);
          if (frontmatterEnd !== -1) {
            const frontmatter = content.slice(0, frontmatterEnd);
            const aliasMatches = frontmatter.match(/aliases:\s*\n((?:\s*-\s*"[^"]*"\s*\n)*)/);
            if (aliasMatches) {
              const aliasSection = aliasMatches[1];
              const aliases = aliasSection.match(/- "([^"]*)"/g);
              if (aliases) {
                aliases.forEach(alias => {
                  const cleanAlias = alias.replace(/- "([^"]*)"/, '$1');
                  slugs.add(cleanAlias);
                  slugs.add(cleanAlias.toLowerCase());
                  slugs.add(cleanAlias.toLowerCase().replace(/\s+/g, '-'));
                });
              }
            }
          }
        }
      } catch (err) {
        // Skip files that can't be read
      }
    }
  }

  return slugs;
}

function findWikilinksInFile(filepath) {
  try {
    const content = fs.readFileSync(filepath, 'utf8');
    const wikilinkRegex = /\[\[([^\]]+)\]\]/g;
    const wikilinks = [];
    let match;

    while ((match = wikilinkRegex.exec(content)) !== null) {
      const target = match[1].trim();
      wikilinks.push({
        target,
        line: content.substring(0, match.index).split('\n').length,
        context: match[0]
      });
    }

    return wikilinks;
  } catch (err) {
    return [];
  }
}

function generateTargetVariants(target) {
  const variants = new Set();

  variants.add(target);
  variants.add(target.toLowerCase());
  variants.add(target.toLowerCase().replace(/\s+/g, '-'));

  // Title case with spaces to hyphens
  const titleCase = target.replace(/\w\S*/g, (txt) =>
    txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  ).replace(/\s+/g, '-');
  variants.add(titleCase);

  // CamelCase to kebab-case
  const kebabCase = target
    .replace(/([A-Z])/g, '-$1')
    .toLowerCase()
    .replace(/^-/, '');
  variants.add(kebabCase);

  return Array.from(variants);
}

function findBrokenWikilinks(contentDir) {
  console.log('Scanning for all pages and aliases...');
  const allSlugs = getAllPageSlugs(contentDir);
  console.log(`Found ${allSlugs.size} page slugs and aliases`);

  console.log('\nScanning for wikilinks...');
  const brokenLinks = [];
  const allLinks = [];

  function scanDirectory(dir) {
    const files = fs.readdirSync(dir);

    for (const file of files) {
      const filepath = path.join(dir, file);
      const stat = fs.statSync(filepath);

      if (stat.isDirectory()) {
        scanDirectory(filepath);
      } else if (file.endsWith('.md')) {
        const relativePath = path.relative(contentDir, filepath);
        const wikilinks = findWikilinksInFile(filepath);

        for (const link of wikilinks) {
          allLinks.push({
            file: relativePath,
            ...link
          });

          // Check if any variant of this target exists
          const variants = generateTargetVariants(link.target);
          const hasMatch = variants.some(variant => allSlugs.has(variant));

          if (!hasMatch) {
            brokenLinks.push({
              file: relativePath,
              ...link
            });
          }
        }
      }
    }
  }

  scanDirectory(contentDir);

  return { brokenLinks, allLinks, totalSlugs: allSlugs.size };
}

// Main execution
const contentDir = path.join(__dirname, 'content');

if (!fs.existsSync(contentDir)) {
  console.error('Content directory not found!');
  process.exit(1);
}

console.log('Finding broken wikilinks...\n');

const { brokenLinks, allLinks, totalSlugs } = findBrokenWikilinks(contentDir);

console.log(`\n📊 SUMMARY:`);
console.log(`   Total pages/aliases: ${totalSlugs}`);
console.log(`   Total wikilinks: ${allLinks.length}`);
console.log(`   Broken wikilinks: ${brokenLinks.length}`);
console.log(`   Success rate: ${((allLinks.length - brokenLinks.length) / allLinks.length * 100).toFixed(1)}%`);

if (brokenLinks.length > 0) {
  console.log(`\n❌ BROKEN WIKILINKS (${brokenLinks.length}):`);

  // Group by target for easier reading
  const grouped = {};
  brokenLinks.forEach(link => {
    if (!grouped[link.target]) {
      grouped[link.target] = [];
    }
    grouped[link.target].push(link);
  });

  Object.keys(grouped).sort().forEach(target => {
    console.log(`\n   [[${target}]]:`);
    grouped[target].forEach(link => {
      console.log(`     ${link.file}:${link.line}`);
    });
  });

  // Generate list of unique broken targets
  const uniqueBrokenTargets = [...new Set(brokenLinks.map(link => link.target))].sort();
  console.log(`\n📝 UNIQUE BROKEN TARGETS (${uniqueBrokenTargets.length}):`);
  uniqueBrokenTargets.forEach(target => {
    console.log(`   - [[${target}]]`);
  });

} else {
  console.log(`\n✅ No broken wikilinks found! All links are working.`);
}

console.log('\nDone!');