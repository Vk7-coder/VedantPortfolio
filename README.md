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

The builder writes `index.html` for GitHub Pages and the matching `templates/index.html` for the existing Flask application. Asset URLs include content hashes so browsers receive updated styles and scripts after a release.

## Deployment

The existing GitHub Actions workflow publishes committed files from `main` to GitHub Pages. Commit the generated HTML together with any source or asset changes. The approved portrait remains at `static/images/vedant-kulkarni-profile-2026.jpeg`.

The previous public design is preserved on the `backup-portfolio-before-ui-refresh-2026-10-27` branch.
