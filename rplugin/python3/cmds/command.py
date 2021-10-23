from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, nvim, helper):
        self.nvim = nvim
        self.helper = helper

    @abstractmethod
    def run(self, args, ragen):
        pass
