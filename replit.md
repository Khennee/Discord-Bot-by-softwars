# Traydor Discord Bot

## Overview
A Discord bot that manages a point-based game system called "Traydor" with seasonal leaderboards. Users can give each other random points (1-5) with cooldowns, check scores, and view leaderboards. The system automatically resets every 30 days for new seasons.

## Current State
- ✅ Python Discord bot fully configured and running
- ✅ All dependencies installed (discord.py, python-dotenv)
- ✅ Environment variables configured (DISCORD_BOT_TOKEN)
- ✅ Workflow configured for continuous operation
- ✅ SQLite database integration working
- ✅ Project structure optimized for Replit environment

## Project Architecture

### Core Files
- `discord_bot.py` - Main bot entry point, handles Discord connection
- `commands.py` - Discord slash commands implementation (TraydorCommands cog)
- `database.py` - SQLite database operations and schema management
- `helpers.py` - Utility functions for season management and date handling
- `requirements.txt` - Python dependencies

### Database
- Uses SQLite with two main tables:
  - `traydor_points` - Stores user points and usernames
  - `seasons` - Tracks season numbers and start dates
- Automatic 30-day season resets
- Data persists in `traydor.db` file

### Discord Commands
- `/hello` - Test bot connectivity
- `/addtraydor @user` - Give 1-5 random points (10min cooldown)
- `/checktraydor @user` - Check user's current points
- `/leaderboards` - Display top 10 players for current season
- `/helpme` - Show command help

### Workflow Configuration
- **Name**: Discord Bot
- **Command**: `python discord_bot.py`
- **Type**: Backend service (console output)
- **Status**: Running continuously

## Environment Setup
- Python 3.11 with discord.py 2.6.3
- Environment variable: DISCORD_BOT_TOKEN (configured in Replit Secrets)
- No frontend component - pure Discord bot backend

## Recent Changes
- 2025-09-04: Initial Replit environment setup
- Fixed typing issues in helpers.py for proper datetime handling
- Configured Python environment and dependencies
- Set up continuous workflow for bot operation
- Updated .gitignore for Python best practices

## User Preferences
- Backend-only Discord bot application
- Console-based monitoring and logging
- Automated seasonal resets every 30 days
- SQLite database for simple deployment