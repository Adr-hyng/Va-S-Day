import pyautogui

class ImageCapture:
    def __init__(self):
        self._running = True
        self._mouse_position = None
        
    def _is_match_found(self):
        icon = pyautogui.locateOnScreen("match.png", confidence = 0.99)
        print("Running")
        if icon is None: return False
        return True
