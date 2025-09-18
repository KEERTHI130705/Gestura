import { useState } from "react";
import { motion } from "framer-motion";
import { FaBars, FaTimes } from "react-icons/fa";
import "../styles/navbar.css";

export default function Navbar({ sectionRefs }) {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleNav = (section) => {
    sectionRefs[section]?.current?.scrollIntoView({ behavior: "smooth" });
    setMenuOpen(false); // close menu after click
  };

  return (
    <motion.nav
      className="navbar"
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.7 }}
    >
      <div className="navbar-content">
        <span className="navbar-logo" onClick={() => handleNav("about")}>
          Gestura
        </span>
        <button
          className="navbar-hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <FaTimes /> : <FaBars />}
        </button>
        <ul className={`navbar-links ${menuOpen ? "open" : ""}`}>
          <li>
            <button onClick={() => handleNav("about")}>About</button>
          </li>
          <li>
            <button onClick={() => handleNav("techstack")}>TechStack</button>
          </li>
          <li>
            <button onClick={() => handleNav("demo")}>Demo</button>
          </li>
          <li>
            <button onClick={() => handleNav("team")}>Team</button>
          </li>
          <li>
            <button onClick={() => handleNav("contact")}>Contact</button>
          </li>
        </ul>
      </div>
    </motion.nav>
  );
}