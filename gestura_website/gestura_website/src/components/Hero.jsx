import { motion } from "framer-motion";
import "../styles/hero.css";

export default function Hero({ onExplore }) {
  return (
    <section className="hero-bg">
      <motion.div
        className="hero-content"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        <h1>Gestura</h1>
        <p className="tagline">Bridging communication through gestures</p>
        <button className="cta-btn" onClick={onExplore}>
          Explore Project
        </button>
      </motion.div>
    </section>
  );
}