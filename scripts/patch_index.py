import os
import re

with open("site/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. HTML Shell modifications wrapper
html = html.replace(
    '<h1>European Job Market Visualizer <a href="https://github.com/karpathy/jobs">GitHub</a></h1>',
    '''<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <h1 data-i18n="title" style="margin-bottom:0px;">European Job Market Visualizer</h1>
      <select id="languageSelect" style="padding:4px 8px; border-radius:4px; font-size:12px; background:var(--bg2); color:var(--fg); border: 1px solid rgba(255,255,255,0.2);">
        <option value="en">English (EN)</option>
        <option value="bg">Bulgarian (BG)</option>
        <option value="cs">Czech (CS)</option>
        <option value="da">Danish (DA)</option>
        <option value="de">German (DE)</option>
        <option value="el">Greek (EL)</option>
        <option value="es">Spanish (ES)</option>
        <option value="et">Estonian (ET)</option>
        <option value="fi">Finnish (FI)</option>
        <option value="fr">French (FR)</option>
        <option value="ga">Irish (GA)</option>
        <option value="hr">Croatian (HR)</option>
        <option value="hu">Hungarian (HU)</option>
        <option value="it">Italian (IT)</option>
        <option value="lt">Lithuanian (LT)</option>
        <option value="lv">Latvian (LV)</option>
        <option value="mt">Maltese (MT)</option>
        <option value="nl">Dutch (NL)</option>
        <option value="pl">Polish (PL)</option>
        <option value="pt">Portuguese (PT)</option>
        <option value="ro">Romanian (RO)</option>
        <option value="sk">Slovak (SK)</option>
        <option value="sl">Slovenian (SL)</option>
        <option value="sv">Swedish (SV)</option>
      </select>
    </div>'''
)

html = html.replace(
    '<p>This is a research tool that visualizes <b>over 400 occupations</b>',
    '<p data-i18n="intro1_html">This is a research tool that visualizes <b>over 400 occupations</b>'
)
html = html.replace(
    '<p><b>LLM-powered coloring:</b> The <a href="https://github.com/karpathy/jobs">source code</a> includes',
    '<p data-i18n="intro2_html"><b>LLM-powered coloring:</b> The <a href="https://github.com/karpathy/jobs">source code</a> includes'
)
html = html.replace(
    '<summary>View the Digital AI Exposure scoring prompt (example)</summary>',
    '<summary data-i18n="prompt_summary">View the Digital AI Exposure scoring prompt (example)</summary>'
)
html = html.replace(
    '<p><b>Caveat on Digital AI Exposure scores:</b> These are rough LLM estimates, not rigorous predictions.',
    '<p data-i18n="caveat_html"><b>Caveat on Digital AI Exposure scores:</b> These are rough LLM estimates, not rigorous predictions.'
)
html = html.replace('<h3>Layer</h3>', '<h3 data-i18n="layer">Layer</h3>')
html = html.replace('<button data-mode="outlook" class="active">Growth Outlook</button>', '<button data-mode="outlook" class="active" data-i18n="btn_outlook">Growth Outlook</button>')
html = html.replace('<button data-mode="pay">Median Pay</button>', '<button data-mode="pay" data-i18n="btn_pay">Median Pay</button>')
html = html.replace('<button data-mode="education">Education</button>', '<button data-mode="education" data-i18n="btn_education">Education</button>')
html = html.replace('<button data-mode="exposure">Digital AI Exposure</button>', '<button data-mode="exposure" data-i18n="btn_exposure">Digital AI Exposure</button>')

html = html.replace('<span id="legendLow">Declining</span>', '<span id="legendLow" data-i18n="legend_declining">Declining</span>')
html = html.replace('<span id="legendHigh">Growing</span>', '<span id="legendHigh" data-i18n="legend_growing">Growing</span>')
html = html.replace('<h3>Total jobs</h3>', '<h3 data-i18n="total_jobs">Total jobs</h3>')

# 2. Add I18N loader into <script>
script_top = '''<script>
window.__i18n = {};
function _t(key) { return window.__i18n[key] || key; }

'''
html = html.replace('<script>\n', script_top)

# 3. JS Tooltips replacement
html = html.replace('<span class="label">Median pay</span>', '<span class="label">${_t("tt_median_pay")}</span>')
html = html.replace('<span class="label">Jobs (2024)</span>', '<span class="label">${_t("tt_jobs")}</span>')
html = html.replace('<span class="label">Outlook</span>', '<span class="label">${_t("tt_outlook")}</span>')
html = html.replace('<span class="label">Education</span>', '<span class="label">${_t("tt_education")}</span>')

# 4. JS Blocks Replacement
# block 2 Outlook
html = html.replace('<h3>Avg. outlook</h3>', '<h3>${_t("avg_outlook")}</h3>')
html = html.replace('<div class="stat-label">job-weighted</div>', '<div class="stat-label">${_t("job_weighted")}</div>')
html = html.replace('<h3>Jobs by outlook</h3>', '<h3>${_t("jobs_by_outlook")}</h3>')
html = html.replace('<h3>Outlook tiers</h3>', '<h3>${_t("outlook_tiers")}</h3>')
html = html.replace('<h3>Outlook by pay</h3>', '<h3>${_t("outlook_by_pay")}</h3>')
html = html.replace('<h3>Outlook by education</h3>', '<h3>${_t("outlook_by_education")}</h3>')
html = html.replace('<h3>Declining jobs</h3>', '<h3>${_t("declining_jobs")}</h3>')
html = html.replace('<div class="stat-label">negative outlook</div>', '<div class="stat-label">${_t("negative_outlook")}</div>')
html = html.replace('<h3>Growing jobs</h3>', '<h3>${_t("growing_jobs")}</h3>')
html = html.replace('<div class="stat-label">positive outlook</div>', '<div class="stat-label">${_t("positive_outlook")}</div>')

# block Pay
html = html.replace('<h3>Avg. pay</h3>', '<h3>${_t("avg_pay")}</h3>')
html = html.replace('<h3>Jobs by pay</h3>', '<h3>${_t("jobs_by_pay")}</h3>')
html = html.replace('<h3>Pay tiers</h3>', '<h3>${_t("pay_tiers")}</h3>')
html = html.replace('<h3>Pay by education</h3>', '<h3>${_t("pay_by_education")}</h3>')
html = html.replace('<h3>Pay by outlook</h3>', '<h3>${_t("pay_by_outlook")}</h3>')
html = html.replace('<h3>Total wages</h3>', '<h3>${_t("total_wages")}</h3>')
html = html.replace('<div class="stat-label">annual</div>', '<div class="stat-label">${_t("annual")}</div>')

# block EDU
html = html.replace("<h3>Bachelor's+</h3>", '<h3>${_t("bachelors_plus")}</h3>')
html = html.replace('<div class="stat-label">of all jobs</div>', '<div class="stat-label">${_t("of_all_jobs")}</div>')
html = html.replace('<h3>Jobs by education</h3>', '<h3>${_t("jobs_by_education")}</h3>')
html = html.replace('<h3>Education tiers</h3>', '<h3>${_t("education_tiers")}</h3>')
html = html.replace('<h3>Avg pay by education</h3>', '<h3>${_t("avg_pay_by_edu")}</h3>')
html = html.replace('<h3>Avg outlook by education</h3>', '<h3>${_t("avg_outlook_by_edu")}</h3>')
html = html.replace('<h3>No degree / HS</h3>', '<h3>${_t("no_degree_hs")}</h3>')
html = html.replace('<div class="stat-label">jobs, no degree required</div>', '<div class="stat-label">${_t("no_degree_req")}</div>')

# block Exposure
html = html.replace('<h3>Avg. exposure</h3>', '<h3>${_t("avg_exposure")}</h3>')
html = html.replace('<div class="stat-label">job-weighted, 0\\u201310</div>', '<div class="stat-label">${_t("0_10")}</div>')
html = html.replace('<h3>Jobs by exposure</h3>', '<h3>${_t("jobs_by_exposure")}</h3>')
html = html.replace('<h3>Exposure tiers</h3>', '<h3>${_t("exposure_tiers")}</h3>')
html = html.replace('<h3>Exposure by pay</h3>', '<h3>${_t("exposure_by_pay")}</h3>')
html = html.replace('<h3>Exposure by education</h3>', '<h3>${_t("exposure_by_edu")}</h3>')
html = html.replace('<h3>Wages exposed</h3>', '<h3>${_t("wages_exposed")}</h3>')
html = html.replace('<div class="stat-label">annual, in jobs scoring 7+</div>', '<div class="stat-label">${_t("in_jobs_7_plus")}</div>')


# Replace Load section logic
load_replacement = """function applyI18nToDOM() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (window.__i18n[key]) el.innerHTML = window.__i18n[key];
  });
}

function loadLanguage(lang) {
  fetch("i18n/" + lang + ".json")
    .then(r => r.json())
    .then(dict => {
      window.__i18n = dict;
      applyI18nToDOM();
      if(data.length > 0) {
        updateStats();
        drawGradientLegend();
        draw();
      }
    }).catch(e => console.error("Missing translation:", e));
}

document.getElementById("languageSelect").addEventListener("change", (e) => {
  loadLanguage(e.target.value);
});

fetch("data.json")
  .then(r => r.json())
  .then(d => {
    data = d;
    loadLanguage("en");
    updateStats();
    drawGradientLegend();
    resize();
  });"""

html = re.sub(r'fetch\("data\.json"\).*?\}\);', load_replacement, html, flags=re.DOTALL)

with open("site/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated site/index.html to use i18n placeholders.")
