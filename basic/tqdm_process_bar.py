from random import random, randint
from time import sleep

from tqdm import tqdm

if __name__ == '__main__':
    outer = tqdm(total=100)

    for i in range(10):

        outer.update(10)
        outer.set_description(str(i))
        inter = tqdm(total=100, leave=False)
        for j in range(10):
            inter.update(10)
            sleep(0.5)
        inter.close()
        outer.set_postfix(loss=random(), gen=randint(1, 999), str='h',
                          lst=[1, 2])
        outer.display("bb")
        tqdm.write("Done task %i" % i)
    outer.close()
