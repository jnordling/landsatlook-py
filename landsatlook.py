class LandSatLook(object):
    """docstring for LandSatLook"""
    def __init__(self, arg):
        super(LandSatLook, self).__init__()
        self.arg = arg
        self.bounding_box = []
        self.where_query = None
        self.rasterFunction = None
        self.fields = None
        self.service_url = None
        self.object_ids = None
        self.output_directory = None

    def main():
        # Start of the program
        # Make sure all fields needed are valid and sunElevation
        if self.bounding_box == None:
            return None
        if self.where_query == None:
            return None
        if self.rasterFunction == None:
            return None
        if self.fields == None:
            return None
        if service_url == None:
            return None
        if object_ids == None:
            return None

        # Get ObjectID's

    # Util function to make requests and turn back JSON Object
    def _make_request(url,parms):
        request = requests.get(url)
        data = None
        if request.status_code == 200:
            data = json.loads(request.text)
        return data

    def get_object_ids(url):
        data = _make_request(url)
        for obj in data["features"]:
            download_image(obj)

    def download_image(obj):
        obj_id = str(obj["attributes"]["OBJECTID"])
        month = str(obj["attributes"]["month"])
        year = str(obj["attributes"]["year"])
        day_of_year = str(obj["attributes"]["dayOfYear"])
        url = "http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/exportImage?bbox="+bbox_string+"&bboxSR=102100&size=1433%2C802&imageSR=102100&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=%7B%22mosaicMethod%22%3A%22esriMosaicLockRaster%22%2C%22ascending%22%3Atrue%2C%22lockRasterIds%22%3A%5B"+obj_id+"%5D%2C%22mosaicOperation%22%3A%22MT_FIRST%22%7D&renderingRule=%7B%22rasterFunction%22%3A%22Stretch%22%2C%22rasterFunctionArguments%22%3A%7B%22StretchType%22%3A3%2C%22NumberOfStandardDeviations%22%3A3%2C%22DRA%22%3Atrue%7D%2C%22variableName%22%3A%22Raster%22%7D&f=image"
        image_request = requests.get(url)
        with open(year+"_"+day_of_year+'.jpg', 'wb') as image:
            image.write(image_request.content)
