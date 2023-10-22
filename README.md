# GPT3.5_pdf_reader
This script is designed to efficiently navigate through a vast collection of over 100 PDFs containing Standard Operating Procedures (SOPs).

Key Features:
PDF Keyword Search: Quickly find any keyword within individual PDFs. The search results provide the specific PDF name and the page number where the keyword appears.
AI-Powered Query Assistant: Ask specific questions related to any chosen PDF, and receive relevant AI-generated answers.
Demonstration:
For a practical demonstration, I've uploaded three of my biology practical PDFs.

Technical Details:
The solution utilizes the text-davinci-003 API model from OpenAI.
I've trained the model on 1,000-word text segments sourced from a pre-existing database. This ensures the AI can generate accurate responses based solely on the provided data.
A user-friendly interface has been made to allow users to ask questions and retrieve AI responses.
To enhance efficiency, I've implemented a feature that saves the trained AI model to a designated location. This eliminates the need to retrain the model every time it's utilized.
