import unittest


def testDrawingGeometry(feature_manager, scenario):
    class TestDrawingGeometry(unittest.TestCase):

        def test_class_can_draw_in_XY_plane(self):
            self.assertEqual(feature_manager.view_space.view_plane, 'XY')
            # feature_manager.work_piece.didUpdateQueries()
            for feature in feature_manager.features:
                feature.didUpdateQueries()
            feature_manager.reDrawAll()
            self.testDrawnEntities(scenario, 'XY')

        def test_class_can_draw_in_YZ_plane(self):
            feature_manager.view_space.view_plane = 'YZ'
            feature_manager.changeViewPlane()
            self.testDrawnEntities(scenario, 'YZ')

        def test_class_can_draw_in_XZ_plane(self):
            feature_manager.view_space.view_plane = 'XZ'
            feature_manager.changeViewPlane()
            self.testDrawnEntities(scenario, 'XZ')


        def testDrawnEntities(self, scenario, plane):
            if 'benchmark' in scenario.keys():
                if 'num_drawn_entities' in scenario['benchmark'].keys():
                    entities = feature_manager.view_space.canvas.find_all()
                    for key in scenario['benchmark']['num_drawn_entities'][plane].keys():
                        actual = entities.count(key)
                        expected = scenario['benchmark']['num_drawn_entities'][plane][key]
                        self.assertEqual(
                            actual,
                            expected,
                            'Bad number of entities for %s %s, actual %i vs expected %i' % (plane, key, actual, expected)
                        )



    suite = unittest.TestSuite()
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_XY_plane"))
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_YZ_plane"))
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_XZ_plane"))

    unittest.TextTestRunner().run(suite)
