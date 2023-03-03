import math
import time
import random

from rich.progress import track, Progress

if __name__ == '__main__':
    with Progress() as progress:
        task1 = progress.add_task("[red]Downloading...", total=1000)

        while not progress.finished:
            progress.update(task1, advance=100, description=str(random.randint(1, 9)))
            time.sleep(0.5)
