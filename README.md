WearCast AI: Cloud-Native Generative Styling Engine
Project Overview
WearCast AI is a full-stack application that leverages OpenAI's GPT models and Open-Meteo's real-time weather data to solve a daily human problem: deciding what to wear. Built with a "Security-First" and "Serverless-First" mindset, the application provides instantaneous, natural-language recommendations through a globally distributed frontend and a containerized backend.

The Architecture: How It Was Built
1. The Intelligence Layer (Backend)
The backend is a Python Flask API designed for high-concurrency and intelligent data enrichment.

Data Orchestration: The API captures user input, queries the Open-Meteo API for precise local weather variables (temperature, precipitation, wind speed), and feeds this telemetry into OpenAI's GPT SDK.

Prompt Engineering: Logic was implemented to ensure the AI returns concise, style-conscious, and weather-appropriate advice.

Production Grade: The application utilizes Gunicorn as a WSGI server to manage multiple worker processes, ensuring the API remains responsive under load.

2. The Containerization & DevOps Pipeline
To ensure environment parity and rapid scaling, the backend was fully dockerized.

Dockerization: The Python environment was packaged into a lightweight Docker image.

Image Registry: Images are versioned and hosted securely in Amazon ECR (Elastic Container Registry).

Orchestration: Deployed using AWS ECS Fargate, removing the overhead of managing EC2 instances. This serverless container approach allows the application to scale automatically based on traffic.

Traffic Management: An Application Load Balancer (ALB) serves as the entry point for the backend, performing health checks and distributing traffic across the container fleet.

3. Global Edge Delivery (Frontend)
The user interface was built to be lightweight and extremely fast.

Static Hosting: The HTML/TailwindCSS frontend is hosted on Amazon S3.

Content Delivery (CDN): Amazon CloudFront is utilized to cache and serve the frontend from edge locations worldwide, drastically reducing latency and providing SSL/TLS encryption.

Technical Evidence
Infrastructure Performance
The images below demonstrate the successful deployment and connectivity of the serverless backend. <img width="956" height="410" alt="WearCast-After" src="https://github.com/user-attachments/assets/8e4e6613-5bd1-4a45-a4fd-769179daf24d" /> Figure 1: Verified backend API response and service health.

<img width="955" height="409" alt="WearCast-Before" src="https://github.com/user-attachments/assets/0091309a-22fd-4bce-abb0-d0fa018d309d" /> Figure 2: Initial system logs showing successful container initialization and ECR image pull.

Technical Stack
Frontend & UI
HTML / TailwindCSS: Responsive, utility-first styling.

JavaScript: Asynchronous API handling for real-time updates.

Backend & AI
Python 3 / Flask: Core logic and RESTful API development.

OpenAI SDK: Generative AI enrichment for natural language output.

Requests: High-performance HTTP client for weather data retrieval.

Cloud Infrastructure (AWS)
Compute: ECS Fargate (Serverless Containers).

Networking: VPC, Public/Private Subnets, Application Load Balancer.

Storage & CDN: Amazon S3 & CloudFront.

Security: IAM Roles (Least Privilege), Security Groups.

Skills Demonstrated
Generative AI Integration: Implementing LLMs to transform structured data into unstructured natural language.

Cloud Architecture: Designing multi-tier, highly available systems on AWS.

Container Orchestration: Managing the lifecycle of microservices via Docker and ECS.

CI/CD Fundamentals: Streamlining code to cloud deployment using ECR and Fargate task definitions.
