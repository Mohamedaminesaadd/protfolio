# AI Fitness Coach — Real-Time Exercise Analysis and Form Evaluation Using Computer Vision

## Project Overview

The AI Fitness Coach is a real-time computer-vision fitness coaching system that uses a webcam to detect human body landmarks, analyze exercise movements, count repetitions, evaluate movement quality, provide corrective feedback, and track workout progress. The system transforms webcam video through human pose detection and body landmark extraction into geometric measurements, exercise state determination, movement quality evaluation, and real-time feedback delivery. The repository describes the system as an intelligent fitness coach capable of detecting, analyzing, and evaluating exercise quality in real time using a webcam, with MediaPipe Pose, custom repetition logic, and fuzzy logic.

## Problem Context

Traditional fitness applications often focus on counting repetitions or providing predefined workout plans. However, simply counting repetitions is not enough to determine whether an exercise is being performed correctly. During a push-up, a person may perform an incomplete movement, lose body alignment, move too quickly, become unstable, or perform an incorrect posture. Similarly, during a squat, the quality of the movement depends on knee angle, body alignment, movement stability, depth of the squat, and execution consistency. A human trainer can observe these factors, but continuous personal coaching is not always available. The objective of this project was to build a computer-vision-based virtual fitness coach capable of analyzing exercise movements through a normal webcam.

## Primary Objectives

The main objective was to develop a real-time AI fitness assistant that can act as a virtual coach. The system aims to detect a person's body pose using a webcam, extract human body landmarks, calculate joint angles, calculate body alignment, measure movement stability, detect exercise repetitions, determine whether a repetition is complete, evaluate movement quality, provide a quality score, provide visual feedback, provide voice feedback, support multiple exercises, generate workout plans, track sets and repetitions, implement rest periods, store workout history, and display workout statistics. The current repository includes dedicated analysis scripts for exercises such as push-ups, squats, and leg raises, as well as a main application that manages workout plans and real-time exercise analysis.

## System Architecture

### High-Level Architecture

The system architecture follows a pipeline from webcam input through pose detection to feedback delivery. The webcam provides video frames through OpenCV video capture to the PoseEngine, which uses MediaPipe Pose to detect body landmarks. From these landmarks, the system extracts angles, alignment metrics, and stability measurements. The ExerciseManager processes these features to detect repetitions and manage exercise state. The FuzzyCoach evaluates movement quality and generates a quality score. This score drives visual feedback through the display, voice feedback through text-to-speech, and workout statistics tracking. The implementation separates pose detection, exercise management, fuzzy evaluation, exercise-specific analysis, and the main user interface into distinct modules.

### Computer Vision Layer

The first layer captures the user through a webcam using OpenCV video capture. Each video frame is converted to RGB format and processed through MediaPipe Pose to extract pose landmarks. The PoseEngine class uses OpenCV and MediaPipe Pose with configurable detection confidence, tracking confidence, and model complexity. The repository uses complexity=1 for the main real-time processing.

### PoseEngine

The PoseEngine is the central computer-vision abstraction providing pose detection through the find_pose method, which processes the webcam frame through MediaPipe Pose and optionally draws the detected skeleton. The get_positions method extracts landmarks with pixel coordinates, normalized coordinates, and visibility confidence. Each landmark stores its pixel coordinates as x and y positions, normalized coordinates, and visibility confidence, making the landmarks convenient for downstream geometric analysis.

### Geometric Pose Analysis

The system does not simply use the raw landmarks but converts them into meaningful geometric features. The calculate_angle method calculates the angle formed by three body landmarks, such as shoulder, elbow, and wrist for push-up analysis, or hip, knee, and ankle for squat analysis. The angle is obtained from the relative vectors using atan2 and converted into degrees. The PoseEngine also implements a distance-ratio calculation that normalizes measurements relative to a reference body distance, making geometric measurements less dependent on the user's distance from the camera.

### ExerciseManager

The ExerciseManager is responsible for turning continuous movement into repetitions through a finite-state machine approach. The manager stores the current state, repetition count, bottom-position timestamp, angle history, alignment history, stability history, last quality score, and feedback message. The state machine transitions from standing state through bottom state to repetition completion based on angle thresholds and minimum bottom-position duration.

### Repetition Detection

A repetition is not counted simply because an angle crosses a threshold. The manager verifies the movement sequence from start through moving down, reaching bottom, holding minimum time, moving up, and reaching the upper threshold. For a repetition to be considered valid, the system checks the configured down and up thresholds and a minimum bottom-position duration. The manager then increments the repetition counter, preventing simple frame-by-frame angle fluctuations from being interpreted as multiple repetitions.

