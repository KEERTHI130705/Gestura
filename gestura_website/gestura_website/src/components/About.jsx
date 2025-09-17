import React from "react";
import "../styles/about.css";

function About() {
  return (
    <section className="about-section">
      <h1 className="about-title">
        About <span className="highlight">Gestura</span>
      </h1>

      <p className="about-text">
        Gestura is an assistive technology project designed to empower people 
        with speech disabilities. Using advanced sign language recognition, 
        Gestura translates hand gestures into text and speech in real time. 
        Our mission is to bridge the communication gap, helping individuals 
        express themselves more confidently and connect with the world without barriers.
      </p>

      <div className="about-cards">
        <div className="about-card">
          <img src="/pictures/signlanguage.png" alt="Sign Language Recognition" />
          <h3>Sign Language Recognition</h3>
          <p>
            Converts hand signs into meaningful text instantly with accuracy.
          </p>
        </div>

        <div className="about-card">
          <img src="/pictures/text&speech.png" alt="Text-to-Speech" />
          <h3>Text & Speech Output</h3>
          <p>
            Translates recognized signs into clear speech for better interaction.
          </p>
        </div>

        <div className="about-card">
          <img src="/pictures/disability.png" alt="Accessibility First" />
          <h3>Accessibility First</h3>
          <p>
            Created to support people with speech and hearing disabilities, 
            ensuring inclusivity and empowerment.
          </p>
        </div>
      </div>
    </section>
  );
}

export default About;
