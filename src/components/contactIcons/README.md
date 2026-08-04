# Contact Icons Component

A reusable component that displays social media icons with links configured from `config.json`.

## Features

- ✅ Reads links from `config.json`
- ✅ Bootstrap Icons for most platforms
- ✅ Custom SVG for Viber
- ✅ Hover animations
- ✅ Can be used anywhere with `{{COMPONENT:contactIcons}}`
- ✅ Works in nested components (e.g., inside footer)

## Configuration

### In config.json:

```json
{
  "social": {
    "telegram": "https://t.me/yourusername",
    "whatsapp": "https://wa.me/1234567890",
    "instagram": "https://instagram.com/yourusername",
    "signal": "https://signal.me/#p/+1234567890",
    "viber": "viber://chat?number=1234567890"
  }
}
```

### Supported Platforms:

- **telegram** - Telegram messenger
- **whatsapp** - WhatsApp
- **instagram** - Instagram
- **signal** - Signal messenger
- **viber** - Viber (uses custom SVG)
- **facebook** - Facebook
- **twitter** - Twitter/X
- **linkedin** - LinkedIn
- **youtube** - YouTube
- **github** - GitHub
- **email** - Email (use `mailto:` link)
- **phone** - Phone (use `tel:` link)

## Usage

### In Pages

**pages/contact/contact.json:**
```json
{
  "page": "contact",
  "title": "Contact Us",
  "components": [
    {
      "name": "contactIcons"
    }
  ]
}
```

**pages/contact/contact.html:**
```html
<div class="container">
  <h1>Contact Us</h1>
  <p>Connect with us on social media:</p>
  
  {{COMPONENT:contactIcons}}
</div>
```

### In Components

The component can be used inside other components:

**components/footer/footer.html:**
```html
<footer>
  <h5>Follow Us</h5>
  {{COMPONENT:contactIcons}}
</footer>
```

### In Content Files

**pages/about/about.html:**
```html
<div class="about-section">
  <h2>Stay Connected</h2>
  {{COMPONENT:contactIcons}}
</div>
```

## Output

The component generates Bootstrap Icon links:

```html
<div class="social-links d-flex justify-content-left gap-4">
  <a href="https://t.me/yourusername" target="_blank" rel="noopener" aria-label="Telegram">
    <i class="bi bi-telegram"></i>
  </a>
  <a href="https://wa.me/1234567890" target="_blank" rel="noopener" aria-label="WhatsApp">
    <i class="bi bi-whatsapp"></i>
  </a>
  <a href="https://instagram.com/yourusername" target="_blank" rel="noopener" aria-label="Instagram">
    <i class="bi bi-instagram"></i>
  </a>
  <a href="https://signal.me/#p/+1234567890" target="_blank" rel="noopener" aria-label="Signal">
    <i class="bi bi-signal"></i>
  </a>
  <a href="viber://chat?number=1234567890" target="_blank" rel="noopener" aria-label="Viber">
    <svg class="bi" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="..."/></svg>
  </a>
</div>
```

## Styling

The component includes built-in CSS:

```css
.social-links a {
  color: #667eea;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.social-links a:hover {
  color: #e07a1f;
  transform: translateY(-3px);
}
```

### Custom Styling

Override in your page or component CSS:

```css
.social-links a {
  color: #your-color;
  font-size: 2rem;
}

.social-links a:hover {
  color: #your-hover-color;
}
```

## Adding More Platforms

### 1. Add to config.json:

```json
{
  "social": {
    "facebook": "https://facebook.com/yourpage",
    "twitter": "https://twitter.com/yourusername"
  }
}
```

### 2. Icons automatically supported:

The component already supports these platforms - just add the link!

## Conditional Display

Only platforms with configured URLs will appear. Empty or missing links are skipped:

```json
{
  "social": {
    "telegram": "https://t.me/yourusername",
    "whatsapp": "",  // Won't appear
    "instagram": "https://instagram.com/yourusername"
  }
}
```

**Result:** Only Telegram and Instagram icons appear.

