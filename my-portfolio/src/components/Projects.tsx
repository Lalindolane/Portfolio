type Project = {
    title: string;
    description: string;
    github: string;
};

const projects: Project[] = [
    {
        title: "Dijkstra's Algorithm",
        description:
            "Models tsunami pathing using Dijkstra's algorithm to determine the fastest route from origin to impact point.",
        github:
            "https://github.com/Lalindolane/Portfolio/tree/main/Dijkstra",
    },

    {
        title: "Basic Markov Chains",
        description:
            "Predictive text generation using Yoda speech as sample training data.",
        github:
            "https://github.com/Lalindolane/Portfolio/tree/main/MarkovChains",
    },

    {
        title: "Breadth First Search",
        description:
            "Uses BFS to model the Degrees of Bacon relationship between actors.",
        github:
            "https://github.com/Lalindolane/Portfolio/tree/main/BreadthFirstSearch",
    },

    {
        title: "Convolution Filtering",
        description:
            "Uses convolution filtering to improve image clarity and clean noisy audio signals.",
        github:
            "https://github.com/Lalindolane/Portfolio/tree/main/ConvolutionFiltering",
    },

    {
        title: "Facial Recognition",
        description:
            "Uses Eigenfaces to identify the closest facial match to a provided image.",
        github:
            "https://github.com/Lalindolane/Portfolio/tree/main/FacialRecognition",
    },

    {
        title: "Fourier Transform",
        description:
            "Creates chords, waves, and arpeggios using FFT and DFT signal processing techniques.",
        github:
            "https://github.com/Lalindolane/Portfolio/tree/main/FourierTransform",
    },
];

export default function Projects() {
    return (
        <section
            id="projects"
            className="section"
        >
            <h2 className="section-title">
                Projects
            </h2>

            <div className="projects-grid">
                {projects.map((project, index) => (
                    <div
                        key={index}
                        className="project-card"
                    >
                        <h3>{project.title}</h3>

                        <p>{project.description}</p>

                        <a
                            href={project.github}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            View Code →
                        </a>
                    </div>
                ))}
            </div>
        </section>
    );
}