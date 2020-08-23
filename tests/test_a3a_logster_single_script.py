import sys
sys.path.insert(0, 'D:/Dropbox/hobby/Modding/Programs/Github/My_Repos/A3A_Logster_repo/A3A_Logster')
import configparser
from helper_functions import config_value_as_list
import pytest


def config_value_as_list_test():
    CONFIG_LOC = 'D:/Dropbox/hobby/Modding/Programs/Github/My_Repos/A3A_Logster_repo/tests/sample_config.ini'
    CFG = configparser.ConfigParser(delimiters='|', allow_no_value=True)
    CFG.read(CONFIG_LOC)
    assert config_value_as_list(CFG, 'test', 'no_spaces_good') == ['a', 'b', 'c', 'd', 'e', 'f']
    assert config_value_as_list(CFG, 'test', 'spaces_good') == ['a', 'b', 'c', 'd', 'e', 'f']
    assert config_value_as_list(CFG, 'test', 'spaces_trailing_comma_good') == ['a', 'b', 'c', 'd', 'e', 'f']
    assert config_value_as_list(CFG, 'test', 'spaces_leading_comma_good') == ['a', 'b', 'c', 'd', 'e', 'f']
    assert config_value_as_list(CFG, 'test', 'spaces_leading_and_trailing_comma_good') == ['a', 'b', 'c', 'd', 'e', 'f']