### Movement Quality Evaluation

Once a repetition is completed, the system aggregates information from the entire repetition including angle measurements, alignment measurements, and stability measurements. It calculates the best angle, average alignment, and average stability. These values are passed to the fuzzy-logic coach for evaluation. The architecture processes video frames into frame-level measurements, aggregates these into repetition data, evaluates through fuzzy logic, and generates a quality score.

### Fuzzy Logic Coach

One of the strongest technical aspects of this project is that the movement-quality evaluation is not implemented as a simple hard-coded score but uses fuzzy logic with scikit-fuzzy. The FuzzyCoach defines three input variables including amplitude ranging from 0 to 100, alignment ranging from 0 to 200, and stability ranging from 0 to 20, and one output variable for quality ranging from 0 to 100. The repository defines fuzzy membership functions for amplitude with incomplete and correct categories, alignment with good, medium, and bad categories, stability with stable and unstable categories, and quality with low, medium, and good categories. These membership functions and rules are implemented in coach_logic.py.

### Fuzzy Rules

The project uses rules such as when amplitude is correct, alignment is good, and stability is stable, then quality is good. Another rule evaluates when amplitude is correct and alignment is medium or stability is unstable, then quality is medium. An important safety-oriented rule is when alignment is bad, then quality is low. The repository explicitly prioritizes alignment as a safety factor, particularly for the back and shoulders, demonstrating that the project is not simply counting repetitions but attempting to reason about movement quality and safety.

### Push-Up Analysis

The push-up analyzer combines several measurements. The elbow angle uses shoulder, elbow, and wrist landmarks to calculate the elbow angle. Body horizontal alignment calculates a body alignment angle and determines whether the body is sufficiently horizontal using a horizontal tolerance of approximately 10 degrees. Stability measures the change in shoulder vertical position between consecutive frames. The three measurements are passed into the exercise manager as elbow angle, alignment error, and stability, which then feeds into the fuzzy coach. The push-up analyzer also provides voice feedback through pyttsx3.

### Squat Analysis

The squat analyzer uses knee angle calculated from hip, knee, and ankle landmarks. Torso alignment calculates shoulder, hip, and ankle angle and compares the resulting angle against an ideal posture. Stability tracks vertical movement of the pelvis by comparing hip Y position between consecutive frames. The squat analyzer uses a down threshold around 100 degrees and an up threshold around 155 degrees for repetition detection.

### Multiple Exercise Support

The main application is not restricted to one exercise. The repository contains separate modules for push-ups, squats, leg raises, and glute bridges. It also contains an exercise-management layer that allows the application to associate exercises with their own parameters and landmark configurations. Each exercise defines its main angle, alignment points, down threshold, up threshold, and specific logic, making the system extensible.

### Workout Plan

The project goes beyond individual exercise detection. The main application manages a complete workout with multiple exercises, each having sets, repetitions, and rest periods. During the workout, the application tracks current exercise, current set, completed repetitions, completed sets, progress percentage, rest time, and workout duration. The main application updates these values during real-time webcam processing.

### Real-Time User Interface

The main application provides a desktop interface around the computer-vision engine managing exercise selection, workout plan, webcam activation, video display, repetition statistics, quality score, workout progress, rest periods, feedback, and voice output. The webcam processing runs in a dedicated thread so the interface can continue responding while video analysis is running.

### Visual Feedback

During exercise analysis, the system displays information such as the current exercise, repetition count, quality score, set progress, and feedback messages. The quality score controls visual feedback with scores above 70 indicating good performance, scores between 40 and 70 indicating medium performance, and scores below 40 indicating poor performance or warnings. The application changes the displayed feedback based on the quality score.

### Voice Feedback

The project uses pyttsx3 to provide audio feedback, announcing repetition counts, workout completion, rest completion, posture warnings, and exercise feedback. This creates a more natural coaching experience because the user does not need to continuously look at the screen.

### Workout Statistics

The application stores workout information in workout_stats.json including workout date, workout plan or level, exercises performed, total repetitions, total sets, duration, and workout history. The application loads this information when starting and saves it when finishing or closing the application.

## Technology Stack

### Programming Language
Python serves as the primary programming language for all system components.

### Computer Vision
OpenCV provides video capture and image processing capabilities, while MediaPipe Pose enables human pose detection and landmark extraction.

