import sys
import time

from colorama import Fore


def animation_spinner(text:str,
                      time_of_loading: int=6,
                      delay: float=0.15) -> None:
    """
        Displays a simple spinner animation next to the given text.

        Args:
            text (str): Message to show before the spinner starts.
            time_of_loading (int, optional): How many full spins to perform. Default is 6.
            delay (float, optional): Time (in seconds) between each frame. Default is 0.15.

        Behavior:
            Prints the text once, then loops through the spinner symbols
            ['|', '/', '-', '\\'] to simulate loading. Animation updates in-place.

        Notes:
            Used for aesthetic/UX purposes while a process is running or "loading".
            Does not return anything.
    """
    spinner = ['|', '/', '-', '\\']
    print()
    print(Fore.GREEN + text, end=' ', flush=False)
    for _ in range(time_of_loading):
        for symbol in spinner:
            sys.stdout.write(Fore.GREEN + symbol)
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write('\b')
    print()


def loading(text:str,
            time_of_loading:int=6,
            delay:float=0.5) -> None:
    """
    Simulates a simple loading animation by printing dots after the given text.

        Args:
           text (str): The base message to display (e.g., "Loading").
           time_of_loading (int, optional): Number of animation steps (default: 6).
           delay (float, optional): Pause duration between steps in seconds (default: 0.5).

       Behavior:
           Prints the text with an increasing number of dots (e.g., "Loading.", "Loading..", etc.)
           on the same line using carriage return (\r). Useful for creating a visual delay effect.

       Returns:
           None
    """
    print()
    for i in range(time_of_loading):
        print(Fore.GREEN + f"{text}{'.' * i}", end='\r', flush=True)
        time.sleep(delay)
    print()

