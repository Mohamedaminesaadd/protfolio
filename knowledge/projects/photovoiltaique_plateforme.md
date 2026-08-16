# B-Project — AI-Powered Photovoltaic Project Management Platform

## Project Overview

The B-Project is an AI-powered platform for managing photovoltaic installation projects that combines project management, task management, technician management, authentication, statistics, and machine learning. The platform addresses the complexity of photovoltaic installation projects by providing a centralized digital solution that integrates machine learning for predicting task durations. Instead of relying only on manually entered estimates, the platform uses an XGBoost regression model to estimate how many hours a photovoltaic task may require based on contextual factors including task characteristics, technician experience, weather conditions, and seasonal factors.

## Problem Context

Photovoltaic installation projects involve many interconnected activities including customer management, project planning, installation phases, technician assignment, task scheduling, equipment and documentation management, project progress tracking, deadline management, weather condition consideration, technician experience evaluation, and resource allocation. Managing these activities manually makes it difficult to estimate realistic task durations, assign technicians efficiently, monitor project progress, and coordinate the different phases of a photovoltaic installation. The project addresses this problem by developing a centralized digital platform that combines project management, task management, technician management, authentication, statistics, and machine learning to optimize resource planning and project execution.

## Primary Objectives

The main objective was to build a complete web platform capable of managing the lifecycle of photovoltaic installation projects while integrating machine learning into operational decision-making. The project aims to centralize photovoltaic project information, manage customers and users, implement secure authentication, manage user roles, create and manage photovoltaic projects, divide projects into installation phases, create and manage tasks, assign tasks to technicians, track project progress, monitor project status, manage project documentation, display project statistics, provide notifications, estimate task duration automatically, use technician experience as a prediction feature, take weather and season into account, expose the ML model through an API, integrate ML predictions into the web application, and improve resource planning. The repository README explicitly lists secure authentication, user and role management, project management, photovoltaic installation tracking, task scheduling, document management, dashboards and statistics, project-status monitoring, notifications, and responsive design as platform features.

## System Architecture

### Overall Architecture

The system follows a full-stack with machine-learning microservice-style architecture. The Angular frontend communicates with the Node.js and Express backend through HTTP REST APIs. The backend connects to MongoDB for persistent data storage and to the Machine Learning API for intelligent predictions. The Machine Learning API, built with FastAPI, serves the XGBoost task duration prediction model. This separation between the business application and the ML inference service allows each component to evolve independently while maintaining clean integration boundaries.

### Frontend Architecture

The frontend is implemented with Angular and TypeScript, generated with Angular CLI 21.1.2. The repository contains a complete Angular project with the standard structure including public assets, source code, angular.json configuration, package.json dependencies, TypeScript configuration, and project README. The frontend acts as the main interface providing authentication, dashboard visualization, project management, phase management, task management, technician management, document management, statistics visualization, and notification handling. The interface enables users to interact with all platform features through a responsive web application.

### Backend Architecture

The backend uses Node.js and Express.js organized into several layers following a classic separation-of-concerns architecture. The config directory handles application configuration, controllers contain the business logic for different domains including PhaseController, ml.controller, projectController, tacheController, and user.controllers. The middlewares directory handles authentication and request processing. The models directory contains MongoDB models for phase, project, tache, and user entities. The router directory defines API routes, services directory handles business operations, and utils directory provides helper functions. This structured approach separates business operations by domain with controllers for projects, tasks, phases, users, and machine learning functionality.

### Authentication Architecture

The platform implements authentication using JSON Web Tokens. Users login through the Angular frontend, the Node.js backend validates credentials, generates a JWT upon successful authentication, and returns it to the frontend. Subsequent authenticated requests include the JWT, which is validated by middleware before allowing access to protected resources. This enables secure separation between public and protected operations while maintaining stateless authentication.

### Role-Based Architecture

The application includes user and role management to prevent every user from having access to every operation. The architecture supports different roles including administrators with full system access, managers with project and planning access, and technicians with task and assigned work access. This role-based approach is important for a real photovoltaic management platform because project managers and field technicians have different responsibilities and access requirements.

### Project Management Structure

The core of the application is hierarchical project management. A photovoltaic project contains multiple phases, each phase contains multiple tasks, and each task is assigned to a technician. The platform provides this hierarchical organization with separate models and controllers for projects, phases, and tasks. Projects contain phase information including installation stages, phases contain task details including scheduling, and tasks contain assignment information including technician allocation.

### Task Management

Tasks are central to the intelligent part of the platform. Each task contains information related to estimated duration, complexity, priority, phase, technician, technician experience, weather conditions, and seasonal factors. These features are directly reflected in the ML inference API, enabling the system to move from task creation through task context collection to ML prediction, estimated duration generation, and task planning optimization.

## Machine Learning Architecture

The machine-learning component is one of the most interesting parts of the project. The repository contains a dedicated machineLearning directory with data generation scripts, the FastAPI implementation, the photovoltaic task dataset, the trained XGBoost model, and local inference scripts. This confirms that the project contains not just an ML concept but a complete implementation with dataset, trained model, local inference, and API layer.

