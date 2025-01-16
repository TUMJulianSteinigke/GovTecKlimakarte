# service_account = 'dashboardwebsite@govtecklimakarte.iam.gserviceaccount.com'
# import ee
# credentials = ee.ServiceAccountCredentials(service_account, '.private-key.json')
# ee.Initialize(credentials)
#
#
#
# # Define Parameters
# shape_id = 'DEU-ADM3-1590546715-B5479'  # Shape ID for Munich
# borders = ee.FeatureCollection('projects/sat-io/open-datasets/geoboundaries/HPSCGS-ADM3')
# boundary = borders.filter(ee.Filter.eq('shapeID', shape_id)).geometry()
#
# # Area of Interest (AOI)
# aoi = boundary
#
# # Time Range
# start_date = '2024-07-01'
# end_date = '2024-08-31'
#
# # -------------------------
# # Helper Functions
# # -------------------------
# def apply_scale_factors(image):
#     """Applies scaling factors to Landsat 8 data."""
#     optical_bands = image.select('SR_B.*').multiply(0.0000275).add(-0.2)
#     thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
#     return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)
#
# def mask_l8sr(image):
#     """Applies cloud masking to Landsat 8 data."""
#     cloud_shadow_bitmask = (1 << 3)
#     clouds_bitmask = (1 << 5)
#     qa = image.select('QA_PIXEL')
#     mask = qa.bitwiseAnd(cloud_shadow_bitmask).eq(0).And(qa.bitwiseAnd(clouds_bitmask).eq(0))
#     return image.updateMask(mask)
#
#
# # Image Collection Processing
# landsat_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')\
#     .filterDate(start_date, end_date)\
#     .filterBounds(aoi)\
#     .map(apply_scale_factors)\
#     .map(mask_l8sr)\
#     .median()
#
# # Clip the image to the boundary
# landsat_clipped = landsat_collection.clip(boundary)
#
# # -------------------------
# # Visualization Parameters
# # -------------------------
# true_color_vis = {
#     'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
#     'min': 0.0,
#     'max': 0.3,
# }
# ndvi_vis = {
#     'min': -1,
#     'max': 1,
#     'palette': ['blue', 'white', 'green'],
# }
# lst_vis = {
#     'min': 7,
#     'max': 50,
#     'palette': [
#         '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
#         '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
#         '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
#         'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
#         'ff0000', 'de0101', 'c21301', 'a71001', '911003'
#     ]
# }
#
# # -------------------------
# # NDVI Calculation
# # -------------------------
# ndvi = landsat_clipped.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
#
# # NDVI Statistics
# ndvi_stats = ndvi.reduceRegion(
#     reducer=ee.Reducer.minMax(),
#     geometry=aoi,
#     scale=30,
#     maxPixels=1e9
# )
# ndvi_min = ee.Number(ndvi_stats.get('NDVI_min'))
# ndvi_max = ee.Number(ndvi_stats.get('NDVI_max'))
#
# # Fraction of Vegetation (FV)
# fv = ndvi.subtract(ndvi_min).divide(ndvi_max.subtract(ndvi_min)).pow(2).rename('FV')
#
# # Emissivity Calculation (EM)
# em = fv.multiply(0.004).add(0.986).rename('EM')
#
# # -------------------------
# # LST Calculation
# # -------------------------
# thermal_band = landsat_clipped.select('ST_B10').rename('Thermal')
# lst = thermal_band.expression(
#     'tb / (1 + ((11.5 * (tb / 14380)) * log(em))) - 273.15',
#     {
#         'tb': thermal_band.select('Thermal'),  # Brightness temperature in Kelvin
#         'em': em                              # Emissivity
#     }
# ).rename('LST')
#
# # Step 1: Calculate the 90th Percentile (Top 10% Threshold)
# lst_threshold = ee.Number(lst.reduceRegion(
#     reducer=ee.Reducer.percentile([90]),  # Calculate 90th percentile
#     geometry=aoi,
#     scale=30,
#     maxPixels=1e9
# ).get('LST'))
#
# # Step 2: Convert the Threshold to an Image
# lst_threshold_image = ee.Image.constant(lst_threshold)
#
# # Step 3: Mask Areas Below the Threshold
# lst_uhi_masked = lst.updateMask(lst.gte(lst_threshold_image))
#
# # Step 4: Visualization Parameters for UHIs
# uhi_vis = {
#     'min': 35,  # Adjust based on your expected LST range
#     'max': 55,
#     'palette': ['yellow', 'orange', 'red'],  # Highlight UHIs with a gradient
# }

# args = {"toolbar_ctrl":False}
# m = geemap.Map(**args)
# m.setOptions(styles={'minZoom':6, 'maxZoom':9})
#
#
# m.addLayer(lst_uhi_masked, uhi_vis, "Top 10% LST - Urban Heat Islands")
# boundary = ee.FeatureCollection(ee.Feature(boundary))
#
# m.addLayer(boundary.style(fillColor='00000000') )
# m.setLocked(True,1,1)
# m.centerObject(aoi, 12)
# m.to_streamlit(height=700)
