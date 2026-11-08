from pathlib import Path
import json, html, re

ROOT = Path(__file__).parent
SITE = ROOT
D = json.loads((ROOT / 'portfolio.json').read_text(encoding='utf-8'))
P = D['person']
CS = {c['id']:c for c in D['companies']}
PS = {p['id']:p for p in D['projects']}
E = lambda x: html.escape(str(x),quote=True)
BASE = 'https://geniusmma.github.io/'
LINKEDIN = 'https://www.linkedin.com/in/michael-asistin-28042918b/'
DATE = '6 November 2026'
ARROW = '<span aria-hidden="true">↗</span>'
SHORT = {'workstaff360':'WorkStaff360 / O’Dorisio','transitional-builders':'Transitional Builders, Inc.','convergence-esl':'Convergence Realty / ESL','mega-m':'Mega M Builder / Freelance','sta-clara':'Sta. Clara International'}
ROLE = {'arcadis':'Business intelligence, automation & quantity surveying','workstaff360':'Construction coordination & estimating','transitional-builders':'Project coordination & estimating','timberworx':'Construction coordination & estimating','goel':'Estimating & construction support','convergence-esl':'Quantity surveying & cost control','mega-m':'Civil engineering & project coordination','sta-clara':'Tendering, site engineering & quantity surveying'}
SUMMARY = {'arcadis':'Cost planning, reporting and automation for infrastructure and procurement teams.','workstaff360':'Project administration, concrete takeoffs and estimating support for U.S. construction teams.','transitional-builders':'Preconstruction support across takeoffs, bids, RFIs and project documentation.'}

def tags(values):
    return '<p class="tool-list">'+E(' · '.join(values))+'</p>'

def expertise():
    return '''<section class="home-section expertise" id="skills"><div class="section-heading"><h2>Skills that connect the work.</h2></div><div class="expertise-grid"><div><h3>Construction &amp; estimating</h3><p>Takeoffs, RFIs, cost planning and project coordination. Expert in Autodesk tools.</p><p class="expertise-tools">Autodesk · Procore · Bluebeam · PlanSwift</p></div><div><h3>Business Intelligence</h3><p>Expertise in turning project data into useful models, dashboards and reports.</p><p class="expertise-tools">Power BI · Power Query · DAX</p></div><div><h3>Automation</h3><p>Expertise in connecting workflows and reducing recurring reporting tasks.</p><p class="expertise-tools">Power Automate · VBA · Power Apps</p></div></div></section>'''

def skill_highlights(c,compact=False):
    tools=c['tools']
    if compact:
        selected={'arcadis':['Power BI','Power Automate','Excel'],'transitional-builders':['Autodesk','Procore','Bluebeam','PlanSwift'],'timberworx':['Autodesk','Procore','Bluebeam','PlanSwift']}
        tools=selected.get(c['id'],tools[:4])
    skills=f'<p><strong>Skills</strong><span>{E(" · ".join(c["skills"]))}</span></p>' if c.get('skills') else ''
    tool_line=f'<p><strong>Tools</strong><span>{E(" · ".join(tools))}</span></p>' if tools else ''
    return '<div class="skill-highlights">'+skills+tool_line+'</div>'

def bullets(values,cls=''):
    return '<ul class="'+cls+'">'+''.join('<li>'+E(v)+'</li>' for v in values)+'</ul>'

def status(value):
    return '<span class="status'+(' current' if value=='Current' else '')+'">'+E(value)+'</span>'

def header(pre='',current=''):
    nav=''.join(f'<a href="{pre}{url}"'+(' aria-current="page"' if key==current else '')+f'>{text}</a>' for url,text,key in [('projects.html','Work','work'),('work.html','Experience','experience'),('profile.html','About','about')])
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header container"><a class="brand" href="{pre}index.html" aria-label="Michael Asistin home">Michael Asistin<span aria-hidden="true">.</span></a><button class="menu-button" type="button" aria-controls="main-nav" aria-expanded="false">Menu</button><nav class="main-nav" id="main-nav" aria-label="Main navigation">{nav}<a href="mailto:{E(P['email'])}" class="nav-contact">Contact {ARROW}</a></nav></header>'''

