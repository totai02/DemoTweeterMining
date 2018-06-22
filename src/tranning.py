import hfihu.train
import nb.train
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'nb':
            nb.train.train()
        else:
            hfihu.train.train()