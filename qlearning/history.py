class History(object):
    """History of experiences."""

    def __init__(self, max_size):
        self.experiences = []
        self.max_size = max_size

    def append(self, experience):
        self.experiences = self.experiences[:self.max_size - 1]
        self.experiences.append(experience)

    def clean(self):
        self.experiences = []

    def last(self):
        return self.experiences[-1]

    def total_reward(self):
        return sum(map(lambda exp: exp.reward, self.experiences))

    def __iter__(self):
        return self.experiences.__iter__()