def footer(pre=''):
    return f'''<footer class="site-footer container"><span>© 2026 Michael Asistin</span><div><a href="mailto:{E(P['email'])}">Email</a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn {ARROW}</a><a href="{pre}resume.pdf" download="Michael-Asistin-CV.pdf">Download CV ↓</a></div></footer>'''

def contact():
    return f'''<section class="contact" id="contact"><p class="eyebrow">Available for a new role</p><h2>Ready for what’s next.</h2><p>I have completed my previous engagements and am looking for my next role.<br class="desktop-break"> Open to construction, estimating, quantity surveying, BI and automation opportunities.</p><div class="intro-actions"><a class="button" href="mailto:{E(P['email'])}">Let’s talk {ARROW}</a><a class="quiet-link" href="resume.pdf" download="Michael-Asistin-CV.pdf">Download CV ↓</a></div><a class="email-link" href="mailto:{E(P['email'])}">{E(P['email'])}</a><p class="small">Philippines · Remote work · Freelance enquiries welcome · Phone on request</p></section>'''

def write(path,title,desc,body,current='',schema=None):
    pre='../'*(len(Path(path).parts)-1)
    data=json.dumps(schema or {'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':BASE+path},ensure_ascii=False).replace('</','<\\/')
    doc=f'''<!doctype html>
<html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Michael Asistin</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#ffffff"><link rel="canonical" href="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title)} | Michael Asistin"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/img/Dexter.jpg"><link rel="icon" href="{pre}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{pre}styles.css"><script type="application/ld+json">{data}</script><script src="{pre}script.js" defer></script></head><body>{header(pre,current)}{body}{footer(pre)}</body></html>'''
    target=SITE/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc,encoding='utf-8')

def project_row(p,level=3,pre='',filterable=False,home=False):
    c=CS[p['companyId']];company=SHORT.get(c['id'],c['name'])
    titles={'us-construction-support':'Construction coordination & estimating','infrastructure-estimating':'Infrastructure cost planning','weekly-snapshots':'Weekly reporting automation'}
    summaries={'us-construction-support':'RFIs, takeoffs, procurement tracking and estimating support for U.S. construction projects.','infrastructure-estimating':'Cost plans and estimates before tender for transport and utilities assignments.','weekly-snapshots':'Automated weekly snapshots that preserve reporting history in SharePoint and Power BI.'}
    title=titles.get(p['id'],p['title']) if home else p['title']
    summary=summaries.get(p['id'],p['summary']) if home else p['summary']
    attrs=''
    if filterable:
        query=' '.join([p['title'],p['summary'],c['name'],p['category'],*p['tools'],*p['deliverables']]).lower()
        attrs=f' data-project data-category="{E(p["category"])}" data-search="{E(query)}"'
    return f'''<article class="project-row"{attrs}><div><p class="row-meta">{E(company)} <span aria-hidden="true">/</span> {E(p['category'])}</p><h{level}><a href="{pre}projects/{p['id']}.html">{E(title)} {ARROW}</a></h{level}><p class="row-summary">{E(summary)}</p></div></article>'''

def company_row(c,level=3,pre='',home=False):
    title=SHORT.get(c['id'],c['name'])
    period={'arcadis':'Jan 2019 to Oct 2026','transitional-builders':'Ended Sep 2026 · About 5 months','workstaff360':'Completed engagement'}.get(c['id'],c['period']) if home else c['period']
    return f'''<article class="company-row"><div class="company-title"><h{level}><a href="{pre}companies/{c['id']}.html">{E(title)} {ARROW}</a></h{level}><span class="period">{E(period)}</span></div><p class="role">{E(ROLE[c['id']])}</p>{skill_highlights(c,compact=home)}<p class="row-summary">{E(SUMMARY.get(c['id'],c['summary']))}</p></article>'''

