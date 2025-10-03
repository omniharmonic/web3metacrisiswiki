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
      slugs.add(basename);
      slugs.add(basename.toLowerCase());
      slugs.add(basename.toLowerCase().replace(/\s+/g, '-'));

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
        file: filepath,
        line: content.substring(0, match.index).split('\n').length
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

  const titleCase = target.replace(/\w\S*/g, (txt) =>
    txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  ).replace(/\s+/g, '-');
  variants.add(titleCase);

  const kebabCase = target
    .replace(/([A-Z])/g, '-$1')
    .toLowerCase()
    .replace(/^-/, '');
  variants.add(kebabCase);

  return Array.from(variants);
}

function categorizeConcept(concept) {
  const lowerConcept = concept.toLowerCase();

  // Core Web3 & Blockchain
  if (lowerConcept.includes('dao') || lowerConcept.includes('defi') ||
      lowerConcept.includes('blockchain') || lowerConcept.includes('smart contract') ||
      lowerConcept.includes('ethereum') || lowerConcept.includes('web3') ||
      lowerConcept.includes('token') || lowerConcept.includes('nft') ||
      lowerConcept.includes('crypto') || lowerConcept.includes('proof of')) {
    return 'Core Web3 & Blockchain';
  }

  // Governance & Democracy
  if (lowerConcept.includes('governance') || lowerConcept.includes('democra') ||
      lowerConcept.includes('voting') || lowerConcept.includes('participation') ||
      lowerConcept.includes('consensus') || lowerConcept.includes('collective')) {
    return 'Governance & Democracy';
  }

  // Economics & Finance
  if (lowerConcept.includes('economic') || lowerConcept.includes('financial') ||
      lowerConcept.includes('market') || lowerConcept.includes('capital') ||
      lowerConcept.includes('income') || lowerConcept.includes('cooperative') ||
      lowerConcept.includes('wealth')) {
    return 'Economics & Finance';
  }

  // Environment & Ecology
  if (lowerConcept.includes('climate') || lowerConcept.includes('ecological') ||
      lowerConcept.includes('environment') || lowerConcept.includes('carbon') ||
      lowerConcept.includes('ecosystem') || lowerConcept.includes('regenerative') ||
      lowerConcept.includes('biodiversity')) {
    return 'Environment & Ecology';
  }

  // Social & Community
  if (lowerConcept.includes('social') || lowerConcept.includes('community') ||
      lowerConcept.includes('digital commons') || lowerConcept.includes('cooperation') ||
      lowerConcept.includes('collaboration')) {
    return 'Social & Community';
  }

  // Privacy & Security
  if (lowerConcept.includes('privacy') || lowerConcept.includes('security') ||
      lowerConcept.includes('surveillance') || lowerConcept.includes('encryption') ||
      lowerConcept.includes('zero-knowledge')) {
    return 'Privacy & Security';
  }

  // Cognitive & Behavioral
  if (lowerConcept.includes('bias') || lowerConcept.includes('cognitive') ||
      lowerConcept.includes('behavioral') || lowerConcept.includes('epistemic') ||
      lowerConcept.includes('information')) {
    return 'Cognitive & Behavioral';
  }

  return 'Other';
}

function analyzeFrequency(contentDir) {
  console.log('Analyzing broken wikilink frequencies...\n');

  const allSlugs = getAllPageSlugs(contentDir);
  const brokenLinkCounts = new Map();
  const brokenLinkFiles = new Map();

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
          const variants = generateTargetVariants(link.target);
          const hasMatch = variants.some(variant => allSlugs.has(variant));

          if (!hasMatch) {
            const count = brokenLinkCounts.get(link.target) || 0;
            brokenLinkCounts.set(link.target, count + 1);

            if (!brokenLinkFiles.has(link.target)) {
              brokenLinkFiles.set(link.target, []);
            }
            brokenLinkFiles.get(link.target).push({
              file: relativePath,
              line: link.line
            });
          }
        }
      }
    }
  }

  scanDirectory(contentDir);

  // Sort by frequency
  const sortedByFrequency = Array.from(brokenLinkCounts.entries())
    .sort((a, b) => b[1] - a[1]);

  // Categorize concepts
  const categorized = new Map();
  sortedByFrequency.forEach(([concept, count]) => {
    const category = categorizeConcept(concept);
    if (!categorized.has(category)) {
      categorized.set(category, []);
    }
    categorized.get(category).push({ concept, count, files: brokenLinkFiles.get(concept) });
  });

  return { sortedByFrequency, categorized, brokenLinkFiles };
}

// Main execution
const contentDir = path.join(__dirname, 'content');

if (!fs.existsSync(contentDir)) {
  console.error('Content directory not found!');
  process.exit(1);
}

const { sortedByFrequency, categorized, brokenLinkFiles } = analyzeFrequency(contentDir);

console.log('🔥 TOP 50 MOST FREQUENTLY REFERENCED MISSING CONCEPTS:\n');
sortedByFrequency.slice(0, 50).forEach(([concept, count], index) => {
  console.log(`${(index + 1).toString().padStart(2)}. [[${concept}]] (${count} references)`);
});

console.log('\n📊 BY CATEGORY:\n');
for (const [category, concepts] of categorized) {
  const topConcepts = concepts.slice(0, 10);
  console.log(`## ${category.toUpperCase()} (${concepts.length} total concepts)`);
  topConcepts.forEach(({ concept, count }, index) => {
    console.log(`   ${index + 1}. [[${concept}]] (${count}x)`);
  });
  if (concepts.length > 10) {
    console.log(`   ... and ${concepts.length - 10} more`);
  }
  console.log('');
}

console.log('\n🎯 STRATEGIC PRIORITY RECOMMENDATIONS:\n');

// High-impact concepts (referenced 5+ times)
const highImpact = sortedByFrequency.filter(([concept, count]) => count >= 5);
console.log(`**TIER 1 - HIGH IMPACT** (${highImpact.length} concepts, 5+ references each):`);
highImpact.slice(0, 20).forEach(([concept, count]) => {
  console.log(`   - [[${concept}]] (${count}x)`);
});

console.log(`\n**TIER 2 - MEDIUM IMPACT** (3-4 references each):`);
const mediumImpact = sortedByFrequency.filter(([concept, count]) => count >= 3 && count < 5);
mediumImpact.slice(0, 15).forEach(([concept, count]) => {
  console.log(`   - [[${concept}]] (${count}x)`);
});

console.log(`\n**TIER 3 - FOUNDATIONAL** (2 references each):`);
const foundational = sortedByFrequency.filter(([concept, count]) => count === 2);
console.log(`   ${foundational.length} concepts with 2 references each`);

console.log('\nDone!');