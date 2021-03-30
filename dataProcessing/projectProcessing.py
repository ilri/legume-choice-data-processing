import pandas as pd
from datetime import datetime

def getProjectDetails(project):
    project["rawdata"]["projectInfo"]

    date=project["rawdata"]["projectSecret"]["dateAvailable"]
    date =date[0:19]
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    projectData={
    "projectName":[project["rawdata"]["projectInfo"]["projectName"]],
    "projectID":[project["rawdata"]["projectInfo"]["projectID"]],
    "firstname":[project["rawdata"]["projectInfo"]["user"]["firstname"]],
    "surname":[project["rawdata"]["projectInfo"]["user"]["surname"]],
    "email":[project["rawdata"]["projectInfo"]["user"]["email"]],
    "institution":[project["rawdata"]["projectInfo"]["user"]["institution"]],

    "locationAll":[project["rawdata"]["location"]],
    "PolygonPoint1Lat":[project["rawdata"]["location"][0]["lat"]],
    "PolygonPoint1Lon":[project["rawdata"]["location"][0]["lng"]],
    "PolygonPoint2Lat":[project["rawdata"]["location"][1]["lat"]],
    "PolygonPoint2Lon":[project["rawdata"]["location"][1]["lng"]],
    "PolygonPoint3Lat":[project["rawdata"]["location"][2]["lat"]],
    "PolygonPoint3Lon":[project["rawdata"]["location"][2]["lng"]],
    "PolygonPoint4Lat":[project["rawdata"]["location"][3]["lat"]],
    "PolygonPoint4Lon":[project["rawdata"]["location"][3]["lng"]],

    "country":[project["rawdata"]["projectInfo"]["country"]],
    "majorRegion":[project["rawdata"]["projectInfo"]["majorRegion"]],
    "minorRegion":[project["rawdata"]["projectInfo"]["minorRegion"]],
    "communityName":[project["rawdata"]["projectInfo"]["communityName"]],
    "communityType":[project["rawdata"]["projectInfo"]["communityType"]],
    "description":[project["rawdata"]["projectInfo"]["description"]],
    "date":[project["rawdata"]["projectSecret"]["dateAvailable"]],

    "year":[date.year],
    "month":[date.month],
    "day":[date.day],
    "dateTime":[date.isoformat()]
    }

    return pd.DataFrame(projectData)

    