def heading(title,link='',label=''):
    return f'<div class="section-heading"><h2>{E(title)}</h2>'+ (f'<a class="quiet-link" href="{link}">{E(label)} <span aria-hidden="true">→</span></a>' if link else '')+'</div>'

ordered_ids=['us-construction-support','infrastructure-estimating','weekly-snapshots','transitional-preconstruction']
ordered=[PS[x] for x in ordered_ids]+[p for p in D['projects'] if p['id'] not in ordered_ids]
featured=[PS[x] for x in ordered_ids[:3]]
def featured_work():
    return '''<div class="featured-work">
    <article class="feature feature-construction">
      <div class="feature-copy"><p class="eyebrow">Construction · WorkStaff360 / O’Dorisio</p><h3>The details that<br>keep a project moving.</h3><p>I supported U.S. construction teams with takeoffs, RFIs, change order pricing and procurement tracking.</p><p class="feature-tools">Procore · ProjectHQ · Bluebeam · Excel</p><a class="text-link" href="projects/us-construction-support.html">Explore my contribution <span aria-hidden="true">↗</span></a></div>
      <div class="work-evidence"><p class="evidence-label">What I delivered</p><div><span class="evidence-number">01</span><p><strong>Clear project records</strong><span>RFI logs, submittal trackers and meeting actions</span></p></div><div><span class="evidence-number">02</span><p><strong>Estimating inputs</strong><span>Takeoff markups, pricing sheets and change order support</span></p></div><div><span class="evidence-number">03</span><p><strong>Procurement visibility</strong><span>Purchase order and project status trackers</span></p></div></div>
    </article>
    <article class="feature"><p class="eyebrow">Business Intelligence · Arcadis</p><h3>Reporting that supports<br>the next decision.</h3><p>I implemented purchase order reporting changes, validated the logic and supported deployment and checks after release.</p><p class="feature-tools">Power BI · SharePoint · Power Platform</p><a class="text-link" href="projects/po-lifecycle.html">See the reporting work <span aria-hidden="true">↗</span></a></article>
    <article class="feature"><p class="eyebrow">Automation · Arcadis</p><h3>A reporting history.<br>Built automatically.</h3><p>I built weekly file copy automation and combined dated SharePoint snapshots into reporting history, with checks for empty inputs.</p><p class="feature-tools">Power Automate · SharePoint · Power Query</p><a class="text-link" href="projects/weekly-snapshots.html">See the workflow <span aria-hidden="true">↗</span></a></article>
    </div>'''

def home_experience():
    rows = []
    for key in ['arcadis', 'transitional-builders', 'workstaff360']:
        c = CS[key]
        period = {'arcadis':'Jan 2019 to Oct 2026','transitional-builders':'Ended Sep 2026 · About 5 months','workstaff360':'Completed engagement'}[key]
        rows.append(f'<a class="experience-link" href="companies/{key}.html"><div><h3>{E(SHORT.get(key,c["name"]))}</h3><p>{E(ROLE[key])}</p></div><span>{E(period)}</span><span class="experience-arrow" aria-hidden="true">↗</span></a>')
    return ''.join(rows)

home=f'''<main class="container home" id="main"><section class="intro"><p class="availability"><span aria-hidden="true"></span>Available for a new role</p><div class="intro-identity"><img class="avatar" src="assets/img/Dexter.jpg" alt="Michael’s illustrated profile avatar" width="64" height="64" fetchpriority="high"><p>Michael Asistin <span>AssocRICS · Civil Engineer</span></p></div><h1>Construction expertise.<br><span>Smarter delivery.</span></h1><p class="intro-role">Project Coordinator · Estimator · Quantity Surveyor</p><p class="intro-summary">I help construction teams manage takeoffs, RFIs and cost reporting.<br class="desktop-break"> I am also a Business Intelligence and Automation expert.</p><div class="intro-actions"><a class="button" href="#selected-work">Explore my work <span aria-hidden="true">↓</span></a><a class="quiet-link" href="resume.pdf" download="Michael-Asistin-CV.pdf">Download CV ↓</a></div></section><section class="home-section selected" id="selected-work">{heading('A closer look at my work.','projects.html','All work')}{featured_work()}</section>{expertise()}<section class="home-section" id="experience">{heading('Experience, in brief.','work.html','Full experience')}<p class="section-intro">My previous engagements are complete. I am now looking for a new role.</p><div class="experience-list">{home_experience()}</div></section>{contact()}</main>'''

