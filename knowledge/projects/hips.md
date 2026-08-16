# HPIS — Human Performance Intelligence System

## Project Overview

The Human Performance Intelligence System (HPIS) is an AI-powered wearable and distributed data platform designed to collect physiological and activity data, analyze human performance, detect abnormal or stressful states, and provide personalized recommendations. The platform combines multiple physiological and behavioral data sources into a unified intelligent system that generates meaningful insights rather than just displaying raw sensor measurements.

## Problem Context

Current wearable platforms such as smartwatches generally provide isolated measurements including heart rate, sleep, activity, SpO₂, and calories. The main problem is that raw measurements do not directly answer important questions such as why the user is tired, why recovery is low, whether the user is under stress, whether training should occur today, whether physiological state has changed compared with normal baseline, and which physiological factors explain the current state. HPIS addresses this problem by combining multiple physiological and behavioral data sources into a unified intelligent system that builds a more complete representation of the user's state and uses AI to generate meaningful insights.

## Primary Objectives

The objective of HPIS is to build an open and extensible Human Performance Intelligence System capable of collecting physiological data from wearable sensors, simulating a smart wearable using an ESP32, ingesting real-time sensor streams, processing and storing time-series data, detecting stress and other relevant states using machine learning, coordinating specialized AI agents, providing real-time information to the user, combining multiple data sources, generating personalized recommendations, and creating an extensible architecture for additional sensors and AI models. The project follows an MVP-first approach where data flows from the wearable through data collection, real-time streaming, data processing, AI prediction, agent analysis, personalized recommendation generation, and finally to the user dashboard.

## System Architecture

### High-Level Architecture

HPIS uses a distributed architecture combining IoT, streaming, databases, machine learning, AI agents, APIs, and a web dashboard. The ESP32 wearable device collects sensor data and transmits it via WiFi or WebSocket to the FastAPI backend API. From the backend, data flows into Kafka for streaming and ingestion. The streaming layer distributes data to Cassandra for persistent historical storage, Redis for real-time access and low-latency data availability, and the processing layer for analysis. The AI and ML models process historical and real-time data, while RabbitMQ enables asynchronous messaging for AI-agent orchestration. The various agents including stress agents, sleep agents, and other specialized agents analyze the data and generate personalized insights that are displayed through the frontend dashboard.

The current repository reflects this distributed structure through dedicated backend, frontend, modeles_IA, rabbitmq, and wearable_esp32 directories.

### Infrastructure Components

The project uses Docker Compose to orchestrate the main infrastructure components including Redis for low-latency access to recent information and real-time application data, Zookeeper for Kafka coordination, Kafka as the streaming and ingestion layer, RabbitMQ for asynchronous messaging and AI-agent orchestration, and Cassandra as the distributed time-series storage layer for physiological data. The Compose configuration defines persistent volumes and a dedicated HPIS network to ensure reliable data storage and service communication.

### Data Flow Pipeline

The intended real-time pipeline begins with the ESP32 collecting sensor data and sending it to the FastAPI backend. The data is then published to Kafka for streaming and ingestion. From Kafka, the data flows through multiple paths: to Redis for real-time access and low-latency availability to the user interface, to Cassandra for persistent historical storage, and to stream processing components for analysis. The historical data stored in Cassandra feeds into AI and ML models for training and inference. The AI models generate predictions that are passed through RabbitMQ to AI agents for further analysis. The agents produce recommendations and insights that are delivered through the frontend dashboard to the user.

### Kafka Streaming Layer

Kafka acts as the streaming and ingestion layer for the entire platform. The current Docker configuration uses Confluent Kafka 7.4.0 and exposes Kafka on ports 9092 and 9093, enabling reliable event streaming and data ingestion at scale.

### Redis Caching Layer

Redis is used for low-latency access to recent information and real-time application data. The current deployment uses Redis 7 Alpine with persistent storage, ensuring that recent data is available quickly for dashboard updates and real-time analysis.

### Cassandra Storage Layer

Cassandra is used as the distributed time-series storage layer for physiological data. The current deployment uses Cassandra 4.1.3 with persistent storage, providing scalable and reliable storage for historical physiological data that can be analyzed over time.

### RabbitMQ Messaging Layer

RabbitMQ provides asynchronous messaging for AI-agent orchestration. The current Docker configuration uses RabbitMQ 3.12 with its management interface, enabling reliable communication between system components and specialized agents.

## Technology Stack

### IoT and Embedded Systems
The ESP32 serves as the wearable device platform, programmed using PlatformIO with C and C++. WiFi and WebSocket enable communication between the wearable and backend. The MAX30105 sensor provides physiological data acquisition capabilities. The repository contains a dedicated wearable_esp32 project with PlatformIO configuration, source code, libraries, tests, and an application file.

