# Intelligent Invoice Data Extraction System — OCR + Vision Transformer

## Project Overview

The Intelligent Invoice Data Extraction System is a Python-based document-intelligence application that automatically extracts structured information from invoice images using two complementary approaches: Tesseract OCR for traditional text recognition and rule-based extraction, and Donut for intelligent document understanding using a vision-encoder and decoder Transformer. The system converts an invoice image into structured business information including invoice number, date, total amount, VAT, supplier, customer, payment method, and IBAN or RIB. The application provides a desktop interface with invoice upload, preview, extraction method selection, data display, history tracking, and JSON export capabilities.

## Problem Context

Invoices are semi-structured documents where different companies use completely different layouts, making traditional fixed-position extraction unreliable. Manual invoice processing is time-consuming, repetitive, error-prone, difficult to scale, and dependent on document layout. The project addresses this problem by creating an intelligent document-processing system capable of converting invoice images into structured data. The core problem flows from invoice image through unstructured visual information to OCR or document understanding, and finally to structured information. The repository explicitly identifies invoice number, date, total, VAT, supplier, client, payment method, and IBAN or RIB as target fields.

## Primary Objectives

The main objective was to automate invoice information extraction while maintaining a fallback mechanism between traditional OCR and an AI-based document model. The system aims to load invoice images, display the original document, extract text using Tesseract, extract structured information using Donut, normalize outputs from both extraction methods, detect invoice-related fields, handle OCR errors using fuzzy matching, extract dates, extract invoice numbers, extract total amounts, extract VAT, extract supplier information, extract customer information, extract payment methods, extract IBAN and RIB, keep a processing history, export extracted information as JSON, use GPU when available for Donut inference, and fall back to Tesseract if Donut cannot be loaded or does not produce useful output. The project follows a strategy where images are processed through extraction method selection with options for Tesseract, Donut, or automatic mode, producing structured invoice data that feeds into history tracking and JSON export. The automatic mode prioritizes Donut and falls back to Tesseract if the Donut result is empty or unavailable.

## System Architecture

### High-Level Architecture

The system architecture follows a pipeline from invoice image through extraction to structured output. The Tkinter GUI provides the user interface for uploading invoices and selecting extraction methods. The extraction layer offers three strategies: Tesseract OCR with rule-based extraction, Donut document AI with structured output generation, and automatic mode that prioritizes Donut and falls back to Tesseract. Both extraction methods feed into a unified data schema that supports display, history tracking, and JSON export. The implementation is centralized in main.py through the CombinedOCRApp class.

### User Interface Layer

The application uses Tkinter for the desktop GUI and Pillow for image handling. The interface provides invoice upload, invoice preview, extraction-method selection, extracted-data display, status information, invoice history, detailed history view, and JSON export. The GUI window is configured at approximately 1200 by 900 pixels with a minimum size of 1000 by 800 pixels. The main interface is divided into header controls for loading invoices, exporting JSON, and accessing history, method selection for choosing Donut, Tesseract, or Automatic extraction, a split preview area showing the invoice image and extracted data side by side, and a status bar for displaying processing information. This makes the project a usable application rather than only a command-line OCR script.

### Tesseract OCR Pipeline

The first extraction engine is Tesseract OCR with a pipeline that processes invoice images through Pillow for image handling, Tesseract for text recognition, raw text generation, text cleaning, fuzzy keyword matching, regular expression extraction, and structured field generation. The implementation calls pytesseract.image_to_string with French OCR language support for improved recognition of French invoices.

### Fuzzy Matching System

One interesting part of the implementation is that the system does not depend exclusively on exact keyword matching. OCR can produce errors such as variations of facture appearing as fact ure, factr, factue, or factuer. The application defines multiple possible variations for important keywords and uses fuzzy string matching through the is_similar helper function, which uses fuzzywuzzy.fuzz.partial_ratio with a default threshold of 80. The project defines fuzzy keyword groups for facture, date, total, TVA, fournisseur, client, paiement, and IBAN or RIB, making the traditional OCR pipeline more tolerant of imperfect OCR output.

