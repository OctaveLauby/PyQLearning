class History(object):
    """History of experiences."""

    def __init__(self, max_size):
        self.experiences = []
        self.max_size = max_size

    def append(self, experience):
        self.experiences = self.experiences[:self.max_size - 1]
        self.experiences.append(experience)

    def last(self):
        return self.experiences[-1]

    def __iter__(self):
        return self.experiences.__iter__()
