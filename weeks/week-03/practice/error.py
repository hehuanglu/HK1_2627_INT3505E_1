import uuid

from flask import jsonify, request

ERROR_BASE = "https://api.example.com/problems"


class ApiProblem(Exception):
    def __init__(self, status, title, detail=None, type_path=None, **extra):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = f"{ERROR_BASE}/{type_path}" if type_path else f"{ERROR_BASE}/generic"
        self.extra = extra

    def get_response(self):
        body = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "instance": request.path,
            "trace_id": str(uuid.uuid4()),
        }

        if self.detail:
            body["detail"] = self.detail
        body.update(self.extra)

        resp = jsonify(body)
        resp.status_code = self.status
        resp.headers["Content-Type"] = "application/problem+json"
        return resp