export default function Contact() {
    return (
        <section
            id="contact"
            className="section contact"
        >
            <h2 className="section-title">
                Contact
            </h2>

            <div className="contact-card">
                <p>
                    <a href="mailto:lalindo.lane@gmail.com">
                        lalindo.lane@gmail.com
                    </a>
                </p>

                <p>
                    Mobile:
                    {" "}
                    +1 (385) 985-7545
                </p>

                <p>
                    LinkedIn:
                    {" "}
                    <a
                        href="https://www.linkedin.com/in/lane-lindstrom-879364356"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        View Profile
                    </a>
                </p>
            </div>
        </section>
    );
}