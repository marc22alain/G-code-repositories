import unittest


def testDrawingGeometry(feature_manager):
    class TestDrawingGeometry(unittest.TestCase):

        def test_class_can_draw_in_XY_plane(self):
            for feature in feature_manager.features:
                feature.didUpdateQueries()
            feature_manager.reDrawAll()

        def test_class_can_draw_in_YZ_plane(self):
            feature_manager.view_space.view_plane = 'YZ'
            feature_manager.changeViewPlane()

        def test_class_can_draw_in_XZ_plane(self):
            feature_manager.view_space.view_plane = 'XZ'
            feature_manager.changeViewPlane()



    suite = unittest.TestSuite()
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_XY_plane"))
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_YZ_plane"))
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_XZ_plane"))

    unittest.TextTestRunner().run(suite)
