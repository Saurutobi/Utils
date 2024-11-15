import re, sys, time, requests, json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options as FirefoxOptions

url =  sys.argv[1]

def extract_matchdef(html):
    start_index = str(html).find('matchDef = {') + 11
    end_index = str(html).rfind(';\\n        scores = {') 

    json_string = str(html)[start_index:end_index]
    
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError:
        return None  # Invalid JSON format

def extract_scores(html):
    start_index = str(html).find('scores = {') + 9
    end_index = str(html).rfind(';\\n        results = [{') 

    json_string = str(html)[start_index:end_index]
    
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError:
        return None  # Invalid JSON format

def extract_results(html):
    start_index = str(html).find('results = [{') + 10
    end_index = str(html).rfind(';\\n\\n        resultsLoaded = ') 

    json_string = str(html)[start_index:end_index]
    
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError:
        return None  # Invalid JSON format

def get_shooterID(lastName, firstName, html):
    matchdef = extract_matchdef(html)['match_shooters']
    for shooter in matchdef:
        if shooter['sh_ln'].lower() == lastName and shooter['sh_fn'].lower() == firstName:
            return { 
                "id": shooter['sh_uuid'], 
                "class": shooter['sh_dvp'],
              }

def get_stage_info(shooter, html):
    def get_stage_place(stageInfo):
        for shooter in stageInfo:
            if shooter['shooter'] == shooterID:
                info = {
                    "name": stageName, 
                    "place": shooter['place'], 
                    "percent": shooter['stagePercent'], 
                    "hitFactor": shooter['hitFactor']
                    }
                return info

    def get_overall_info(stageInfo):
        for shooterInfo in stageInfo:
            if shooterInfo['shooter'] == shooterID:
                shooter['possiblePoints'] = shooterInfo['possiblePoints']
                shooter['matchPercent'] = shooterInfo['matchPercent']
                shooter['place'] = f"{shooterInfo['pscPlace']}/{len(stageInfo)}"
                shooter['percent'] = shooterInfo['percentOfPossible']
                shooter['points'] = shooterInfo['matchPoints']
    
    def get_div_info(stageInfo):
        newInfo = {}
        for i in range(1, len(stageInfo)):
            if shooter['class'] in stageInfo[i]:
                for shooterInfo in stageInfo[i][shooter['class']]:
                    if shooterInfo['shooter'] == shooterID:
                        newInfo['classPercent'] = shooterInfo['matchPercent']
                        newInfo['classPlace'] = f"{shooterInfo['pscPlace']}/{len(stageInfo[i][shooter['class']])}"
                        newInfo['classPercentPossible'] = shooterInfo['percentOfPossible']
                        return newInfo

    shooterClass = shooter['class']
    shooterID = shooter['id']
    results = extract_results(html)
    stageInfo = []
    get_overall_info(results[0]['Match'][0]['Overall'])
    shooter.update(get_div_info(results[0]['Match']))
    for i in range(1, len(results)):
        stageName = list(results[i].keys())
        stageName.sort()
        stageName = stageName[0]
        for div in results[i][stageName]:
            if shooterClass in div:
                stageInfo.append(get_stage_place(div[shooterClass]))
    return stageInfo

def find_scores(shooter, html):
    def find_shooter(stagescores):
        for shooter in stagescores:
            if shooter['shtr'] == shooterID:
                scores = {
                    'A': 0,
                    'C': 0,
                    'D': 0,
                    'M': 0,
                    'NPM': 0,
                    'NS': 0,
                    'PROC': 0,
                    'time': 0
                }
                try:
                    if 'ts' in shooter:
                        rawScores = shooter['ts']
                    else:
                        rawScores = 0
                    for timeInSec in shooter['str']:
                        scores['time'] += timeInSec
                    if 'proc' in shooter:
                        scores['PROC'] += shooter['proc']
                    scores['A'] += shooter['poph']
                    scores['M'] += shooter['popm']
                    for score in rawScores:
                        # alpha = 1
                        # charlie = 256
                        # delta = 4096
                        # ns = 65536
                        # mike = 1048577
                        # npm = 16777216
                        scores['NPM'] += score // 16777216
                        score %= 16777216
                        scores['M'] += score // 1048576
                        score %= 1048576
                        scores['NS'] += score // 65536
                        score %= 65536
                        scores['D'] += score // 4096
                        score %= 4096
                        scores['C'] += score // 256
                        score %= 256
                        scores['A'] += score
                except:
                    test = 0
                return scores    

    scores = extract_scores(html)
    totalScores = []
    shooterID = shooter['id']
    for stage in scores['match_scores']:
        val = find_shooter(stage['stage_stagescores'])
        if val:
            totalScores.append(val)   
    return totalScores

