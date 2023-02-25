from pathlib import Path
import json

tarot_path: Path = Path(__file__).parent / "tarot.json"
with open(tarot_path, 'r', encoding='utf-8') as f:
	content = json.load(f)
	all_cards = content.get("cards")
            
MajorArcana = {k: v for k, v in all_cards.items() if int(k) < 22}

print(MajorArcana)