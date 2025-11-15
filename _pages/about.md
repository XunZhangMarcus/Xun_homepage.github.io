---
permalink: /
title: "About Me"
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

<div class="hero-panel about-hero">
  <h1>About me</h1>
  <p>Hello there! I'm Xun, currently a Research Assistant in Hydraulic Engineering at Tongji University.</p>
  <p>My academic journey began with a Bachelor's degree in Water Conservancy and Hydraulic Engineering from Northwest A&F University, where I studied everything related to hydraulic engineering complex and its interaction with the environment. During my Master studies, I discovered a more creative fusion between Data Science and Hydrogeology. My research specifically focused on <strong>groundwater flow and solute transport modeling</strong>, which is crucial for evaluating groundwater quality and contamination risks, thereby ensuring the safety of drinking water. Briefly, my work primarily concentrated on two areas: developing new deep learning-based parameterization methods (DLPMs) and creating deep learning surrogate models to predict groundwater solute transport.</p>
  <p>I plan to pursue a PhD degree in the near future.</p>
  <p>Feel free to reach out for discussion, collaboration, or any exciting opportunities!</p>
  <p class="highlight-chip">E-mail: 2232324[at]tongji[dot]edu[dot]cn</p>
</div>

<div class="card-panel about-interests">
  <h2>💻 Current Research Interest</h2>
  <p>Groundwater Pollution, Urban Flooding, Data Assimilation, Physics-informed Deep Learning and Generative AI</p>
</div>

<div class="card-panel about-links">
  <h2>Explore My Work</h2>
  <div class="quick-links-grid">
    <a class="quick-link-card" href="{{ '/news/' | relative_url }}">
      <span class="quick-link-title">🔥 News</span>
    </a>
    <a class="quick-link-card" href="{{ '/publications/' | relative_url }}">
      <span class="quick-link-title">📝 Publications and Conferences</span>
    </a>
    <a class="quick-link-card" href="{{ '/hydro90/' | relative_url }}">
      <span class="quick-link-title">💧 Hydro90</span>
    </a>
    <a class="quick-link-card" href="{{ '/honors/' | relative_url }}">
      <span class="quick-link-title">🎖 Honors and Awards</span>
    </a>
    <a class="quick-link-card" href="{{ '/education/' | relative_url }}">
      <span class="quick-link-title">📖 Educations</span>
    </a>
  </div>
</div>
