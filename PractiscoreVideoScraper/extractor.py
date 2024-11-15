import json

def extract_matchdef(file_path):
    with open('test.txt') as file:
        text = file.read()

        start_index = text.find('matchDef = {') + 11
        end_index = text.rfind(';\n        scores = {') 

        json_string = text[start_index:end_index]
        
        try:
            json_object = json.loads(json_string)
            return json_object
        except json.JSONDecodeError:
            return None  # Invalid JSON format
            
def extract_scores(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

        start_index = text.find('scores = {') + 9
        end_index = text.rfind(';\n        results = [{') 

        json_string = text[start_index:end_index]
        
        try:
            json_object = json.loads(json_string)
            return json_object
        except json.JSONDecodeError:
            return None  # Invalid JSON format

def extract_results(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

        start_index = text.find('results = [{') + 10
        end_index = text.rfind(';\n\n        resultsLoaded = ') 

        json_string = text[start_index:end_index]
        
        try:
            json_object = json.loads(json_string)
            return json_object
        except json.JSONDecodeError:
            return None  # Invalid JSON format
            
if __name__ == "__main__":
    file_path = "C:/Git/Utils/PractiscoreVideoScraper/test.txt"  # Replace with the actual path to your file
    matchdef = extract_matchdef(file_path)

    if matchdef:
        print(matchdef)
    else:
        print("No valid JSON object found in the file.")
        
    scores = extract_scores(file_path)

    if scores:
        print(scores)
    else:
        print("No valid JSON object found in the file.")
        
    results = extract_results(file_path)

    if results:
        print(results)
    else:
        print("No valid JSON object found in the file.")
        