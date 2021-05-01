import pytest
import os
from ..simulation_1 import *

@pytest.mark.all
def test_sim1_1():
    prob_11()
    assert os.path.exists('./fig1_1.jpg')
    os.system('rm -rf fig1_1.jpg')

@pytest.mark.all
def test_sim1_2():
    prob_12()
    assert os.path.exists('./fig1_2.jpg')
    os.system('rm -rf fig1_2.jpg')

@pytest.mark.all
def test_sim2_1():
    prob_21()
    assert os.path.exists('./fig2_1.jpg')
    os.system('rm -rf fig2_1.jpg')

@pytest.mark.all
def test_sim2_2():
    prob_22()
    assert os.path.exists('./fig2_2.jpg')
    os.system('rm -rf fig2_2.jpg')
