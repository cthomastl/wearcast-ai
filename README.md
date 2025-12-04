WearCast AI is a full-stack, cloud-native application that generates real-time outfit recommendations based on live weather conditions.

Users enter a city, the app fetches actual meteorological data from Open-Meteo, enriches it using OpenAI, and returns natural-language styling advice — fast, simple, and accurate.

The frontend is deployed globally on Amazon S3 + CloudFront, while the backend runs in a secure, scalable AWS ECS Fargate environment.

✨ Features
Frontend

Modern UI built with HTML + TailwindCSS + JavaScript

Responsive, mobile-first design

Calls backend API for recommendations

Backend

Python Flask API

Gunicorn production server

Integrates:

OpenAI GPT for generating outfit suggestions

Open-Meteo API for live weather data

Cloud & DevOps

Dockerized backend application

Private image hosting with Amazon ECR

Serverless containers on AWS ECS Fargate

Application Load Balancer (ALB) for routing + health checks

Frontend hosted on Amazon S3, accelerated with CloudFront CDN

Secure architecture using VPC subnets, security groups, IAM roles

🔧 Tech Stack
Frontend

HTML

TailwindCSS

JavaScript

Backend

Python 3

Flask

Gunicorn

Requests

OpenAI Python SDK

Cloud & Deployment

Docker

Amazon ECR

Amazon ECS Fargate

Application Load Balancer

Amazon S3

Amazon CloudFront

IAM / Security Groups / VPC


![Untitled](https://github.com/user-attachments/assets/b32e0847-0516-4992-904b-cbd27d21e424)

<img width="956" height="410" alt="WearCast-After" src="https://github.com/user-attachments/assets/8e4e6613-5bd1-4a45-a4fd-769179daf24d" />

<img width="955" height="409" alt="WearCast-Before" src="https://github.com/user-attachments/assets/0091309a-22fd-4bce-abb0-d0fa018d309d" />

