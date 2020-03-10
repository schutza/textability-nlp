import json

from textability.dialog_acts.nlp.affirmations import SpacyAffirmationDetector
from textability.dialog_acts.nlp.language_processor import NLP

UOP_INPUT = '/Users/aschutz/workbench/workspace-textability/data/gen-eap-university-of-phoenix/2-shaped/uphoenix-18.03.01-SS-Chat-Transcripts.json'

def get_customer_text(line):
    obj = json.loads(line)
    if obj.get('actor_type') != 'customer':
        return None
    return obj.get('message_body')

def process_line_by_line(path, process):
    n = 0
    with open(path) as f:
        for line in f:
            customer_text = get_customer_text(line)
            if customer_text:
                process(customer_text)
                n = n + 1
            if n > 100:
                return
            
def detect_affirmations(text):
    detector = SpacyAffirmationDetector()
    is_aff, detected_aff = detector.detect(text)
    if is_aff:
        print(f'TEXT: {text}')
        print(f'AFFIRMATION: [{detected_aff}]')

def detect_entities(text):
    nlp = NLP.get('en')
    doc = nlp(text)
    entities = doc.ents
    if entities:
        print(f'TEXT: {text}')
        for entity in entities:
            print(entity.text, entity.start_char, entity.end_char, entity.label_)

    

if __name__ == "__main__":
    # process_line_by_line(UOP_INPUT, detect_affirmations)
    process_line_by_line(UOP_INPUT, detect_entities)
