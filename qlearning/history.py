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

    def is_empty(self):
        return len(self) == 0

    def is_full(self):
        return len(self) == self.max_size

    def pop(self):
        return self.experiences.pop(-1)

    def total_reward(self):
        return sum(map(lambda exp: exp.reward, self.experiences))

    def __len__(self):
        return len(self.experiences)

    def __iter__(self):
        return self.experiences.__iter__()