### Machine Learning Problem

The ML problem is a regression problem: given the characteristics and context of a photovoltaic installation task, predict its expected duration in hours. The XGBoost regressor takes input features including estimated time, complexity, priority, task type, technician experience, weather conditions, and season, and outputs a predicted task duration in hours. This addresses the operational challenge of estimating how long photovoltaic installation tasks will take.

### Machine Learning Features

The FastAPI implementation constructs the model input using seven features: heure_estimee representing the estimated time, complexite representing task complexity, priorite representing task priority, tache representing the task or phase type, experience_technicien representing technician experience level, meteo representing weather conditions, and saison representing the season. The model returns a predicted value in hours. The API implementation constructs the feature vector in exactly this order before calling the trained model, ensuring consistency between training and inference.

### Dataset

The repository contains dataset_pv_taches.csv with approximately 5,001 lines and around 109 KB in size. The dataset represents photovoltaic installation tasks and their contextual characteristics. The prediction pipeline flows from the photovoltaic task dataset through feature engineering to training data, XGBoost training, and model serialization as model_xgboost_tache1.pkl. The dataset is particularly interesting because it is not a generic ML dataset but is designed around the operational problem of estimating photovoltaic task duration.

### XGBoost Model

The project uses XGBoost for regression, with the trained model stored as model_xgboost_tache1.pkl. The model performs regression where the input X consists of task characteristics and the output Y is the task duration in hours. The model learns the relationship between estimated time, complexity, priority, task or phase type, technician experience, weather, season, and the actual duration of photovoltaic installation tasks.

### Machine Learning API

One of the strongest aspects of the project is that the trained model is not left inside a notebook but is exposed through a FastAPI service. The API endpoint POST /predict_tache1 accepts a JSON object containing the task features. The implementation loads the trained Joblib model, receives the input data, extracts the seven required features, converts them into a NumPy array, calls model.predict, returns the predicted duration, and reports the result in hours. This is directly implemented in machineLearning/api.py.

The complete inference architecture flows from Angular through Node.js and Express to the ML API, FastAPI, XGBoost, and prediction generation, returning the duration in hours to the application. This turns the ML model into an actual application service rather than an isolated experiment.

### Local ML Inference

The repository also contains predict_local.py, which demonstrates local inference using a sample task. The script creates a feature vector containing estimated time, complexity, priority, phase, technician experience, weather, and season, and uses the trained model to produce a predicted duration in hours. The script provides a simple way to test the trained model independently of the web application.

## Technology Stack

### Frontend Technologies
Angular provides the frontend framework with TypeScript for type-safe development, HTML5 for markup, CSS3 for styling, and Bootstrap for responsive design and UI components.

### Backend Technologies
Node.js provides the JavaScript runtime, Express.js handles HTTP routing and middleware, REST APIs enable frontend-backend communication, and JWT Authentication secures protected endpoints.

### Machine Learning Technologies
Python provides the ML development environment with scikit-learn for preprocessing and evaluation, XGBoost for gradient boosting regression, PyTorch listed as an additional ML technology, NumPy for numerical operations, Joblib for model serialization, and FastAPI for serving the ML model as a microservice.

### Database
MongoDB provides NoSQL document storage with flexible schemas for projects, phases, tasks, and users.

### Development Tools
Git and GitHub provide version control, npm manages JavaScript dependencies, Angular CLI enables frontend development and building, and Python virtual environments manage ML dependencies.

The README explicitly lists Angular, TypeScript, HTML5, CSS3, Bootstrap, Node.js, Express.js, JWT, FastAPI, scikit-learn, PyTorch, and MongoDB as the main technologies.

## Model Implementation

### Primary Production Model
The primary production model is the XGBoost Regressor for predicting the expected duration of photovoltaic installation tasks. The input consists of task context including estimated time, complexity, and priority, technician context including experience level, and environmental context including weather and season. The output is the predicted duration in hours.

### Additional ML Technology
The repository README also lists PyTorch among the machine-learning technologies. However, the concrete deployed task-duration artifact visible in the repository is the XGBoost model model_xgboost_tache1.pkl. The project emphasizes XGBoost as the production model for this particular prediction service.

## Implementation Responsibilities

As the Full-Stack and Machine Learning Engineer for this project, responsibilities spanned frontend development, backend development, machine learning, and system integration.

In frontend development, responsibilities included Angular application architecture, TypeScript components, project-management interfaces, dashboard interfaces, task-management interfaces, statistics visualization, responsive UI design, and frontend-backend integration.

In backend development, responsibilities included Node.js backend implementation, Express.js REST APIs, controller development, MongoDB models, routing, authentication, JWT-based authorization, business logic, project management, phase management, task management, and user management. The backend follows a structured architecture separating configuration, controllers, middleware, models, routers, services, and utilities.

In machine learning, responsibilities included dataset generation and preparation, feature selection, model training with XGBoost, regression modeling, model serialization with Joblib, local inference implementation, FastAPI deployment, and backend integration. The development pipeline flowed from dataset through feature engineering, XGBoost training, model serialization, FastAPI service, prediction API, and web application integration.

