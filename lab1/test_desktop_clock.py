import unittest
from unittest.mock import patch, MagicMock
import time


class TestDesktopClock(unittest.TestCase):
    @patch('desktop_clock.tk.Tk')
    def test_init_creates_window(self, mock_tk):
        with patch('desktop_clock.tk.Label'):
            from desktop_clock import DesktopClock
            clock = DesktopClock()
            mock_tk.assert_called_once()
            clock.root.title.assert_called_with("桌面时钟")
            clock.root.configure.assert_called_with(bg="#1a1a1a")
            clock.root.attributes.assert_any_call("-topmost", True)
            clock.root.attributes.assert_any_call("-alpha", 0.9)
            clock.root.resizable.assert_called_with(False, False)

    @patch('desktop_clock.tk.Tk')
    @patch('desktop_clock.time.strftime')
    def test_update_time_updates_labels(self, mock_strftime, mock_tk):
        mock_strftime.side_effect = ["14:30:45", "2024-01-15 Monday"]
        mock_label = MagicMock()
        
        with patch('desktop_clock.tk.Label', return_value=mock_label):
            from desktop_clock import DesktopClock
            clock = DesktopClock()
            clock.time_label = mock_label
            clock.date_label = mock_label
            clock.root = MagicMock()
            
            clock.update_time()
            
            mock_label.config.assert_called()
            clock.root.after.assert_called()


if __name__ == "__main__":
    unittest.main()
