# brickwork-demo

A demo storefront showcasing the [**brickwork-ssg**](https://github.com/Dimitriuses/brickwork-ssg)
static-site engine. The engine is embedded here as a **git submodule** at `engine/`;
this repo holds only the site's content (`config.json`, `pages/`, `assets/`, `shared/`).

> **Provenance:** this repository was extracted from a larger private project and
> later separated alongside the independent `brickwork-ssg` engine. The current
> commit history does not reflect the full development timeline.

## Build

```bash
git clone --recurse-submodules <this-repo-url>
npm run build            # -> build/   (runs: node engine/cli.js build)
```

Cloned without submodules? Fetch the engine:

```bash
git submodule update --init --recursive
```

## What it showcases

Beyond the built-in components and product generator, this site exercises the
engine's **site-extension** surface without modifying the engine:

- **A site component** — `components/blocks/testimonials/`, mapped by
  `components/registry.json` and rendered on the home page. It declares its own
  sub-component (`testimonials.json` → `testimonial`) and uses the build-script
  helpers (`raw`, `escapeHtml`).
- **A site generator** — a `pages/guides` **template page** drives the data-only
  `generators/guides.js` (mapped in `generators/registry.json`) to emit a static
  "buying guide" page per entry via the `generate(ctx, options)` contract.
- **Product pages** — a `pages/product-detail` template page turns the `products`
  collection into one detail page each via the built-in `products` generator.
- **Site tests** — `test/demo.test.js`, run with `npm test` (= `ssg test`) after
  a build, on top of the engine's standard checks.
- **Theming** — `assets/css/global.css` reskins the storefront by overriding the
  engine's `--bw-*` CSS variables (no component edits).

```bash
npm test                 # build, then run standard checks + test/*.test.js
```

## Admin panel (optional)

```bash
npm --prefix engine install   # one-time: install the engine's admin deps
npm run admin                 # http://localhost:3000
```

## Update the engine

```bash
git -C engine fetch
git -C engine checkout <commit-or-tag>
git add engine && git commit -m "bump engine"
```

## Deploy

The static output is in `build/`. Point any static host (Netlify, GitHub Pages, …)
at build command `npm run build` and publish directory `build/`.
