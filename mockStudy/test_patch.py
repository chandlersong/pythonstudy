import unittest
from unittest import TestCase
from unittest.mock import patch

from mockStudy.entry import OutClass, InnerClass


class TestPatch(TestCase):
    @patch('mockStudy.entry.InnerClass.run')
    def testPatch(self, mock_run_method):
        OutClass().run_inn()
        self.assertTrue(mock_run_method.called)

    def test_with_patch(self):
        with patch.object(InnerClass, 'run', return_value=None) as mock_method:
            OutClass().run_inn()

        mock_method.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
