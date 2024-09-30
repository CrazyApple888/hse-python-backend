from lecture_1.hw import handlers

routes: list[handlers.BaseHandler] = [
    handlers.FibonacciHandler(),
    handlers.FactorialHandler(),
    handlers.MeanHandler(),
]
