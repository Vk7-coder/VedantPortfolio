from pathlib import Path
from html import escape
from string import Template
import json
import hashlib

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
data = json.loads((ROOT / 'content.json').read_text())


def tags(items):
    return ''.join('<span class="tool-tag">' + escape(item) + '</span>' for item in items)


def project_card(project, index):
    title = escape(project['title'])
    project_id = escape(project['id'])
    implementation = ''.join('<li>' + escape(item) + '</li>' for item in project['bullets'][:-1])
    search_text = ' '.join([project['title'], project['domain'], project['description'],
                            project['scope'], *project['tools'], *project.get('methods', []),
                            *project['bullets']]).lower()
    featured = project.get('featured', False)
    flow = ''
    if featured:
        steps = ''.join(f'<li><span>{escape(label)}</span><strong>{escape(tools)}</strong></li>'
                        for label, tools in project['flow'])
        flow = f'<ol class="project-flow" aria-label="Project data flow">{steps}</ol>'
    methods = ''
    if project.get('methods'):
        methods = '<p class="project-methods"><strong>Methods:</strong> ' + escape(', '.join(project['methods'])) + '</p>'
    return f'''<article class="project-card{' project-featured' if featured else ''}" id="{project_id}" data-category="{escape(project['filter'])}" data-search="{escape(search_text, quote=True)}" aria-labelledby="{project_id}-title">
      <div class="project-topline"><span>{index:02}</span><p>{escape(project['domain'])}</p></div>
      <div class="project-overview"><div><h4 class="project-title" id="{project_id}-title">{title}</h4><p class="project-description">{escape(project['description'])}</p></div>{flow}</div>
      <div class="tool-tags">{tags(project['tools'][:4])}</div>
      <p class="project-output"><span>OUTPUT</span>{escape(project['output'])}</p>
      <details class="project-details"><summary aria-label="Read project details: {title}">{escape(project['details_label'])}<span class="plus-icon" aria-hidden="true"></span></summary>
        <div class="details-body"><p class="full-stack"><strong>Tools:</strong> {escape(', '.join(project['tools']))}</p>{methods}<h5>{escape(project.get('implementation_heading', 'Implementation'))}</h5><ul>{implementation}</ul><h5>{escape(project['validation_heading'])}</h5><ul><li>{escape(project['bullets'][-1])}</li></ul></div>
      </details>
    </article>'''


def project_groups():
    groups = []
    project_numbers = {p['id']: i for i, p in enumerate(data['projects'], 1)}
    for group in data['project_groups']:
        projects = [p for p in data['projects'] if p['filter'] == group['id']]
        cards = ''.join(project_card(p, project_numbers[p['id']]) for p in projects)
        group_id = escape(group['id'])
        groups.append(f'''<section class="project-group group-{escape(group['tone'])}" data-project-group="{group_id}" aria-labelledby="group-{group_id}-heading">
          <div class="project-group-heading"><span class="group-number">{group['number']}</span><div><h3 id="group-{group_id}-heading">{escape(group['title'])}</h3><p>{escape(group['description'])}</p></div><span class="group-count" aria-label="{len(projects)} projects">{len(projects):02}</span></div>
          <div class="project-grid">{cards}</div>
        </section>''')
    return ''.join(groups)


def role_card(role, index):
    position, company, dates, bullets = role
    contexts = ['E-commerce, CRM and payment datasets', 'Voice AI evaluation and product benchmarking', 'Acquisition, conversion and campaign analytics']
    items = ''.join('<li>' + escape(item) + '</li>' for item in bullets)
    return f'''<article class="experience-card"><div class="role-topline"><span class="role-date">{escape(dates)}</span>{'<span class="current-label">Current role</span>' if index == 0 else ''}</div><h3>{escape(position)}</h3><p class="company-name">{escape(company)}</p><p class="role-context">{contexts[index]}</p><details class="role-details" {'open' if index == 0 else ''}><summary>Responsibilities &amp; contributions<span class="plus-icon" aria-hidden="true"></span></summary><ul>{items}</ul></details></article>'''


