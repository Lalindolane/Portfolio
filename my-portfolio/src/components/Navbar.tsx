export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <div className="logo">
                    <a href="#home">Lane Lindstrom</a>
                </div>

                <ul className="nav-links">
                    <li><a href="#projects">Projects</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>

                <a href="#contact" className="nav-button">
                    Get in touch
                </a>
            </div>
        </nav>
    );
}