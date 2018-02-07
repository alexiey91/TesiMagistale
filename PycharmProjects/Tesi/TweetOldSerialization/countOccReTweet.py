class countOccReTweet(object):
    def __init__(self, edge, count):
        self.edge = edge
        self.count = count

    def __str__(self):
        return self.edge + " " + str(self.count)