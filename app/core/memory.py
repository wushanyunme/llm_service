import redis
import json

class MemoryManager:
    def __init__(self):
        self.r = redis.Redis(host="localhost", port=6379, decode_responses= True)

    def get(self, session_id):
        data = self.r.get(session_id)
        return json.loads(data) if data else None

    def save(self, session_id, messages):
        self.r.set(session_id, json.dumps(messages[-20:]))