# Satisfying Ball - A Relaxing Bouncing Ball Simulation 🧘‍♀️

# TEST REPO!
![header](https://steamuserimages-a.akamaihd.net/ugc/930428699254564693/FFA99C866B4EA6BC93D1B9664083DEB6BA1E3386/?imw=512&amp;imh=288&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true)

Welcome to **Satisfying Ball** - a simple yet captivating game designed to help you relax and relieve stress. In this game, a ball bounces inside a circle, and you can customize various parameters and game modes. Ideal for relaxation, meditation, or just passing the time. The game doesn't require significant computing resources and runs smoothly on most computers. Developed using PyCharm 💻, we recommend using this environment for the most comfortable experience. However, the game should also run in other development environments like VS Code or the terminal, although some nuances may arise.

## Features ✨

*   **Multiple Game Modes:** 🎮
    *   **Classic Mode:** A ball simply bounces inside a circle, following the laws of physics. ⚪
    *   **Paint Map Mode:** The ball leaves a colored trail on the screen, creating unique patterns. 🎨
    *   **Duplication Mode:** Each time the ball collides with the circle wall, it duplicates, making the game more dynamic. 👯
    *   **Merge Mode:** Balls merge upon collision, forming larger balls, which creates interesting effects. 🧲
    *   **Shrinking Space Mode:** The circle gradually shrinks, increasing the difficulty and making the ball move more actively. 🕳️
*   **Extensive Customization Options:** ⚙️
    *   **Ball Size:** Change the ball's size for a more comfortable experience. 📏
    *   **Ball Speed:** Control the ball's movement speed for a more dynamic or calm gameplay. 💨
    *   **Sound Volume:** Adjust the volume of sound effects, including the sound of the ball colliding with the walls. 🔊
    *   **FPS (Frames Per Second):** Set the desired FPS for smooth animation. **Note:** For very low-performance computers, it is recommended not to set the FPS value too high to avoid performance issues. 🎬
    *   **Sound Change:** Choose your own sound file to be played when the ball collides. 🎶
    *   **Ball Color:** Change the ball's color randomly at each collision. 🌈
    *   **Pulse Effect:** Enable or disable the pulse effect when the ball collides with the circle wall. 💥
*   **Relaxing and Anti-Stress Gameplay:** The game is perfect for relieving tension and relaxing. 😌
*   **Great for TikTok and Shorts:** Create unique and soothing videos using Satisfying Ball. 📱
*   **Free and Virus-Free:** This project is made for enjoyment and is distributed completely free of charge. ✅

## How to Install and Run 🚀

### 1. Install Python 🐍

Make sure that you have **Python 3** installed on your computer. If not, download and install it from the official website:

*   **Link:** [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2. Install Pygame and Pygame-GUI 🕹️

**Pygame** is a library for creating 2D games in Python.

**Pygame-GUI** is a library for creating graphical interfaces in Pygame.

To install them, run the following commands in your terminal or command prompt:

*   **Installation via pip:**
    ```bash
    pip install pygame pygame-gui
    ```
*   **Installation via pip3 (if pip doesn't work):**
    ```bash
    pip3 install pygame pygame-gui
    ```
   If you have problems with `pip` or `pip3` make sure that folder where python is installed included in PATH.

### 3. Download Game Files 💾

1.  Go to the GitHub repository.
2.  Click the "Code" button and select "Download ZIP".
3.  Extract the archive to a convenient location.

   Alternatively, you can use `git clone`:
    ```bash
    git clone https://github.com/mulle7799/satisfying-ball.git
    ```

### 4. Run the Game ▶️

1.  Open the terminal or command prompt.
2.  Navigate to the folder where you extracted the game files using the `cd` command. For example:
    ```bash
    cd path/to/your/satisfying-ball/folder
    ```
3.  Run the game by executing the command:
    ```bash
    python bouncing_ball.py
    ```
    or
    ```bash
    python3 bouncing_ball.py
    ```
    depending on your operating system.

### 5. Select Sound File 🎵
Upon the first launch, the game will prompt you to select a sound file to be played when the ball collides. Choose a file in .mp3 or .wav format.

## Controls 🖱️

*   **Settings Menu:** Use your mouse to click buttons in the menu and change game parameters.
*   **Parameter Adjustments:** Drag the sliders to adjust the ball size, speed, volume, and FPS.
*   **Gameplay:** The ball moves automatically; you do not need to control it directly.

## Game Settings ⚙️

*   **Settings:** Click the "Settings" button in the main menu to open the settings window.
    *   **"Change Sound"**: Allows you to choose your own sound for collision events. 🎶
    *   **"Toggle Color Change"**: Enables/disables random color changes of the ball on collision. 🌈
    *   **"Toggle Pulse Effect"**: Enables/disables the pulse effect upon collision. 💥
    *   **"Reset Settings"**: Resets all settings to their default values. 🔄
    *   **"Back"**: Closes the settings window. ↩️
*   **Game Modes**: Click the "Modes" button to open a menu with different game modes.
    *   **"Classic"**: A standard mode with the bouncing ball. ⚪
    *   **"Paint Map"**: The ball leaves a colored trail behind it. 🎨
    *   **"Duplication"**: Balls are duplicated upon each collision. 👯
    *   **"Merge"**: Balls merge into bigger ones. 🧲
    *  **"Shrink"**: The space shrinks over time. 🕳️

## License 📜

This project is distributed under the [MIT License](https://opensource.org/licenses/MIT). This means that you are free to use, modify, and distribute this code for any purpose.
(more details [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) ).

## Contribution 🙌

If you have any ideas or want to improve this project, feel free to fork the repository and send your changes via a Pull Request. We are always happy to receive new ideas and improvements!

## Development Recommendations 🛠️

For a more convenient coding experience, we recommend using **PyCharm** (or another IDE) of the latest version. PyCharm provides many features that simplify Python development. Here's a step-by-step installation guide:

1.  **Download PyCharm:** 🌐
    *   Go to the download page: [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)
    *   Choose the "Community" (free) version for personal use or the "Professional" (paid) version if you need additional features.
    *   Download the installer file for your operating system (Windows, macOS, or Linux).
2.  **Install PyCharm:** 📦
    *   **Windows:** Run the downloaded `.exe` file and follow the installation wizard.
    *   **macOS:** Drag the downloaded `.dmg` file to the "Applications" folder and launch the program.
    *   **Linux:** Run the downloaded `.tar.gz` file, go to the `bin` folder, and run `pycharm.sh`.
3.  **Configure PyCharm (first run):** ⚙️
    *   When you launch PyCharm for the first time, accept the terms of the user agreement.
    *   Select a theme (e.g., Darkula for a dark theme).
    *   Configure plugins (you can skip this step at this stage).
    *   Select "Create New Project".
    *   In the "Location" field, specify the path to your project folder (the `satisfying-ball` folder).
    *   In the "Interpreter" field, select the Python interpreter that you installed earlier.
    *   Click "Create" to open the project.
4.  **Using PyCharm:** 💻
    *   Now you can open the `bouncing_ball.py` file and start editing the code.
    *   PyCharm automatically highlights syntax, offers code completion, and has a built-in debugger.
    *   It is also possible to configure Git for tracking code changes.

Main advantages of PyCharm:
* Code auto-completion. ✅
* Debugger. 🐛
* Git integration. 🌳
* And much more. ➕

## Note About Bugs 🐞

Despite all efforts, the game may contain minor bugs. If you encounter any problems, we recommend clicking the **"Reset Settings"** button in the settings menu to reset all parameters to their default values. This can help fix most issues.

## Note About Performance ⚡

The game is designed to run on computers with various specifications. However, if your computer has low performance, it is recommended not to set the FPS value too high to avoid slowdowns.

## Link 🔗

[Link to the GitHub repository](https://github.com/mulle7799/satisfying-ball)

## Developer 👨‍💻

mulle7799