### Backend Technologies
Python powers the backend implementation with FastAPI providing REST APIs and WebSocket communication for real-time data exchange. The backend is organized into API and agent components, with the current API directory containing a dedicated stress endpoint and module.

### Streaming and Messaging
Apache Kafka handles event streaming with Zookeeper for coordination, enabling scalable data ingestion and processing. RabbitMQ provides AMQP messaging for asynchronous agent communication, allowing the system to handle AI analysis without blocking the real-time ingestion pipeline.

### Databases
Apache Cassandra provides distributed time-series storage for physiological data, while Redis enables low-latency access to recent information and real-time application data.

### Machine Learning
XGBoost serves as the primary machine learning framework for stress classification, with Scikit-learn providing additional modeling capabilities. Joblib handles model serialization and storage. Feature engineering and classification pipelines prepare physiological data for analysis.

### Frontend Technologies
Angular provides the frontend framework with TypeScript for type-safe development, HTML and CSS for interface design, and Angular CLI for project management and build processes. The current frontend is an Angular project generated with Angular CLI 21.1.2.

### Infrastructure and DevOps
Docker and Docker Compose enable containerization of all services with persistent volumes for data durability and a dedicated Docker network for service communication.

## Machine Learning Models

### Stress Detection Model

The main implemented machine-learning model is an XGBoost stress-classification model. The trained model is currently stored in the repository as modele_stress_xgb.joblib, confirming that the repository contains a serialized XGBoost stress model rather than only a conceptual model. The conceptual pipeline processes physiological signals through preprocessing, feature extraction, and the XGBoost classifier to generate stress predictions, which are then passed to agents for further analysis and recommendation generation.

### AI Agents Architecture

HPIS introduces an agent-based intelligence layer where specialized agents handle different aspects of human performance. The backend currently contains an agents directory with a dedicated sleep agent implementation, supporting the architecture of using specialized agents rather than relying on a single monolithic model. The intended architecture evolves toward an AI orchestrator that coordinates stress agents, sleep agents, recovery agents, and other specialized agents to produce comprehensive human performance intelligence and personalized recommendations.

## Data Sources and Processing

### WESAD Dataset

The main dataset used for the stress-detection component is WESAD, which provides multimodal physiological data for stress-related machine-learning experiments. This dataset can be used to train the initial stress model before replacing or augmenting it with data collected from the ESP32 wearable.

### ESP32 Real-Time Data

The ESP32 wearable provides the project's real-time data source. The architecture was designed around physiological signals including ECG, heart-rate-related measurements, SpO₂, and activity-related measurements. The project also targets additional human-performance variables such as HRV, sleep, activity, and calories, creating a transition from public dataset offline training to ESP32 real-time data online prediction.

### Data Processing Pipeline

Raw sensor data undergoes validation to ensure quality, cleaning to remove noise and artifacts, signal processing to extract meaningful features, and feature extraction to create feature vectors for ML prediction. The repository contains a data/processed directory and a dedicated AI-model structure containing data-cleaning, model, and training components.

## Implementation Responsibilities

As the AI Engineer and IoT and Distributed Systems Developer for this project, responsibilities spanned multiple domains. In IoT, responsibilities included designing the ESP32-based wearable prototype, integrating physiological sensors, implementing sensor-data acquisition, and implementing communication between the wearable and backend. In backend development, responsibilities included developing FastAPI backend services, designing APIs for physiological data and AI predictions, and integrating the backend with the streaming infrastructure. In data engineering, responsibilities included designing the Kafka-based ingestion pipeline, designing the Cassandra time-series storage layer, using Redis for low-latency data access, and using RabbitMQ for asynchronous AI-agent communication.

In machine learning, responsibilities included preparing physiological data for machine learning, developing the stress-detection pipeline, training an XGBoost model, serializing and integrating the trained model into the backend, and designing the inference pipeline. In AI agents, responsibilities included designing specialized agents for human-performance analysis, implementing a sleep-oriented agent, and designing the architecture for additional agents such as stress and recovery analysis. In frontend development, responsibilities included developing the Angular-based monitoring interface, integrating backend data into the dashboard, and designing the platform for real-time visualization. In DevOps, responsibilities included containerizing the infrastructure using Docker, creating Docker Compose infrastructure, configuring Kafka, Zookeeper, Redis, RabbitMQ, and Cassandra, and configuring persistent volumes and a dedicated Docker network.

## Project Results

