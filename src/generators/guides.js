// SITE-authored data-only generator (v0.3 contract). Resolved by name ("guides")
// via generators/registry.json and driven by the pages/guides template page. It has
// no collection (a hardcoded list), so it ignores ctx.collection.
//   generate(ctx, options) -> [{ slug, title, description, vars }]
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
    const { slugify } = ctx.lib;
    return GUIDES.map(guide => ({
      slug: slugify(guide.title),
      title: guide.title,
      description: guide.body,
      vars: { GUIDE_TITLE: guide.title, GUIDE_BODY: guide.body }
    }));
  }
};
