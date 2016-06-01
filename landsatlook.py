from progress.bar import Bar
import requests
import json
import urllib
import os
import sys, os



class LandSatLook(object):
    """docstring for LandSatLook"""
    def __init__(self, arg):
        super(LandSatLook, self).__init__()
        self.arg = arg
        for i in self.arg:
            self.validateField(i)
        # Init defaule parms
        self.bounding_box = self.arg["bounding_box"]
        self.url = self.arg["url"]
        self.output_directory = self.arg["output_directory"]
        if not os.path.exists(self.output_directory):
            print "Error: Output path needs to be valid"
            return
        self.image_type = self.arg["image_type"]
        self.image_size = self.arg["image_size"]
        self.renderingRule = self.arg["renderingRule"]
        self.image_objects = self.set_image_objects()
        bar = Bar('Downloading Images:', max=len(self.image_objects))
        for image in self.image_objects:
            bar.next()
            self.download_image(image)
        bar.finish()


    def validateField(self,field):
        if not self.arg[field]:
            print "Error: LandSatLook needs valid `"+field+"`"
            return


    # Util function to make requests and turn back JSON Object
    def _query(self,parms):
        # url = self.url+"query?"+urllib.urlencode(parms)
        request = requests.get(self.url+"query?"+urllib.urlencode(parms))
        data = None
        if request.status_code == 200:
            data = json.loads(request.text)
        return data

    def set_image_objects(self):
        landsat8 = "(acquisitionDate >= date'2013-01-01' AND acquisitionDate <= date'2016-12-31') AND (dayOfYear >=1 AND dayOfYear <= 366) AND (sensor = 'OLI') AND (cloudCover <= 20)"
        landsat7 = "(acquisitionDate >= date'2003-01-01' AND acquisitionDate <= date'2016-12-31') AND (dayOfYear >=1 AND dayOfYear <= 366) AND (sensor = 'ETM_SLC_OFF') AND (cloudCover <= 20)"
        landsat4_5 = "(acquisitionDate >= date'1982-01-01' AND acquisitionDate <= date'2011-12-31') AND (dayOfYear >=1 AND dayOfYear <= 366) AND (sensor = 'TM') AND (cloudCover <= 20)"
        landsat1_5 = "(acquisitionDate >= date'1972-01-01' AND acquisitionDate <= date'2013-12-31') AND (dayOfYear >=1 AND dayOfYear <= 366) AND (sensor = 'MSS') AND (cloudCover <= 20)"
        queries_name = ["landsat8","landsat7","landsat4_5","landsat1_5"]
        queries = [landsat8,landsat7,landsat4_5,landsat1_5]
        # query = self._query(parms)
        obj = []
        count = 0
        for q in queries:
            parms = {
                "f":"json",
                "where":q,
                "geometry":self.bounding_box["geometry"],
                "returnGeometry":"false",
                "spatialRel":"esriSpatialRelIntersects",
                "geometryType":"esriGeometryEnvelope",
                "inSR":self.bounding_box["geometry"]["spatialReference"]["wkid"],
                "outSR":self.bounding_box["geometry"]["spatialReference"]["wkid"],
                "outFields":"*",
                "orderByFields":"dayOfYear"
            }
            query = self._query(parms)
            bar = Bar("Requesting data: "+queries_name[count] , max=len(queries))
            for i in query["features"]:
                obj.append(i)
                bar.next()
            bar.finish()
            count = count + 1
        return obj

    def download_image(self,obj):
        obj_id = str(obj["attributes"]["OBJECTID"])
        month = str(obj["attributes"]["month"])
        year = str(obj["attributes"]["year"])
        day_of_year = str(obj["attributes"]["dayOfYear"])

        parms = {
            "bbox":",".join([self.bounding_box["geometry"]["xmin"],self.bounding_box["geometry"]["ymin"],self.bounding_box["geometry"]["xmax"],self.bounding_box["geometry"]["ymax"]]),
            "bboxSR":self.bounding_box["geometry"]["spatialReference"]["wkid"],
            "size":",".join([self.image_size["width"],self.image_size["height"]]),
            "imageSR":self.bounding_box["geometry"]["spatialReference"]["wkid"],
            "format":self.image_type,
            "pixelType":"U8",
            "noDataInterpretation":"esriNoDataMatchAny",
            "interpolation":"+RSP_BilinearInterpolation",
            "mosaicRule":{
                "mosaicMethod":"esriMosaicLockRaster",
                "ascending":"true",
                "lockRasterIds":[obj_id],
                "mosaicOperation":"MT_FIRST"
            },
            "renderingRule":self.renderingRule,
            "f":"image"
        }
        # print self.url+"exportImage?"+urllib.urlencode(parms)
        image_request = requests.get(self.url+"exportImage?"+urllib.urlencode(parms))
        image_name = "-".join([year,day_of_year])+ "." + self.image_type
        with open(os.path.join(self.output_directory,image_name), 'w+') as image:
            image.write(image_request.content)
