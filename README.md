# 🧠 AI-Solving Game: Rise of the Undead Nightfall – The Zombie War

## 🎮 Game Introduction
Defending-Zombie-Simulation is a single-player strategy game where the player must deploy various elements (Sniper, Shotgun, Charizard, Samurai, Bomb) to fend off incoming zombies and protect the lawn from being overrun.

## 🕒 Gameplay Mechanics
- **Duration**: The game lasts 60 seconds.
- **Progression**: Every 20 seconds, the number of incoming zombies increases.
- **Combat**: Zombies will attack the placed elements and vice versa.

For a detailed breakdown of the game mechanics, refer to `game.txt`.

![Game Screenshot](images/image2.png)

## 🧩 AI Strategy & Implementation
Our AI-powered agent is designed to maximize your winning probability across 50+ test cases using a combination of heuristic analysis and utility-based decision making.

### 🔍 1. Heuristic-Based Decision Making
- **Frame-by-Frame Analysis**: The agent continuously analyzes the current game state.
- **Heuristics Used**:
  - Zombie Density: Identifies the row with the highest concentration of zombies.
  - Weapon Suitability: Chooses the best weapon based on current threats.
  - Time Sensitivity: Assesses the remaining time to gauge the urgency for defensive placements.

### ⚙️ 2. Strategic Weapon Placement
- **Valid Placement**: Weapons are placed only on valid tiles within the 5×5 lawn.
- **Decision Factors**:
  - Proximity of zombies
  - Weapon cooldowns and fire rate
  - A calculated row-based threat score
- **Permanent Setup**: Once a weapon is placed, it remains until destroyed, making each decision critical.

### 📐 3. Utility Function Design
- **Priority Scoring**: Assigns a priority score to each row based on the threat level.
- **Collision Estimation**: Calculates the time until zombies reach your defenses.
- **Resource Balancing**: Weighs offensive power against available resources.

The agent then executes the highest-scoring move each frame for rapid, efficient decision-making.

For an in-depth explanation of the AI logic, decision flow, and sample scenarios, please refer to `agent.txt`.

![Game Screenshot](images/image3.png)

## 🔥 Features
### 1️⃣ Single-Player Mode
- **Dual Modes**: Play manually or let the AI agent take control.
- **Mode Switch**: Modify `game_settings.py`:
  - `agent_play = 1` → AI agent plays the game.
  - `agent_play = 0` → Manual player control.

### 🎨 2️⃣ Graphical User Interface (GUI)
- **Built with Pygame**: Enjoy a clean and intuitive interface.
- **Asset Management**: Visual assets, including:
  - GIF animations and sprite frames (handled via `assets.py`)
  - Realistic environmental elements like the lawn and path
- **Customizable Visuals**: Zombies feature adjustable appearances to enrich gameplay.
- **User-Friendly Layout**: UI elements such as the weapon selection bar, score display, and game-over overlay ensure a smooth experience.

### 3️⃣ Legal Moves
- **Placement Restriction**: Weapons (Sniper, Shotgun, Charizard, Samurai, Bomb) can only be placed on the 5×5 green lawn.
- **Tactical Importance**: Strategic placement is key, as each weapon remains fixed once deployed.

## 📜 Game Rules
### 🧩 1. Initial Setup
The game begins with a 5×5 grid lawn, where players can place weapons to defend against waves of zombies.

Interface Includes: A weapon selection bar at the top, current score tracker, and an animated game scene.

![Game Screenshot](images/image1.png)

### ⏱️ 2. Game Duration & Objective
- **Total Duration**: 60 seconds.
- **Objective**: Eliminate as many zombies as possible before time runs out.
- **Game Over Conditions**:
  - A zombie breaches the left edge of the lawn.
  - Zombies overrun your defense as time expires.

*Survive the horde. Defend your garden. One minute is all you've got!*

![Game Screenshot](images/image4.png)

### 3. Legal Moves & Placement
- **Valid Area**: Weapons can only be placed on the 5×5 green lawn (not on the sidewalk or zombie path).
- **Strategic Placement**: Once placed, a weapon remains until destroyed.

### 🎮 4. Controls
- **Select Weapon**: Click on a gun in the selection bar to activate it.
- **Place Weapon**: Click on a valid tile in the lawn grid to deploy the selected gun.
- **Automatic Action**: Each gun automatically shoots at the closest zombie in its row.

### 🧮 5. Scoring
- **Point System**: Every zombie eliminated adds +1 to your score.
- **Final Score**: Displayed at the end of the game.

*Challenge: Can you beat your high score and survive the full 60 seconds?*


## 🛠️ Installation Guide
1. **Clone the repository**:
   ```sh
   git clone https://github.com/Chaitanyakotipalli/AI-Game-Solving-Agent
   
   ```
2. **Install dependencies**:
   ```sh
   pip install pygame
   ```
3. **Run the game**:
   ```sh
   python main_game.py
   ```

---

## 🚀 Future Enhancements
- **Integrate Reinforcement Learning** to improve AI adaptability.
- **Train the AI on more test cases** and expand the game environment.
- **Enhance UI/UX** with better graphics and interactive elements.
- **Implement real-time gameplay analytics** for deeper insights.

---

*Happy gaming! 🚀🧠🎮*

