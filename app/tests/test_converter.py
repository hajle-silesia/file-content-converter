import unittest

from app.src.converter import XMLConverter


class TestConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.empty_raw_content = ""
        cls.header_only_raw_content = "<?xml version='1.0' encoding='UTF-8'?>"
        with open("./files/converter.xml", encoding="utf-8") as file:
            cls.nonempty_raw_content = file.read()

    @classmethod
    def set_tested_objects(cls):
        cls.xml_converter = XMLConverter()

    @classmethod
    def set_expected_results(cls):
        cls.expected_empty_content = {}
        cls.expected_nonempty_content = {'note': {'to': "Smith",
                                                  'from': "Adams",
                                                  'heading': "Test",
                                                  'body': "Test body",
                                                  },
                                         }

    def test_Should_GetEmptyContent_When_GivenEmptyRawContent(self):
        self.xml_converter.process(self.empty_raw_content)

        self.assertEqual(self.expected_empty_content, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_GivenHeaderOnlyRawContent(self):
        self.xml_converter.process(self.header_only_raw_content)

        self.assertEqual(self.expected_empty_content, self.xml_converter.content)

    def test_Should_GetNonemptyContent_When_GivenNonemptyRawContent(self):
        self.xml_converter.process(self.nonempty_raw_content)

        self.assertEqual(self.expected_nonempty_content, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_GivenEmptyRawContentBecomesHeaderOnly(self):
        self.xml_converter.process(self.empty_raw_content)
        self.xml_converter.process(self.header_only_raw_content)

        self.assertEqual(self.expected_empty_content, self.xml_converter.content)

    def test_Should_GetNonemptyContent_When_GivenHeaderOnlyRawContentBecomesNonempty(self):
        self.xml_converter.process(self.header_only_raw_content)
        self.xml_converter.process(self.nonempty_raw_content)

        self.assertEqual(self.expected_nonempty_content, self.xml_converter.content)

    def test_Should_GetNonemptyContent_When_GivenEmptyRawContentBecomesNonempty(self):
        self.xml_converter.process(self.empty_raw_content)
        self.xml_converter.process(self.nonempty_raw_content)

        self.assertEqual(self.expected_nonempty_content, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_GivenNonemptyRawContentBecomesHeaderOnly(self):
        self.xml_converter.process(self.nonempty_raw_content)
        self.xml_converter.process(self.header_only_raw_content)

        self.assertEqual(self.expected_empty_content, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_GivenHeaderOnlyRawContentBecomesEmpty(self):
        self.xml_converter.process(self.header_only_raw_content)
        self.xml_converter.process(self.empty_raw_content)

        self.assertEqual(self.expected_empty_content, self.xml_converter.content)

    def test_Should_GetEmptyContent_When_GivenNonemptyRawContentBecomesEmpty(self):
        self.xml_converter.process(self.nonempty_raw_content)
        self.xml_converter.process(self.empty_raw_content)

        self.assertEqual(self.expected_empty_content, self.xml_converter.content)