skill_groups = []
for index, (name, items) in enumerate(data['skills'], 1):
    skill_groups.append(f'<article class="expertise-group"><span class="expertise-number">{index:02}</span><h3>{escape(name)}</h3><div class="tool-tags">{tags(items)}</div></article>')
skill_groups.append('<article class="expertise-group"><span class="expertise-number">08</span><h3>Requirements &amp; solution analysis</h3><div class="tool-tags">' + tags(data['business_skills']) + '</div></article>')

degrees = []
for degree, university, country, dates in data['degrees']:
    degrees.append(f'<article class="education-card"><p class="qualification-date">{escape(dates)}</p><h3>{escape(degree)}</h3><p>{escape(university)}</p><span>{escape(country)}</span></article>')

certificates = []
for cert, mark in zip(data['certifications'], ['ECBA', 'Agile', 'Py', 'GA']):
    date = f'<span class="certification-date">{escape(cert["date"])}</span>' if cert['date'] else ''
    note = f'<p class="training-note">{escape(cert["note"])}</p>' if cert.get('note') else ''
    reference = f'<p class="credential-reference">Credential reference: {escape(cert["reference"])}</p>' if cert.get('reference') else ''
    certificates.append(f'''<article class="certification-card"><span class="training-mark" aria-hidden="true">{mark}</span><div class="certification-content"><div class="certification-meta"><span>{escape(cert['kind'])}</span>{date}</div><h4>{escape(cert['name'])}</h4><p class="certification-issuer">{escape(cert['issuer'])}</p><div class="tool-tags">{tags(cert['topics'])}</div><details class="training-details"><summary>View learning focus<span class="plus-icon" aria-hidden="true"></span></summary><p>{escape(cert['description'])}</p>{note}{reference}</details></div></article>''')

approach = []
for index, (label, title, description) in enumerate(data['approach'], 1):
    approach.append(f'<li><span class="approach-node" aria-hidden="true">{index:02}</span><div><span class="step-number">{escape(label.upper())}</span><h3>{escape(title)}</h3><p>{escape(description)}</p></div></li>')

filters = [f'<button type="button" data-filter="all" aria-pressed="true">All work <span>{len(data["projects"])}</span></button>']
for category, label in [('pipelines', 'Pipelines & quality'), ('process', 'Process & solutions'), ('analytics', 'Analytics & ML')]:
    count = sum(p['filter'] == category for p in data['projects'])
    filters.append(f'<button type="button" data-filter="{category}" aria-pressed="false">{escape(label)} <span>{count}</span></button>')

hero_intro = escape(data['intro'])
for phrase in ['Azure data pipelines', 'SQL, Python and PySpark']:
    hero_intro = hero_intro.replace(escape(phrase), '<strong>' + escape(phrase) + '</strong>', 1)
hero_intro = hero_intro.replace('e-commerce', '<span class="nowrap">e-commerce</span>', 1)

output = Template((ROOT / 'site-template.html').read_text()).substitute(
    hero_intro=hero_intro, hero_support=escape(data['intro_support']),
    approach=''.join(approach), project_filters=''.join(filters), projects=project_groups(),
    experience=''.join(role_card(role, i) for i, role in enumerate(data['roles'])),
    skills=''.join(skill_groups), education=''.join(degrees), certifications=''.join(certificates),
)
for asset in ['style.css', 'refinements.css', 'app.js', 'favicon.svg']:
    digest = hashlib.sha256((REPOSITORY / 'static/portfolio' / asset).read_bytes()).hexdigest()[:12]
    output = output.replace('assets/' + asset, 'static/portfolio/' + asset + '?v=' + digest)
output = output.replace('assets/portrait.jpeg', 'static/images/vedant-kulkarni-profile-2026.jpeg')
(REPOSITORY / 'templates').mkdir(exist_ok=True)
(REPOSITORY / 'index.html').write_text(output)
(REPOSITORY / 'templates/index.html').write_text(output)
print(f'Built public portfolio: {len(data["projects"])} projects, {len(data["approach"])} contribution stages, {len(data["certifications"])} training entries, {len(data["roles"])} unchanged roles.')
