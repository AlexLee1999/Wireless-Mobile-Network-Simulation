import matplotlib.pyplot as plt
from random import randint, uniform
from math import sqrt, log10, pi, cos, sin


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
SQRT_3 = sqrt(3)
SQRT_3_div_2 = (sqrt(3) / 2)
NEG_SQRT_3 = (-1) * sqrt(3)
NEG_SQRT_3_div_2 = (-1) * (sqrt(3) / 2)
UE_NUM = 100
SCALE = 250 / SQRT_3_div_2


class Map():
    def __init__(self):
        self._cluster = []
    
    def add_cluster(self, cluster):
        self._cluster.append(cluster)

    @property
    def cluster(self):
        return self._cluster
    
    def plot_map(self):
        x = []
        y = []
        for j in range(len(self.cluster)):
            for i in range(len(self.cluster[j].bs)):
                x.append(self.cluster[j].bs[i].x)
                y.append(self.cluster[j].bs[i].y)
        plt.scatter(x, y, color='r', marker='^')
        plt.axis('square')
        plt.title('UE Map')
        plt.xlabel("X(m)")
        plt.ylabel("Y(m)")
        plt.savefig('./map.jpg')
        plt.close()


class Cluster():
    def __init__(self, loc_x, loc_y, ma):
        self._bs = []
        self._bs.append(Bs(0 + loc_x, 0 + loc_y, 10, self))
        self._bs.append(Bs(0 + loc_x, 500 + loc_y, 11, self))
        self._bs.append(Bs(0 + loc_x, 1000 + loc_y, 12, self))
        self._bs.append(Bs(0 + loc_x, -500 + loc_y, 9, self))
        self._bs.append(Bs(0 + loc_x, -1000 + loc_y, 8, self))
        self._bs.append(Bs(250 * NEG_SQRT_3 + loc_x, 250 + loc_y, 6, self))
        self._bs.append(Bs(250 * NEG_SQRT_3 + loc_x, -250 + loc_y, 5, self))
        self._bs.append(Bs(250 * NEG_SQRT_3 + loc_x, -750 + loc_y, 4, self))
        self._bs.append(Bs(250 * NEG_SQRT_3 + loc_x, 750 + loc_y, 7, self))
        self._bs.append(Bs(250 * SQRT_3 + loc_x, 250 + loc_y, 15, self))
        self._bs.append(Bs(250 * SQRT_3 + loc_x, -250 + loc_y, 14, self))
        self._bs.append(Bs(250 * SQRT_3 + loc_x, 750 + loc_y, 16, self))
        self._bs.append(Bs(250 * SQRT_3 + loc_x, -750 + loc_y, 13, self))
        self._bs.append(Bs(500 * SQRT_3 + loc_x, 0 + loc_y, 18, self))
        self._bs.append(Bs(500 * SQRT_3 + loc_x, 500 + loc_y, 19, self))
        self._bs.append(Bs(500 * SQRT_3 + loc_x, -500 + loc_y, 17, self))
        self._bs.append(Bs(500 * NEG_SQRT_3 + loc_x, 0 + loc_y, 2, self))
        self._bs.append(Bs(500 * NEG_SQRT_3 + loc_x, 500 + loc_y, 3, self))
        self._bs.append(Bs(500 * NEG_SQRT_3 + loc_x, -500 + loc_y, 1, self))
        self._ma = ma
    
    def gen_ue(self):
        for i in range(UE_NUM):
            bs_num = randint(1, 19)
            bs = self._bs[bs_num - 1]
            ue = Ue(bs, self._ma, i+1)
            bs.add_ue(ue)

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
            for j in range(len(self.bs[i].ue)):
                ue_x.append(self.bs[i].ue[j].x)
                ue_y.append(self.bs[i].ue[j].y)
        plt.scatter(x, y, color='r', marker='^')
        for i in range(len(self.bs)):
            plt.annotate(self.bs[i].num, (x[i], y[i]))
        plt.axis('square')
        plt.title('UE Map')
        plt.xlabel("X(m)")
        plt.ylabel("Y(m)")
        plt.savefig('./figbonus_1.jpg')
        plt.close()

        plt.scatter(x, y, color='r', marker='^')
        plt.scatter(ue_x, ue_y, marker='.')
        for i in range(len(self.bs)):
            plt.annotate(self.bs[i].num, (x[i], y[i]))
        plt.axis('square')
        plt.title('UE Map')
        plt.xlabel("X(m)")
        plt.ylabel("Y(m)")
        plt.savefig('./figbonus_2.jpg')
        plt.close()


class Bs():
    def __init__(self, x, y, num, cluster):
        self._loc_x = x
        self._loc_y = y
        self._num = num
        self._ue = []
        self._cluster = cluster

    @property
    def ue(self):
        return self._ue

    @property
    def x(self):
        return self._loc_x

    @property
    def y(self):
        return self._loc_y
    
    @property
    def num(self):
        return self._num

    def add_ue(self, ue):
        self._ue.append(ue)


