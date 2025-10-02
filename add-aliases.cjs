#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function generateAliases(filename) {
  const basename = path.basename(filename, '.md');
  const aliases = new Set();

  // Original filename
  aliases.add(basename);

  // Lowercase
  aliases.add(basename.toLowerCase());

  // Lowercase with spaces to hyphens
  aliases.add(basename.toLowerCase().replace(/\s+/g, '-'));

  // Title case with spaces to hyphens
  const titleCase = basename.replace(/\w\S*/g, (txt) =>
    txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  ).replace(/\s+/g, '-');
  aliases.add(titleCase);

  // CamelCase to kebab-case
  const kebabCase = basename
    .replace(/([A-Z])/g, '-$1')
    .toLowerCase()
    .replace(/^-/, '');
  aliases.add(kebabCase);

  // Remove the original (it shouldn't be an alias to itself)
  aliases.delete(basename);

  return Array.from(aliases).filter(alias => alias !== basename);
}

function addAliasesToFile(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const basename = path.basename(filepath, '.md');
  const aliases = generateAliases(filepath);

  // Check if file already has frontmatter
  if (content.startsWith('---')) {
    // Has frontmatter, check if aliases already exist
    const frontmatterEnd = content.indexOf('---', 3);
    const frontmatter = content.slice(0, frontmatterEnd + 3);
    const body = content.slice(frontmatterEnd + 3);

    if (frontmatter.includes('aliases:')) {
      console.log(`Skipping ${basename} - already has aliases`);
      return;
    }

    // Add aliases to existing frontmatter
    const newFrontmatter = frontmatter.slice(0, -3) +
      `aliases:\n${aliases.map(alias => `  - "${alias}"`).join('\n')}\n---`;

    const newContent = newFrontmatter + body;
    fs.writeFileSync(filepath, newContent);
    console.log(`Added aliases to ${basename}`);
  } else {
    // No frontmatter, add it
    const frontmatter = `---
aliases:
${aliases.map(alias => `  - "${alias}"`).join('\n')}
---

`;

    const newContent = frontmatter + content;
    fs.writeFileSync(filepath, newContent);
    console.log(`Created frontmatter with aliases for ${basename}`);
  }
}

function processDirectory(dir) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const filepath = path.join(dir, file);
    const stat = fs.statSync(filepath);

    if (stat.isDirectory()) {
      processDirectory(filepath);
    } else if (file.endsWith('.md')) {
      addAliasesToFile(filepath);
    }
  }
}

// Process the content directory
const contentDir = path.join(__dirname, 'content');
if (fs.existsSync(contentDir)) {
  console.log('Adding aliases to all markdown files...');
  processDirectory(contentDir);
  console.log('Done!');
} else {
  console.error('Content directory not found!');
}