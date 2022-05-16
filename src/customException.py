class noValue(Exception):
    def __init__(self, message="Null Values present in data"):
        self.message = message
        super().__init__(self.message)