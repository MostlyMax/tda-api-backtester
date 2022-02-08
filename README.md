# tda-api-backtester

The goal of this project was to create an easy to use strategy backtester on top of Alex Golec's [tda-api wrapper](https://tda-api.readthedocs.io/en/latest/) for TDAmeritrade's api. Note that access to TDAmeritrade's api is required for the program to work. Currently does not support options strategies. 

## Set-Up

Set-up relies mostly on creating a class that extends the Algorithm class in AlgorithmInterface.py - this will give you all the built in tools that are documented below. It is recommended to copy the format used in AlgorithmExample.py along with the executable code at the end of the file to make the program run as similar as possible to the documentation. Below is the recommended format:

```python
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
```

- The class init method is used to initialize any environment settings (See section 'Initialization' for more details)

- The OnData method is called for every tick update at the established frequency. (See section 'Available Tools')

- The OnFinish method is called after the algorithm succesfully finishes or when a KeyboardInterrupt is caught (See section 'Plotting Data')


## Initialization

WIP

## Available Tools

WIP

## Plotting Data

WIP
