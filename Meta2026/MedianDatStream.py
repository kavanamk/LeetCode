import heapq

class MedianFinder:
    def __init__(self):
        self.low = []   # max-heap (negated)
        self.high = []  # min-heap

    def balance(self):
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))
        if len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))

    def addNum(self, num):
        heapq.heappush(self.low, -num)
        # Fix ordering: low's max must be <= high's min
        if self.high and -self.low[0] > self.high[0]:
            heapq.heappush(self.high, -heapq.heappop(self.low))
        self.balance()

    def findMedian(self):
        if len(self.low) == len(self.high):
            return (-self.low[0] + self.high[0]) / 2.0
        return -self.low[0]
