@echo off
echo Starting Whiteout Survival Battle Calculator Development Environment...
echo.

echo Starting Backend Server (FastAPI)...
start "Backend Server" cmd /k "cd server && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Frontend (React Native/Expo)...
start "Frontend" cmd /k "cd BattleSimApp && npm start"

echo Starting Prisma Studio...
start "Prisma Studio" cmd /k "prisma studio --port 5555"

echo.
echo All services are starting up!
echo - Backend: http://localhost:8000
echo - Frontend: Expo development server
echo - Prisma Studio: http://localhost:5555
echo.
echo Press any key to close this window...
pause > nul
