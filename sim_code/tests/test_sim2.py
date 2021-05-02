import pytest
import os
from .. import simulation_2

@pytest.mark.all
def test_sim1_1():
    ma = simulation_2.sim2.Map()
    cent_bs = ma.bs[0]
    simulation_2.sim2.prob_11(cent_bs)
    assert os.path.exists('./fig1_1.jpg')
    os.system('rm -rf fig1_1.jpg')

@pytest.mark.all
def test_sim1_2():
    ma = simulation_2.sim2.Map()
    cent_bs = ma.bs[0]
    simulation_2.sim2.prob_12(cent_bs)
    assert os.path.exists('./fig1_2.jpg')
    os.system('rm -rf fig1_2.jpg')

@pytest.mark.all
def test_sim1_3():
    ma = simulation_2.sim2.Map()
    cent_bs = ma.bs[0]
    simulation_2.sim2.prob_13(ma)
    assert os.path.exists('./fig1_3.jpg')
    os.system('rm -rf fig1_3.jpg')

@pytest.mark.all
def test_sim2_1():
    ma = simulation_2.sim2.Map()
    cent_bs = ma.bs[0]
    simulation_2.sim2.prob_21(cent_bs)
    assert os.path.exists('./fig2_1.jpg')
    os.system('rm -rf fig2_1.jpg')

@pytest.mark.all
def test_sim2_2():
    ma = simulation_2.sim2.Map()
    cent_bs = ma.bs[0]
    simulation_2.sim2.prob_22(cent_bs)
    assert os.path.exists('./fig2_2.jpg')
    os.system('rm -rf fig2_2.jpg')

@pytest.mark.all
def test_sim2_3():
    ma = simulation_2.sim2.Map()
    cent_bs = ma.bs[0]
    simulation_2.sim2.prob_23(cent_bs)
    assert os.path.exists('./fig2_3.jpg')
    os.system('rm -rf fig2_3.jpg')
