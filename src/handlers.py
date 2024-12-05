class RequestError(ValueError):

    def __init__(self, query):
        super().__init__(self)
        self.query = query


    def __str__(self) -> str:
        return f"По запросу {self.query} ничего не найдено"