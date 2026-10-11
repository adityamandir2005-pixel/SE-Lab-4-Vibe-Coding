# SE Lab-4 VIbe Coding — Fruit Catcher

A small Pygame arcade game about catching fruit and dodging hazards.

## Run the game

Requirements: Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
python main.py
```

If your computer has more than one Python installation, use the same Python
launcher for both commands (for example, `py -3.13 -m pip install -r
requirements.txt` followed by `py -3.13 main.py`).

## Controls

- Move the basket with **A / D** or the **Left / Right arrow keys**.
- Press **R** on the Game Over screen to restart.
- Close the game window to exit.

## How to play

- Catch apples, oranges, and grapes for **+1 point**.
- Letting a regular fruit hit the floor costs **1 life**.
- Catching rotten fruit costs **1 point** (score cannot go below zero).
- Catching a bomb costs **1 life**. Hazards can be dodged safely.
- The game ends at zero lives and freezes until restarted.
- As the score rises, new items fall faster and spawn more often.
- Colored splash droplets appear when an item is caught or hits the floor.

The game begins with 3 lives. Restarting clears the score, lives, falling items,
and particle effects and resets the difficulty.

## Implementation notes

- `game/game_engine.py` handles scoring, lives, difficulty, collisions, game
  states, and splash particles.
- `game/fruit.py` draws the fruit types, rotten fruit, and bombs.
- `game/basket.py` handles basket movement and screen boundaries.
- `main.py` starts the Pygame window and main loop.

## Lab submission checklist

- [x] Fixed missed-fruit scoring and life loss.
- [x] Added rotten fruit and bomb hazards.
- [x] Added score-based falling-speed and spawn-rate escalation.
- [x] Added fruit splash particles for catches and floor impacts.
- [x] Before-change recording is included as `before update.mp4` (14.1 seconds).
- [x] After-change recording is included as `after update.mp4` (19.31 seconds).
- [x] Conversation transcript is included as `chat_history.docx`.
- [x] The project chat is available at the
  [shared conversation link](https://chatgpt.com/s/cx_6acb9877ae20819181ddc6cea015e8a5).

The handout requests 10-second videos. The included recordings are longer;
trim each to 10 seconds if the instructor requires an exact duration.

The lab submission is organized in this repository: the game source, dependency
list, before/after recordings, and conversation transcript are included. The
chat-history document contains the visible prompts and replies; the shared link
opens the conversation page.

