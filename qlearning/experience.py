class Experience(object):
    """An experience in learning process."""

    def __init__(self, state, action, reward, next_state):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state

    def __str__(self):
        return (
            "{state}--{action}-->{next_state}[{reward}]"
            .format(**self.__dict__)
        )
