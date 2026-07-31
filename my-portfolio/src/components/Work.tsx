const experiences = [
  {
    title: "Computer Science Research Assistant",
    company: "Brigham Young University Provo",
    dates: "May 2026 – Present",
    bullets: [
      "Develop full-stack multiplayer browser game using React, TypeScript, Python, SQL, and FastAPI.",
      "Design and optimize evolutionary AI agents using genetic algorithms.",
      "Build backend services and asynchronous game systems.",
      "Containerize applications with Docker."
    ]
  },
  {
    title: "Calculus I & Linear Algebra Grader",
    company: "Brigham Young University Provo",
    dates: "Sept 2025 – Apr 2026",
    bullets: [
      "Graded coursework for over 250 students.",
      "Provided detailed feedback on mathematical reasoning.",
      "Helped students improve problem-solving techniques."
    ]
  },
  {
    title: "Mathematics Research Assistant",
    company: "Brigham Young University Provo",
    dates: "Sept 2025 – Dec 2025",
    bullets: [
      "Researched restricted partition generating functions using the circle method.",
      "Reviewed mathematical literature and proofs.",
      "Collaborated on simplifying and refining research."
    ]
  },
  {
    title: "Public Representative",
    company: "The Church of Jesus Christ of Latter-day Saints Neuquén Argentina Mission",
    dates: "Aug 2022 – Aug 2024",
    bullets: [
      "Led community outreach and service projects.",
      "Taught English to local communities.",
      "Trained and supervised over 75 volunteers.",
      "Fluent in Spanish."
    ]
  }
];

export default function Work() {
  return (
    <section id="work" className="experience">
      <h2>Work Experience</h2>

      <div className="experience-grid">
        {experiences.map((job) => (
          <div className="experience-card" key={job.title}>
            <h3>{job.title}</h3>

            <div className="job-info">
              <span>{job.company}</span>
              <span>{job.dates}</span>
            </div>

            <ul>
              {job.bullets.map((bullet) => (
                <li key={bullet}>{bullet}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}