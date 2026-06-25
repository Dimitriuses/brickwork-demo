// SITE-authored generator (v0.2 contract): module.exports = { generate(ctx) }.
// Emits one static "buying guide" page per entry, proving a site can add its own
// generator alongside the engine's product generators. ctx provides:
//   { siteRoot, engineRoot, buildDir, outputDir, lib: { slugify, escapeHtml, raw } }
const fs = require('fs');
const path = require('path');

const GUIDES = [
  {
    title: 'Choosing the right brick',
    body: 'Match the brick to the load. Engineering bricks for foundations and '
      + 'retaining walls; facing bricks where looks matter; commons where they '
      + 'will be rendered over.'
  },
  {
    title: 'How much mortar do I need?',
    body: 'As a rule of thumb, one bag of mortar lays roughly 50–60 standard '
      + 'bricks. Order ten percent extra for waste and pointing.'
  }
];

module.exports = {
  generate(ctx) {
    const { slugify, escapeHtml } = ctx.lib;
    const written = [];
    GUIDES.forEach(guide => {
      const slug = slugify(guide.title);
      const pageConfig = {
        page: `guide-${slug}`,
        title: guide.title,
        description: guide.body,
        header_theme: 'dark',
        layout: '_layout',
        components: [],
        content: `<main class="container py-5" style="padding-top:90px;">`
          + `<h1>${escapeHtml(guide.title)}</h1>`
          + `<p class="lead">${escapeHtml(guide.body)}</p>`
          + `<p><a href="shop.html">Browse the shop &rarr;</a></p></main>`
      };
      const file = path.join(ctx.outputDir, `_generated-guide-${slug}.json`);
      fs.writeFileSync(file, JSON.stringify(pageConfig, null, 2));
      written.push(file);
    });
    console.log(`[GUIDES] Generated ${written.length} guide page(s)`);
    return written;
  }
};
