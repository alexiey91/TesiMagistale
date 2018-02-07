class countOccTweet(object):
    def __init__(self, username,count):
        self.username = username
        self.count = count

    def __str__(self):
        return self.username+" "+str(self.count)