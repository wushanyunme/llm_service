class ModelRouter:
    def __init__(self, adapters):
        self.adapters = adapters

    def route(self, request):
        if request.model != "auto":
           return self.adapters[request.model]
        
        if "代码" in request.prompt:
            return self.adapters["deepseek"]

        return self.adapters["openai"]