The project resulted in an end-to-end prototype architecture connecting IoT through streaming, storage, machine learning, AI agents, and web application. Main achievements include building an ESP32-based wearable data acquisition layer, creating a FastAPI backend, implementing real-time data ingestion architecture, integrating Kafka for event streaming, integrating Redis for real-time data access, integrating Cassandra for persistent time-series storage, integrating RabbitMQ for asynchronous AI-agent communication, training and storing an XGBoost stress model, creating an AI-agent layer with a dedicated sleep agent, developing an Angular frontend, containerizing the infrastructure using Docker Compose, creating persistent infrastructure volumes, and designing the platform as an extensible multi-sensor architecture. The current repository structure directly reflects these components through backend, frontend, modeles_IA, rabbitmq, wearable_esp32, processed data, and Docker infrastructure directories.

## Key Challenges

### Real-Time Physiological Data Processing

Physiological signals are inherently noisy and sensitive to movement, sensor placement, and environmental conditions. The system requires robust filtering, cleaning, and feature extraction to produce reliable predictions from raw signals. This challenge required careful signal processing design to handle the variability in real-world sensor data.

### Multi-Technology Integration

The project combines several distributed technologies including ESP32, FastAPI, Kafka, Redis, Cassandra, RabbitMQ, AI agents, and Angular. Making these components communicate reliably was a major engineering challenge that required careful configuration of each component and robust error handling across the entire pipeline.

### Streaming versus Storage Requirements

Real-time applications and historical analysis have different requirements. Redis provides low-latency access for real-time data, while Cassandra provides persistent storage for historical analysis. This required separating real-time data for Redis from historical data for Cassandra, with appropriate data routing and synchronization between the two systems.

### Asynchronous AI Processing

AI analysis does not necessarily need to block the real-time ingestion pipeline. RabbitMQ was introduced as an asynchronous communication layer between the data-processing system and AI agents, allowing the system to continue ingesting data while AI analysis proceeds in the background. This decoupling improves system responsiveness and scalability.

### Machine Learning Integration

A trained ML model must be integrated into a real application rather than simply evaluated in a notebook. The complete inference pipeline requires API request handling, input validation, feature extraction, model inference, and API response generation. The repository currently exposes a stress API module and stores the trained XGBoost model as a Joblib artifact.

### Multi-User Scalability

The original architecture was designed with the idea that many users could send physiological data simultaneously. This motivated the use of Kafka for scalable event streaming, Cassandra for distributed storage, Redis for fast access, and RabbitMQ for asynchronous workloads. Scaling to multiple users required careful design of each component to handle concurrent data ingestion and processing.

## Lessons Learned

### AI Systems Require More Than a Model

One of the biggest lessons from HPIS was that a machine-learning model is only one component of an intelligent product. An AI product encompasses sensors, data engineering, machine learning, backend systems, agents, frontend interfaces, and infrastructure. This systems perspective is essential for building deployable AI applications that provide real value to users.

### Event-Driven Architecture for IoT

Wearable devices continuously generate data, making an event-driven architecture more appropriate than sending every operation through synchronous request-response communication. Event-driven design enables efficient handling of continuous data streams and better scalability for IoT applications.

### Database Specialization Matters

Redis and Cassandra are not interchangeable. Redis provides fast, real-time access for recent data, while Cassandra provides persistent, distributed time-series data storage. Using the right database for each use case is essential for system performance and reliability.

### AI Agents Layer Above ML Models

The XGBoost model can answer whether a physiological pattern is associated with stress. An agent can operate at a higher level, considering the user's stress levels along with recent sleep and recovery context before recommending training intensity. This creates a layered intelligence architecture where sensors feed ML models, which feed AI agents, which generate human-level recommendations.

### IoT and AI Create Continuous Feedback Loops

The ultimate architecture is a continuous cycle of measuring, understanding, predicting, recommending, user action, and measuring again. This makes HPIS fundamentally different from a simple dashboard and enables continuous improvement in user health and performance.

### Open Architecture Importance

The platform was designed so that additional sensors, models, agents, and data sources can be added without redesigning the entire system. ECG, HRV, and sleep data can all flow through the same architecture, with specialized agents for stress, recovery, and performance analysis generating recommendations. This modularity is one of the core architectural principles of HPIS.

## GitHub Repository

The project repository is available at [https://github.com/Mohamedaminesaadd/HIPS](https://github.com/Mohamedaminesaadd/HIPS?utm_source=chatgpt.com). The current repository contains the complete project structure including the backend with FastAPI APIs and agent implementations, the Angular frontend for dashboard visualization, AI models and training components with the serialized XGBoost stress model, RabbitMQ configuration for asynchronous messaging, the ESP32 wearable project with PlatformIO configuration, processed data directories, and Docker Compose infrastructure for containerized deployment. This comprehensive implementation serves as a reference for building intelligent wearable platforms that combine IoT, streaming, machine learning, and AI agents.