#!/bin/bash

echo "Starting Whiteout Survival Battle Calculator Development Environment..."
echo

# Function to start service in new terminal
start_service() {
    local service_name=$1
    local command=$2
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && $command\""
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - try different terminal emulators
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd) && $command; exec bash"
        elif command -v konsole &> /dev/null; then
            konsole -e bash -c "cd $(pwd) && $command; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e bash -c "cd $(pwd) && $command; exec bash"
        else
            echo "No supported terminal found. Please run manually: $command"
        fi
    else
        echo "Unsupported OS. Please run manually: $command"
    fi
}

echo "Starting Backend Server (FastAPI)..."
start_service "Backend" "cd server && python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo "Starting Frontend (React Native/Expo)..."
start_service "Frontend" "cd BattleSimApp && npm start"

echo "Starting Prisma Studio..."
start_service "Prisma" "prisma studio --port 5555"

echo
echo "All services are starting up!"
echo "- Backend: http://localhost:8000"
echo "- Frontend: Expo development server"
echo "- Prisma Studio: http://localhost:5555"
echo
echo "Press Enter to close this window..."
read
