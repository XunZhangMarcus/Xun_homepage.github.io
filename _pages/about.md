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
  <p>Hello there! I'm Xun, a graduate of the College of Civil Engineering at Tongji University (June 2025), and currently a Research Assistant in the same department.</p>
  <p>My academic journey began with a Bachelor's degree in Hydraulic Engineering from Northwest A&F University, where I studied everything related to hydraulic engineering complex and its interaction with the environment. During my Master studies, I discovered a more creative fusion between Data Science and Hydrogeology. My Master’s research focused on groundwater flow and solute transport modeling, with my thesis centered on developing new deep learning-based parameterization methods (DLPMs) and building deep learning surrogate models for predicting groundwater solute transport.</p>
  <p>Feel free to reach out for discussion, collaboration, or any exciting opportunities!</p>
  <p>I plan to pursue a PhD degree in the near future.</p>
  <p class="highlight-chip">E-mail: 2232324[at]tongji[dot]edu[dot]cn</p>
</div>

<div class="card-panel about-interests">
  <h2>💻 Current Research Interest</h2>
  <p>Groundwater Modelling, Urban Flooding, Scientific Machine Learning, Inverse Problem, Data Assimilation</p>
  <p>As I am still at an early stage of my research career, I explored a broad range of topics. Some representative examples include:<p>
  <p>Methods side: data assimilation; inverse problems (parameter estimation; interpolation and reconstruction); generative modeling (DDPM, VAE, GAN, flow matching); surrogate modeling (reduced-order modeling); physics-informed neural networks; operator learning; transfer learning; reinforcement learning; graph learning; uncertainty quantification; federated machine learning; causal inference; geostatistics; interpretable machine learning (SHAP, Grad-CAM); upscaling methods for geologic models; coupled surface water–groundwater modeling...<p>
   <p>Applications side: groundwater contamination source identification and high-resolution characterization of hydraulic conductivity fields; groundwater well placement optimization; urban flooding; computational fluid dynamics; atmospheric pollution modeling (Gaussian plume models); seismic waveform inversion; structural health monitoring; inverse design of materials; battery state estimation and structural design of fuel cell catalyst layers; debris floods; inversion of groundwater storage from satellite gravimetry; image-based sediment detection; remote sensing (carbon sources and sinks in lakes); Arctic sea ice...<p> 
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
