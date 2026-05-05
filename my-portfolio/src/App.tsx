import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Projects from "./components/Projects";
import Contact from "./components/Contact";

function App() {
  return (
    <>
      <Navbar name="Lane Lindstrom" />
      <Hero />
      <Projects />
      <Contact />
    </>
  );
}

export default App;