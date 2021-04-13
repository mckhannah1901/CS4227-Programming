class InterceptorManager:
    def __init__(self):
        self.interceptors = set()

    def add(self, interceptor):
        self.interceptors.add(interceptor)

    def execute(self, request):
        for interceptor in self.interceptors:
            interceptor.execute(request)


class Interceptor:
    def execute(self, request):
        print(request)


class LoggingInterceptor(Interceptor):
    def execute(self, log):
        log.log()
