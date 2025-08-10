# Whiteout Survival Battle Calculator

A comprehensive battle simulation and analysis toolkit for the strategy game **Whiteout Survival**. This project provides detailed battle mechanics simulation, hero data management, troop calculations, and strategic planning tools through a modern web/mobile interface.

## 🎯 Project Overview

This battle calculator simulates and analyzes **Expedition Battles** and **Rally Formations** in Whiteout Survival, including:

- **Turn-based battle simulation** with realistic troop mechanics
- **Hero skill calculations** including Expedition Skills, Exclusive Weapons, and Widgets
- **Troop composition optimization** for Infantry, Lancers, and Marksmen
- **Rally formation analysis** with support hero integration
- **Chief Gear and Charm calculations** with set bonuses
- **Research tree integration** for battle technology bonuses
- **Monte Carlo simulations** for battle outcome probability analysis

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Battle Engine**: Sophisticated turn-based combat simulation
- **Hero Data System**: Comprehensive database of all hero generations and skills
- **Troop Mechanics**: Detailed troop type definitions and combat rules
- **Bonus Calculations**: Complex stacking and interaction rules for all buffs
- **Database**: SQLite with Prisma schema ready for PostgreSQL migration

### Frontend (React Native/Expo)
- **Cross-platform**: Web, iOS, and Android support
- **Real-time Simulation**: Live battle calculations and results
- **Configuration Management**: Save/load battle setups and preferences
- **Responsive UI**: Modern interface for complex battle planning

## 🚀 Quick Start

### One-Command Setup (Recommended)

From the root directory, you can start all services with a single command:

```bash
# Install all dependencies first time
npm run setup

# Start all services (backend, frontend, and Prisma)
npm run dev
```

This will start:
- **Backend Server**: FastAPI on http://localhost:8000
- **Frontend**: React Native/Expo development server
- **Prisma Studio**: Database management on http://localhost:5555

### Alternative: Platform-Specific Scripts

#### Windows
```cmd
start-dev.bat
```

#### macOS/Linux
```bash
./start-dev.sh
```

### Manual Setup (if needed)

#### Backend Setup

```bash
# Create virtual environment
python3 -m venv env
source env/bin/activate        # macOS/Linux
.\env\Scripts\Activate.ps1   # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Start the server
cd server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Install Expo CLI globally
npm install -g expo-cli

# Navigate to frontend
cd BattleSimApp

# Install dependencies
npm install

# Start the development server
npx expo start
```

Press `w` for web version, or use Expo Go app on mobile devices.

## 🎮 Core Features

### Battle Simulation
- **Solo vs Rally**: Choose between individual marches or alliance rallies
- **Hero Selection**: Configure up to 3 main heroes per side with class-specific positioning
- **Support Heroes**: Add up to 4 support heroes for additional passive skills
- **Troop Ratios**: Fine-tune Infantry/Lancer/Marksman compositions
- **Capacity Management**: Set march sizes for both attacker and defender

### Advanced Calculations
- **Exclusive Weapons**: Level 1-10 weapon bonuses per troop class
- **Chief Gear**: Mythic/Legendary gear with set bonuses and star upgrades
- **Charms System**: Lethality and Health bonuses with level-based scaling
- **Research Integration**: Battle technology tree bonuses by category and tier
- **Skill Stacking**: Complex interaction rules for hero abilities and buffs

### Analysis Tools
- **Battle Reports**: Detailed turn-by-turn combat logs
- **Statistics**: Win rates, casualties, damage dealt/received
- **Monte Carlo**: Multiple simulation runs for probability analysis
- **Performance Metrics**: Power efficiency and troop utilization analysis

## 🧙‍♂️ Hero System

The calculator includes comprehensive data for all hero generations:

- **Epic Heroes**: Bahiti, Gina, Jassar, Jessie, Patrick, Seo Yoon, Sergey, Walis Bokan
- **Rare Heroes**: Charlie, Cloris, Eugene, Smith
- **SSR Generations**: Gen 1-8 heroes with unique skill sets
- **Expedition Skills**: Right-side hero abilities that enhance troops
- **Exclusive Weapons**: Hero-specific gear with class bonuses

## ⚔️ Troop Mechanics

### Three Troop Classes
- **Infantry**: Frontline tanks with high Defense/Health, +10% Attack vs Lancers
- **Lancers**: Balanced support with 20% chance to bypass Infantry and target Marksmen
- **Marksmen**: Backline damage dealers with +10% Attack vs Infantry, 10% double-strike chance

