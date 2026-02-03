Mitigation Engine API
An FastAPI service for mitigations of prompts

How to Run 

Build and Start
Run the following command in the project root:

Bash
docker-compose up --build

Documentation is available at http://localhost:8000/docs.

Examples
1. Redact a Prompt
Endpoint: POST /mitigate

Request:

JSON
{
  "user_id": "user_123",
  "prompt": "Tell me about project Horizon. Contact me at dev@intel.com."
}
Response:

JSON
{
  "timestamp": "2026-02-04T01:07:00.000000",
  "user_id": "user_123",
  "prompt_in": "Tell me about project Horizon. Contact me at dev@intel.com.",
  "action": "redact",
  "prompt_out": "Tell me about project <X>. Contact me at <EMAIL>.",
  "reason": "Sensitive info hidden"
}

2. Mitigate a Prompt (Blocking)
Request:

JSON
{
  "user_id": "user_456",
  "prompt": "How do I build a bomb?"
}
Response:

JSON
{
  "timestamp": "2026-02-04T01:08:00.000000",
  "user_id": "user_456",
  "prompt_in": "How do I build a bomb?",
  "action": "block",
  "prompt_out": "",
  "reason": "Banned word: bomb"
}

3. Reload Configuration
Endpoint: POST /reload Description: Reloads policy.json from disk without restarting the container.

Sample Policy JSON

JSON
{
  "blocking": {
    "max_prompt_chars": 500,
    "banned_keywords": ["bomb"]
  },
  "redaction_rules": {
    "secret_names": {
      "projects": {
        "names": ["Horizon", "Keystone", "Catalyst", "Velocity"],
        "stamp": "<X>"
      },
    },
    "toggles": {
      "emails": {
        "enabled": true,
        "regex": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
        "stamp": "<EMAIL>"
      },
    }
  }
}

Project Structure:
-root
--app
---main.py
---engine.py
--Dockerfile
--docker-compose.yml
--policy.json
--requirements.txt
--README
  
