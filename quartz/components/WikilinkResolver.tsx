import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

export default (() => {
  const WikilinkResolver: QuartzComponent = ({ allFiles }: QuartzComponentProps) => {
    // Generate page slugs for lookup
    const pageSlugSet = new Set(allFiles.map(file => file.slug))

    // Generate alias variants for a title
    const generateAliases = (title: string): string[] => {
      const aliases = []

      // Original title
      aliases.push(title)

      // Lowercase with spaces replaced by hyphens
      aliases.push(title.toLowerCase().replace(/\s+/g, '-'))

      // Lowercase
      aliases.push(title.toLowerCase())

      // Title case to kebab-case
      aliases.push(title.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, ''))

      // Remove duplicates
      return [...new Set(aliases)]
    }

    const script = `
      (function() {
        const pageSet = new Set(${JSON.stringify([...pageSlugSet])});

        function generateAliases(title) {
          const aliases = [];
          aliases.push(title);
          aliases.push(title.toLowerCase().replace(/\\s+/g, '-'));
          aliases.push(title.toLowerCase());
          aliases.push(title.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, ''));
          return [...new Set(aliases)];
        }

        function resolveWikilinks() {
          // Find all text nodes that contain [[...]]
          const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
          );

          const textNodes = [];
          let node;
          while (node = walker.nextNode()) {
            if (node.textContent.includes('[[') && node.textContent.includes(']]')) {
              textNodes.push(node);
            }
          }

          textNodes.forEach(textNode => {
            const text = textNode.textContent;
            const newHTML = text.replace(/\\[\\[([^\\]]+)\\]\\]/g, function(match, title) {
              const aliases = generateAliases(title.trim());

              for (const alias of aliases) {
                if (pageSet.has(alias)) {
                  return '<a href="/' + alias + '" class="internal-link">' + title + '</a>';
                }
              }

              // If no match found, mark as broken link
              return '<span class="broken-link">' + title + '</span>';
            });

            if (newHTML !== text) {
              const wrapper = document.createElement('span');
              wrapper.innerHTML = newHTML;
              textNode.parentNode.replaceChild(wrapper, textNode);
            }
          });
        }

        // Run after page load
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', resolveWikilinks);
        } else {
          resolveWikilinks();
        }
      })();
    `

    return (
      <script dangerouslySetInnerHTML={{ __html: script }} />
    )
  }

  WikilinkResolver.displayName = "WikilinkResolver"
  return WikilinkResolver
}) satisfies QuartzComponentConstructor