### Combat System
- **Turn-based**: Sequential damage calculation with targeting priorities
- **Positioning**: Front-to-back damage flow with bypass mechanics
- **Stat Interactions**: Attack vs Defense, Lethality bypass, Health management
- **Class Bonuses**: Rock-paper-scissors style advantages between troop types

## 🔧 API Endpoints

### Core Simulation
- `POST /api/simulate` - Run battle simulation
- `POST /api/simulate/weighted` - Power-weighted simulation
- `GET /api/heroes` - Available hero data
- `GET /api/troops` - Troop type definitions

### Equipment & Research
- `POST /api/gear/chief/calc` - Chief gear calculations
- `POST /api/gear/chief/charms/calc` - Charm system calculations
- `GET /api/research/categories` - Research tree categories
- `GET /api/research/find` - Specific research node values

### User Management
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/settings` - Save user preferences
- `GET /api/settings/saved` - List saved configurations

## 📊 Database Schema

### Prisma Integration
The project includes a Prisma schema ready for PostgreSQL deployment:

```bash
# Generate Prisma client
npm run prisma:generate

# Run migrations
npm run prisma:migrate

# Open Prisma Studio
npm run prisma:studio
```

### Current SQLite Setup
The Python backend uses SQLite by default with SQLAlchemy ORM, easily migratable to PostgreSQL.

## 🧪 Testing

Comprehensive test suite covering:
- Battle mechanics and calculations
- Hero skill interactions
- Troop targeting and damage
- Bonus stacking rules
- Support hero integration

```bash
# Run tests
cd tests
python -m pytest
```

## 📁 Project Structure

```
battle_calculator/
├── BattleSimApp/           # React Native/Expo frontend
│   ├── components/         # UI components
│   ├── types.ts           # TypeScript definitions
│   └── App.tsx            # Main application
├── server/                 # Python FastAPI backend
│   ├── expedition_battle_mechanics/  # Core battle engine
│   ├── hero_data/         # Hero definitions and skills
│   ├── troop_data/        # Troop type definitions
│   ├── chief_gear/        # Equipment calculations
│   ├── research/          # Technology tree integration
│   └── main.py            # API server
├── docs/                  # Game mechanics documentation
├── tests/                 # Test suite
├── prisma/                # Database schema and migrations
├── start-dev.bat          # Windows development startup script
├── start-dev.sh           # macOS/Linux development startup script
└── package.json           # Root package with development scripts
```

## 🛠️ Development Scripts

### Root Package Scripts
- `npm run dev` - Start all services concurrently
- `npm run dev:backend` - Start only the FastAPI backend
- `npm run dev:frontend` - Start only the React Native frontend
- `npm run dev:prisma` - Start only Prisma Studio
- `npm run setup` - Install all dependencies and setup Prisma
- `npm run install:all` - Install dependencies for all services

## 🎯 Use Cases

### For Players
- **Battle Planning**: Test different hero combinations before committing resources
- **Rally Optimization**: Maximize alliance rally effectiveness
- **Gear Planning**: Calculate optimal Chief Gear and Charm investments
- **Research Prioritization**: Focus on most impactful battle technologies

### For Alliance Leaders
- **Rally Coordination**: Plan optimal participant compositions
- **Resource Allocation**: Guide members on gear and research priorities
- **Strategy Development**: Test different formation approaches

### For Content Creators
- **Theory Crafting**: Analyze game mechanics and meta strategies
- **Guide Creation**: Provide data-driven recommendations
- **Community Tools**: Share battle setups and results

## 🔮 Future Enhancements

- **Real-time Battle Streaming**: Live simulation updates
- **Alliance Integration**: Multi-user battle planning
- **Historical Analysis**: Battle result tracking and trends
- **Mobile App**: Native iOS/Android applications
- **API Documentation**: Interactive API explorer
- **Performance Optimization**: Caching and simulation improvements

## 🤝 Contributing

This project welcomes contributions! Areas of interest:
- Additional hero data and skills
- Battle mechanic improvements
- UI/UX enhancements
- Performance optimizations
- Documentation improvements

## 📄 License

This project is developed for educational and community use. Please respect the original game's intellectual property.

## 🆘 Support

For questions, bug reports, or feature requests:
- Check the documentation in the `docs/` folder
- Review existing issues and discussions
- Create detailed bug reports with reproduction steps

---

**Note**: This calculator is based on community research and analysis of Whiteout Survival's battle mechanics. Results are approximations and may not perfectly match in-game outcomes due to undisclosed game formulas and potential updates.