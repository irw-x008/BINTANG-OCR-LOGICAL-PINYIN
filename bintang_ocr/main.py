import os
import sys

# Root path fixing for pyinstaller/nuitka bundled environment
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)
sys.path.insert(0, application_path)

from utils.config_manager import load_config
from ui.styles import apply_global_styles
from ui.loading_screen import LoadingScreen
from ui.main_window import MainWindow

def main():
    # 1. Load Environment Variables / API Keys
    load_config()
    
    # 2. Init global styles
    apply_global_styles()
    
    # 3. Initialize Main Window (Hidden initially)
    app = MainWindow()
    app.withdraw()
    
    # 4. Show Animated Loading Screen
    splash = LoadingScreen(app)
    
    def on_loading_complete():
        splash.destroy()
        app.deiconify() # Reveal Main Window
        
    # Simulate loading process (3 seconds) before revealing main app
    app.after(3000, on_loading_complete)
    
    # 5. Start Event Loop
    app.mainloop()

if __name__ == "__main__":
    main()
