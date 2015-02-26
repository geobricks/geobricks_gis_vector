import uuid
import os
import subprocess
import fiona
from geobricks_common.core.log import logger
from geobricks_common.core.filesystem import create_tmp_filename, get_filename
import shutil
import time

log = logger(__file__)


def crop_vector_on_vector_bbox_and_postgis(input_path, db_connection_string, query, output_path=None):
    '''
    Crop a shapefile by a postgis layer stored in the database
    :param input_path: input shapefile to crop
    :param db_connection_string: connections string to the database
    :param query: query to the postgis vector layer
    :param output_path: optional output_path to the shapefile
    :return: the path to the cropped shapefile
    '''
    start = time.time()
    # create shp from postgis
    crop_shp_path = create_shp_from_postgis(db_connection_string, query)
    log.info("crop_shp_path: " + crop_shp_path)

    # crop input_path to the bbox of the exported postgis layer
    cropped_by_bbox_path = crop_vector_with_bounding_box(crop_shp_path, input_path)
    log.info("cropped_by_bbox_path: " + cropped_by_bbox_path)

    # crop the produced cropped_by_bbox shp with the crop_shp_path (i.e. GAUL0 'Italy')
    clipped_path = crop_by_vector_by_vector(crop_shp_path, cropped_by_bbox_path, output_path)
    log.info("Final output clipped_path: " + clipped_path)

    # remove temporary folders
    shutil.rmtree(os.path.dirname(crop_shp_path))
    shutil.rmtree(os.path.dirname(cropped_by_bbox_path))

    end = time.time()
    log.info("Time to process:" + str(end - start))
    return clipped_path


def crop_vector_with_bounding_box(input_file_bbox, file_to_crop, output_path=None):
    # ogr2ogr -f "ESRI Shapefile" output.shp input.shp -clipsrc <x_min> <y_min> <x_max> <y_max>
    with fiona.open(input_file_bbox) as c:
        if output_path is None:
            output_path = create_tmp_filename('shp', 'tmp_shp_bbox', 'tmp_shp_bbox_' + str(uuid.uuid4()), False)
            bounds = c.bounds
            # check bounds
            if bounds[0] == 0.0 and bounds[1] == 0.0 and bounds[2] == 0.0 and bounds[3] == 0.0:
                msg = "Shapefile " + input_file_bbox + " has 0 invalide size"
                log.error(msg)
                raise Exception(msg)
            args = [
                'ogr2ogr',
                '-f',
                '"ESRI Shapefile"',
                output_path,
                file_to_crop,
                '-clipsrc',
                str(bounds[0]),
                str(bounds[1]),
                str(bounds[2]),
                str(bounds[3])
            ]
            try:
                cmd = " ".join(args)
                log.info(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                p.wait()
            except Exception, e:
                log.error(e)
                raise Exception(e)
    return output_path


def create_shp_from_postgis(db_connection_string, query, output_path=None):
    '''
    Create a shp from a post
    :param db_connection_string:
    :param query:
    :return:
    '''
    # ogr2ogr -f "ESRI Shapefile" /home/vortex/Desktop/export/afg.shp PG:"host=localhost user=fenix dbname=fenix password=Qwaszx" -sql "select * from spatial.gaul0_2015_4326 where adm0_code IN ('1')"
    # ogr2ogr -f "ESRI Shapefile" output.shp PG:"" -sql "query"
    if output_path is None:
        output_path = create_tmp_filename('shp', 'tmp_shp_postgis', 'tmp_shp_postgis_' + str(uuid.uuid4()), False)
    else:
        # TODO:
        # get the folder by output_path filename
        # check if the folder is created, otherwise create it
        log.warn("TODO: get the folder by output_path filename. check if the folder is created, otherwise create it.")
    args = [
        'ogr2ogr',
        '-f',
        '"ESRI Shapefile"',
        output_path,
        db_connection_string,
        "-sql",
        "\"" + query + "\""
    ]
    try:
        cmd = " ".join(args)
        log.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
    except Exception, e:
        log.error(e)
        raise Exception(e)
    return output_path


def crop_by_vector_by_vector(crop_shp_path, input_path, output_path=None):
    # ogr2ogr -skipfailures -clipsrc afg.shp output.shp G2014_2013_1_mid.shp
    if output_path is None:
        output_path = create_tmp_filename('shp', 'tmp_shp', 'tmp_shp_' + str(uuid.uuid4()), False)
    else:
        # TODO:
        # get the folder by output_path filename
        # check if the folder is created, otherwise create it
        log.warn("TODO: get the folder by output_path filename. check if the folder is created, otherwise create it.")
    args = [
        'ogr2ogr',
        '-skipfailures',
        '-clipsrc',
        crop_shp_path,
        output_path,
        input_path,
    ]
    try:
        cmd = " ".join(args)
        log.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
    except Exception, e:
        log.error(e)
        raise Exception(e)
    return output_path


# input_path = '/home/vortex/Desktop/export/G2014_2013_1_mid.shp'
#input_path = '/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/GEZ2010/gez_2010_wgs84.shp'
# path = crop_vector_on_vector_bbox_and_postgis(input_path, '"PG:host=localhost dbname=fenix user=fenix password=Qwaszx"', "select * from spatial.gaul0_2015_4326 where adm0_name IN ('Brazil')")
#path = crop_vector_on_vector_bbox_and_postgis(input_path, '"PG:host=localhost dbname=fenix user=fenix password=Qwaszx"', "select * from spatial.gaul0_faostat_4326 where areanamee IN ('Malta')")
#print "Output Path: ", path