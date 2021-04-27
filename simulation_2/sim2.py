import numpy as np
import matplotlib.pyplot as plt
import random
import math


BW = 10E6
TEMP = 27 + 273.15
BASE_P = 33 - 30
UE_P = 23 - 30
TX_G = 14
RX_G = 14
B_H = 51.5
UE_H = 1.5
BOLTZ_CONST = 1.38E-23
EX = 4
SQRT_3 = math.sqrt(3)
SQRT_3_div_2 = (math.sqrt(3) / 2)
NEG_SQRT_3 = (-1) * math.sqrt(3)
NEG_SQRT_3_div_2 = (-1) * (math.sqrt(3) / 2)
UE_NUM = 50
SCALE = 250 / SQRT_3_div_2


class Map():
    def __init__(self):
        self._bs = []
        self._bs.append(Bs(0, 0))
        self._bs.append(Bs(0, 500))
        self._bs.append(Bs(0, 1000))
        self._bs.append(Bs(0, -500))
        self._bs.append(Bs(0, -1000))
        self._bs.append(Bs(250 * NEG_SQRT_3, 250))
        self._bs.append(Bs(250 * NEG_SQRT_3, -250))
        self._bs.append(Bs(250 * NEG_SQRT_3, -750))
        self._bs.append(Bs(250 * NEG_SQRT_3, 750))
        self._bs.append(Bs(250 * SQRT_3, 250))
        self._bs.append(Bs(250 * SQRT_3, -250))
        self._bs.append(Bs(250 * SQRT_3, 750))
        self._bs.append(Bs(250 * SQRT_3, -750))
        self._bs.append(Bs(500 * SQRT_3, 0))
        self._bs.append(Bs(500 * SQRT_3, 500))
        self._bs.append(Bs(500 * SQRT_3, -500))
        self._bs.append(Bs(500 * NEG_SQRT_3, 0))
        self._bs.append(Bs(500 * NEG_SQRT_3, 500))
        self._bs.append(Bs(500 * NEG_SQRT_3, -500))

    @property
    def bs(self):
        return self._bs

    def plot_map(self):
        x = []
        y = []
        ue_x = []
        ue_y = []
        for i in range(len(self.bs)):
            x.append(self.bs[i].x)
            y.append(self.bs[i].y)
            for j in range(len(self.bs[i].Ue_lst)):
                ue_x.append(self.bs[i].Ue_lst[j].x)
                ue_y.append(self.bs[i].Ue_lst[j].y)
        plt.scatter(x, y, color='r', marker='^')
        plt.scatter(ue_x, ue_y, marker='.')
        plt.axis('square')
        plt.title('UE Map')
        plt.xlabel("X(m)")
        plt.ylabel("Y(m)")
        plt.savefig('./figbonus_1.jpg')
        plt.close()


class Bs():
    def __init__(self, x, y):
        self._loc_x = x
        self._loc_y = y
        self._Ue_lst = []
        for i in range(UE_NUM):
            ue = Ue(self)
            self._Ue_lst.append(ue)

    @property
    def Ue_lst(self):
        return self._Ue_lst

    @property
    def x(self):
        return self._loc_x

    @property
    def y(self):
        return self._loc_y


class Ue():
    def __init__(self, bs):
        self._x, self._y = gen_loc()
        self._dis = math.sqrt((self._x) ** 2 + (self._y) ** 2)
        self._x += bs.x
        self._y += bs.y
        self._down_rxp = down_rxp(self._dis)
        self._up_rxp = up_rxp(self._dis)
        self._bs = bs

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def dis(self):
        return self._dis

    @property
    def down_rxp(self):
        return self._down_rxp

    @property
    def up_rxp(self):
        return self._up_rxp

    @property
    def bs(self):
        return self._bs


def gen_loc():
    while True:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if (y <= SQRT_3_div_2) and (y >= NEG_SQRT_3_div_2) and (SQRT_3 * x + y <= SQRT_3) and (SQRT_3 * x + y >= NEG_SQRT_3) and (NEG_SQRT_3 * x + y <= SQRT_3) and (NEG_SQRT_3 * x + y >= NEG_SQRT_3):
            return x * SCALE, y * SCALE


def down_rxp(dis):
    g = (B_H * UE_H) ** 2 / (dis ** EX)
    g_db = 10 * np.log10(g)
    rx_p = g_db + BASE_P + TX_G + RX_G
    return rx_p


def up_rxp(dis):
    g = (B_H * UE_H) ** 2 / (dis ** EX)
    g_db = 10 * np.log10(g)
    rx_p = g_db + UE_P + TX_G + RX_G
    return rx_p


def db_to_int(n):
    return 10 ** (n / 10)


def Sinr(power_db, inf):
    noise = BOLTZ_CONST * TEMP * BW
    p = db_to_int(power_db)
    s = p / (noise + inf)
    return 10 * math.log10(s)


def all_inf(ma, ue):
    inf = 0
    Bs = ue.bs
    for bs in ma.bs:
        for ues in bs.Ue_lst:
            dis = math.sqrt((ues.x - Bs.x) ** 2 + (ues.y - Bs.y) ** 2)
            inf += db_to_int(up_rxp(dis))
    return inf


def all_inf_bs(bs):
    inf = 0
    for ue in bs.Ue_lst:
        inf += db_to_int(ue.up_rxp)
    return inf


