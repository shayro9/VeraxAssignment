import json
import re
from datetime import datetime


def _redact_toggles(prompt, toggles):
    modified_prompt = prompt
    redacted_any = False

    for rule in toggles.values():
        if rule.get("enabled", False):
            pattern = rule.get("regex")
            if re.search(pattern, modified_prompt):
                stamp = rule.get("stamp")
                modified_prompt = re.sub(pattern, stamp, modified_prompt)
                redacted_any = True

    return modified_prompt, redacted_any


def _redact_names(prompt, names):
    modified_prompt = prompt
    redacted_any = False
    for rule in names.values():
        stamp = rule.get("stamp")
        for name in rule.get("names"):
            pattern = re.compile(re.escape(name), re.IGNORECASE)
            modified_prompt, count = pattern.subn(stamp, modified_prompt)

            if count > 0:
                redacted_any = True

    return modified_prompt, redacted_any


class MitigationEngine:
    def __init__(self, policy_path="policy.json"):
        self.policy_path = policy_path
        self.policy = dict()
        self.history = list()
        self.load_policy()

    def load_policy(self):
        with open(self.policy_path, 'r') as f:
            self.policy = json.load(f)

    def get_history(self, n=20):
        return self.history[-n:]

    def mitigate(self, user_id: str, prompt: str):
        # --- BLOCKING ---
        blocking = self.policy.get("blocking")
        if len(prompt) > blocking.get("max_prompt_chars"):
            return self._record(user_id, "block", prompt, "", "Prompt too long")

        for word in blocking.get("banned_keywords"):
            if word.lower() in prompt.lower():
                return self._record(user_id, "block", prompt, "", f"Banned word: {word}")

        # --- REDACTION ---

        toggles = self.policy.get("redaction_rules").get("toggles")
        modified_prompt, r1 = _redact_toggles(prompt, toggles)

        secret_names = self.policy.get("redaction_rules").get("secret_names")
        modified_prompt, r2 = _redact_names(modified_prompt, secret_names)
        # --- DECISION ---

        redacted_any = r1 or r2
        action = "redact" if redacted_any else "allow"
        reason = "Sensitive info hidden" if redacted_any else "Safe"

        return self._record(user_id, action, prompt, modified_prompt, reason)

    def _record(self, user_id, action, prompt, prompt_out, reason):
        decision = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "prompt_in": prompt,
            "action": action,
            "prompt_out": prompt_out,
            "reason": reason
        }
        self.history.append(decision)
        return decision