### Rule-Based Field Extraction

After Tesseract produces text, the system applies specialized extraction rules. For dates, the system recognizes multiple formats including day slash month slash year, day dash month dash year, and day month year with French month names, normalizing French month names into numerical months. For invoice numbers, when an invoice-related keyword is detected, the system searches for a numeric identifier containing at least four digits. For totals, the system searches for numerical amounts associated with keywords such as total, montant, or TTC, supporting formats involving decimal separators and currency indicators. For VAT, the extractor searches for VAT percentages such as 19 percent, 20 percent, or 7.5 percent using regular expressions. For suppliers and customers, the system detects lines associated with fournisseur or client and stores the relevant line as the extracted value. For payment methods, the application recognizes payment methods including virement, chèque, carte, espèces, prélèvement, PayPal, and mandat, checking whether these terms appear in the OCR text. For IBAN and RIB, the system includes regular expressions for detecting IBAN and RIB patterns and extracts the corresponding banking identifier.

### Donut Document AI Pipeline

The second extraction engine is Donut, which is fundamentally different from Tesseract. Instead of processing images through OCR to text to rules, Donut uses a vision encoder and transformer decoder to directly generate structured representations from invoice images. The repository loads naver-clova-ix/donut-base-finetuned-cord-v2 using Hugging Face Transformers' DonutProcessor and VisionEncoderDecoderModel. This model is specifically fine-tuned for document understanding tasks.

### Donut Model Architecture

The Donut pipeline implemented in the project processes invoice images through the DonutProcessor to generate pixel tensors, which feed into the Vision Encoder and Transformer Decoder. The decoder generates a sequence that is decoded into tokens and converted into a JSON-like structure, finally producing the invoice fields. The implementation uses the CORD v2 task prompt and generates the model output using the decoder configuration.

### GPU and CPU Inference

The application automatically checks whether CUDA is available and moves the Donut model to CUDA when available or CPU when not. This makes the application adaptable to different hardware environments, enabling faster inference when a GPU is present while maintaining functionality on CPU-only systems.

### Donut Structured Output

After generation, the model output is decoded and converted into a JSON-like representation using token2json. The application then converts Donut's output into the same internal schema used by the Tesseract pipeline. The unified schema includes date, total, tva, numero_facture, fournisseur, client, mode_paiement, and iban_rib. This is an important architectural decision because it allows both extraction engines to feed the same downstream application.

### Hybrid OCR Strategy

The strongest part of the project is arguably the combination of both methods. Instead of choosing only Tesseract or Donut, the application provides three modes: Donut-only, Tesseract-only, and Automatic. In automatic mode, the system attempts Donut first and falls back to Tesseract if the Donut result is empty or the model is unavailable. The implementation explicitly performs this fallback when Donut is unavailable or returns no useful extracted values, creating a practical fallback architecture from AI model to fallback OCR.

### Unified Data Representation

Regardless of which extraction method is selected, the final output follows one schema. Tesseract and Donut outputs are converted to the same unified schema, which feeds into display, history, and JSON export. This is good software architecture because the GUI does not need to know which extraction engine generated the result, enabling seamless switching between methods.

### Invoice History

The application maintains a processing history where each history item contains the file path, timestamp, extracted data, and method used. The history interface displays date and time, file name, extraction method, invoice number, and total amount. The user can also open a detailed history view showing the extracted fields, enabling review of past extractions.

### JSON Export

Extracted information can be exported as JSON with a structure containing date, total, tva, numero_facture, fournisseur, client, mode_paiement, and iban_rib. The application generates a timestamped filename such as facture_YYYYMMDD_HHMMSS.json and writes the structured data using UTF-8 encoding. This makes the extracted information usable by other systems including accounting software, databases, and analytics applications.

## Technology Stack

### Programming Language
Python serves as the primary programming language for the entire application.

### OCR Technology
Tesseract OCR provides traditional text recognition with pytesseract as the Python interface, enabling rule-based extraction from OCR text.

