import { motion } from "framer-motion";
import "../styles/features.css";

const features = [
  {
    title: "Real-time Hand Detection",
    desc: "Instantly detects hand gestures using advanced computer vision.",
    icon: "🖐️",
  },
  {
    title: "Gesture-to-Text/Speech",
    desc: "Converts recognized gestures into readable text and speech.",
    icon: "🔊",
  },
  {
    title: "Accessibility Benefits",
    desc: "Empowers communication for everyone, including those with speech or hearing impairments.",
    icon: "♿",
  },
];

export default function Features() {
  return (
    <section className="features-section">
      <h2>Features</h2>
      <div className="features-cards">
        {features.map((f, i) => (
          <motion.div
            className="feature-card"
            key={f.title}
            whileHover={{ scale: 1.05 }}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: i * 0.2 }}
            viewport={{ once: true }}
          >
            <span className="feature-icon">{f.icon}</span>
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}