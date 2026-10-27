# Vedant Kulkarni — Portfolio

Public website: https://vk7-coder.github.io/VedantPortfolio/

A responsive portfolio covering data workflows, analytics, requirements and process design. The website uses semantic HTML, CSS and progressively enhanced JavaScript. Content remains readable without JavaScript; motion respects reduced-motion preferences.

## Update the content

- Edit `portfolio/content.json` for experience, projects, skills, education and training.
- Edit `portfolio/site-template.html` for the page structure.
- Edit the assets in `static/portfolio/` for styling and interactions.

Regenerate both website entry points with Python 3:

```sh
python3 portfolio/build.py
```

The builder writes `index.html` for GitHub Pages and the matching `templates/index.html` for the existing Flask application. Both include the complete stylesheet and interaction script, so the first visit does not need separate CSS or JavaScript downloads to finish rendering and initialise controls. No page loader or font-ready gate hides the content.

It also combines `style.css`, `refinements.css` and `responsive.css` into `static/portfolio/site.css` and embeds that same CSS into each HTML entry point. Edit those source stylesheets or `app.js` and rebuild; do not edit generated files directly. Phone layouts use a single column below 768px, while the approved desktop layout remains intact. External fonts load without blocking the initial page render, with system-font fallbacks. The original portrait is preloaded and remains at full resolution.

## Deployment

The existing GitHub Actions workflow publishes committed files from `main` to GitHub Pages. Commit the generated HTML together with any source or asset changes. The approved portrait remains at `static/images/vedant-kulkarni-profile-2026.jpeg`.

The previous public design is preserved on the `backup-portfolio-before-ui-refresh-2026-10-27` branch.
