# AI Voice Agent for Restaurant 🎙️🍽️

An intelligent voice-powered restaurant receptionist built with real-time speech recognition, natural language processing, and text-to-speech capabilities. This AI agent can handle customer inquiries, provide menu information, and manage table reservations through voice interactions.

## ✨ Features

- **Real-time Voice Interaction**: Continuous speech recognition using Deepgram
- **Natural Language Understanding**: Powered by Google Gemini 2.5 Flash
- **Voice Responses**: High-quality speech synthesis with ElevenLabs
- **Restaurant Functions**:
  - Menu inquiry and pricing
  - Restaurant hours and location
  - Table reservation booking
- **FastAPI Web Server**: RESTful API endpoints for integration
- **Database Integration**: PostgreSQL for storing reservations
- **WebSocket Support**: Real-time communication capabilities

## 🛠️ Tech Stack

- **Speech-to-Text**: Deepgram SDK
- **Text-to-Speech**: ElevenLabs API
- **LLM**: Google Gemini 2.5 Flash
- **Web Framework**: FastAPI
- **Database**: PostgreSQL
- **Audio Processing**: sounddevice, soundfile
- **Additional**: python-dotenv, websockets

## 📁 Project Structure
voice agent/
├── agent/
│ ├── llm_agent.py # Gemini LLM integration with tool calling
│ └── tools.py # Restaurant functions (menu, booking, etc.)
├── config/
│ └── settings.py # Environment configuration
├── database/
│ └── db.py # PostgreSQL database operations
├── speech/
│ ├── stt.py # Speech-to-text module
│ ├── tts.py # Text-to-speech module
│ └── memory.py # Conversation memory management
├── main.py # FastAPI application
├── realtime_voice_agent.py # Real-time voice interaction
├── websocket_server.py # WebSocket server
├── requirements.txt # Python dependencies
└── .env # Environment variables (not in repo)

Install dependencies

Configure environment variables

Create a .env file in the project root:

Set up the database

Ensure PostgreSQL is running and the database is created with the necessary tables for reservations.

💻 Usage
Running the FastAPI Server
The server will start at http://localhost:8000

Running the Real-time Voice Agent
Speak into your microphone to interact with the AI restaurant receptionist.

Testing Individual Components
Test Speech-to-Text: python test_stt.py
Test Text-to-Speech: python test_tts.py
Test LLM: python test_llm.py
Test Streaming STT: python test_streaming_stt.py
📡 API Endpoints
Health Check
Chat Endpoint
🎯 Supported Restaurant Functions
The AI agent can handle:

Menu Inquiry: "What's on the menu?" / "Show me the menu"
Pricing: "How much is pasta alfredo?"
Hours: "What are your hours?" / "When are you open?"
Location: "Where are you located?"
Reservations: "Book a table for 4 people at 7 PM under the name John"
🔧 Configuration
Menu Items
Edit the menu dictionary in tools.py to customize menu items and prices.

Voice Settings
Modify voice parameters in tts.py for different voice characteristics.

System Prompt
Customize the AI behavior by editing SYSTEM_PROMPT in llm_agent.py.

🧪 Testing
Run individual test files to verify components:

📝 API Keys Required
Google Gemini API: Get from Google AI Studio
Deepgram API: Get from Deepgram Console
ElevenLabs API: Get from ElevenLabs
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
This project is open source and available under the MIT License.

👤 Author
Priyansh Agarwal

GitHub: @priyanshiiitr
🙏 Acknowledgments
Deepgram for speech recognition
ElevenLabs for voice synthesis
Google Gemini for language understanding
FastAPI for the web framework
Note: Make sure to keep your API keys secure and never commit them to version control.

Claude Sonnet 4.5 • 0.9x
