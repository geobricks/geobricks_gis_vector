import unittest
import os
import shutil
from geobricks_common.core.log import logger
from geobricks_gis_vector.core.vector import crop_shp_by_shp

log = logger(__file__)

class GeobricksTest(unittest.TestCase):

    def test_crop_by_vector_by_vector(self):
        # file that has to be cropped (i.e. cut the gaul1 (italy + malta) on malta in this case)
        crop_shp_path = 'data/storage/vector/gaul1_italy_malta_4326/gaul1_italy_malta_4326.shp'
        # input file used to crop the crop_shp_path file
        input_path = 'data/storage/vector/gaul0_malta_4326/gaul0_malta_4326.shp'
        crop_shp_path = os.path.normpath(os.path.join(os.path.dirname(__file__), crop_shp_path))
        input_path = os.path.normpath(os.path.join(os.path.dirname(__file__), input_path))
        output_path = crop_shp_by_shp(crop_shp_path, input_path)
        self.assertEqual(os.path.isfile(output_path), True)
        # removing produced output
        shutil.rmtree(os.path.dirname(output_path))


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()