### Numerical Computing
NumPy and Python's math module provide the numerical computing foundation for geometric calculations and feature extraction.

### Fuzzy AI
scikit-fuzzy implements the fuzzy logic system for movement quality evaluation, providing interpretable rule-based reasoning.

### Audio
pyttsx3 provides text-to-speech capabilities for voice feedback and coaching.

### GUI
Tkinter provides the desktop interface with PIL and ImageTk for image handling and display.

### Concurrency
Python threading enables real-time video processing in the background while maintaining a responsive user interface.

### Persistence
JSON provides lightweight data persistence for workout history and statistics.

### Development
Python virtual environment manages dependencies, while Git and GitHub provide version control.

The repository README specifically lists MediaPipe, OpenCV, NumPy, scikit-fuzzy, pyttsx3, math, and time as the main dependencies, recommending Python 3.10 and documenting MediaPipe 0.10.9 as a fallback installation version.

## Models and Intelligent Components

### MediaPipe Pose
The main AI and computer-vision model is MediaPipe Pose, which transforms video frames into human body landmarks. The project does not train a pose-estimation model from scratch but uses MediaPipe Pose as the low-level perception layer and builds its own reasoning system on top. The repository configures MediaPipe Pose with adjustable model complexity and detection and tracking confidence.

### Fuzzy Logic Model
The second intelligent component is the custom FuzzyCoach, which is rule-based rather than neural network-based. Amplitude, alignment, and stability inputs pass through fuzzy membership functions, fuzzy rules, and defuzzification to produce a quality score. This makes the decision process more interpretable than a black-box classifier. The project implements the fuzzy system directly using scikit-fuzzy.

### Exercise State Machine
The third important computational component is the custom repetition engine, which behaves like a finite-state machine transitioning through UP, DOWN, HOLD, and REPETITION states. This component is implemented manually rather than using an external exercise-counting model.

The complete AI architecture combines MediaPipe for perception, custom geometry for feature extraction, a state machine for repetition detection, fuzzy logic for movement quality, and a feedback engine for coaching.

## Data Processing

No traditional training dataset is required by the current implementation. The system is primarily based on pretrained pose estimation, geometric feature extraction, rule-based repetition detection, and fuzzy inference. The input is generated directly from the user's webcam through video frames, MediaPipe landmarks, geometric features, and fuzzy evaluation. The project also stores workout history in workout_stats.json, but this is application data rather than a supervised training dataset.

## Implementation Responsibilities

As the Computer Vision and AI Engineer for this project, responsibilities spanned multiple domains. In computer vision, responsibilities included implementing webcam video acquisition, pose detection integration, landmark extraction, pixel-coordinate processing, normalized-coordinate handling, visibility and confidence handling, joint-angle computation, and distance normalization. The central PoseEngine encapsulates these capabilities.

In exercise recognition, responsibilities included developing custom exercise logic for push-ups, squats, leg raises, and glute bridges, with each exercise using relevant body landmarks and movement-specific geometric measurements. In repetition counting, responsibilities included implementing a state-machine-based repetition counter that detects downward and upward movement, checks thresholds, verifies minimum bottom duration, accumulates movement statistics, and validates completed repetitions.

In movement quality evaluation, responsibilities included implementing a fuzzy-logic quality evaluator based on movement amplitude, body alignment, and stability, producing a continuous quality score rather than only a binary correct or incorrect result. In user feedback, responsibilities included implementing real-time visual feedback, repetition counters, quality scores, posture warnings, voice feedback, and rest countdowns. In workout management, responsibilities included implementing exercise selection, workout plans, sets, repetitions, rest periods, progress tracking, workout history, and persistent statistics.

## Project Results

The project produced a functional real-time AI fitness coach capable of using a standard webcam as the primary sensor. The complete system performs pose detection through webcam input, body landmark extraction, feature extraction, exercise analysis, repetition detection, quality evaluation, and both visual and voice feedback delivery, all integrated with workout statistics tracking. Main achievements include real-time human pose detection, real-time exercise analysis, automatic repetition counting, movement-quality scoring, fuzzy-logic evaluation, posture and alignment checking, stability analysis, multiple exercise support, voice coaching, workout-plan management, set and repetition tracking, rest-period management, and workout-history persistence. These capabilities are implemented across the repository's pose engine, exercise manager, fuzzy coach, exercise-specific analyzers, and main application.

## Key Challenges

