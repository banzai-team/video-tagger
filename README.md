# Video Tagging Application

This application is designed to automatically tag and categorize videos using advanced machine learning techniques. It consists of several components working together to provide accurate and efficient video classification.

## Stack Overview

1. **Frontend**: A web interface built with modern web technologies.
2. **Backend API**: FastAPI-based service handling requests and managing the application logic.
3. **Database**: PostgreSQL for storing video metadata and tags.
4. **Message Broker**: RabbitMQ for managing asynchronous tasks.
5. **ML Service**: A dedicated service for running machine learning models.
6. **Celery Workers**: For processing background tasks.
7. **Docker**: Used for containerization and easy deployment.
8. **Traefik**: As a reverse proxy and load balancer.

## Machine Learning Pipeline

Our ML pipeline uses a hierarchical approach for video tagging. It incorporates:

- Image analysis for visual content
- Audio processing for speech and sound recognition
- Natural Language Processing for text analysis of video descriptions and titles

For a detailed explanation of the ML algorithm and its architecture, please refer to [@README.ml-algo.md](./ml/README.ml-algo.md).

## Running the Application

To set up and run the application, follow the instructions in [@README.ml-run.md](./ml/README.ml-run.md). This guide includes:

- Setting up the Python virtual environment
- Installing dependencies
- Configuring the environment
- Running the application using Docker Compose

## Key Features

- Hierarchical category prediction
- Multi-modal analysis (video, audio, text)
- Scalable architecture for processing large volumes of videos
- Flexible and adaptable to various video classification tasks

For more information on the machine learning aspects and how to run the ML pipeline, please consult the referenced README files.
