import React from "react";
import "../styles/techstack.css";

const TechStack = () => {
  return (
    <section className="techstack" id="techstack">
      <h2 className="techstack-title">Our Tech Stack</h2>
      <div className="techstack-container">

        {/* Frontend */}
        <div className="tech-category">
          <h3>Frontend</h3>
          <div className="tech-logos">
            <div className="logo-circle">
              <img src="/assets/react.png" alt="React" />
            </div>
            <div className="logo-circle">
              <img src="/assets/html.png" alt="HTML5" />
            </div>
            <div className="logo-circle">
              <img src="/assets/css.png" alt="CSS3" />
            </div>
          </div>
        </div>

        {/* AI / Backend */}
        <div className="tech-category">
          <h3>AI / Backend</h3>
          <div className="tech-logos">
            <div className="logo-circle">
              <img src="/assets/python.png" alt="Python" />
            </div>
            <div className="logo-circle">
              <img src="/assets/opencv.png" alt="OpenCV" />
            </div>
            <div className="logo-circle">
              <img src="/assets/scikit.png" alt="Scikit-learn" />
            </div>
          </div>
        </div>

        {/* Deployment */}
        <div className="tech-category">
          <h3>Deployment</h3>
          <div className="tech-logos">
            <div className="logo-circle">
              <img src="/logos/streamlit.png" alt="Streamlit" />
            </div>
            <div className="logo-circle">
              <img src="/assets/github.png" alt="GitHub" />
            </div>
            <div className="logo-circle">
              <img src="/logos/vercel.png" alt="Vercel" />
            </div>
          </div>
        </div>

      </div>
    </section>
  );
};

export default TechStack;