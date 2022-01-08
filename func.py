'''Additional func'''


class ProgressBar:
    """
    @attributes:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    def __init__(self, total, prefix='', suffix='', decimals=1, length=50, fill='█', end="\r"):
        self.curr = 0
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.end = end
        self.output = f'\r{prefix} |{{0}}| {{1}}% {suffix}{end}'

    def __str__(self):
        percent = 100 * (self.curr / self.total)
        percent = f'{percent:.{self.decimals}f}'

        filled = self.length * self.curr // self.total
        progress = self.fill * filled + '-' * (self.length - filled)
        return self.output.format(progress, percent)

    def print(self, curr=None):
        '''print the bar'''
        if curr is not None:
            self.curr = curr
        print(self, end='')
        if self.curr == self.total:
            print()


def main():
    '''test func'''
    import time  # pylint: disable=import-outside-toplevel

    # A List of Items
    items = list(range(0, 60))
    lenght = len(items)

    # Initial call to print 0% progress
    progress_bar = ProgressBar(lenght, prefix='Progress:', length=50)
    progress_bar.print(0)
    for i, _ in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        progress_bar.print(i + 1)


if __name__ == '__main__':
    main()