### Real-Time Processing
The system must process webcam frames continuously with a pipeline that is fast enough to provide interactive feedback. Any expensive processing can introduce latency, requiring careful optimization of the pose detection, landmark extraction, geometry calculation, exercise logic, and feedback generation pipeline.

### Converting Landmarks into Meaningful Features
MediaPipe provides body landmarks, but landmarks alone do not tell the system whether a squat or push-up is correct. The project had to convert landmarks through angles, alignment, stability, and movement quality calculations. This feature-engineering layer is one of the most important parts of the project.

### Repetition Counting
Simply detecting an angle below a threshold would produce unreliable counters. The state-machine approach solves this by explicitly modeling the movement phases, ensuring that angle fluctuations are interpreted as one movement cycle rather than several repetitions.

### Movement Quality Representation
A movement is not simply correct or incorrect but has degrees of quality. The fuzzy-logic system allows the project to represent poor, medium, and good quality based on several factors simultaneously, providing nuanced feedback.

### Camera Distance Variation
Raw pixel measurements change when the user moves closer to the camera. The project includes normalized distance calculations to reduce this dependency and make measurements more robust.

### Exercise-Specific Logic
Different exercises require different measurements. Push-ups need elbow angle and body alignment, squats need knee angle and torso alignment, leg raises need leg and body geometry, and glute bridges need hip elevation and alignment. A generic exercise detector would not be sufficient, so the system uses an extensible exercise-management architecture.

### Real-Time UI and Threading
The application needs to simultaneously capture video, process pose, update the GUI, provide voice feedback, and track the workout. The main application uses a background thread for video processing so the GUI can remain responsive.

## Lessons Learned

### Computer Vision Is More Than Object Detection
A pose-estimation model only provides the perception layer. The real application requires pose processing, geometry calculation, domain knowledge application, decision logic, and feedback generation. This project helped demonstrate how to build intelligence on top of a pretrained vision model.

### Feature Engineering Can Be Powerful
Instead of training a large neural network for every exercise, meaningful geometric features including joint angle, alignment, stability, and amplitude can provide an interpretable solution. These features can then be processed by explicit rules rather than requiring extensive training data.

### Fuzzy Logic Suits Human Movement Evaluation
Human movement is rarely perfectly binary. Alignment can be 90 percent good, 70 percent acceptable, or 40 percent poor. Fuzzy logic provides a natural way to model this uncertainty and generate nuanced quality scores.

### State Machines Are Extremely Useful
Exercise repetition detection is a good example of where a finite-state machine can be more appropriate than a neural network. The explicit state transitions from up through down, bottom, and up to repetition complete provide clear and reliable detection.

### AI Does Not Always Mean Deep Learning
This project uses MediaPipe combined with geometry, a state machine, and fuzzy logic rather than training a custom neural network. This demonstrates the important engineering lesson that the simplest architecture that solves the problem reliably should be chosen.

### Building from Scratch Philosophy
This project strongly reinforces my personal engineering philosophy of building things from scratch to understand what happens underneath the abstraction. I did not simply use an existing AI fitness coach API but built the decision pipeline around the pose model including custom PoseEngine, custom angle calculations, custom alignment logic, custom stability analysis, custom ExerciseManager, custom FuzzyCoach, and custom feedback system. This approach lets me understand exactly how the system transforms a video frame into a coaching decision.

This philosophy is consistent across my other projects including WebSocket From Scratch implementing TCP and WebSocket protocols, PyTorch Learning covering deep learning fundamentals, LLM From Scratch implementing tokenizer, attention, and Transformer, Agent Lab implementing state, tools, and agent orchestration, and HPIS implementing IoT, streaming, ML, and agents. The common engineering philosophy is to not only learn how to use abstractions but to build the underlying mechanism yourself whenever possible, understand its limitations, and then use higher-level tools with a deeper understanding of what is happening underneath.

## GitHub Repository

The project repository is available at [https://github.com/Mohamedaminesaadd/AI-Fitness-Coach-Setup-Dependencies](https://github.com/Mohamedaminesaadd/AI-Fitness-Coach-Setup-Dependencies). The repository currently contains the main coach application with the complete implementation, pose engine for MediaPipe integration, fuzzy-logic engine for quality evaluation, exercise manager for state management, exercise-specific analyzers for push-ups, squats, leg raises, and glute bridges, workout statistics for data persistence, setup documentation for installation, and interface assets for the user interface. This comprehensive implementation serves as a reference for building real-time computer-vision fitness coaching systems that combine pose detection, geometric analysis, state machines, and fuzzy logic.