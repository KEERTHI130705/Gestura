import React from "react";
import "../styles/techstack.css";
import pythonLogo from "../assets/python.png";
import opencvLogo from "../assets/opencv.png";
import scikitLogo from "../assets/scikit.png";
import reactLogo from "../assets/react.png";
import htmlLogo from "../assets/html.png";
import cssLogo from "../assets/css.png";
import githubLogo from "../assets/github.png";

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
              <img src={reactLogo} alt="React" />
            </div>
            <div className="logo-circle">
              <img src={htmlLogo} alt="HTML5" />
            </div>
            <div className="logo-circle">
              <img src={cssLogo} alt="CSS3" />
            </div>
          </div>
        </div>

        {/* AI / Backend */}
        <div className="tech-category">
          <h3>AI / Backend</h3>
          <div className="tech-logos">
            <div className="logo-circle">
              <img src={pythonLogo} alt="Python" />
            </div>
            <div className="logo-circle">
              <img src={opencvLogo} alt="OpenCV" />
            </div>
            <div className="logo-circle">
              <img src={scikitLogo} alt="Scikit-learn" />
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
              <img src={githubLogo} alt="GitHub" />
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