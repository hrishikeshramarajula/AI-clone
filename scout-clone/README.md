# Scout AI Clone

A fully-featured AI assistant application inspired by Scout, built with React, TypeScript, and FastAPI. This clone provides a complete chat interface with real-time WebSocket communication, file management, task tracking, and multiple AI model support.

## 🚀 Features

### Core Functionality
- **AI Chat Interface**: Full-featured chat with streaming responses
- **Multiple AI Models**: Support for Claude, GPT-4, and other models
- **Real-time Communication**: WebSocket-based live updates
- **File Management**: Upload, preview, and manage files
- **Task Tracking**: Create and manage tasks with progress tracking
- **Conversation Management**: Pin, archive, and organize conversations
- **Theme Support**: Light, dark, and system themes
- **Responsive Design**: Works seamlessly on desktop and mobile

### Technical Features
- **Error Boundaries**: Graceful error handling
- **Connection Status**: Real-time connection monitoring
- **State Persistence**: Local storage for conversations and settings
- **Code Highlighting**: Syntax highlighting for code blocks
- **Markdown Support**: Full markdown rendering in messages
- **Keyboard Shortcuts**: Efficient navigation and actions

## 🛠️ Tech Stack

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS v4** - Styling
- **Zustand** - State management
- **Radix UI** - Headless components
- **Framer Motion** - Animations
- **React Hot Toast** - Notifications

### Backend
- **FastAPI** - Python web framework
- **WebSockets** - Real-time communication
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

## 📦 Installation

### Prerequisites
- Node.js 20+ or Bun 1.2+
- Python 3.10+
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/scout-clone.git
cd scout-clone
```

2. **Install dependencies**
```bash
# Frontend (using Bun)
bun install

# Or using npm
npm install

# Backend
cd server
pip install -r requirements.txt
cd ..
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run development servers**
```bash
# Run both frontend and backend
./run.sh

# Or run separately:
# Frontend
bun run dev

# Backend
cd server && python server.py
```

5. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# Access at http://localhost:3000
```

### Manual Docker Build

```bash
# Build image
docker build -t scout-clone .

# Run container
docker run -d -p 3000:80 -p 8000:8000 scout-clone
```

## 🏗️ Project Structure

```
scout-clone/
├── src/                    # Frontend source code
│   ├── components/         # React components
│   │   ├── Chat/          # Chat-related components
│   │   ├── Header/        # Header components
│   │   ├── Sidebar/       # Sidebar components
│   │   └── ui/            # Reusable UI components
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API and WebSocket services
│   ├── store/             # Zustand stores
│   ├── types/             # TypeScript types
│   └── lib/               # Utility functions
├── server/                # Backend source code
│   ├── server.py          # FastAPI application
│   └── requirements.txt   # Python dependencies
├── public/                # Static assets
├── dist/                  # Production build
└── docker/                # Docker configurations
```

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Optional: External API Keys
VITE_OPENAI_API_KEY=your_key
VITE_ANTHROPIC_API_KEY=your_key

# Feature Flags
VITE_ENABLE_VOICE=true
VITE_ENABLE_VISION=true
VITE_ENABLE_PLUGINS=false
```

## 📝 API Documentation

The backend provides a comprehensive REST API and WebSocket endpoints:

### REST Endpoints
- `GET /models` - List available AI models
- `POST /conversations` - Create conversation
- `GET /conversations` - List conversations
- `POST /conversations/{id}/messages` - Send message
- `POST /files/upload` - Upload file
- `POST /bash` - Execute command

### WebSocket Events
- `chat_message` - Send chat message
- `chat_stream` - Receive streaming response
- `tool_call` - Execute tool/function
- `file_upload` - Upload file via WebSocket

Full API documentation available at http://localhost:8000/docs

## 🧪 Testing

```bash
# Run frontend tests
bun test

# Run backend tests
cd server
pytest

# Run end-to-end tests
bun run e2e
```

## 🚀 Production Build

```bash
# Build frontend
bun run build

# Build Docker image
docker build -t scout-clone:latest .

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🎨 Customization

### Adding New AI Models
Edit `server/server.py` and add your model configuration to the `get_models()` function.

### Theming
Modify `src/index.css` to customize the theme colors and design tokens.

### Adding Features
1. Create new components in `src/components/`
2. Add state management in `src/store/`
3. Implement backend endpoints in `server/server.py`

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Scout AI by Scrapybara
- Built with modern web technologies
- UI components from Radix UI and shadcn/ui
- Icons from Lucide

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API docs at `/docs`

## 🔄 Updates

The project is actively maintained with regular updates:
- Bug fixes and performance improvements
- New features and AI model support
- Security updates and dependency upgrades

---

**Note**: This is a clone project for educational purposes. For the official Scout AI, visit [Scrapybara](https://scrapybara.com).