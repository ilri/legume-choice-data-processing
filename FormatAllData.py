import pandas as pd 
import json
import pymongo
import os
import shutil


# Here a series of functions used to query the database are written, making it easier to convert them into
# a simple tabular format.

os.chdir('/home/ubuntu/legumeCHOICE/data-processing') 
from dataProcessing import agroEcoData, contextData, legumeData, pairwiseData, participatoryMatrixData


#--------------------------------------------------------------
#--------------------------------------------------------------
#CONNECTING TO MONGODB AND LOADING THE INITIAL PROJECT DATA
#--------------------------------------------------------------
#--------------------------------------------------------------
def FormatAllData():
    client = pymongo.MongoClient("localhost", 27017)
    db = client["legume-choice"]
    # Extracting the projects data
    projectsData =  db["projects"]

    # Extacting all projects into "object" format
    allProjects = []
    for project in projectsData.find():
            allProjects.append(project)
    projectIDs = [project["projectID"] for project in allProjects]

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #CREATING ALL OF THE NECESSARY BLANK FOLDERS TO PUBLISH THE DATA
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    homepath = os.getenv('HOME')
    os.chdir(homepath) 

    private_data_path = os.path.join(homepath, "AdminLegumeCHOICE")

    public_data_path = os.path.join(homepath, "LegumeCHOICE")
    public_data_individual_path = os.path.join(homepath,"LegumeCHOICE", "IndividualProjects")
    public_data_assembled_path = os.path.join(homepath, "LegumeCHOICE", "AggregatedProjects")


    # Removing all of the previous data
    # Private data
    if os.path.exists(private_data_path) is True:
        shutil.rmtree(private_data_path)
        #os.mkdir(private_data_path)

    # Public datasets
    if os.path.exists(public_data_path) is True:
        shutil.rmtree(public_data_path)
        #os.mkdir(public_data_individual_path)




    # Creating all empty directories
    # Private data
    if not os.path.exists(private_data_path):
        os.mkdir(private_data_path)

    # Public dataests
    if not os.path.exists(public_data_path):
        os.mkdir(public_data_path)

    # Public Individual datasets
    if not os.path.exists(public_data_individual_path):
        os.mkdir(public_data_individual_path)

    # Public aggregated datasets
    if not os.path.exists(public_data_assembled_path):
        os.mkdir(public_data_assembled_path)


    # Create an empty project directory for each individual project
    # Each folder name will be the same as the projectID
    for projectID in projectIDs:
        new_path = os.path.join(public_data_individual_path, projectID)
        os.mkdir(new_path)

        
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #LOOPING THROUGH INDIVIDUAL PROJECTS AND WRITING OUT THE NECESSARY FILES
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    project = allProjects[0]
    for project in allProjects:

        publicfolder = os.path.join(public_data_individual_path, project["projectID"])
        privatefile =  os.path.join(private_data_path, project["projectID"]+".json")
    # AgroEco information is only one row, so have to transform
        agroEcoSingleProj = pd.DataFrame(columns=list(agroEcoData.ExtractProjectAgroEcoData(project).keys()))
        agroEcoSingleProj.loc[0]=agroEcoData.ExtractProjectAgroEcoData(project).values()


        contextSingleProj = pd.DataFrame(contextData.projectContextScores(project=project))
        pairwiseSelectionsSingleProj = pairwiseData.pairWiseSelectionsProject(project=project)
        pairwideSummarySingleProj = pairwiseData.pairWiseSummaryScores(project=project)
        participatoryMatrixSingleProj = participatoryMatrixData.participatoryMatrixScoresProject(project=project)
        legumeDataSingleProj = legumeData.extractAllLegumeData(project=project)

        agroEcoSingleProj.to_csv(os.path.join(publicfolder,"agroEcoData.csv"))
        contextSingleProj.to_csv(os.path.join(publicfolder,"ContextData.csv"))
        pairwiseSelectionsSingleProj.to_csv(os.path.join(publicfolder,"PairwiseSelections.csv"))
        pairwideSummarySingleProj.to_csv(os.path.join(publicfolder,"PairwiseSummaryScores.csv"))
        participatoryMatrixSingleProj.to_csv(os.path.join(publicfolder,"ParticipatoryMatrixScores.csv"))
        legumeDataSingleProj.to_csv(os.path.join(publicfolder,"LegumeResults.csv"))

        with open(privatefile, "w") as outfile:
            JSONData = {
                "currentProject":project["rawdata"]
            }
            json.dump(JSONData,outfile, indent=4)



    #--------------------------------------------------------------
    #--------------------------------------------------------------
    # AGGREGATING ALL OF THE PROJECT INFORMATION FOR LONG CSVs FOR META-ANALYSIS
    #--------------------------------------------------------------
    #--------------------------------------------------------------




    agroEcoAllProj = agroEcoData.ExtractAllAgroEcoData(allProjects)
    contextAllProj = contextData.ContextScoresAllProjects(projects=allProjects)
    pairwiseAllProj = pairwiseData.pairWiseSelectionsAllProjects(projects=allProjects)
    pairwideSummaryAllProj = pairwiseData.pairWiseSelectionSummaryAllProjects(projects=allProjects)
    participatoryMatrixAllProj = participatoryMatrixData.participatoryMatrixAllProjects(projects=allProjects)
    legumeDataAllProj = legumeData.legumeScoresAllProjects(projects=allProjects)

    agroEcoAllProj.to_csv(os.path.join(public_data_assembled_path,"agroEcoData.csv"))
    contextAllProj.to_csv(os.path.join(public_data_assembled_path,"ContextData.csv"))
    pairwiseAllProj.to_csv(os.path.join(public_data_assembled_path,"PairwiseSelections.csv"))
    pairwideSummaryAllProj.to_csv(os.path.join(public_data_assembled_path,"PairwiseSummaryScores.csv"))
    participatoryMatrixAllProj.to_csv(os.path.join(public_data_assembled_path,"ParticipatoryMatrixScores.csv"))
    legumeDataAllProj.to_csv(os.path.join(public_data_assembled_path,"LegumeResults.csv"))




        
        

