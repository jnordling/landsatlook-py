import requests
import json
import urllib
import sys, os
from PIL import Image, ImageSequence

image_size ="1433%2C802"
bbox_string = "3461001.7800615956,3494786.1779246037,3515768.9108278505,3525437.4262669184".replace(",","%2C")

# bounding_box_object = {
# "geometry":{
#     "xmin":3461001.7800615956,
#     "ymin":3494786.1779246037,
#     "xmax":3515768.9108278505,
#     "ymax":3525437.4262669184,
#     "spatialReference":{"wkid":102100}
#     }
# }

bounding_box_object = {
"geometry":{
    "xmin":3461001.7800615956,
    "ymin":3494786.1779246037,
    "xmax":3515768.9108278505,
    "ymax":3525437.4262669184,
    "spatialReference":{"wkid":102100}
    }
}
# bbox_string = "3461001.7800615956,3494786.1779246037,3515768.9108278505,3525437.4262669184".replace(",","%2C")
bbox_string = [bounding_box_object["geometry"]["xmin"],
    bounding_box_object["geometry"]["ymin"],bounding_box_object["geometry"]["xmax"],
    bounding_box_object["geometry"]["ymax"]]
# def makeGif():
    # filename = sys.argv[1]
    # im = Image.open(filename)
    # original_duration = im.info['duration']
    # frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
    # frames.reverse()
    #
    # from images2gif import writeGif
    # writeGif("reverse_" + os.path.basename(filename), frames, duration=original_duration/1000.0, dither=0)

def get_object_ids(url):
    object_id_request = requests.get(url)
    if object_id_request.status_code == 200:
        data = json.loads(object_id_request.text)
        for obj in data["features"]:
            download_image(obj)

def download_image(obj):
    obj_id = str(obj["attributes"]["OBJECTID"])
    month = str(obj["attributes"]["month"])
    year = str(obj["attributes"]["year"])
    day_of_year = str(obj["attributes"]["dayOfYear"])
    url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/exportImage?bbox="+bbox_string+"&bboxSR=102100&size=1433%2C802&imageSR=102100&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=%7B%22mosaicMethod%22%3A%22esriMosaicLockRaster%22%2C%22ascending%22%3Atrue%2C%22lockRasterIds%22%3A%5B"+obj_id+"%5D%2C%22mosaicOperation%22%3A%22MT_FIRST%22%7D&renderingRule=%7B%22rasterFunction%22%3A%22Stretch%22%2C%22rasterFunctionArguments%22%3A%7B%22StretchType%22%3A3%2C%22NumberOfStandardDeviations%22%3A3%2C%22DRA%22%3Atrue%7D%2C%22variableName%22%3A%22Raster%22%7D&f=image"
    # url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/exportImage?f=image&format=jpg&renderingRule=%7B%22rasterFunction%22%3A%22Stretch%22%2C%22rasterFunctionArguments%22%3A%7B%22StretchType%22%3A6%2C%22MinPercent%22%3A0.5%2C%22MaxPercent%22%3A0.5%2C%22DRA%22%3Atrue%7D%2C%22variableName%22%3A%22Raster%22%7D&mosaicRule=%7B%22mosaicMethod%22%3A%22esriMosaicLockRaster%22%2C%22ascending%22%3Atrue%2C%22lockRasterIds%22%3A%5B"+obj_id+"%5D%2C%22mosaicOperation%22%3A%22MT_FIRST%22%7D&bbox="+bbox_string+"&imageSR=102100&bboxSR=102100&size="+image_size
    print url
    image_request = requests.get(url)
    with open(year+"_"+day_of_year+'.jpg', 'wb') as image:
        image.write(image_request.content)


def main():
    extent = urllib.urlencode(bounding_box_object)
    object_id_url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/query?f=json&where=(acquisitionDate%20%3E%3D%20date%271972-01-01%27%20AND%20%20acquisitionDate%20%3C%3D%20date%272013-12-31%27)%20AND%20(dayOfYear%20%3E%3D1%20AND%20%20dayOfYear%20%3C%3D%20366)%20AND%20(sensor%20%3D%20%27MSS%27)%20AND%20(cloudCover%20%3C%3D%2020)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&"+extent+"&geometryType=esriGeometryEnvelope&inSR=102100&outFields=sceneID%2Csensor%2CacquisitionDate%2CdateUpdated%2Cpath%2Crow%2CPR%2CcloudCover%2CsunElevation%2CsunAzimuth%2CreceivingStation%2CsceneStartTime%2Cmonth%2Cyear%2COBJECTID%2CdayOfYear%2CdayOrNight%2CbrowseURL&orderByFields=dayOfYear&outSR=102100"
    # object_id_url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/query?f=json&where=(acquisitionDate%20%3E%3D%20date%271982-01-01%27%20AND%20%20acquisitionDate%20%3C%3D%20date%272011-12-31%27)%20AND%20(dayOfYear%20%3E%3D1%20AND%20%20dayOfYear%20%3C%3D%20366)%20AND%20(sensor%20%3D%20%27TM%27)%20AND%20(cloudCover%20%3C%3D%2020)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&"+extent+"&geometryType=esriGeometryEnvelope&inSR=102100&outFields=sceneID%2Csensor%2CacquisitionDate%2CdateUpdated%2Cpath%2Crow%2CPR%2CcloudCover%2CsunElevation%2CsunAzimuth%2CreceivingStation%2CsceneStartTime%2Cmonth%2Cyear%2COBJECTID%2CdayOfYear%2CdayOrNight%2CbrowseURL&orderByFields=dayOfYear&outSR=102100"
    #object_id_url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/query?f=json&where=(acquisitionDate%20%3E%3D%20date%272013-01-01%27%20AND%20%20acquisitionDate%20%3C%3D%20date%272016-12-31%27)%20AND%20(dayOfYear%20%3E%3D1%20AND%20%20dayOfYear%20%3C%3D%20366)%20AND%20(sensor%20%3D%20%27OLI%27)%20AND%20(cloudCover%20%3C%3D%2020)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&"+extent+"&geometryType=esriGeometryEnvelope&inSR=102100&outFields=sceneID%2Csensor%2CacquisitionDate%2CdateUpdated%2Cpath%2Crow%2CPR%2CcloudCover%2CsunElevation%2CsunAzimuth%2CreceivingStation%2CsceneStartTime%2Cmonth%2Cyear%2COBJECTID%2CdayOfYear%2CdayOrNight%2CbrowseURL&orderByFields=dayOfYear&outSR=102100"
    print object_id_url
    #object_id_url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/query?f=json&where=(acquisitionDate%20%3E%3D%20date%272003-01-01%27%20AND%20%20acquisitionDate%20%3C%3D%20date%272016-12-31%27)%20AND%20(dayOfYear%20%3E%3D1%20AND%20%20dayOfYear%20%3C%3D%20366)%20AND%20(sensor%20%3D%20%27ETM_SLC_OFF%27)%20AND%20(cloudCover%20%3C%3D%2020)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&"+extent+"&geometryType=esriGeometryEnvelope&inSR=102100&outFields=sceneID%2Csensor%2CacquisitionDate%2CdateUpdated%2Cpath%2Crow%2CPR%2CcloudCover%2CsunElevation%2CsunAzimuth%2CreceivingStation%2CsceneStartTime%2Cmonth%2Cyear%2COBJECTID%2CdayOfYear%2CdayOrNight%2CbrowseURL&orderByFields=dayOfYear&outSR=102100"
    get_object_ids(object_id_url)


if __name__ == '__main__':
    main()
