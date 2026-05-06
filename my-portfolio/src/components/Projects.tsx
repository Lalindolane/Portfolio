type Project = {
    title: string;
    description: string;
    github: string;
};

const projects: Project[] = [
    {
        title: "Dijkstra's Algorithm",
        description: "Models tsunami pathing using Dijkstra's to model the quickest path from point of origin to impact point, giving the time it takes to travel as well as reproducing that path",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/Dijkstra",
    },
    {
        title: "Basic Markov Chains",
        description: "Predictive text using Yoda speech as a sample",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/MarkovChains",
    },
    {
        title: "Breadth First Search",
        description: "Uses a BFS to model the 'Degrees of Bacon' in actors",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/BreadthFirstSearch",
    },
    {
        title: "Convolution Filtering",
        description: "Uses convolution to clean up both audio as well as a png image for clearer reproduction and image clarity",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/ConvolutionFiltering",
    },
    {
        title: "Binary Trees",
        description: "Dives in depth into the efficiencies and temporal complexities of Doubly Linked Lists, Binary Trees, and AVL Trees",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/BinaryTrees",
    },
    {
        title: "Fourier Transform",
        description: "Uses Fourier Transform to create chords, waves, arpeggios, etc. using sampling, DFT, and FFT",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/FourierTransform",
    },
    {
        title: "Nearest Neighbor",
        description: "Uses K-D Trees for hand writing recognition",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/NearestNeighbor",
    },
    {
        title: "My Portfolio Website",
        description: "Designed and created my own portfolio website!",
        github: "https://github.com/Lalindolane/Portfolio/tree/main/my-portfolio",
    }
];

export default function Projects() {
    return (
        <section id="projects" style={{ padding: "2rem" }}>
            <h2>Projects</h2>

            {projects.map((project, index) => (
                <div key={index} style={{ marginBottom: "1.5rem" }}>
                    <h3>{project.title}</h3>
                    <p>{project.description}</p>
                    <a
                        href={project.github}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        View Code
                    </a>
                </div>
            ))}
        </section>
    );
}