write('index.html','Construction coordination & estimating','Michael Asistin: construction project coordinator, estimator, AssocRICS quantity surveyor, Business Intelligence and Automation expert.',home,schema={'@context':'https://schema.org','@type':'Person','name':'Michael Asistin','url':BASE,'email':P['email'],'jobTitle':'Project Coordinator, Estimator and Quantity Surveyor','sameAs':[LINKEDIN]})

options=''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in ['All work','Construction','Cost & QS','Data & BI','Automation'])
projects=f'''<main id="main" class="container page-main"><header class="page-heading"><h1>Work</h1><p>Construction, cost and digital work. Open a project for my role, contributions and deliverables.</p></header><div class="filters"><div class="search-control"><label for="project-search" class="sr-only">Search projects, companies or tools</label><input id="project-search" type="search" placeholder="Search projects, companies or tools" autocomplete="off"></div><div><label for="project-category" class="sr-only">Filter by discipline</label><select id="project-category">{options}</select></div></div><div class="results-bar"><span id="result-count" role="status" aria-live="polite">18 projects</span><button type="button" class="reset-button" data-reset>Clear</button></div><div class="work-list" id="project-list">{''.join(project_row(p,level=2,filterable=True) for p in ordered)}</div><div id="empty-state" class="empty-state" hidden><h2>No matching work</h2><p>Try another company, tool or discipline.</p><button class="button" type="button" data-reset>Show all work</button></div><nav class="pagination" aria-label="Project pages" hidden><button type="button" id="previous-page">← Previous</button><span id="page-number">Page 1</span><button type="button" id="next-page">Next →</button></nav><p class="small page-note">Arcadis project names are withheld. Work status is recorded as of {DATE}.</p><noscript><p class="small">All work is shown. Enable JavaScript to use search and filters.</p></noscript></main>'''
write('projects.html','Work','Explore Michael Asistin’s construction, estimating, quantity surveying, reporting and automation work.',projects,'work')

work=f'''<main id="main" class="container page-main"><header class="page-heading"><h1>Experience</h1><p>All previous engagements are complete. I am looking for a new role. Explore the skills, tools and contributions from each company below.</p></header><div class="company-list full-history">{''.join(company_row(c,level=2) for c in D['companies'])}</div><p class="small page-note">Includes employment, remote support and freelance engagements. Some assignments overlap.</p></main>'''
write('work.html','Experience','Michael Asistin’s company experience in construction, estimating, quantity surveying and digital delivery.',work,'experience')

creds=''.join(f'<li><strong>{E(c["title"])}</strong><span>{E(c["body"])}</span></li>' for c in P['credentials'])
about=f'''<main id="main" class="container page-main reading-page"><header class="page-heading"><h1>About me</h1></header><div class="about-intro"><img class="about-avatar" src="assets/img/Dexter.jpg" alt="Michael’s illustrated profile avatar" width="96" height="96"><div><p>I’m Michael Asistin, based in San Pablo City, Laguna, Philippines.</p><p>I am a Business Intelligence and Automation expert, with expertise in Autodesk tools. My work connects construction coordination, estimating and quantity surveying with reporting and automation. I’ve worked across site delivery, commercial support and remote construction teams, and worked in business intelligence and automation at Arcadis until October 2026. My previous engagements are complete, and I am now looking for a new role.</p></div></div><section class="content-section"><h2>How I work</h2><p>I focus on clear records, careful checks and practical follow through when reviewing quantities, coordinating project documents or tracing a reporting issue.</p></section><section class="content-section" id="credentials"><h2>Qualifications</h2><ul class="credentials">{creds}</ul></section><section class="content-section" id="skills"><h2>Skills &amp; tools</h2><p><strong>Autodesk expertise:</strong> Expert in using Autodesk tools for construction workflows.</p><p><strong>Construction:</strong> Autodesk, Procore, ProjectHQ, Bluebeam, PlanSwift, Excel and SharePoint.</p><p><strong>Reporting & automation:</strong> Power BI, Power Query, DAX, Power Automate, Smartsheet, Power Apps and VBA.</p></section><section class="content-section" id="faq"><h2>Working together</h2><p>I’m open to job opportunities, freelance work and project based engagements. Email me with the role or scope you have in mind. My phone number is available on request.</p><div class="intro-actions"><a class="button" href="mailto:{E(P['email'])}">Get in touch {ARROW}</a><a class="quiet-link" href="resume.pdf" download="Michael-Asistin-CV.pdf">Download CV ↓</a></div></section></main>'''
write('profile.html','About','Michael Asistin’s background, qualifications, tools and approach.',about,'about')

