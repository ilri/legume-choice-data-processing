
import pandas as pd

def subsetScoresByVariables(scores, attributeLabel, participantLabel, typologyLabel, average):

    if (average==False):
        for score in scores:
            if (score["scoreType"]=="individual" and 
            score["attribute"]["label"]==attributeLabel and 
            score["participant"]["label"]==participantLabel and 
            score["typology"]["label"]==typologyLabel):
                 return score["score"]

    if (average==True):
        for score in scores:
            if (score["scoreType"]=="average" and 
            score["attribute"]["label"]==attributeLabel): 
                return score["score"]

    raise ValueError("Did not identify correct subset")
    

def ScoresForAllAttributes(scores, attributes, participant, typology, average):
    listOfScores=[]
    for attribute in attributes:
        listOfScores.append(subsetScoresByVariables(scores=scores, 
        attributeLabel=attribute["label"], 
        participantLabel=participant["label"], 
        typologyLabel=typology["label"], 
        average=average))

    return listOfScores


def projectContextScores(project):

    # Initialising Variables
    projectID =  project["projectID"]
    projectName =  project["rawdata"]["projectInfo"]["projectName"]
    country =  project["rawdata"]["projectInfo"]["country"]


    allScores = project["rawdata"]["contextScores"]["scores"]
    attributes = project["rawdata"]["contextScores"]["attributes"]
    participants = project["rawdata"]["contextScores"]["participants"]
    typologies = project["rawdata"]["contextScores"]["typologies"]

    # Creating column names for dataframe
    typologyColumns = [ "typ"+typology["label"] for typology in typologies]
    participantColumns = [participant["label"] for participant in participants]
    allColumns = [typ+particip for typ in typologyColumns for particip in participantColumns]

    # Initialising empty array of scores
    scoresToReturn={}
    column=0
    scoresToReturn["country"] = [country for attribute in attributes]
    scoresToReturn["projectName"] = [projectName for attribute in attributes]
    scoresToReturn["projectID"] = [projectID for attribute in attributes]
    for typology in typologies:
        for participant in participants:
            scoresToReturn[allColumns[column]]=ScoresForAllAttributes(scores=allScores, 
                                                                        attributes=attributes,
                                                                        participant=participant, 
                                                                        typology=typology, 
                                                                        average=False )
            column+=1
    
    scoresToReturn["average"]=ScoresForAllAttributes(scores=allScores, 
                                                        attributes=attributes,
                                                        participant=participants[1], 
                                                        typology=participants[1], 
                                                        average=True )
    return scoresToReturn

def ContextScoresAllProjectsList(projects):
    projectsCombined=[]
    #projectIndex=0
    for project in projects:
        projectsCombined.append(projectContextScores(project=project))
        #projectIndex+=1
    return(projectsCombined)

def ContextScoresAllProjects(projects):
    contextScoresList = ContextScoresAllProjectsList(projects)
    if len(contextScoresList)==1:
        return pd.DataFrame(contextScoresList)
    if len(contextScoresList)>1:
        contextScoresDF=pd.DataFrame(contextScoresList[0])
        for scoreItem in contextScoresList[1:]:
            contextScoresDF = contextScoresDF.append(pd.DataFrame(scoreItem))
    return contextScoresDF
