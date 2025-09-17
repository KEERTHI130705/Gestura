import { useRef } from "react";
import Hero from "./components/Hero";
import About from "./components/About";
import Demo from "./components/Demo";
import Team from "./components/Team";
import Contact from "./components/Contact";
import Navbar from "./components/Navbar";
import TechStack from "./components/TechStack";

function App() {
  const aboutRef = useRef(null);
  const techstackRef = useRef(null); // <-- Add this line
  const demoRef = useRef(null);
  const teamRef = useRef(null);
  const contactRef = useRef(null);

  const handleExplore = () => {
    aboutRef.current.scrollIntoView({ behavior: "smooth" });
  };

  const sectionRefs = {
    about: aboutRef,
    techstack: techstackRef,
    demo: demoRef,
    team: teamRef,
    contact: contactRef,
    
  };

  return (
    <>
      <Navbar sectionRefs={sectionRefs} />
      <Hero onExplore={handleExplore} />
      <div ref={aboutRef}>
        <About />
      </div>
      <div ref={techstackRef}>
        <TechStack />
      </div>
      <div ref={demoRef}>
        <Demo />
      </div>
      <div ref={teamRef}>
        <Team />
      </div>
      <div ref={contactRef}>
        <Contact />
      </div>
    </>
  );
}

export default App;