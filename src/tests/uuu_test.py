import unittest
from unittest.mock import patch
import uuu


# pylint: disable=invalid-name, no-self-use, too-few-public-methods


class _Opts():
    def __init__(self, choco=None, dry_run=None, init_jns=None):
        self.choco = choco
        self.dry_run = dry_run
        self.init_jns = init_jns


class Test_uuu_ValidateCanUpdateChoco(unittest.TestCase):
    
    @patch('jnscommons.jnsos.is_windows')
    @patch('jnscommons.jnsos.is_cygwin')
    def test_does_not_raise_error_when_not_updating_choco(self, m_is_windows, m_is_cygwin):
        m_is_windows.return_value = False
        m_is_cygwin.return_value = False
        
        uuu.validate_can_update_choco(_Opts(choco=False, dry_run=False))
    
    @patch('jnscommons.jnsos.is_windows')
    @patch('jnscommons.jnsos.is_cygwin')
    def test_does_not_raise_error_when_in_windows(self, m_is_windows, m_is_cygwin):
        m_is_windows.return_value = True
        m_is_cygwin.return_value = False
        
        uuu.validate_can_update_choco(_Opts(choco=True, dry_run=False))
    
    @patch('jnscommons.jnsos.is_windows')
    @patch('jnscommons.jnsos.is_cygwin')
    def test_does_not_raise_error_when_in_cygwin(self, m_is_windows, m_is_cygwin):
        m_is_windows.return_value = False
        m_is_cygwin.return_value = True
        
        uuu.validate_can_update_choco(_Opts(choco=True, dry_run=False))
    
    @patch('jnscommons.jnsos.is_windows')
    @patch('jnscommons.jnsos.is_cygwin')
    def test_does_not_raise_error_when_doing_dry_run(self, m_is_windows, m_is_cygwin):
        m_is_windows.return_value = False
        m_is_cygwin.return_value = False
        
        uuu.validate_can_update_choco(_Opts(choco=True, dry_run=True))
    
    @patch('jnscommons.jnsos.is_windows')
    @patch('jnscommons.jnsos.is_cygwin')
    def test_raises_error_when_not_dry_run_and_not_in_valid_os(self, m_is_windows, m_is_cygwin):
        m_is_windows.return_value = False
        m_is_cygwin.return_value = False
        
        with self.assertRaises(uuu.NotChocoOSError):
            uuu.validate_can_update_choco(_Opts(choco=True, dry_run=False))


class Test_uuu_ValidateCanInitJNS(unittest.TestCase):
    
    @patch('jnscommons.jnsos.is_windows')
    def test_does_not_error_when_not_initing(self, m_is_windows):
        m_is_windows.return_value = False
        uuu.validate_can_init_jns(_Opts(init_jns=False, dry_run=False))
    
    @patch('jnscommons.jnsos.is_windows')
    def test_does_not_error_when_doing_dry_run(self, m_is_windows):
        m_is_windows.return_value = False
        uuu.validate_can_init_jns(_Opts(init_jns=True, dry_run=True))
    
    @patch('jnscommons.jnsos.is_windows')
    def test_raises_error_when_in_windows(self, m_is_windows):
        m_is_windows.return_value = True
        
        with self.assertRaises(uuu.NotInitJNSOSError):
            uuu.validate_can_init_jns(_Opts(init_jns=True, dry_run=False))


if __name__ == '__main__':
    unittest.main()
