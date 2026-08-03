export default function Experience() {
    return (
        <section
            id="experience"
            className="section"
        >
            <h2 className="section-title">Featured Project</h2>
            <h3>Takes a Village</h3>
            <a
                style={{
                    color: "var(--blue-soft)",
                    textDecoration: "none",
                    fontWeight: 600,
                    transition: "color 0.2s ease",
                }}
                href="https://github.com/DallinJacksonE/takesAVillage"
                target="_blank"
                rel="noopener noreferrer"
                >
                View on GitHub →
                </a>
                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    gap: "40px",
                    border: "1px solid var(--border)",
                    borderRadius: "12px",
                    padding: "30px",
                }}>
                    <div>
                    <h3 className="section-subtitle" style={{fontSize: '18px'}}>
                    Full Stack Developer Experience (Undergrad Research)
                    </h3>

                    <p>Relevant skills:</p>
                    <ul
                    style={{
                        margin: 0,
                        paddingLeft: "40px",
                    }}
                    >
                    <li>Typescript (Node.js, React)</li>
                    <li>Python (FastAPI, asyncio, httpx)</li>
                    <li>DTOs, Validation</li>
                    <li>Debugging, Testing</li>
                    <li>Vite</li>
                    <li>Docker</li>
                    <li>MySQL</li>
                    <li>Git/GitHub Actions</li>
                    <li>HTML + CSS</li>
                    </ul>
                    </div>

                <div>
            <img
                    src="/images/researchview.png"
                    alt="Takes a Village Research View"
                    style={{
                    width: "800px",
                    borderRadius: "48px",
                    padding: "40px",
                    }}
                />
                </div>
                </div>

            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "16px",
                    background: "var(--surface)",
                    border: "1px solid var(--border)",
                    borderRadius: "12px",
                    padding: "30px",
                    paddingLeft: "80px",
                }}
            >
                {/* Summary Row */}
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        maxWidth: "1000px",
                        alignItems: "flex-start",
                        gap: "16px",
                    }}
                >
                    <div style={{ flex: 0.85 }}>
                        <h3 style={{ paddingTop: "20px" }} className="section-subtitle">
                            Summary:
                        </h3>
                        <p style={{ margin: 0, lineHeight: 1.7 }}>
                            &nbsp;&nbsp;&nbsp;&nbsp;Takes a Village is a browser game where players manage their
                            resources to build a village and thrive. Resources are very scarce
                            and teamwork is required to survive, but the game allows players to
                            lie about their actions and trades. The frontend is written in
                            TypeScript using React and communicates through WebSockets to a
                            Python backend. The backend stores game data in MySQL and supports a
                            separate bot server for AI training. Our genetic AI agents evolve
                            through mutation, crossover, and fitness evaluation, and all
                            services are containerized with Docker.
                        </p>
                        <a style={{
                            color: "var(--blue-soft)",
                            textDecoration: "none",
                            fontWeight: 600,
                            transition: "color 0.2s ease",
                        }}
                            href='https://tav.djackson.dev/' target="_blank" rel="noopener noreferrer">
                            Visit the Game
                        </a>
                    </div>
                    <div style={{paddingTop: '40px'}}>
                    <img
                        src="/images/gameplay.png"
                        alt="Gameplay screenshot"
                        style={{
                            width: "700px",
                            height: "auto",
                            borderRadius: "8px",
                            flexShrink: 0,
                        }}
                    />
                    </div>
                </div>
                <h3 className="section-subtitle" style={{ paddingTop: "20px" }}>
                            Hurdles:
                        </h3>

                        <p style={{ margin: 0, lineHeight: 1.7 }}>
                            &nbsp;&nbsp;&nbsp;&nbsp;One of the main challenges was implementing a robust system for handling player deception
                            and ensuring fair gameplay while still being lightweight and scalable for bot training. To solve this problem we
                            shifted from flaskio to fastapi and asyncio, cut big if/else trees into reusable formats, and highlighted only sending
                            the most important data through websockets asynchronously to reduce computation time and latency. Instead of a command having to pass
                            through a huge tree and the web socket having to broadcast an entire gamestate through JSON, command and action dispatcher structures
                            can look up identifiers in constant time, and personal updates that contain only vital information are broadcast to players individually.
                        </p>

                        <h3 style={{paddingTop: '20px'}}className="section-subtitle">Design/Architecture Choices:</h3>
                        <p>&nbsp;&nbsp;&nbsp;&nbsp;The design choices for Takes a Village were driven by the need for a scalable and maintainable architecture.
                            We opted for a microservices approach, separating the frontend, backend, and bot infrastructure into distinct services. This allows
                            for independent development, testing, and deployment of each component. Additionally, we implemented an event-driven asynchronous
                            architecture to facilitate communication between services and ensure loose coupling.
                        </p>
                        <p>
                            &nbsp;&nbsp;&nbsp;&nbsp;We use an MVP (Model, View, Presenter) structure in Takes a Village. Our Model is contained in the backend,
                            and is the source of truth in our game. The View and Presenter are found in the frontend. The View handles what players can see or
                            click on, and the Presenter manages the logic for updating the view based on the model's state, acting as a middle man.
                            This lets us separate completely what players/bots can see or do (very important for training bots later as well as clean UX for players)
                            from the backend source of truth and logic.
                        </p>
                        <p>
                            &nbsp;&nbsp;&nbsp;&nbsp;The example given in the hurdles section shows the flexibility of the command architecture we chose to be able to use a single
                            action dispatcher or contract factory to handle actions and social interaction between players by simply labeling what actions they are
                            taking to decipher what the proper backend response should be. This lets us call an execute() function universally and cleans up the code.
                        </p>
            </div>
        </section >
    )
}