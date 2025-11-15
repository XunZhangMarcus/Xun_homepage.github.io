---
permalink: /education/
title: "Education Background"
excerpt: "Academic journey and educational achievements"
author_profile: true
classes: wide
---

<style>
.education-container {
  max-width: 1000px;
  margin: 0 auto;
}

.timeline {
  position: relative;
  padding-left: 2em;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 1em;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, #0366d6, #28a745);
}

.education-item {
  position: relative;
  margin-bottom: 3em;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.education-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.education-item::before {
  content: '';
  position: absolute;
  left: -2.5em;
  top: 2em;
  width: 1em;
  height: 1em;
  background: #0366d6;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 0 0 3px #0366d6;
}

.education-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5em;
}

.degree-title {
  font-size: 1.3em;
  font-weight: bold;
  margin-bottom: 0.5em;
}

.institution {
  font-size: 1.1em;
  opacity: 0.9;
  margin-bottom: 0.3em;
}

.duration {
  background-color: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9em;
  display: inline-block;
}

.education-content {
  padding: 1.5em;
}

.major-info {
  background-color: #f8f9fa;
  padding: 1em;
  border-radius: 8px;
  margin-bottom: 1em;
}

.major-title {
  font-weight: bold;
  color: #0366d6;
  margin-bottom: 0.5em;
}

.coursework {
  margin-top: 1em;
}

.coursework h4 {
  color: #28a745;
  margin-bottom: 0.5em;
}

.course-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5em;
  margin-top: 0.5em;
}

.course-item {
  background-color: #e8f4fd;
  padding: 0.5em;
  border-radius: 6px;
  font-size: 0.9em;
  text-align: center;
}

.achievements {
  margin-top: 1em;
  padding: 1em;
  background-color: #f0fff4;
  border-left: 4px solid #28a745;
  border-radius: 0 8px 8px 0;
}

.achievements h4 {
  color: #28a745;
  margin-top: 0;
}

.achievement-item {
  margin-bottom: 0.5em;
  padding-left: 1em;
  position: relative;
}

.achievement-item::before {
  content: '🏆';
  position: absolute;
  left: 0;
}

.research-focus {
  margin-top: 1em;
  padding: 1em;
  background-color: #fff8e1;
  border-left: 4px solid #ffc107;
  border-radius: 0 8px 8px 0;
}

.research-focus h4 {
  color: #f57c00;
  margin-top: 0;
}

.summary-stats {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  padding: 2em;
  border-radius: 12px;
  margin-bottom: 2em;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1em;
  margin-top: 1em;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  display: block;
}

.stat-label {
  opacity: 0.9;
  font-size: 0.9em;
}

