import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Projects from "./components/Projects";
import Contact from "./components/Contact";
import Experience from "./components/Experience"
import "./styles/App.css"

function App() {
  return (
    <div className="app">
      <Navbar />
        <Hero />
        <Experience />
        <Projects />
        <Contact />
    </div>
  );
}

export default App;