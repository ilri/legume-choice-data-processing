import pandas as pd 
import json
import pymongo
import os
import shutil

from datetime import datetime

# Here a series of functions used to query the database are written, making it easier to convert them into
# a simple tabular format.

os.chdir('/home/ubuntu/legumeCHOICE/data-processing') 
#os.chdir("/home/lgorman/Desktop/legumeCHOICE/data-processing")


#--------------------------------------------------------------
#--------------------------------------------------------------
#CONNECTING TO MONGODB AND LOADING THE INITIAL PROJECT DATA
#--------------------------------------------------------------
#--------------------------------------------------------------
def FormatAllData():
    from dataProcessing import agroEcoData, contextData, legumeData, pairwiseData, participatoryMatrixData, projectProcessing

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
    private_project_path=os.path.join(homepath, "AdminLegumeCHOICE","IndividualProjects")
    private_aggregated_path=os.path.join(homepath, "AdminLegumeCHOICE","AggregatedProjectInformation")

    public_data_path = os.path.join(homepath, "LegumeCHOICE")
    public_data_individual_path = os.path.join(homepath,"LegumeCHOICE", "IndividualProjects")
    public_data_assembled_path = os.path.join(homepath, "LegumeCHOICE", "AggregatedProjects")

    test_data_path = os.path.join(homepath, "LegumeCHOICE","TestProjects")
    test_data_individual_path = os.path.join(homepath,"LegumeCHOICE","TestProjects", "IndividualProjects")

    public_data_by_country = os.path.join(homepath, "LegumeCHOICE", "ByCountry")
    private_data_by_country = os.path.join(homepath, "AdminLegumeCHOICE", "ByCountry")


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

    if not os.path.exists(private_project_path):
        os.mkdir(private_project_path)

    if not os.path.exists(private_aggregated_path):
        os.mkdir(private_aggregated_path)

    # Public dataests
    if not os.path.exists(public_data_path):
        os.mkdir(public_data_path)

    # Public Individual datasets
    if not os.path.exists(public_data_individual_path):
        os.mkdir(public_data_individual_path)

    # Public aggregated datasets    
    if not os.path.exists(public_data_assembled_path):
        os.mkdir(public_data_assembled_path)

    if not os.path.exists(public_data_by_country):
        os.mkdir(public_data_by_country)

    if not os.path.exists(private_data_by_country):
        os.mkdir(private_data_by_country)

    # Test Projects paths

    if not os.path.exists(test_data_path):
        os.mkdir(test_data_path)
    if not os.path.exists(test_data_individual_path):
        os.mkdir(test_data_individual_path)



    


        
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #LOOPING THROUGH INDIVIDUAL PROJECTS AND WRITING OUT THE NECESSARY FILES
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    # Create an empty project directory for each individual project
    # Each folder name will be the same as the projectID
    for project in allProjects:
        date=project["rawdata"]["projectSecret"]["dateAvailable"]
        date =date[0:19]
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

        if(datetime.now()>date and project["rawdata"]["projectSecret"]["realOrTestProject"]=="Genuine"):

            public_path_new = os.path.join(public_data_individual_path, project["rawdata"]["projectInfo"]["projectName"])
            os.mkdir(public_path_new)

            private_path_new = os.path.join(private_project_path, project["rawdata"]["projectInfo"]["projectName"])
            os.mkdir(private_path_new)
        
        # Making a folder for test projects
        if(datetime.now()>date and project["rawdata"]["projectSecret"]["realOrTestProject"]=="Test"):

            public_path_new = os.path.join(test_data_individual_path, project["rawdata"]["projectInfo"]["projectName"])
            os.mkdir(public_path_new)

    
    
