from app.core.memory import MemoryManager

class Orchestrator:
    def __init__(self, router):
        self.router = router
        self.memory = MemoryManager()

    def chat(self, request):
        history = self.memory.get(request.session_id)
        
        messages = history + [
            {"role": "user", "content": request.prompt}
        ]

        adapter = self.router.route(request)

        response = adapter.chat(messages)

        messages.append({"role": "assistant", "content": response})
        self.memory.save(request.session_id, messages)

        return response

    def stream(self, request):
        history = self.memory.get(request.session_id)
        
        messages = history + [
            {"role": "user", "content": request.prompt}
        ]

        adapter = self.router.route(request)

        return adapter.stream(messages)