for p in ordered:
    c=CS[p['companyId']]
    tools=tags(p['tools'] or c.get('skills',[]))
    tools_title='Tools used' if p['tools'] else 'Skills applied'
    workflow=bullets(p.get('workflow',[]),'process-list') if p.get('workflow') else ''
    nextsteps=f'<details class="disclosure"><summary>Current next steps</summary>{bullets(p["nextSteps"])}</details>' if p.get('nextSteps') else ''
    privacy='<p class="small">Project name withheld.</p>' if c['id']=='arcadis' else ''
    related=[q for q in ordered if q['companyId']==p['companyId'] and q['id']!=p['id']][:2]
    related_html=''.join(f'<li><a href="{q["id"]}.html">{E(q["title"])} {ARROW}</a></li>' for q in related)
    related_section=f'<section class="related"><h2>More at {E(SHORT.get(c["id"],c["name"]))}</h2><ul>{related_html}</ul></section>' if related else ''
    body=f'''<main id="main" class="container page-main reading-page"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../projects.html">← All work</a><a href="../companies/{c['id']}.html">{E(SHORT.get(c['id'],c['name']))}</a></nav><header class="page-heading project-heading"><p class="eyebrow">{E(p['category'])}</p><h1>{E(p['title'])}</h1><p>{E(p['summary'])}</p></header><dl class="project-facts"><div><dt>Role</dt><dd>{E(p['role'])}</dd></div><div><dt>Period</dt><dd>{E(p['period'])}</dd></div><div><dt>Status</dt><dd>{E(p['status'])}</dd></div></dl><section class="content-section project-tools" id="tools"><h2>{tools_title}</h2>{tools}</section><section class="content-section" id="contribution"><h2>My contribution</h2>{bullets(p['contributions'])}</section><section class="content-section" id="deliverables"><h2>Deliverables</h2>{bullets(p['deliverables'],'deliverables')}</section><section class="content-section" id="status"><h2>Outcome & status</h2><p>{E(p['outcome'])}</p>{nextsteps}</section><div class="details-group"><details class="disclosure" id="overview"><summary>Project context</summary><p>{E(p['context'])}</p>{privacy}</details><details class="disclosure"><summary>Working process</summary>{workflow}</details></div><p class="small page-note">Status as of {DATE}.</p>{related_section}</main>'''
    write('projects/'+p['id']+'.html',p['title'],p['summary'],body,'work')

