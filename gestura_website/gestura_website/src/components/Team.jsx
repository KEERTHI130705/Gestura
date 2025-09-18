import React from "react";
import "../styles/team.css";
import { FaLinkedin, FaGithub } from "react-icons/fa";
import keerthiPic from "../assets/keerthi.png";

const Team = () => {
  return (
    <section className="team" id="team">
      <h2 className="team-title">Meet Our Team</h2>
      <div className="team-container">
        
        {/* Member 1 */}
        <div className="team-member">
          <div className="member-pic">
            <img src={keerthiPic} alt="Keerthi" />
          </div>
          <h3 className="member-name">Keerthi Harsha</h3>
          <p className="member-role">Frontend & Deployment</p>
          <div className="member-links">
            <a href="https://linkedin.com/in/keerthi-harsha-alle" target="_blank" rel="noreferrer">
              <FaLinkedin />
            </a>
            <a href="https://github.com/keerthi130705" target="_blank" rel="noreferrer">
              <FaGithub />
            </a>
          </div>
        </div>

        {/* Member 2 */}
        <div className="team-member">
          <div className="member-pic">
            <img src="/team/member2.jpg" alt="Teammate" />
          </div>
          <h3 className="member-name">Preethi</h3>
          <p className="member-role">AI/ML & Backend Developer</p>
          <div className="member-links">
            <a href="https://linkedin.com/in/oruganti-preethi-19268b368" target="_blank" rel="noreferrer">
              <FaLinkedin />
            </a>
            <a href="https://github.com/o-preethi" target="_blank" rel="noreferrer">
              <FaGithub />
            </a>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Team;
