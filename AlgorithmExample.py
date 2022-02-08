from Backtester import *

logger = logging.getLogger('Backtester.py')


class AlgoExample(Algorithm):
    def __init__(self):
        super().__init__()

    def OnData(self):
        pass

    def OnFinish(self, market):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--Update", action='store_true', help="Update CSV Files")
    args = parser.parse_args()

    InitializeBacktest(AlgoExample(), args.Update)