@media (max-width: 768px) {
  .timeline {
    padding-left: 1em;
  }
  
  .timeline::before {
    left: 0.5em;
  }
  
  .education-item::before {
    left: -1.5em;
  }
  
  .education-header {
    padding: 1em;
  }
  
  .education-content {
    padding: 1em;
  }
  
  .course-list {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="education-container">

# 📖 Education Background

<div class="summary-stats">
  <h3>Academic Journey Overview</h3>
  <div class="stats-grid">
    <div class="stat-item">
      <span class="stat-number">7</span>
      <span class="stat-label">Years of Study</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">2</span>
      <span class="stat-label">Degrees</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">2</span>
      <span class="stat-label">Universities</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">3+</span>
      <span class="stat-label">Research Papers</span>
    </div>
  </div>
</div>

<div class="timeline">

<div class="education-item">
  <div class="education-header">
    <div class="degree-title">Master of Engineering (M.Eng.)</div>
    <div class="institution">Tongji University, Shanghai</div>
    <div class="duration">June 2022 - June 2025</div>
  </div>
  
  <div class="education-content">
    <div class="major-info">
      <div class="major-title">Major: Civil Engineering</div>
      <div><strong>College:</strong> College of Civil Engineering</div>
      <div><strong>Specialization:</strong> Hydraulic Engineering & Groundwater Modeling</div>
      <div><strong>Research Focus:</strong> Deep Learning Applications in Hydrogeology</div>
    </div>

    <div class="research-focus">
      <h4>🔬 Master's Research</h4>
      <p><strong>Thesis Topic:</strong> Deep Learning-Based Parameterization Methods for Groundwater Flow and Solute Transport Modeling</p>
      <p><strong>Supervisor:</strong> Prof. S. Jiang</p>
      <p><strong>Key Research Areas:</strong></p>
      <ul>
        <li>Development of Deep Learning-based Parameterization Methods (DLPMs)</li>
        <li>Creation of deep learning surrogate models for groundwater solute transport prediction</li>
        <li>Integration of DDPM and ILUES for contaminant source identification</li>
        <li>Non-Gaussian hydraulic conductivity field characterization</li>
      </ul>
    </div>

    <div class="coursework">
      <h4>📚 Key Coursework</h4>
      <div class="course-list">
        <div class="course-item">Advanced Fluid Mechanics</div>
        <div class="course-item">Groundwater Hydrology</div>
        <div class="course-item">Numerical Methods</div>
        <div class="course-item">Data Science & Machine Learning</div>
        <div class="course-item">Environmental Engineering</div>
        <div class="course-item">Mathematical Modeling</div>
        <div class="course-item">Statistics & Probability</div>
        <div class="course-item">Research Methodology</div>
      </div>
    </div>

    <div class="achievements">
      <h4>🏆 Master's Achievements</h4>
      <div class="achievement-item">Outstanding Master's Graduates of Tongji University (2025)</div>
      <div class="achievement-item">Outstanding Graduate Student of Tongji University (2024)</div>
      <div class="achievement-item">Graduate National Scholarship (2024)</div>
      <div class="achievement-item">Outstanding Graduate Student Presentation Award - International Forum on Groundwater (2024)</div>
      <div class="achievement-item">Published 3 peer-reviewed research papers</div>
      <div class="achievement-item">Editorial Board Member of Hydro90 Community</div>
    </div>
  </div>
</div>

<div class="education-item">
  <div class="education-header">
    <div class="degree-title">Bachelor of Engineering (B.Eng.)</div>
    <div class="institution">Northwest A&F University, Yangling</div>
    <div class="duration">September 2018 - June 2022</div>
  </div>
  
  <div class="education-content">
    <div class="major-info">
      <div class="major-title">Major: Water Conservancy and Hydraulic Engineering</div>
      <div><strong>College:</strong> College of Water Resources and Architectural Engineering</div>
      <div><strong>Focus:</strong> Hydraulic Engineering Complex and Environmental Interaction</div>
    </div>

    <div class="research-focus">
      <h4>🔬 Undergraduate Research</h4>
      <p><strong>Research Areas:</strong></p>
      <ul>
        <li>Hydraulic engineering systems and their environmental impacts</li>
        <li>Water resource management and conservation</li>
        <li>Foundation studies in fluid mechanics and hydrology</li>
        <li>Introduction to computational methods in water engineering</li>
      </ul>
    </div>

    <div class="coursework">
      <h4>📚 Core Curriculum</h4>
      <div class="course-list">
        <div class="course-item">Hydraulic Engineering</div>
        <div class="course-item">Water Resources Engineering</div>
        <div class="course-item">Fluid Mechanics</div>
        <div class="course-item">Hydrology</div>
        <div class="course-item">Structural Engineering</div>
        <div class="course-item">Environmental Engineering</div>
        <div class="course-item">Engineering Mathematics</div>
        <div class="course-item">Computer Programming</div>
        <div class="course-item">Engineering Drawing</div>
        <div class="course-item">Materials Science</div>
      </div>
    </div>

    <div class="achievements">
      <h4>🏆 Undergraduate Achievements</h4>
      <div class="achievement-item">Chunyu Scholarship (2019-2021)</div>
      <div class="achievement-item">National College Students Mathematics Competition - National First Prize (2021)</div>
      <div class="achievement-item">National College Students English Competition - Second Prize (2021)</div>
      <div class="achievement-item">National Undergraduate Mathematical Modeling Competition - Shaanxi Province Second Prize (2020)</div>
      <div class="achievement-item">Consistent academic excellence throughout undergraduate studies</div>
    </div>
  </div>
</div>

</div>

---

## Academic Evolution & Future Plans

My educational journey reflects a **progressive specialization** from broad hydraulic engineering foundations to cutting-edge applications of artificial intelligence in groundwater research:

### 🎯 Undergraduate Foundation (2018-2022)
- Built strong fundamentals in hydraulic engineering and water resources
- Developed mathematical and computational skills through competition success
- Established interest in environmental applications of engineering

### 🚀 Graduate Specialization (2022-2025)
- Specialized in groundwater modeling and data science integration
- Pioneered research in deep learning applications for hydrogeology
- Achieved recognition through publications and international presentations

### 🔮 Future Aspirations
- **PhD Studies**: Planning to pursue doctoral degree in related field
- **Research Focus**: Continue advancing AI applications in environmental engineering
- **Global Impact**: Contribute to solving water security and climate challenges

*This educational foundation has prepared me for advanced research in hydraulic engineering and positions me well for future contributions to the field of environmental engineering and water sciences.*

</div> 