#--------------------------------------------------------------
#--------------------------------------------------------------
#LOOPING THROUGH INDIVIDUAL PROJECTS AND WRITING OUT THE NECESSARY FILES
#----------------------------     ----------------------------------
#--------------------------------------------------------------

    #project = allProjects[0]
    for project in allProjects:

        date=project["rawdata"]["projectSecret"]["dateAvailable"]
        date =date[0:19]
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

        if(datetime.now()>date and project["rawdata"]["projectSecret"]["realOrTestProject"]=="Genuine"):

            publicfolder = os.path.join(public_data_individual_path, project["rawdata"]["projectInfo"]["projectName"])
            # AgroEco information is only one row, so have to transform
            agroEcoSingleProj = pd.DataFrame(columns=list(agroEcoData.ExtractProjectAgroEcoData(project).keys()))
            agroEcoSingleProj.loc[0]=agroEcoData.ExtractProjectAgroEcoData(project).values()


            contextSingleProj = pd.DataFrame(contextData.projectContextScores(project=project))
            pairwiseSelectionsSingleProj = pairwiseData.pairWiseSelectionsProject(project=project)
            pairwideSummarySingleProj = pairwiseData.pairWiseSummaryScores(project=project)
            participatoryMatrixSingleProj = participatoryMatrixData.participatoryMatrixScoresProject(project=project)
            legumeDataSingleProj = legumeData.extractAllLegumeData(project=project)

            agroEcoSingleProj.to_csv(os.path.join(publicfolder,"agroEcoData.csv"), index=False)
            contextSingleProj.to_csv(os.path.join(publicfolder,"ContextData.csv"), index=False)
            pairwiseSelectionsSingleProj.to_csv(os.path.join(publicfolder,"PairwiseSelections.csv"), index=False)
            pairwideSummarySingleProj.to_csv(os.path.join(publicfolder,"PairwiseSummaryScores.csv"), index=False)
            participatoryMatrixSingleProj.to_csv(os.path.join(publicfolder,"ParticipatoryMatrixScores.csv"), index=False)
            legumeDataSingleProj.to_csv(os.path.join(publicfolder,"LegumeResults.csv"), index=False)

            privatefolder=os.path.join(private_project_path, project["rawdata"]["projectInfo"]["projectName"])
            privatefile =  os.path.join(privatefolder, "rawdata.json")
            with open(privatefile, "w") as outfile:
                JSONData = {
                    "currentProject":project["rawdata"]
                }
                json.dump(JSONData,outfile, indent=4)
            projectDetails = projectProcessing.getProjectDetails(project)
            projectDetails.to_csv(os.path.join(privatefolder,"projectInformation.csv"), index=False)


        if(datetime.now()>date and project["rawdata"]["projectSecret"]["realOrTestProject"]=="Test"):

            testfolder = os.path.join(test_data_individual_path, project["rawdata"]["projectInfo"]["projectName"])
            # AgroEco information is only one row, so have to transform
            agroEcoSingleProj = pd.DataFrame(columns=list(agroEcoData.ExtractProjectAgroEcoData(project).keys()))
            agroEcoSingleProj.loc[0]=agroEcoData.ExtractProjectAgroEcoData(project).values()


            contextSingleProj = pd.DataFrame(contextData.projectContextScores(project=project))
            pairwiseSelectionsSingleProj = pairwiseData.pairWiseSelectionsProject(project=project)
            pairwideSummarySingleProj = pairwiseData.pairWiseSummaryScores(project=project)
            participatoryMatrixSingleProj = participatoryMatrixData.participatoryMatrixScoresProject(project=project)
            legumeDataSingleProj = legumeData.extractAllLegumeData(project=project)

            agroEcoSingleProj.to_csv(os.path.join(testfolder,"agroEcoData.csv"), index=False)
            contextSingleProj.to_csv(os.path.join(testfolder,"ContextData.csv"), index=False)
            pairwiseSelectionsSingleProj.to_csv(os.path.join(testfolder,"PairwiseSelections.csv"), index=False)
            pairwideSummarySingleProj.to_csv(os.path.join(testfolder,"PairwiseSummaryScores.csv"), index=False)
            participatoryMatrixSingleProj.to_csv(os.path.join(testfolder,"ParticipatoryMatrixScores.csv"), index=False)
            legumeDataSingleProj.to_csv(os.path.join(testfolder,"LegumeResults.csv"), index=False)

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    # AGGREGATING ALL OF THE PROJECT INFORMATION FOR LONG CSVs FOR META-ANALYSIS
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    availableProjects = os.listdir(public_data_individual_path)

    publicSheetsToAggregate = ["agroEcoData","ContextData","LegumeResults","PairwiseSelections","PairwiseSummaryScores","ParticipatoryMatrixScores"]

    privateSheetsToAggregate = ["projectInformation"]




    count=0
    for projectID in availableProjects:
        count+=1
        if (count==1):
            publicProjectPath=os.path.join(public_data_individual_path,projectID)

            agroEcoDatadf=pd.read_csv(os.path.join(publicProjectPath,"agroEcoData.csv"))
            ContextDatadf=pd.read_csv(os.path.join(publicProjectPath,"ContextData.csv"))
            LegumeResultsdf=pd.read_csv(os.path.join(publicProjectPath,"LegumeResults.csv"))
            PairwiseSelectionsdf=pd.read_csv(os.path.join(publicProjectPath,"PairwiseSelections.csv"))
            PairwiseSummaryScoresdf=pd.read_csv(os.path.join(publicProjectPath,"PairwiseSummaryScores.csv"))
            ParticipatoryMatrixScoresdf=pd.read_csv(os.path.join(publicProjectPath,"ParticipatoryMatrixScores.csv"))

            privateProjectPath=os.path.join(private_project_path,projectID)
            projectInformationdf=pd.read_csv(os.path.join(privateProjectPath,"projectInformation.csv"))




            # Make first dataframes

        if (count>1):
            # Merge Dataframes together
            publicProjectPath=os.path.join(public_data_individual_path,projectID)

            agroEcoDatadf = agroEcoDatadf.append(pd.read_csv(os.path.join(publicProjectPath,"agroEcoData.csv")), ignore_index=True)
            ContextDatadf = ContextDatadf.append(pd.read_csv(os.path.join(publicProjectPath,"ContextData.csv")), ignore_index=True)
            LegumeResultsdf = LegumeResultsdf.append(pd.read_csv(os.path.join(publicProjectPath,"LegumeResults.csv")), ignore_index=True)
            PairwiseSelectionsdf = PairwiseSelectionsdf.append(pd.read_csv(os.path.join(publicProjectPath,"PairwiseSelections.csv")), ignore_index=True)
            PairwiseSummaryScoresdf = PairwiseSummaryScoresdf.append(pd.read_csv(os.path.join(publicProjectPath,"PairwiseSummaryScores.csv")), ignore_index=True)
            ParticipatoryMatrixScoresdf = ParticipatoryMatrixScoresdf.append(pd.read_csv(os.path.join(publicProjectPath,"ParticipatoryMatrixScores.csv")), ignore_index=True)

            privateProjectPath=os.path.join(private_project_path,projectID)
            projectInformationdf = projectInformationdf.append(pd.read_csv(os.path.join(privateProjectPath,"projectInformation.csv")), ignore_index=True)



    projectInformationdf.to_csv(os.path.join(private_aggregated_path,"projectInformation.csv"), index=False)

    agroEcoDatadf.to_csv(os.path.join(public_data_assembled_path,"agroEcoData.csv"), index=False)
    ContextDatadf.to_csv(os.path.join(public_data_assembled_path,"ContextData.csv"), index=False)
    LegumeResultsdf.to_csv(os.path.join(public_data_assembled_path,"LegumeResults.csv"), index=False)
    PairwiseSelectionsdf.to_csv(os.path.join(public_data_assembled_path,"PairwiseSelections.csv"), index=False)
    PairwiseSummaryScoresdf.to_csv(os.path.join(public_data_assembled_path,"PairwiseSummaryScores.csv"), index=False)
    ParticipatoryMatrixScoresdf.to_csv(os.path.join(public_data_assembled_path,"ParticipatoryMatrixScores.csv"), index=False)


    #--------------------------------------------------------------
    #--------------------------------------------------------------
    # AGGREGATING ALL OF THE PROJECT INFORMATION BY COUNTRY FOR META ANALYSIS
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    public_data_by_country = os.path.join(homepath, "LegumeCHOICE", "ByCountry")
    private_data_by_country = os.path.join(homepath, "AdminLegumeCHOICE", "ByCountry")

    ParticipatoryMatrixScores = pd.read_csv(os.path.join(public_data_assembled_path,"ParticipatoryMatrixScores.csv"))
    allCountries=list(ParticipatoryMatrixScores["country"].unique())
    for country in allCountries:
        public_path_new = os.path.join(public_data_by_country, country)
        os.mkdir(public_path_new)

        private_path_new = os.path.join(private_data_by_country, country)
        os.mkdir(private_path_new)

        
    for country in allCountries:

        agroEcoData=pd.read_csv(os.path.join(public_data_assembled_path,"agroEcoData.csv"))
        ContextData=pd.read_csv(os.path.join(public_data_assembled_path,"ContextData.csv"))
        LegumeResults=pd.read_csv(os.path.join(public_data_assembled_path,"LegumeResults.csv"))
        PairwiseSelections=pd.read_csv(os.path.join(public_data_assembled_path,"PairwiseSelections.csv"))
        PairwiseSummaryScores=pd.read_csv(os.path.join(public_data_assembled_path,"PairwiseSummaryScores.csv"))
        ParticipatoryMatrixScores=pd.read_csv(os.path.join(public_data_assembled_path,"ParticipatoryMatrixScores.csv"))
        projectInformation=pd.read_csv(os.path.join(private_aggregated_path,"projectInformation.csv"))


        agroEcoDataSubset = agroEcoData["country"]==country
        ContextDataSubset = ContextData["country"]==country
        LegumeResultsSubset = LegumeResults["country"]==country
        PairwiseSelectionsSubset = PairwiseSelections["country"]==country
        PairwiseSummaryScoresSubset = PairwiseSummaryScores["country"]==country
        ParticipatoryMatrixScoresSubset = ParticipatoryMatrixScores["country"]==country
        projectInformationSubset = projectInformation["country"]==country

        agroEcoDataSubset = agroEcoData.loc[agroEcoDataSubset,:]
        ContextDataSubset = ContextData.loc[ContextDataSubset,:]
        LegumeResultsSubset = LegumeResults.loc[LegumeResultsSubset,:]
        PairwiseSelectionsSubset = PairwiseSelections.loc[PairwiseSelectionsSubset,:]
        PairwiseSummaryScoresSubset = PairwiseSummaryScores.loc[PairwiseSummaryScoresSubset,:]
        ParticipatoryMatrixScoresSubset = ParticipatoryMatrixScores.loc[ParticipatoryMatrixScoresSubset,:]
        projectInformationSubset = projectInformation.loc[projectInformationSubset,:]



        agroEcoDataSubset.to_csv(os.path.join(public_data_by_country,country,"agroEcoData.csv"), index=False)
        ContextDataSubset.to_csv(os.path.join(public_data_by_country,country,"ContextData.csv"), index=False)
        LegumeResultsSubset.to_csv(os.path.join(public_data_by_country,country,"LegumeResults.csv"), index=False)
        PairwiseSelectionsSubset.to_csv(os.path.join(public_data_by_country,country,"PairwiseSelections.csv"), index=False)
        PairwiseSummaryScoresSubset.to_csv(os.path.join(public_data_by_country,country,"PairwiseSummaryScores.csv"), index=False)
        ParticipatoryMatrixScoresSubset.to_csv(os.path.join(public_data_by_country,country,"ParticipatoryMatrixScores.csv"), index=False)
        projectInformationSubset.to_csv(os.path.join(private_data_by_country,country,"projectInformation.csv"), index=False)

