export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <div className="logo">
                    <a href="#home">
                        Lane Lindstrom
                    </a>
                </div>

                <ul className="nav-links">

                    <li>
                        <a href="#experience">
                            Experience
                        </a>
                    </li>

                    <li>
                        <a href="#projects">
                            Smaller Projects
                        </a>
                    </li>

                    <li>
                        <a href="#contact">
                            Contact
                        </a>
                    </li>
                </ul>
                <div>
                    <a
                        href="https://acme.byu.edu"
                        target="_blank"
                    >
                    <img
                        src="/images/acme.png"
                        alt="Acme logo"
                        width="35px"
                    />
                    </a>
                </div>
            </div>
        </nav>
    );
}