In system integration, responsibilities included connecting all layers from Angular through Node.js and MongoDB, and from the Angular backend through FastAPI and XGBoost. This transformed the project from a simple CRUD application into an AI-assisted project-management platform.

## Project Results

### Functional Results
The platform provides secure authentication with JWT, user and role management for administrators, managers, and technicians, project management for photovoltaic installations, phase management for project stages, task scheduling with assignment capabilities, technician management, document management, dashboards and statistics visualization, project-status monitoring, notifications, and a responsive interface. These capabilities are documented in the repository README.

### AI Results
The ML component provides task information processing through XGBoost regression to generate predicted duration in hours. The trained model is persisted in model_xgboost_tache1.pkl and served through a FastAPI endpoint, enabling real-time predictions integrated with the web application.

### Engineering Result
The most important result is the integration of several engineering layers including frontend, backend, database, machine learning, and API into a cohesive full-stack AI application. This makes the project a complete AI-assisted platform rather than only a machine-learning experiment.

## Key Challenges

### Integrating Machine Learning into a Web Application
Training a model is relatively independent from building a production application. The challenge was connecting the ML model through FastAPI to the backend and frontend while maintaining consistent input formats and reliable communication between components.

### Feature Consistency
The prediction model expects features in a specific order including estimated time, complexity, priority, task type, technician experience, weather, and season. If the application sends features in the wrong order, the model can produce incorrect predictions. The API explicitly constructs the NumPy feature vector in the expected order to ensure consistency.

### ML Model Deployment
A trained model stored on disk is not automatically usable by a web application. The system needed to move from the .pkl model through the Python runtime and FastAPI to the HTTP endpoint and application, representing an important step from ML experimentation to ML integration.

### Full-Stack Integration
The application combines different programming ecosystems including Angular and TypeScript, Node.js and JavaScript, MongoDB, Python and FastAPI, and XGBoost. Each layer has different conventions, data structures, and runtime requirements that must be carefully coordinated.

### Real-World Prediction Factors
Task duration is not determined by one variable but depends on task characteristics, complexity, priority, technician experience, weather, and season. This makes the prediction problem more representative of an actual operational planning problem than a simple single-variable regression.

### Separating Responsibilities
The backend and ML service have different responsibilities with Node.js handling the business application and FastAPI handling machine learning inference. Keeping these responsibilities separated makes the architecture easier to maintain and allows each component to evolve independently.

## Lessons Learned

### Machine Learning Value Through Integration
A model's value is not only its prediction accuracy but how the prediction improves the application. In this project, predictions flow from task duration estimation through planning and resource allocation to better project management, demonstrating how ML becomes valuable when integrated into real workflows.

### ML APIs as Bridge Between AI and Software Engineering
The FastAPI service demonstrates how a trained model can become a reusable application component. The pattern of model through API to application is highly transferable to production AI systems and enables clean separation between ML and application logic.

### Full-Stack AI Requires Multiple Disciplines
This project required understanding frontend, backend, database, authentication, APIs, machine learning, and model deployment. It demonstrates that AI engineering is not only about training models but about building complete systems that integrate ML with business applications.

### Feature Engineering Importance
The model's inputs represent the operational context of a photovoltaic task. The quality of these features directly influences the usefulness of the prediction, making feature engineering a critical part of the ML implementation.

### Architecture Matters as Much as Implementation
Separating Angular, Node.js, MongoDB, FastAPI, and XGBoost allows each layer to evolve independently. This modular architecture makes the system easier to maintain, test, and extend.

### Building from Scratch Philosophy
This project fits my broader engineering philosophy of building things from scratch to understand how systems work underneath the abstractions. I do not only want to know how to use a technology but want to understand its internal mechanisms and then connect those mechanisms into real systems. The goal is to build a simplified version, understand the internals, use the abstraction intelligently, and integrate it into a larger system. This philosophy appears across my projects including PyTorch Learning for deep learning fundamentals, WebSocket From Scratch for networking and protocols, LLM From Scratch for tokenization and Transformers, Agent LangChain for LLM applications and RAG, Agent Lab for agent orchestration, B-Project for applying ML inside a full-stack business system, and HPIS for applying AI inside an IoT and distributed system.

## GitHub Repository

The project repository is available at [https://github.com/Mohamedaminesaadd/platefome-de-gestion-de-travaill-dans-les-project-photopholtiaque](https://github.com/Mohamedaminesaadd/platefome-de-gestion-de-travaill-dans-les-project-photopholtiaque?utm_source=chatgpt.com). The repository currently contains the Angular frontend with complete project structure and components, the Node.js and Express backend with controllers, models, and middleware, the MongoDB-oriented data models for projects, phases, tasks, and users, the machine-learning dataset with photovoltaic task data, the XGBoost model serialized as model_xgboost_tache1.pkl, the prediction scripts for local inference, the FastAPI inference API for serving predictions, and supporting project assets. This comprehensive implementation serves as a reference for building full-stack AI applications that integrate machine learning with business systems.