# Hooda Project - Halal Cart Chatbot

A web-based chatbot that integrates halal cart references into responses for user questions, with location-aware recommendations and interactive maps.

## Why You Need This Beyond the Fulfillment of Your Unrestrained Appetite

### Fitness Companion
A chatbot that subtly reminds users of nearby parks, gyms, or running trails while discussing any topic. The bot naturally weaves in suggestions like "If you're feeling stressed about that work deadline, Green Park just 5 minutes from you has a great walking trail that might help clear your mind," encouraging physical activity as part of daily life without being pushy.

### Language Learning Support
A chatbot that recommends nearby cultural events, language exchanges, or authentic restaurants related to the language being learned. While helping with vocabulary or grammar questions, it might mention "There's actually a Spanish film festival this weekend at Cinema Arts just 10 minutes from you" or "If you want to practice ordering in French, Petit Café on Oak Street has native French-speaking staff," creating real-world immersion opportunities.

### Networking Assistant
A chatbot for professionals that recommends relevant local meetups, conferences, or coworking spaces based on career interests discussed. During conversations about industry challenges or career goals, it might suggest "There's a tech networking event at Innovation Hub tomorrow evening, just 3 blocks from your location" or "Many remote workers in your field meet at The Common Space cafe on Thursdays, which is near you," helping users build professional connections in their area.

## Features

- Clean, modern web interface inspired by ChatGPT
- Interactive chat experience with session memory
- Responses always include halal cart references and recommendations
- Location-aware recommendations using browser geolocation
- Google Maps integration with clickable links to cart locations
- Persistent chat history within a browser session
- "Clear Chat" button to reset conversation
- Simple Flask-based backend

## Setup and Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your environment variables:
   - Create a `.env` file in the root directory with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   FLASK_SECRET_KEY=a_secure_random_string_for_sessions
   ```

3. Run the web application:
   ```
   python main.py
   ```

4. Access the application in your browser at `http://127.0.0.1:8080`

## API Keys Required

- **OpenAI API Key**: For generating chatbot responses
- **Google Maps API Key**: For Places API and Geocoding API to find nearby halal carts

## Deployment

This application is configured for Vercel deployment with the following files:
- `api/index.py`: Entry point for Vercel
- `vercel.json`: Configuration for routing and server setup

## Usage

1. Allow location access when prompted in your browser
2. Type your questions or comments in the chat input
3. The chatbot will respond with relevant information and halal food recommendations
4. Click on the restaurant names to view their location on Google Maps
5. Use the "Clear Chat" button to start a new conversation

## Project Structure

- `main.py`: Main application logic and API endpoints
- `templates/index.html`: Frontend UI and JavaScript
- `api/index.py`: Vercel deployment entry point
- `.env`: Environment variables (not included in repository)