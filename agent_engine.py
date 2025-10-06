import yaml
import re

class AgentEngine:
    def __init__(self, agents_md_path="AGENTS.md"):
        with open(agents_md_path, 'r') as f:
            raw = f.read()
        # Split on markdown code fences with YAML sections
        parts = re.split(r"``````", raw, flags=re.DOTALL)
        # parts: [pre, section1, body1, section2, body2, ...]
        self.sections = {}
        for i in range(1, len(parts), 2):
            name = parts[i].strip()
            body = parts[i+1]
            try:
                self.sections[name] = yaml.safe_load(body)
            except yaml.YAMLError:
                self.sections[name] = {}

    def get_time_window_rules(self, window_name: str) -> dict:
        return self.sections.get("Time Window Rules", {}).get(window_name, {})

    def get_confidence_weights(self) -> dict:
        return self.sections.get("Confidence Scoring", {})

    def get_timeframe_rules(self) -> dict:
        return self.sections.get("Multi-Timeframe Confirmation", {})

    def get_exit_rules(self) -> dict:
        return self.sections.get("Exit Strategy", {})
    
    def get_timeframe_analysis_config(self) -> dict:
        return self.sections.get("Timeframe Analysis Configuration", {})

    def get_candle_intelligence_config(self) -> dict:
        return self.sections.get("Candle Intelligence", {})
