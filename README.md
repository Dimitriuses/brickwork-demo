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
