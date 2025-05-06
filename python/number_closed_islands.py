# Leetcode Problem: https://leetcode.com/problems/number-of-closed-islands/


class Solution(object):
    def __init__(self):
        self.seen = []
        self.grid = []
        self.scannedN = 0

    def get_next(self):
        """
        Get the first i,j index-pair of some unseen cell attached to an island
        """
        nCells = len(self.seen) * len(self.seen[0])
        while self.scannedN < nCells:
            i, j = self.scannedN // len(self.seen[0]), self.scannedN % len(self.seen[0])
            if self.seen[i][j] == 0:
                if self.grid[i][j] == 0:
                    return i, j
                self.seen[i][j] = 1
            self.scannedN += 1
        return None, None

    def crawl_island(self, i, j):
        """
        Crawl an island w/ BFS, marking all attached cells as seen
        Returns whether this island is closed or not
        """
        closed = True
        crawl_stack = [(i, j)]
        while crawl_stack:
            i, j = crawl_stack.pop(0)

            # Cell out of range. Mark is *not* closed
            if i < 0 or i >= len(self.grid) or j < 0 or j >= len(self.grid[0]):
                closed = False
                continue

            # Cell has been seen already or is water
            if self.seen[i][j] == 1 or self.grid[i][j] == 1:
                self.seen[i][j] = 1
                continue

            # Cell is unseen land. Mark as seen & add top, bottom, left, right to crawl stack
            self.seen[i][j] = 1
            crawl_stack.append((i + 1, j))
            crawl_stack.append((i - 1, j))
            crawl_stack.append((i, j - 1))
            crawl_stack.append((i, j + 1))
        return closed

    def closedIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        if len(grid) == 0 or len(grid[0]) == 0:
            return 0

        # Setup
        self.scannedN = 0
        self.seen = [[0] * len(grid[0]) for _ in range(len(grid))]
        self.grid = grid

        # Search for & crawl islands until none left
        islands_found = 0
        i, j = self.get_next()
        while i is not None:
            closed = self.crawl_island(i, j)
            if closed:
                islands_found += 1
            i, j = self.get_next()
        return islands_found
