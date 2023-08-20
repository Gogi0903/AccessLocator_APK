import sys
import time
import random


def loading_bar(total, progress, length=50):
    percent = progress / total
    blocks = int(round(percent * length))
    spaces = length - blocks
    sys.stdout.write(f'\rProgress: [{"█" * blocks}{"-" * spaces}] {int(percent * 100)}%')
    sys.stdout.flush()

def main():
    total_items = 100
    for i in range(total_items + 1):
        loading_bar(total_items, i)
        time.sleep(random.uniform(0, .03))

    sys.stdout.write('\nCompleted!\n')


if __name__ == "__main__":
    main()
