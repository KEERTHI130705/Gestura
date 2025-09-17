import React from "react";
import "../styles/demo.css";

const Demo = () => {
  return (
    <section className="demo" id="demo">
      <div className="demo-container">
        <h2 className="demo-title">Try Gestura Live</h2>
        <p className="demo-description">
          Experience how <span>Gestura</span> translates sign language into text
          and speech. Click below to launch the demo in real-time and see the
          power of gesture-based communication for the speech-impaired.
        </p>
        <a
          href="https://your-streamlit-link-here.streamlit.app"
          target="_blank"
          rel="noopener noreferrer"
          className="demo-button"
        >
          Launch Demo
        </a>
      </div>
    </section>
  );
};

export default Demo;
