import pandas as pd


def pairWiseSelectionsProjectGender(project,gender):

    selections = project["rawdata"]["pairWiseScores"][gender]["pairwiseSelection"]
    projectName= project["rawdata"]["projectInfo"]["projectName"]
    projectID= project["projectID"]
    country =  project["rawdata"]["projectInfo"]["country"]


    selectionsToReturn=[]

    for selection in selections:
        selectionToAppend={
            "country": country,
            "projectName": projectName,
            "projectID":projectID,
            "option1": selection["funct1"]["name"],
            "option2": selection["funct2"]["name"],
            gender+"Choice": selection["value"]["name"],
        }
        selectionsToReturn.append(selectionToAppend)
    return pd.DataFrame(selectionsToReturn)

def pairWiseSelectionsProject(project):
    male=pairWiseSelectionsProjectGender(project=project,gender="male")
    female=pairWiseSelectionsProjectGender(project=project,gender="female")

    allSelections = male
    allSelections["femaleChoice"] = female["femaleChoice"]
    return allSelections

def pairWiseSelectionsAllProjects(projects):
    if len(projects)==1:
        return pairWiseSelectionsProject(projects)
    if len(projects)>1:
        pairWiseScoresDF=pairWiseSelectionsProject(projects[0])
        for project in projects[1:]:
            pairWiseScoresDF = pairWiseScoresDF.append(pairWiseSelectionsProject(project))
    return pairWiseScoresDF

def pairWiseSummaryScores(project):
    country =  project["rawdata"]["projectInfo"]["country"]
    projectID = project["projectID"]
    projectName = project["rawdata"]["projectInfo"]["projectName"]
    maleTotals = project["rawdata"]["pairWiseScores"]["male"]["totals"]
    femaleTotals = project["rawdata"]["pairWiseScores"]["female"]["totals"]
    averages = project["rawdata"]["pairWiseScores"]["averages"]


    pairWiseAverages = []
    for scoreIndex in range(0,len(maleTotals)):
        scoresToAppend = {
            "country": country,
            "projectName":projectName,
            "projectID":projectID,
            "attribute": maleTotals[scoreIndex]["attribute"]["name"],
            "countMale": maleTotals[scoreIndex]["value"],
            "countFemale": femaleTotals[scoreIndex]["value"],
            "average": averages[scoreIndex]["value"],
        }
        pairWiseAverages.append(scoresToAppend)

    return pd.DataFrame(pairWiseAverages)

def pairWiseSelectionSummaryAllProjects(projects):
    if len(projects)==1:
        return pairWiseSummaryScores(projects)
    if len(projects)>1:
        pairWiseSummaryScoresDF=pairWiseSummaryScores(projects[0])
        for project in projects[1:]:
            pairWiseSummaryScoresDF = pairWiseSummaryScoresDF.append(pairWiseSummaryScores(project))
    return pairWiseSummaryScoresDF
