from time import sleep

from tqdm import tqdm

if __name__ == '__main__':
    pbar = tqdm(total=100)
    for i in range(10):
        sleep(0.5)
        pbar.update(10)
        pbar.set_description(str(i))
    pbar.close()
