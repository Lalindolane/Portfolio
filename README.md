# Lane Lindstrom Portfolio

A portfolio showcasing my software engineering projects, full-stack development experience, and technical interests.

**Live Site:** https://portfolio-psi-wheat-67.vercel.app/

---

## About

This portfolio highlights projects that demonstrate my experience building full-stack applications, multiplayer systems, backend infrastructure, and AI-powered software.

My primary featured project, **Takes a Village**, combines a React frontend with a FastAPI backend, real-time WebSocket communication, Dockerized services, MySQL persistence, and genetic algorithm AI agents. The portfolio also includes additional projects that showcase my work in web development and software engineering.

[Visit takesAVillage repo](https://github.com/DallinJacksonE/takesAVillage)

---

## Built With

### Frontend

- React
- TypeScript
- Vite
- HTML5
- CSS3

### Backend Experience

- Python
- FastAPI
- asyncio
- WebSockets
- MySQL

### Tools

- Docker
- Git
- GitHub
- GitHub Actions

---

# Featured Project

## Takes a Village

Takes a Village is a multiplayer social-deduction resource management game where players must cooperate to survive while having complete freedom to deceive one another during trades and negotiations.

Players gather resources, construct developments, hire others as workers, negotiate contracts, build campfires, and attempt to outlast the rest of the village.

[Visit takesAVillage repo](https://github.com/DallinJacksonE/takesAVillage)

### Languages + Packages

- React
- TypeScript
- Python
- FastAPI
- WebSockets
- MySQL
- Docker

### Technical Highlights

- Designed a multiplayer client/server architecture
- Implemented asynchronous communication using FastAPI and asyncio
- Reduced network traffic by broadcasting only player-specific updates instead of entire game states asynchronously
- Created reusable command dispatchers and action factories to simplify backend logic
- Built genetic algorithm AI agents capable of learning through mutation, crossover, and fitness evaluation
- Containerized frontend, backend, database, and AI training infrastructure with Docker

### Engineering Challenges

One of the largest challenges was creating a backend architecture that supported both human players and autonomous AI agents while remaining scalable.

The original backend relied heavily on large conditional logic and broadcasting complete game states. This was redesigned using reusable command dispatchers, contract factories, and asynchronous WebSocket communication that transmits only essential information to each connected player. The result was cleaner code, lower latency, and a backend architecture that is easier to extend.

---


# Running Locally

Clone the repository

```bash
git clone https://github.com/Lalindolane/Portfolio.git
```

Navigate to the portfolio

```bash
cd Portfolio/my-portfolio
```

Install dependencies

```bash
npm install
```

Start the development server

```bash
npm run dev
```

Open your browser

```
http://localhost:5173
```

Create a production build

```bash
npm run build
```

Preview the production build

```bash
npm run preview
```

---

# Deployment

This portfolio is deployed using **Vercel**.

Every push to the `main` branch automatically generates a new production deployment.

---

# Future Improvements

- Additional project case studies
- Interactive project demos
- Blog documenting engineering decisions
- Improved accessibility
- Additional animations and polish
- Expanded mobile optimizations

---

# Contact

**Lane Lindstrom**

Portfolio  
https://portfolio-psi-wheat-67.vercel.app/

GitHub  
https://github.com/Lalindolane

LinkedIn  
*(Add your LinkedIn URL)*

Email  
*(Add your preferred contact email)*

---

# License

This project is licensed under the MIT License.