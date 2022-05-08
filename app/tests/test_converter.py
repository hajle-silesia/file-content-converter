import unittest

from app.src.converter import XMLConverter


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.set_test_arguments()
        self.set_tested_objects()
        self.set_test_expected_results()

    def set_test_arguments(self):
        pass

    def set_tested_objects(self):
        self.xml_converter = XMLConverter()

    def set_test_expected_results(self):
        pass

    def test_Should_GetEmptyContent_When_RawContentIsEmpty(self):
        raw_content = ""
        self.xml_converter.process(raw_content)

        self.assertEqual({}, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_RawContentHasOnlyHeader(self):
        raw_content = "<?xml version='1.0' encoding='UTF-8'?>"
        self.xml_converter.process(raw_content)

        self.assertEqual({}, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_RawContentIsNotEmpty(self):
        expected_content = {'note': {'to': "Smith",
                                     'from': "Adams",
                                     'heading': "Test",
                                     'body': "Test body",
                                     },
                            }

        with open("./files/converter.xml", encoding="utf-8") as file:
            raw_content = file.read()
        self.xml_converter.process(raw_content)

        self.assertEqual(expected_content, self.xml_converter.content)