for c in D['companies']:
    projects_html=''.join(project_row(PS[x],level=3,pre='../') for x in c['projectIds'])
    privacy='<p class="small">Project names are withheld; the pages describe my contributions and deliverables.</p>' if c['id']=='arcadis' else ''
    tools=f'<section class="content-section experience-highlights" id="tools"><h2>Skills &amp; tools</h2>{skill_highlights(c)}</section>'
    # Arcadis has many workstreams: show three first, with an optional full list.
    if len(c['projectIds'])>3:
        projects_html=''.join(project_row(PS[x],level=3,pre='../') for x in c['projectIds'][:3])+f'<details class="disclosure additional-work"><summary>More work at {E(c["name"])} ({len(c["projectIds"])-3})</summary>'+''.join(project_row(PS[x],level=3,pre='../') for x in c['projectIds'][3:])+'</details>'
    body=f'''<main id="main" class="container page-main reading-page"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../work.html">← All experience</a></nav><header class="page-heading"><h1>{E(c['name'])}</h1><p>{E(c['summary'])}</p></header><dl class="project-facts"><div><dt>Role</dt><dd>{E(c['role'])}</dd></div><div><dt>Period</dt><dd>{E(c['period'])}</dd></div><div><dt>Status</dt><dd>{E(c['status'])}</dd></div></dl>{tools}<section class="content-section" id="scope"><h2>Responsibilities</h2>{bullets(c['scope'])}</section><section class="content-section" id="projects"><h2>Selected work</h2>{privacy}<div class="work-list">{projects_html}</div></section></main>'''
    write('companies/'+c['id']+'.html',c['name']+': Experience',c['summary'],body,'experience')

resume_companies=''.join(f'<article class="resume-company"><h3>{E(c["name"])}</h3><p class="role">{E(c["role"])}</p><p class="small">{E(c["period"])} · {E(c["status"])}</p><p>{E(c["summary"])}</p>{bullets(c["scope"][:3])}</article>' for c in D['companies'])
resume=f'''<main id="main" class="container page-main reading-page resume-page"><div class="print-bar"><a class="quiet-link" href="resume.pdf" download="Michael-Asistin-CV.pdf">Download PDF ↓</a><button class="reset-button" type="button" data-print>Print CV</button></div><header class="page-heading"><h1>Michael Asistin</h1><p>Construction Project Coordinator · Estimator · AssocRICS Quantity Surveyor</p><p class="small">San Pablo City, Laguna, Philippines<br>{E(P['email'])} · Phone available on request</p></header><p class="availability-note">Available for a new role. My previous engagements are complete.</p><p>{E(P['summary'])}</p><section class="content-section"><h2>Qualifications</h2><ul class="credentials">{creds}</ul></section><section class="content-section"><h2>Professional experience</h2>{resume_companies}</section><section class="content-section"><h2>Skills &amp; tools</h2><p>Business Intelligence and Automation expert. Expert in Autodesk tools.</p><p>Autodesk, Procore, ProjectHQ, Bluebeam, PlanSwift, Excel, SharePoint, Power BI, Power Query, DAX, Power Automate, Smartsheet, Power Apps and VBA.</p></section></main>'''
write('resume.html','CV','Michael Asistin’s construction coordination, estimating, quantity surveying and digital experience.',resume)

for old,target in [('case-studies.html','projects.html'),('courses.html','profile.html#credentials'),('faq.html','profile.html#faq')]:
    (SITE/old).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{BASE}{target}"><title>Michael Asistin</title></head><body><p><a href="{target}">Continue to the updated page</a>.</p></body></html>',encoding='utf-8')
write('404.html','Page not found','Return to Michael Asistin’s portfolio.',f'<main id="main" class="container page-main"><header class="page-heading"><h1>Page not found</h1><p>This page may have moved.</p></header><a class="button" href="{BASE}">Back to the portfolio →</a></main>')
nf=SITE/'404.html';nf.write_text(re.sub(r'(href|src)="(?!https?:|mailto:|#)([^\"]+)"',lambda m:f'{m[1]}="{BASE}{m[2]}"',nf.read_text(encoding='utf-8')),encoding='utf-8')
(SITE/'navigation.html').write_text(header(),encoding='utf-8')
(SITE/'footer.html').write_text(footer(),encoding='utf-8')
(SITE/'.nojekyll').write_text('',encoding='utf-8')
paths=['index.html','projects.html','work.html','profile.html','resume.html']+['projects/'+p['id']+'.html' for p in ordered]+['companies/'+c['id']+'.html' for c in D['companies']]
(SITE/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{p}</loc><lastmod>2026-11-06</lastmod></url>' for p in paths)+'</urlset>',encoding='utf-8')
(SITE/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n',encoding='utf-8')
print(f'Built minimalist portfolio: {len(paths)} pages; 3 homepage work highlights.')
