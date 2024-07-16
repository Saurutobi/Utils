import requests, sys, json

firstName = sys.argv[1].lower()
lastName = sys.argv[2].lower()
isMarcel = sys.argv[3].lower() == 'true'


def get_shooterID(lastName, firstName):
    matchdef = open("localfile/match_def.json")
    response = json.load(matchdef)['match_shooters']
    for shooter in response:
        if shooter['sh_ln'].lower() == lastName and shooter['sh_fn'].lower() == firstName:
            return { 
                "id": shooter['sh_uuid'], 
                "class": shooter['sh_dvp'],
              }

def get_stage_info(shooter):
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
    matchdef = open("localfile/results.json")
    response = json.load(matchdef)
    stageInfo = []
    get_overall_info(response[0]['Match'][0]['Overall'])
    shooter.update(get_div_info(response[0]['Match']))
    for i in range(1, len(response)):
        stageName = list(response[i].keys())
        stageName.sort()
        stageName = stageName[0]
        for div in response[i][stageName]:
            if shooterClass in div:
                stageInfo.append(get_stage_place(div[shooterClass]))
    return stageInfo


def find_scores(shooter):
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

    matchdef = open("localfile/match_scores.json")
    response = json.load(matchdef)
    totalScores = []
    shooterID = shooter['id']
    for stage in response['match_scores']:
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


shooterInfo = get_shooterID( lastName, firstName)

stagePlace = get_stage_info( shooterInfo)
scores = find_scores(shooterInfo)

if isMarcel is True:
    marcel_print(stagePlace, scores, shooterInfo)
else: 
    don_print(stagePlace, scores, shooterInfo)

sys.stdout.flush()