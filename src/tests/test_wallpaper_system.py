import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.wallpaper_system import WallpaperSystem


class WallpaperSystemTests(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"XDG_CURRENT_DESKTOP": "KDE"}, clear=True):
            self.system = WallpaperSystem()

    def state(self, count=1, current=0, geometry="4096, 1536",
              viewport="2048, 768", dimensions="Width: 1024\nHeight: 768"):
        output = (f"_NET_NUMBER_OF_DESKTOPS(CARDINAL) = {count}\n"
                  f"_NET_CURRENT_DESKTOP(CARDINAL) = {current}\n"
                  f"_NET_DESKTOP_GEOMETRY(CARDINAL) = {geometry}\n"
                  f"_NET_DESKTOP_VIEWPORT(CARDINAL) = {viewport}\n")
        with patch.object(self.system, '_run_output', side_effect=[output, dimensions]):
            return self.system._workspace_state()

    def test_compiz_rows_and_columns(self):
        self.assertEqual(self.state(), (8, 6))

    def test_different_screen_size(self):
        self.assertEqual(self.state(geometry="5760, 1080", viewport="3840, 0",
                                   dimensions="Width: 1920\nHeight: 1080"), (3, 2))

    def test_ordinary_desktops(self):
        self.assertEqual(self.state(count=4, current=2, geometry="1024, 768",
                                   viewport="0, 0, 0, 0, 0, 0, 0, 0"), (4, 2))

    def test_viewports_for_multiple_desktops(self):
        self.assertEqual(self.state(count=2, current=1,
                                   viewport="0, 0, 2048, 768"), (16, 14))

    def test_unavailable_or_malformed_properties(self):
        for output in ("", "_NET_CURRENT_DESKTOP: not found.",
                       "_NET_CURRENT_DESKTOP(CARDINAL) = bad"):
            with self.subTest(output=output), patch.object(self.system, '_run_output', return_value=output):
                self.assertEqual(self.system._workspace_state(), (1, 0))

    def test_invalid_geometry_falls_back(self):
        for geometry in ("0, 0", "100, 768", "1025, 768", "bad"):
            with self.subTest(geometry=geometry):
                self.assertEqual(self.state(geometry=geometry), (1, 0))
        self.assertEqual(self.state(dimensions=""), (1, 0))
        self.assertEqual(self.state(dimensions="Width: 0\nHeight: 0"), (1, 0))
        self.assertEqual(self.state(viewport="99999, 0"), (1, 0))

    def test_kde_and_plasma_detection(self):
        self.assertEqual(self.system.desktop, 'kde')
        with patch.dict(os.environ, {"DESKTOP_SESSION": "plasma"}, clear=True):
            self.assertEqual(WallpaperSystem().desktop, 'kde')

    def test_kde_quotes_filename_and_maps_styles(self):
        filename = '/tmp/a"; bad(); //\\\n café.png'
        for style, fill_mode in [('0', 6), ('1', 0), ('2', 1), ('3', 2), ('4', 3), ('bad', 1)]:
            with self.subTest(style=style), patch('lib.wallpaper_system.subprocess.run') as run:
                self.system.set_wallpaper(filename, style)
                args, kwargs = run.call_args
                command = args[0]
                self.assertEqual(command[:3], ['gdbus', 'call', '--session'])
                self.assertIn('org.kde.PlasmaShell.evaluateScript', command)
                script = command[-1]
                self.assertIn(f'd.writeConfig("Image", {json.dumps(Path(filename).as_uri())});', script)
                self.assertIn(f'd.writeConfig("FillMode", {fill_mode});', script)
                self.assertNotIn(filename, script)
                self.assertTrue(kwargs['check'])
                self.assertFalse(kwargs.get('shell', False))

    def test_kde_errors_are_not_silenced(self):
        with patch('lib.wallpaper_system.subprocess.run', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                self.system.set_wallpaper('/tmp/image.png', '2')

    def test_gnome_backend_preserved(self):
        self.system.desktop = 'gnome'
        with patch.object(self.system, '_run') as run:
            self.system.set_wallpaper('/tmp/image.png', '2')
        self.assertEqual(run.call_count, 3)
        self.assertEqual(run.call_args.args[0][-2:], ['picture-options', 'scaled'])


if __name__ == '__main__':
    unittest.main()