## Link Formats

### Messenger Apps:

```json
{
  "telegram": "https://t.me/username",
  "whatsapp": "https://wa.me/1234567890",
  "signal": "https://signal.me/#p/+1234567890",
  "viber": "viber://chat?number=1234567890"
}
```

### Social Media:

```json
{
  "instagram": "https://instagram.com/username",
  "facebook": "https://facebook.com/pagename",
  "twitter": "https://twitter.com/username",
  "linkedin": "https://linkedin.com/in/username"
}
```

### Contact:

```json
{
  "email": "mailto:contact@example.com",
  "phone": "tel:+1234567890"
}
```

## Examples

### Example 1: Contact Page

```html
<div class="container text-center">
  <h1>Get In Touch</h1>
  <p class="lead">Connect with us through your preferred platform</p>
  
  {{COMPONENT:contactIcons}}
  
  <p class="mt-4">Or send us an email at: {{CONTACT_EMAIL}}</p>
</div>
```

### Example 2: Footer

```html
<footer class="bg-dark text-white py-4">
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        <h5>{{SITE_NAME}}</h5>
      </div>
      <div class="col-md-6">
        <h5>Follow Us</h5>
        {{COMPONENT:contactIcons}}
      </div>
    </div>
  </div>
</footer>
```

### Example 3: About Page Section

```html
<section class="social-section py-5">
  <div class="container text-center">
    <h2>Join Our Community</h2>
    <p>Stay updated with our latest news and updates</p>
    {{COMPONENT:contactIcons}}
  </div>
</section>
```

## File Structure

```
components/contactIcons/
├── contactIcons.html         ← Template
├── contactIcons.build.js     ← Reads config, generates icons (Viber glyph inlined here)
└── style.css                 ← Styles
```

No image files: every glyph is either a Bootstrap Icons font class or, for Viber,
an inline SVG in the build script. The component deploys without carrying assets.

## How It Works

1. **Build script reads config.json**
   ```javascript
   const config = JSON.parse(fs.readFileSync('config.json'));
   const socialLinks = config.social || {};
   ```

2. **Generates HTML for each platform**
   ```javascript
   Object.entries(socialLinks).forEach(([platform, url]) => {
     // Generate icon HTML
   });
   ```

3. **Injects into template**
   ```html
   <div class="social-links">
     {{SOCIAL_ICONS}}
   </div>
   ```

## Bootstrap Icons Required

The component uses Bootstrap Icons. Make sure your layout includes:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
```

`_layout.html` already includes this.

## Viber Custom Icon

Bootstrap Icons has no Viber glyph, so `contactIcons.build.js` inlines an SVG —
a copy of the Bootstrap Icons "telephone" path (MIT). It carries
`fill="currentColor"` and `width/height: 1em`, so it picks up the same colour and
size as its neighbours from `.social-links a` with no extra styling.

Inlining keeps the component self-contained: a site adopting it needs no
`assets/images/` file alongside.

## Troubleshooting

### Icons not appearing?

**Check:**
1. Config has social links: `config.social.telegram`
2. Links are not empty strings
3. Bootstrap Icons CSS is loaded
4. Component CSS is included

### Wrong icon colors?

**Solution:** Override in your CSS:
```css
.social-links a {
  color: #your-color !important;
}
```

### Viber icon wrong size?

The inline SVG is sized in `em`, so it follows the link's font-size:
```css
.social-links a {
  font-size: 1.5rem;
}
```

## Benefits

✅ **Centralized** - Update all social links in one place  
✅ **Reusable** - Use anywhere with one placeholder  
✅ **Consistent** - Same styling everywhere  
✅ **Maintainable** - Easy to add/remove platforms  
✅ **Flexible** - Works in pages and components  

## Summary

**Create once, use everywhere!**

```html
{{COMPONENT:contactIcons}}
```

**Configure in config.json:**
```json
{ "social": { "telegram": "...", "instagram": "..." } }
```

**Renders automatically with correct icons and links!** 🎉
