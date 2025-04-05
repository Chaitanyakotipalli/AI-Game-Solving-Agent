# 🧠 AI-Solving Game: Rise of the Undead Nightfall: The Zombie War

## 🎮 Game Introduction
**Defending-Zombie-Simulation** is a **single-player** strategy game where the player must place different elements (**Sniper, Shotgun, Charizard, Samurai, Bomb**) to defend against incoming zombies, preventing them from crossing the lawn.

### 🕒 Gameplay Mechanics
- The game lasts **60 seconds**.
- Every **20 seconds**, the number of incoming zombies increases.
- Zombies will **attack** the placed elements and vise-versa.
- For a detailed breakdown of the game mechanics, refer to `game.txt`.

![Game Screenshot](images/image2.png)

---

🧩 AI Strategy & Implementation
Our AI agent is built with the following approach:

🔍 1. Heuristic-Based Decision Making
The agent continuously analyzes the current game state frame-by-frame.

It uses heuristic evaluation functions to determine:

Which row has the highest zombie density

Which weapons are best suited for the current threat level

How much time is left and the urgency of placing defenses

⚙️ 2. Strategic Weapon Placement
The agent selects weapons and places them only on valid tiles within the 5×5 lawn.

Placement decisions are made based on:

Zombie proximity

Weapon cooldowns and fire rate

Row-based threat score

Once placed, the AI does not re-evaluate that weapon (non-movable logic), making the initial placement critical.

📐 3. Utility Function Design
Multiple utility functions are defined to:

Assign a priority score to each row

Estimate time to collision for incoming zombies

Balance offense vs. resource availability

The highest-scoring move is executed per frame, ensuring greedy optimization with minimal computation time.

📂 More Details
Refer to agent.txt for a breakdown of the AI logic, decision flow, and sample scenarios.

🧠 With the help of frame-by-frame analysis and well-tuned heuristics, the AI agent can survive all 60 seconds and eliminate maximum zombies without manual input.

![Game Screenshot](images/image3.png)

---

## 🔥 Features
### 1️⃣ Single-Player Mode
- The game can be played **manually** or by the **AI agent**.
- Modify `game_settings.py` to switch between modes:
  - **agent_play = 1** → AI agent plays the game.
  - **agent_play = 0** → Player controls the game manually.

🎨 2️⃣ Graphical User Interface (GUI)
The game features a clean and user-friendly interface built using Pygame.

Visual assets are managed via assets.py, which handles:

🎞️ GIF animations and sprite frames for smooth and dynamic zombie and weapon movements

🌿 Realistic environmental elements (lawn, path, etc.)

Zombies come with customizable appearances to enhance visual diversity and game immersion.

UI elements such as the weapon selection bar, score display, and game-over overlay are intuitively designed for a smooth gameplay experience.

### 3️⃣ Legal Moves
- Weapons(**Sniper, Shotgun, Charizard, Samurai, Bomb**) can only be placed on the **5×5 green lawn**.

---

## 📜 Game Rules
🧩 1. Initial Setup
The game begins with a 5×5 grid lawn, where players can place weapons to defend against waves of zombies.

The interface includes a weapon selection bar at the top, current score tracker, and an animated game scene.
   ![Game Screenshot](images/image1.png)
⏱️ 2. Game Duration & Objective
The game runs for a total of 60 seconds.

Your goal is to eliminate as many zombies as possible before time runs out.

Game Over Conditions:

A zombie breaches the left edge of the lawn.

Time runs out and zombies overrun your defense.

🧟‍♂️ Survive the horde. Defend your garden. One minute is all you've got!
   - ![Game Screenshot](images/image4.png)
3. Legal Moves & Placement
Weapons can only be placed on the 5×5 green lawn (not on the sidewalk or zombie path).

Strategic placement is crucial — once a weapon is placed, it stays until destroyed.


🎮 4. Controls
Click on a gun from the selection bar to activate it.

Click on a valid tile in the lawn grid to place the gun.

Each gun automatically shoots at the closest zombie in its row.

🧮 5. Scoring
Every zombie eliminated adds +1 to your score.

Your final score is displayed at the end of the game.

🏆 Can you beat your high score and survive the full 60 seconds?



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

