export default function Hero() {
    return (
        <section
            id="home"
            className="section hero"
        >
            <h1>
                Lane <span>Lindstrom</span>
            </h1>

            <h2>
                Machine Learning Engineer • Full-Stack Developer
            </h2>

            <p>
                I build intelligent software—from multiplayer web applications to
                evolutionary AI systems that learn through genetic algorithms.
                I'm currently a Computer Science Research Assistant at BYU where I
                develop AI agents and model social interaction through game theory.
            </p>

            <div className="hero-buttons">
                
                <a href="#experience" style={{
                    'color': '#5CC6D0',

                    'transition': 'color 0.2s ease',

                    'padding': '0.5rem 1rem',
                    }}>
                    View My Work
                </a>
                <a href="/Lindstrom_Lane.pdf" style={{
                    'color': '#5CC6D0',

                    'transition': 'color 0.2s ease',

                    'padding': '0.5rem 1rem',
                    }}> Resume</a>
            </div>
        </section>
    );
}