class Ue():
    def __init__(self, bs, ma, num):
        self._x, self._y = gen_loc()
        self._x += bs.x
        self._y += bs.y
        self._bs = bs
        self._ma = ma
        self.get_direction()
        self._num = num

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def bs(self):
        return self._bs

    def get_direction(self):
        self._angle, self._speed, self._time = change_direction() 
    
    def update_loc(self):
        if self._time == 0:
            self.get_direction()
            x_speed = self._speed * cos(self._angle) 
            y_speed = self._speed * sin(self._angle)
            self._x += x_speed
            self._y += y_speed
            self._time -= 1
        else:
            x_speed = self._speed * cos(self._angle) 
            y_speed = self._speed * sin(self._angle)
            self._x += x_speed
            self._y += y_speed
            self._time -= 1
    
    def change_bs(self, time, count, events):
        max_sinr = -1 * float('inf')
        max_bs = self._bs
        for cluster in ma.cluster:
            for bs in cluster.bs:
                dis = sqrt((self.x - bs.x) ** 2 + (self.y - bs.y) ** 2)
                inf = all_inf(self._ma, bs) - db_to_int(up_rxp(dis))
                sinr = Sinr(up_rxp(dis), inf)
                if sinr > max_sinr:
                    max_sinr = sinr
                    max_bs = bs
        self_dis = sqrt((self.x - self.bs.x) ** 2 + (self.y - self.bs.y) ** 2)
        self_inf = all_inf(self._ma, self.bs) - db_to_int(up_rxp(self_dis))
        self_sinr = Sinr(up_rxp(self_dis), self_inf)
        if max_sinr > self_sinr + 10:
            print(f"Num : {self._num:3}, Time : {time:3}, Before : {self._bs.num:2}, After : {max_bs.num:2}")
            events[f'{self._num}'].append(f"Num : {self._num:3}, Time : {time:3}, Before : {self._bs.num:2}, After : {max_bs.num:2}")
            self._bs.ue.remove(self)
            self._bs = max_bs
            self._bs.add_ue(self)
            count += 1
        return count



def Sinr(power_db, inf):
    noise = BOLTZ_CONST * TEMP * BW
    p = db_to_int(power_db)
    s = p / (noise + inf)
    return 10 * log10(s)



def all_inf(ma, Bs):
    inf = 0
    for cluster in ma.cluster:
        for bs in cluster.bs:
            for ues in bs.ue:
                dis = sqrt((ues.x - Bs.x) ** 2 + (ues.y - Bs.y) ** 2)
                inf += db_to_int(up_rxp(dis))
    return inf

def gen_loc():
    while True:
        x = uniform(-1, 1)
        y = uniform(-1, 1)
        if (y <= SQRT_3_div_2) and (y >= NEG_SQRT_3_div_2) and (SQRT_3 * x + y <= SQRT_3) and (SQRT_3 * x + y >= NEG_SQRT_3) and (NEG_SQRT_3 * x + y <= SQRT_3) and (NEG_SQRT_3 * x + y >= NEG_SQRT_3):
            return x * SCALE, y * SCALE


def down_rxp(dis):
    g = (B_H * UE_H) ** 2 / (dis ** EX)
    g_db = 10 * log10(g)
    rx_p = g_db + BASE_P + TX_G + RX_G
    return rx_p


def up_rxp(dis):
    g = (B_H * UE_H) ** 2 / (dis ** EX)
    g_db = 10 * log10(g)
    rx_p = g_db + UE_P + TX_G + RX_G
    return rx_p


def db_to_int(n):
    return 10 ** (n / 10)


def change_direction():
    angle = uniform(0, 2 * pi)
    speed = uniform(1, 15)
    time = randint(1, 6)
    return angle, speed, time


if __name__ == "__main__":
    ma = Map()
    ma.add_cluster(Cluster(0, 0, ma))
    ma.add_cluster(Cluster(4.5 * SCALE, 1750, ma))
    ma.add_cluster(Cluster(-3 * SCALE, 2000, ma))
    ma.add_cluster(Cluster(-7.5 * SCALE, 250, ma))
    ma.add_cluster(Cluster(-4.5 * SCALE, -1750, ma))
    ma.add_cluster(Cluster(3 * SCALE, -2000, ma))
    ma.add_cluster(Cluster(7.5 * SCALE, -250, ma))
    cc = ma.cluster[0]
    cc.gen_ue()
    cc.plot_map()
    count = 0
    Handoff_events = {}
    for i in range(UE_NUM):
        Handoff_events[f'{i+1}'] = []
    for time in range(1, 901):
        for cluster in ma.cluster:
            for bs in cluster.bs:
                for ue in bs.ue:
                    ue.update_loc()
                    count = ue.change_bs(time, count, Handoff_events)
    print(f"Total handoff {count} times.")
    for i in range(UE_NUM):
        print(f"{i + 1} : {Handoff_events[f'{i+1}']}")
