import pyautogui
import time


def tmux_move(direction):
    """
    Move to second pane
    :param direction: direction parameters: left, right, up, down
    """
    pyautogui.hotkey('ctrl', 'B')
    pyautogui.press(direction)


def enter_command(command_to_execute):
    pyautogui.typewrite(command_to_execute)
    pyautogui.press('enter')


def run_as_standalone():
    time.sleep(5)
    tmux_move("left")
    enter_command("watch --color git status")
    tmux_move("down")
    enter_command("watch --color git remote -v")
    tmux_move("left")
    enter_command("watch --color git diff")


if __name__ == "__main__":
    run_as_standalone()
