import React from "react";
import "../styles/demo.css";
const Demo = () => {
  return (
    <section className="demo" id="demo">
      <div className="demo-container">
        <h2 className="demo-title">Demo Video</h2>
        <p className="demo-description">
          This is how <span>Gestura</span> translates sign language into text
          and speech.
        </p>
        <video
          className="demo-video"
          src="/demo_video.mp4"
          controls
          autoPlay={false}
          style={{ width: "100%", maxWidth: "600px", borderRadius: "16px", marginTop: "2rem" }}
        />
      </div>
    </section>
  );
};

export default Demo;