def prob_11(bs):
    Ue_lst_x = []
    Ue_lst_y = []
    for i in range(len(bs.Ue_lst)):
        Ue_lst_x.append(bs.Ue_lst[i].x)
        Ue_lst_y.append(bs.Ue_lst[i].y)
    plt.title('UE Map')
    plt.scatter(Ue_lst_x, Ue_lst_y, marker='.')
    plt.scatter(bs.x, bs.y, color='r', marker='^')
    plt.axis('square')
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig('./fig1_1.jpg')
    plt.close()


def prob_12(bs):
    Ue_lst_rxp = []
    Ue_lst_dis = []
    for ue in bs.Ue_lst:
        Ue_lst_rxp.append(ue.down_rxp)
        Ue_lst_dis.append(ue.dis)
    plt.title('Power')
    plt.scatter(Ue_lst_dis, Ue_lst_rxp, marker='.')
    plt.xlabel("Distance(m)")
    plt.ylabel("Power(dB)")
    plt.savefig('./fig1_2.jpg')
    plt.close()


def prob_13(ma):
    sinr_lst = []
    dis_lst = []
    bs = ma.bs[0] ## Central BS
    for ue in bs.Ue_lst:
        inf_p = 0
        for j in range(1, len(ma.bs)):
            dis = math.sqrt((ma.bs[j].x - ue.x) ** 2 + (ma.bs[j].y - ue.y) ** 2)
            inf_p += db_to_int(down_rxp(dis))
        sinr = Sinr(ue.down_rxp, inf_p)
        sinr_lst.append(sinr)
        dis_lst.append(ue.dis)
    plt.title('SINR')
    plt.xlabel("Distance(m)")
    plt.ylabel("SINR(dB)")
    plt.scatter(dis_lst, sinr_lst, marker='.')
    plt.savefig('./fig1_3.jpg')
    plt.close()


def prob_21(bs):
    Ue_lst_x = []
    Ue_lst_y = []
    for i in range(len(bs.Ue_lst)):
        Ue_lst_x.append(bs.Ue_lst[i].x)
        Ue_lst_y.append(bs.Ue_lst[i].y)
    plt.title('UE Map')
    plt.scatter(Ue_lst_x, Ue_lst_y, marker='.')
    plt.scatter(bs.x, bs.y, color='r', marker='^')
    plt.axis('square')
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig('./fig2_1.jpg')
    plt.close()


def prob_22(bs):
    Ue_lst_rxp = []
    Ue_lst_dis = []
    for i in range(len(bs.Ue_lst)):
        Ue_lst_rxp.append(bs.Ue_lst[i].up_rxp)
        Ue_lst_dis.append(bs.Ue_lst[i].dis)
    plt.title('Power')
    plt.scatter(Ue_lst_dis, Ue_lst_rxp, marker='.')
    plt.xlabel("Distance(m)")
    plt.ylabel("Power(dB)")
    plt.savefig('./fig2_2.jpg')
    plt.close()


def prob_23(bs):
    sinr_lst = []
    dis_lst = []
    for ue in bs.Ue_lst:
        inf_p = all_inf_bs(bs) - db_to_int(ue.up_rxp)
        sinr = Sinr(ue.up_rxp, inf_p)
        sinr_lst.append(sinr)
        dis_lst.append(ue.dis)
    plt.title('SINR')
    plt.xlabel("Distance(m)")
    plt.ylabel("SINR(dB)")
    plt.scatter(dis_lst, sinr_lst, marker='.')
    plt.savefig('./fig2_3.jpg')
    plt.close()


def prob_bonus1(ma):
    ma.plot_map()


def prob_bonus2(ma):
    Ue_lst_rxp = []
    Ue_lst_dis = []
    for j in range(len(ma.bs)):
        for i in range(len(ma.bs[j].Ue_lst)):
            Ue_lst_rxp.append(ma.bs[j].Ue_lst[i].down_rxp)
            Ue_lst_dis.append(ma.bs[j].Ue_lst[i].dis)
    plt.title('Power')
    plt.scatter(Ue_lst_dis, Ue_lst_rxp, marker='.')
    plt.xlabel("Distance(m)")
    plt.ylabel("Power(dB)")
    plt.savefig('./figbonus_2.jpg')
    plt.close()


def prob_bonus3(ma):
    sinr_lst = []
    dis_lst = []
    for bs in ma.bs:
        for ue in bs.Ue_lst:
            inf_p = all_inf(ma, ue) - db_to_int(ue.up_rxp)
            sinr = Sinr(ue.up_rxp, inf_p)
            sinr_lst.append(sinr)
            dis_lst.append(ue.dis)
    plt.title('SINR')
    plt.xlabel("Distance(m)")
    plt.ylabel("SINR(dB)")
    plt.scatter(dis_lst, sinr_lst, marker='.')
    plt.savefig('./figbonus_3.jpg')
    plt.close()


if __name__ == "__main__":
    ma = Map()
    cent_bs = ma.bs[0]
    prob_11(cent_bs)
    prob_12(cent_bs)
    prob_13(ma)
    prob_21(cent_bs)
    prob_22(cent_bs)
    prob_23(cent_bs)
    prob_bonus1(ma)
    prob_bonus2(ma)
    prob_bonus3(ma)