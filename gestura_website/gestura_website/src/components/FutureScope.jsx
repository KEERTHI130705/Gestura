import React from "react";
import "../styles/futurescope.css";

const futurePoints = [
  {
    title: "Integration with Video Call Platforms",
    desc: "Seamlessly integrate gesture recognition into platforms like Zoom, Meet, and Teams for real-time accessibility.",
    icon: "🎥",
  },
  {
    title: "Support for Multiple Sign Languages",
    desc: "Expand recognition to ISL, BSL, and other sign languages for global inclusivity.",
    icon: "🌍",
  },
  {
    title: "Two-Way Communication",
    desc: "Enable direct translation between speech and signs for interactive conversations.",
    icon: "🔄",
  },
  {
    title: "Offline Lightweight Model",
    desc: "Deploy models that work without internet, ensuring accessibility anywhere.",
    icon: "📦",
  },
  {
    title: "Direct Sign Language Translation",
    desc: "Translate directly from one sign language to another for cross-language communication.",
    icon: "🔗",
  },
];

const FutureScope = () => (
  <section className="future-scope-section" id="future-scope">
    <h2 className="future-scope-title">Future Scope</h2>
    <div className="future-scope-cards">
      {futurePoints.map((point) => (
        <div className="future-scope-card" key={point.title}>
          <div className="future-scope-icon">{point.icon}</div>
          <div className="future-scope-content">
            <h3>{point.title}</h3>
            <p>{point.desc}</p>
          </div>
        </div>
      ))}
    </div>
  </section>
);

export default FutureScope;