from time import sleep

from tqdm import tqdm

if __name__ == '__main__':
    outer = tqdm(total=100)
    inter = tqdm(total=100)
    for i in range(10):

        outer.update(10)
        outer.set_description(str(i))
        for j in range(10):
            inter.update(10)
            sleep(0.5)
        inter.reset(100)
    outer.close()
