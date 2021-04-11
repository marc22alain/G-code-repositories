import unittest
from option_queries import *


def testDrawingGeometry(feature_manager, scenario):
    class TestDrawingGeometry(unittest.TestCase):

        def test_class_can_draw_in_XY_plane(self):
            self.executePreInstructions(feature_manager, 'XY')
            self.assertEqual(feature_manager.view_space.view_plane, 'XY')
            feature_manager.work_piece.drawGeometry()
            for feature in feature_manager.features:
                feature.didUpdateQueries()
            feature_manager.reDrawAll()
            self.executePostInstructions(feature_manager, 'XY')
            self.testDrawnEntities(scenario, 'XY')

        def test_class_can_draw_in_YZ_plane(self):
            self.executePreInstructions(feature_manager, 'YZ')
            feature_manager.view_space.view_plane = 'YZ'
            feature_manager.changeViewPlane()
            self.executePostInstructions(feature_manager, 'YZ')
            self.testDrawnEntities(scenario, 'YZ')

        def test_class_can_draw_in_XZ_plane(self):
            self.executePreInstructions(feature_manager, 'XZ')
            feature_manager.view_space.view_plane = 'XZ'
            feature_manager.changeViewPlane()
            self.executePostInstructions(feature_manager, 'XZ')
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

        def executePreInstructions(self, feature_manager, plane):
            if 'test-drawing-pre-instructions' in scenario.keys():
                if plane in scenario['test-drawing-pre-instructions'].keys():
                    for instruction in scenario['test-drawing-pre-instructions'][plane]:
                        eval(instruction)

        def executePostInstructions(self, feature_manager, plane):
            if 'test-drawing-post-instructions' in scenario.keys():
                if plane in scenario['test-drawing-post-instructions'].keys():
                    for instruction in scenario['test-drawing-post-instructions'][plane]:
                        eval(instruction)


    suite = unittest.TestSuite()
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_XY_plane"))
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_YZ_plane"))
    suite.addTest(TestDrawingGeometry("test_class_can_draw_in_XZ_plane"))

    unittest.TextTestRunner().run(suite)