### Document AI
Hugging Face Transformers provides the Donut model integration with VisionEncoderDecoderModel and DonutProcessor for document understanding.

### Deep Learning
PyTorch provides the deep learning framework with CUDA and GPU acceleration support for efficient Donut inference.

### Image Processing
Pillow handles image loading, display, and preprocessing for both extraction methods.

### Fuzzy Matching
fuzzywuzzy and python-Levenshtein enable fuzzy string matching for tolerant keyword detection in OCR output.

### Data Handling
JSON provides structured data serialization for export, while NumPy supports numerical operations where needed.

### Interface
Tkinter provides the desktop GUI with ttk for themed widgets and PIL and ImageTk for image display and manipulation.

### Utilities
Regular expressions enable pattern-based extraction, threading supports responsive UI during processing, and datetime handles timestamp generation.

The repository's dependency file explicitly lists Pillow, pytesseract, PyTorch, Transformers, Datasets, fuzzywuzzy, python-Levenshtein, NumPy, tqdm, h5py, and safetensors.

## Models

### Primary AI Model — Donut
The primary AI model is Donut, specifically naver-clova-ix/donut-base-finetuned-cord-v2, used as the intelligent document-understanding component. The application loads DonutProcessor and VisionEncoderDecoderModel from the Hugging Face model repository. The model is responsible for extracting structured information from invoice images without relying on a separate OCR text-extraction stage, directly generating structured outputs from visual input.

### Traditional OCR Engine — Tesseract
Tesseract OCR is used as an independent extraction method, a fallback mechanism, and a rule-based structured-data extraction pipeline. This creates a hybrid system where Tesseract processes images to OCR text, which feeds into a rule engine for structured extraction, while Donut directly generates structured data. Both outputs are unified through the same representation.

## Dataset

The current repository is not a model-training repository. It performs inference using the pretrained Donut model and Tesseract rather than training a new invoice model. The input data consists of invoice images provided by the user through the GUI. The pipeline processes invoice images through document processing to Donut or Tesseract, producing structured invoice data. For the Donut component, the model used is already fine-tuned for the CORD document-understanding task. The project itself does not expose a custom invoice-training dataset in the repository.

## Implementation Responsibilities

As the AI, Computer Vision, and Document Intelligence Engineer for this project, responsibilities spanned multiple domains. In OCR engineering, responsibilities included Tesseract integration with French OCR processing, raw-text extraction, OCR error handling, fuzzy keyword matching, and regex-based field extraction. In Document AI, responsibilities included integrating Hugging Face Transformers, DonutProcessor, VisionEncoderDecoderModel, the CORD v2 fine-tuned Donut model, and GPU and CPU inference management.

In information extraction, responsibilities included designing the structured extraction layer for invoice number, date, total, VAT, supplier, customer, payment method, and IBAN and RIB. In hybrid architecture design, responsibilities included implementing three extraction modes for Donut, Tesseract, and Automatic, with automatic fallback from Donut to Tesseract when necessary. In application engineering, responsibilities included implementing the Tkinter GUI with invoice preview, extraction-method selection, status management, processing history, detailed history views, and JSON export functionality.

## Project Results

The project produced a complete desktop document-intelligence application with a functional pipeline from invoice through image loading and extraction selection to Donut, Tesseract, or Automatic processing, generating structured fields that feed into display, history, and JSON export. The application targets invoice number, date, total amount, VAT, supplier, customer, payment method, and IBAN or RIB, which are explicitly represented in the application's unified output schema.

The engineering result demonstrates the complete transformation from unstructured document through AI and OCR to information extraction, structured data, and machine-readable JSON. This is the fundamental architecture behind many real-world Intelligent Document Processing systems.

## Key Challenges

### OCR Noise Handling
Traditional OCR can produce errors such as facture appearing as fact ure, factr, or factue. This is why fuzzy matching was introduced rather than requiring exact keyword matches, enabling the system to tolerate common OCR errors.

