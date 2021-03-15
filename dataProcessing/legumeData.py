

import pandas as pd


def extractLegumeResults(legume, country, projectName, projectID):
    contextVariables = ["land",
            "labour",
            "seed",
            "inp-serv",
            "knowl-skill",
            "water",
            "markets"]

    functionVariables=["food",
            "feed",
            "income",
            "erosion-control",
            "fuel",
            "soil-fertility"]

    legumeVariables = ["name",
            "type",
            "food",
            "feed",
            "income",
            "erosion-control",
            "fuel",
            "soil-fertility",
            "land",
            "labour",
            "seed",
            "inp-serv",
            "knowl-skill",
            "water",
            "markets",
            "agroecology-source"]

    maxMinVariables=["rainfall",
            "temp",
            "alt",
            "soilpH"]

    legumeData = {
        "country":country, 
        "projectName": projectName, 
        "projectID":projectID,
        "legumeName":legume["name"]

    }
    for variable in  legumeVariables:
        if variable in contextVariables:
            legumeData["context_"+variable]=legume[variable]
        if variable in functionVariables:
            legumeData["function_"+variable]=legume[variable]
    for variable in maxMinVariables:
        legumeData["agroEco_"+variable+"_min"]=legume[variable][0]["min"]
        legumeData["agroEco_"+variable+"_max"]=legume[variable][0]["max"]

    for agroEcoScore in legume["results"]["agroEcoFit"]:
        if "agroEcoFilter" in agroEcoScore.keys():
            scoreAttribute=agroEcoScore["agroEcoFilter"]["label"]
            legumeData["agroEcoScore_"+scoreAttribute]=agroEcoScore["score"]
        if "overallFit" in agroEcoScore.keys():
            legumeData["OVERALL_agroEcoScore"]=agroEcoScore["overallFit"]
        if "overallRank" in agroEcoScore.keys():
            legumeData["OVERALL_agroEcoRank"]=agroEcoScore["overallRank"]

    for contextScore in legume["results"]["contextFit"]:
        if "attribute" in contextScore.keys():
            scoreAttribute=contextScore["attribute"]["label"]
            legumeData["contextScore_"+scoreAttribute]=contextScore["score"]
        if "overallFit" in contextScore.keys():
            legumeData["OVERALL_contextScore"]=contextScore["overallFit"]
        if "overallRank" in contextScore.keys():
            legumeData["OVERALL_contextRank"]=contextScore["overallRank"]

    for functionScore in legume["results"]["functionFit"]:
        if "legumeFunction" in functionScore.keys():
            scoreAttribute=functionScore["legumeFunction"]["label"]
            legumeData["functionScore"+scoreAttribute]=functionScore["score"]
        if "overallFit" in functionScore.keys():
            legumeData["OVERALL_functionScore"]=functionScore["overallFit"]
        if "overallRank" in functionScore.keys():
            legumeData["OVERALL_functionRank"]=functionScore["overallRank"]
    
    return legumeData



def extractAllLegumeData(project):
    legumeData = []
    legumes = project["rawdata"]["results"]["legumes"]

    country =  project["rawdata"]["projectInfo"]["country"]
    projectID = project["projectID"]
    projectName = project["rawdata"]["projectInfo"]["projectName"]
    legumes = project["rawdata"]["results"]["legumes"]

    for legume in legumes:
        legumeData.append(extractLegumeResults(legume=legume, 
                                                country=country, 
                                                projectName=projectName, 
                                                projectID=projectID))

    return pd.DataFrame(legumeData)


def legumeScoresAllProjects(projects):
    if len(projects)==1:
        return extractAllLegumeData(projects)
    if len(projects)>1:
        legumeDataDF=extractAllLegumeData(projects[0])
        for project in projects[1:]:
            legumeDataDF = legumeDataDF.append(extractAllLegumeData(project))
    return legumeDataDF