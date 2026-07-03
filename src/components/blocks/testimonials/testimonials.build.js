// SITE-authored component showcasing the v0.2 extensibility surface:
//   - resolved site-first via components/registry.json ("testimonials" -> blocks/testimonials)
//   - declares its own sub-component (testimonial) in testimonials.json
//   - receives the engine helpers as a 4th argument; uses `raw` to insert the
//     assembled rows as HTML through replaceVariables (which escapes by default).
function build(vars, loadComponent, replaceVariables, helpers) {
  const { raw, escapeHtml } = helpers;
  const quotes = Array.isArray(vars.QUOTES) ? vars.QUOTES : [];
  const row = loadComponent('testimonial');
  const items = quotes
    .map(q => replaceVariables(row, {
      QUOTE: q.quote || '',
      AUTHOR: q.author || 'Anonymous',
      // Inline markup, so opt out of auto-escaping after escaping the text.
      ROLE: q.role ? raw(`<span class="d-block">${escapeHtml(q.role)}</span>`) : ''
    }))
    .join('');
  return replaceVariables(loadComponent('testimonials'), {
    TESTIMONIALS_TITLE: vars.TESTIMONIALS_TITLE || 'What builders say',
    TESTIMONIALS_SUBTITLE: vars.TESTIMONIALS_SUBTITLE || '',
    TESTIMONIALS_ITEMS: raw(items)
  });
}

module.exports = { build };
