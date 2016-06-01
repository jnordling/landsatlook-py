from landsatlook import LandSatLook

def main():

    landsatlook = LandSatLook({
        "url":"http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/",
        "output_directory":"./",
        "image_type":"jpg",
        "bounding_box":{
        "geometry":{
            "xmax":"-12762547.271635106",
            "xmin":"-12868030.370668506",
            "ymax":"4349313.935638487",
            "ymin":"4288011.438953858",
            "spatialReference":{
                "wkid":"102100"
                }
            }
        },
        "image_size":{
            "height":"802",
            "width":"1433"
        },
        "renderingRule":{
            "rasterFunction":"Stretch",
            "rasterFunctionArguments":{
                "StretchType":3,
                "NumberOfStandardDeviations":3,
                "DRA":"true"
            },
            "variableName":"Raster"
        }
    });


if __name__ == '__main__':
    main()
