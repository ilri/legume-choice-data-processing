import pandas as pd



# Extracting farmer data
def participatoryMatrixScoresProject(project):
    #project=allProjects[0]
    country =  project["rawdata"]["projectInfo"]["country"]
    projectID = project["projectID"]
    projectName = project["rawdata"]["projectInfo"]["projectName"]
    farmers = project["rawdata"]["participatoryMatrixScores"]["farmers"]
    farmersClean=[]
    for farmer in farmers:
        newFarmer={}
        newFarmer["country"]=country
        newFarmer["projectID"]=projectID
        newFarmer["projectName"]=projectName
        newFarmer["gender"]=farmer["gender"]
        newFarmer["typology"]=farmer["typology"]
        
        for selection in farmer["selections"]:
            newFarmer[selection["label"]]=selection["score"]
        newFarmer["total"]=farmer["total"]
        farmersClean.append(newFarmer)
    return pd.DataFrame(farmersClean)

def participatoryMatrixAllProjects(projects):
    if len(projects)==1:
        return participatoryMatrixScoresProject(projects)
    if len(projects)>1:
        participatoryMatrixScoresDF=participatoryMatrixScoresProject(projects[0])
        for project in projects[1:]:
            participatoryMatrixScoresDF = participatoryMatrixScoresDF.append(participatoryMatrixScoresProject(project))
    return participatoryMatrixScoresDF
