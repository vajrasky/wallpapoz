from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import daemon_wallpapoz_py3 as daemon


class StopLoop(Exception):
    pass


class DaemonTests(unittest.TestCase):
    def simulate(self, workspaces, times, files=None, random=False):
        system = Mock()
        system.current_workspace.side_effect = [*workspaces, StopLoop()]
        files = files if files is not None else [('one', ['a', 'b']), ('two', ['c', 'd'])]
        with patch.object(daemon, 'existing_files', side_effect=lambda f: f), \
                patch.object(daemon.time, 'monotonic', side_effect=times), \
                patch.object(daemon.time, 'sleep'), \
                patch.object(daemon.random, 'randrange', side_effect=[0, 1, 1]) as choose:
            with self.assertRaises(StopLoop):
                daemon.run_workspace_mode(system, files, '2', 10, random)
        return [call.args[0] for call in system.set_wallpaper.call_args_list], choose.call_count

    def test_return_before_deadline_restores_same_image(self):
        self.assertEqual(self.simulate([0, 1, 0], [0, 1, 2])[0], ['a', 'c', 'a'])

    def test_switch_does_not_reset_deadline(self):
        self.assertEqual(self.simulate([0, 1, 0, 0], [0, 1, 2, 10])[0], ['a', 'c', 'a', 'b'])

    def test_return_after_deadline_advances(self):
        self.assertEqual(self.simulate([0, 1, 0], [0, 1, 12])[0], ['a', 'c', 'b'])

    def test_independent_workspace_timers(self):
        self.assertEqual(self.simulate([0, 1, 0, 1, 1], [0, 5, 10, 11, 15])[0],
                         ['a', 'c', 'b', 'c', 'd'])

    def test_random_choice_preserved_on_return(self):
        applied, choices = self.simulate([0, 1, 0], [0, 1, 2], random=True)
        self.assertEqual(applied, ['a', 'd', 'a'])
        self.assertEqual(choices, 2)

    def test_empty_workspace_and_out_of_range(self):
        self.assertEqual(self.simulate([0, 1, 0, 9, 0, -1, 0], [0, 1, 2, 3, 4],
                                      files=[('one', ['a']), ('empty', [])])[0],
                         ['a', 'a', 'a', 'a'])

    def test_no_usable_wallpapers(self):
        with patch.object(daemon, 'existing_files', return_value=[]):
            self.assertEqual(daemon.run_workspace_mode(Mock(), [('empty', [])], '2', 10, False), 1)

    def test_desktop_mode_still_rotates(self):
        system = Mock()
        with patch.object(daemon, 'existing_files', return_value=['a', 'b']), \
                patch.object(daemon.time, 'sleep', side_effect=[None, StopLoop()]):
            with self.assertRaises(StopLoop):
                daemon.run_desktop_mode(system, ['a', 'b'], '2', 10, False)
        self.assertEqual([call.args[0] for call in system.set_wallpaper.call_args_list], ['a', 'b'])


if __name__ == '__main__':
    unittest.main()