def marcel_print(stages, scores, shooter):
    overallScores = {
        'A': 0,
        'C': 0,
        'D': 0,
        'M': 0,
        "NPM": 0,
        "NS": 0,
        "PROC": 0,
        "time": 0,
    }
    for i in range(len(stages)):
        try:
            place = stages[i]['place']
            shooterClass = shooter['class'] 
            percent = stages[i]['percent']
            stage = stages[i]['name']
            time = scores[i]['time']
            if place == 1:
                printString = "Stage Win"
            elif place % 10 == 1 and place > 20:
                printString = f"{place}st {shooterClass} {percent}%"
            elif place % 10 == 2 and (place > 20 or place < 10):
                printString = f"{place}nd {shooterClass} {percent}%"
            elif place % 10 == 3 and (place > 20 or place < 10):
                printString = f"{place}rd {shooterClass} {percent}%"
            else:
                printString = f"{place}th {shooterClass} {percent}%"
            printString += f" - {stage}\nTime: {time}s, "
            for key in scores[i]:
                overallScores[key] += scores[i][key]
                if scores[i][key] > 0 and key != "time":
                    printString += f"{scores[i][key]}{key}, "
            printString += f"{float(stages[i]['hitFactor']):.4f}HF"
            print(printString)
            print(" ")
        except:
            print("Stage printing failed")
    printString = ""
    print(printString)
    
def marcel_print_insta_reel(stages, scores, shooter):
    overallScores = {
        'A': 0,
        'C': 0,
        'D': 0,
        'M': 0,
        "NPM": 0,
        "NS": 0,
        "PROC": 0,
        "time": 0,
    }
    for i in range(len(stages)):
        try:
            place = stages[i]['place']
            shooterClass = shooter['class'] 
            percent = stages[i]['percent']
            stage = stages[i]['name']
            time = scores[i]['time']
            if place == 1:
                printString = "Stage Win"
            elif place % 10 == 1 and place > 20:
                printString = f"{place}st {shooterClass} {percent}%"
            elif place % 10 == 2 and (place > 20 or place < 10):
                printString = f"{place}nd {shooterClass} {percent}%"
            elif place % 10 == 3 and (place > 20 or place < 10):
                printString = f"{place}rd {shooterClass} {percent}%"
            else:
                printString = f"{place}th {shooterClass} {percent}%"
            printString += f"\n{stage}\nTime: {time}s\n"
            for key in scores[i]:
                overallScores[key] += scores[i][key]
                if scores[i][key] > 0 and key != "time":
                    printString += f"{scores[i][key]}{key}, "
            printString += f"\n{float(stages[i]['hitFactor']):.4f}HF"
            print(printString)
            print(" ")
        except:
            print("Stage printing failed")
    printString = ""
    print(printString)

def don_print(stages, scores, shooter):
    overallScores = {
        'A': 0,
        'C': 0,
        'D': 0,
        'M': 0,
        "NPM": 0,
        "NS": 0,
        "PROC": 0,
        "time": 0,
    }
    for i in range(len(stages)):
        place = stages[i]['place']
        shooterClass = shooter['class'] 
        percent = stages[i]['percent']
        stage = stages[i]['name']
        time = scores[i]['time']
        
        
        printString = f"{stage}"
        
        for key in scores[i]:
            overallScores[key] += scores[i][key]
            if scores[i][key] > 0 and key != "time":
                printString += f"\n{key}: {scores[i][key]}"
        
        printString += f"\nTime: {time}s"
        
        printString += f"\nHF: {float(stages[i]['hitFactor']):.4f}"
        
        printString += "\n"
        
        if place == 1:
            printString += "Stage Win"
        elif place % 10 == 1 and place > 20:
            printString += f"{place}st {shooterClass} {percent}%"
        elif place % 10 == 2 and (place > 20 or place < 10):
            printString += f"{place}nd {shooterClass} {percent}%"
        elif place % 10 == 3 and (place > 20 or place < 10):
            printString += f"{place}rd {shooterClass} {percent}%"
        else:
            printString += f"{place}th {shooterClass} {percent}%"
        print(printString)
        print(" ")
    printString = ""
    print(printString)

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(url)
html = driver.page_source.encode('utf-8')

marcelShooterInfo = get_shooterID("englmaier", "marcel", html)
donShooterInfo = get_shooterID("carroll", "don", html)
ericShooterInfo = get_shooterID("beerbaum", "eric", html)
marcelStagePlace = get_stage_info(marcelShooterInfo, html)
donStagePlace = get_stage_info(donShooterInfo, html)
ericStagePlace = get_stage_info(ericShooterInfo, html)
marcelScores = find_scores(marcelShooterInfo, html)
donScores = find_scores(donShooterInfo, html)
ericScores = find_scores(ericShooterInfo, html)

print("MarcelPrint")
marcel_print(marcelStagePlace, marcelScores, marcelShooterInfo)
marcel_print_insta_reel(marcelStagePlace, marcelScores, marcelShooterInfo)
print("DonniePrint")
don_print(donStagePlace, donScores, donShooterInfo)
print("EricPrint")
marcel_print(ericStagePlace, ericScores, ericShooterInfo)

sys.stdout.flush()