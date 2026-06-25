// SITE-authored test (v0.2). Run after a build with `npm test` (= ssg test).
// It runs on top of the engine's standard checks (unresolved placeholders,
// broken links, etc.) and asserts demo-specific facts. Receives:
//   ctx = { siteRoot, buildDir, read(file), check(name, ok, detail), standardChecks }
module.exports = ({ read, check }) => {
  const home = read('index.html');
  // The registry-mapped site component rendered (Phase A).
  check('home shows the testimonials section', /class="testimonials/.test(home));
  // Its declared sub-component expanded for each quote (Phase B).
  check('testimonials render individual quotes', (home.match(/class="testimonial /g) || []).length >= 2);
  // The site component's CSS was collected and linked.
  check('testimonials CSS linked', /assets\/css\/testimonials\.css/.test(home));
  // The site generator emitted its pages (Phase C).
  check('guides generator produced a page', read('guide-choosing-the-right-brick.html').length > 0);
  // The bundled engine generator still works alongside the site one.
  check('shop lists products', /product-card/.test(read('shop.html')));
};
