# Video Tagging Application

This application is designed to automatically tag and categorize videos using advanced machine learning techniques. It consists of several components working together to provide accurate and efficient video classification.

## How to run


To run the Video Tagging Application, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/video-tagging-app.git
   cd video-tagging-app
   ```

2. Copy the `.env.example` file to `.env` and fill in the necessary environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your specific configuration details.

3. Make sure you have Docker and Docker Compose installed on your system.

4. Build and start the containers:
   ```
   docker-compose up
   ```

5. Once all services are up and running, you can access:
   - The frontend application at: http://localhost
   - The API documentation at: http://api.localhost/docs
   - Flower (Celery monitoring) at: http://localhost:5555

6. To stop the application, use:
   ```
   docker-compose down
   ```

Note: If you're using the vLLM service, ensure you have NVIDIA GPU support configured for Docker.


## Environment Variables

The application uses several environment variables for configuration. Here's a list of the key variables from the `.env` file:

- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `ROOT_DIR`: Root directory for volume mapping
- `API_URL`: URL for the API (e.g., http://api.localhost)
- `REDIS_PORT`: Port for Redis (default: 6379)
- `HOST`: Host for the application (e.g., localhost)
- `OPENROUTER_BASE_URL`: BaseURL for OpenApi compatible API
- `OPENROUTER_API_KEY`: API key for OpenApi compatible API
- `HUGGING_FACE_HUB_TOKEN`: Token for Hugging Face Hub

### Model Configuration

The application supports different model configurations. You can use either the OpenRouter model or a local Hugging Face model. Here are the relevant variables and possible combinations:

1. Using OpenRouter:
   - `MODEL_NAME=openrouter`
   - `OPENROUTER_MODEL_NAME=meta-llama/llama-3.1-70b-instruct`
   - `OPENROUTER_API_KEY=your_openrouter_api_key`

2. Using a local Hugging Face model:
   - `MODEL_NAME=hf`
   - `HF_MODEL_NAME=unsloth/Llama-3.2-1B-Instruct`
   - `HUGGING_FACE_HUB_TOKEN=your_huggingface_token`

Choose one combination based on your preferred model setup. Make sure to set the corresponding API keys or tokens.



For more detailed instructions on running specific components or troubleshooting, please refer to the individual README files in each service's directory.

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
