import { motion } from "framer-motion";
import "../styles/navbar.css";

export default function Navbar({ sectionRefs }) {
  const handleNav = (section) => {
    sectionRefs[section]?.current?.scrollIntoView({ behavior: "smooth" });
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
        <ul className="navbar-links">
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