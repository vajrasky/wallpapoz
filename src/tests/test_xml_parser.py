import os
import unittest

from os.path import realpath, sep, dirname
from collections import OrderedDict

parentdir = dirname(dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from lib.xml_parser import parse_wallpapoz_file, save_treeview_to_wallpapoz_file

tests_dir = dirname(realpath(__file__))


class WallpapozXmlParsingTests(unittest.TestCase):

    def test_parse_xml_workspaces_type(self):
        test_file = os.path.join(tests_dir, 'wallpapoz_example_workspace_type.xml')

        workspaces, conf = parse_wallpapoz_file(test_file)
        self.assertEqual(workspaces, [
            ('workspace1', ['/home/sky/Pictures/wallpapers/naruto.jpg',
                            '/home/sky/Pictures/wallpapers/bleach.jpg']),
            ('workspace_2', ['/home/sky/Pictures/wallpapers/lands_cape.gif',
                             '/home/sky/Pictures/wallpapers/cameron-highland.gif']),
            ('workspace 3', ['/home/sky/wallpapers with space/paris.jpg',
                             '/home/sky/wallpapers with space/café.jpg']),
            ('workspaceчетири', ['/home/sky/unicode/漢語.png',
                                 '/home/sky/unicode/日本語.png'])
        ])

    def test_parse_xml_desktop_type(self):
        test_file = os.path.join(tests_dir, 'wallpapoz_example_desktop_type.xml')
        files, conf = parse_wallpapoz_file(test_file)
        self.assertEqual(files, ['/home/sky/Pictures/wallpapers/naruto.jpg',
                                 '/home/sky/Pictures/wallpapers/bleach.jpg',
                                 '/home/sky/Pictures/wallpapers/lands_cape.gif',
                                 '/home/sky/Pictures/wallpapers/cameron-highland.gif',
                                 '/home/sky/wallpapers with space/paris.jpg',
                                 '/home/sky/wallpapers with space/café.jpg',
                                 '/home/sky/unicode/漢語.png',
                                 '/home/sky/unicode/日本語.png'])


class WallpapozTreeviewToXmlTests(unittest.TestCase):

    def _check_file(self, file_path, expected_path):
        f = open(file_path)
        try:
            result = f.read().rstrip()
            with open(expected_path) as expected_f:
                expected = expected_f.read().rstrip()
                self.assertEqual(expected, result)
        finally:
            f.close()
            os.remove(file_path)

    def test_save_treeview_to_xml_workspace_type(self):
        expected_path = os.path.join(tests_dir, 'wallpapoz_save_to_xml_workspace_type.xml')
        file_path = os.path.join(tests_dir, 'test_file.xml')
        elements = OrderedDict(sorted({
            'workspace_one': ['one', 'two', 'three'],
            'workspace_two': ['beach', 'mountain', 'sunshine'],
        }.items(), key=lambda t: t[0]))
        save_treeview_to_wallpapoz_file(file_path, "workspace", elements,
                                        interval="5",
                                        random="0",
                                        style="2")
        self._check_file(file_path, expected_path)

    def test_save_treeview_to_xml_desktop_type(self):
        expected_path = os.path.join(tests_dir, 'wallpapoz_save_to_xml_desktop_type.xml')
        file_path = os.path.join(tests_dir, 'test_file.xml')
        elements = ['one', 'two', 'three']
        save_treeview_to_wallpapoz_file(file_path, "desktop", elements,
                                        interval="5",
                                        random="0",
                                        style="2")
        self._check_file(file_path, expected_path)


if __name__ == '__main__':
    unittest.main()