### Invoice Layout Variation
The same information can appear in different positions and formats across invoices. Total amounts might appear as "Total: 250 €", "Amount Due ........ 250 €", or "TOTAL TTC 250 EUR". A fixed-position extraction strategy would be fragile, so the project combines Donut's document understanding with keyword and regex extraction to address this problem.

### Traditional OCR versus Document AI Distinction
The project required understanding the difference between Tesseract processing images to text and Donut processing images to structured document representation. This distinction is important in modern document AI and informed the hybrid architecture design.

### Model Loading and Resource Management
Donut is significantly heavier than traditional OCR. The application checks for CUDA availability and uses GPU when available or CPU when not, providing a fallback if the model cannot be loaded. This ensures the application works across different hardware configurations.

### Normalizing Different Outputs
Tesseract and Donut produce fundamentally different outputs. Tesseract produces raw text that requires rule-based extraction, while Donut directly produces structured JSON-like data. The application converts both into the same unified schema including date, total, tva, numero_facture, fournisseur, client, mode_paiement, and iban_rib. This normalization was an important integration challenge.

### Building a Usable Application
The goal was not only a Python script that extracts text but a complete desktop application where users can upload invoices, select extraction methods, view structured data, access history, and export JSON. This required combining AI, data processing, and desktop application development into a cohesive user experience.

## Lessons Learned

### OCR and Document AI Are Different Abstraction Levels
Traditional OCR answers what text is present in the image, while Document AI attempts to answer what information the document contains and how it is structured. This distinction is important for invoice processing and informed the design of the hybrid system.

### Hybrid Systems Can Be More Practical
Instead of assuming one AI model will solve every case, combining Donut, Tesseract, and a fallback mechanism provides a more robust architecture. The system can use a specialized AI model when available and a traditional deterministic pipeline when necessary.

### Fuzzy Matching Is Useful for OCR
OCR output is probabilistic and noisy. A small amount of fuzzy matching can make deterministic extraction significantly more tolerant of recognition errors, enabling the system to handle imperfect OCR output effectively.

### AI Models Should Be Integrated into Software Systems
A pretrained model alone is not an application. The complete system requires the model combined with preprocessing, inference, postprocessing, UI, persistence, and export. This project demonstrates that full pipeline, showing how AI becomes useful when integrated into a complete software system.

### Structured Output Is More Valuable Than Raw OCR
Raw OCR gives scattered text, while the application converts it into structured data with specific fields for invoice number, date, total, and VAT. Structured data can then be consumed by accounting systems, databases, APIs, or analytics applications, making the extraction useful for real business processes.

### Building from Scratch Philosophy
This project fits strongly into my broader engineering philosophy of building things from scratch to understand what happens underneath the abstraction. In this project, I did not simply call an invoice-extraction API but built the complete pipeline around the underlying components including image processing, Tesseract integration, Donut integration, extraction logic, fuzzy matching, regex parsing, unified schema, history tracking, and JSON export. The goal is to understand what abstractions hide so that when using them, I know what is happening underneath and can debug or redesign the system when necessary. This philosophy appears across my other projects including WebSocket From Scratch for TCP and WebSocket protocols, PyTorch Learning for deep learning fundamentals, LLM From Scratch for tokenization and Transformers, AI Fitness Coach for pose and geometry and fuzzy logic, Agent Lab for state and tools and agent orchestration, and HPIS for IoT and streaming and ML and agents.

## GitHub Repository

The project repository is available at [https://github.com/Mohamedaminesaadd/facture_data](https://github.com/Mohamedaminesaadd/facture_data?utm_source=chatgpt.com). The current repository contains main.py with the complete implementation, requirements.txt with all dependencies, a GUI screenshot for documentation, and supporting documentation. The main implementation is approximately 543 lines of Python code and combines Tkinter for the desktop interface, Tesseract for traditional OCR processing, Donut with Transformers and PyTorch for document AI, fuzzy matching for tolerant extraction, invoice-field extraction with regex patterns, history tracking for processing records, and JSON export for structured data output. This comprehensive implementation serves as a reference for building intelligent document processing systems that combine traditional OCR with modern Transformer-based document understanding.