from server.plan.constants import ACTION_TYPES

PLAN_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "tasks"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "overview": {"type": "string"},
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "id",
                    "orderIndex",
                    "title",
                    "filePath",
                    "actionType",
                    "dependencies"
                ],
                "properties": {
                    "id": {"type": "string"},
                    "orderIndex": {"type": "number"},
                    "title": {"type": "string"},
                    "filePath": {"type": "string"},
                    "actionType": {
                        "type": "string",
                        "enum": list(ACTION_TYPES)
                    },
                    "dependencies": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }
}
