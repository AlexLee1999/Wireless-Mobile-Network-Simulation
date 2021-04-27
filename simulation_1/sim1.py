import numpy as np
import matplotlib.pyplot as plt

BW = 10E6 
TEMP = 27 + 273.15
BASE_P = 33E-3 
TX_G = 14
RX_G = 14
B_H = 51.5
UE_H = 1.5
BOLTZ_CONST = 1.38E-23
SIGMA = 6
DIS = 1000
EX = 4

def prob_11():
    ############# Problem 1-1 #############
    rx_list = []
    dis_list = []
    for dis in range(1, DIS):
        g = (B_H * UE_H) ** 2 / (dis ** EX)
        g_db = 10 * np.log10(g)
        rx_p = g_db + BASE_P + TX_G + RX_G
        rx_list.append(rx_p)
        dis_list.append(dis)
    plt.plot(dis_list, rx_list)
    plt.xlabel("Distance")
    plt.ylabel("Power")
    plt.savefig('./fig1_1.jpg')
    plt.close()

def prob_12():
    ############# Problem 1-2 #############
    dis_list = []
    snr_list = []
    noise = BOLTZ_CONST * TEMP * BW
    noise_db = 10 * np.log10(noise)
    for dis in range(1, DIS):
        g = (B_H * UE_H) ** 2 / (dis ** EX)
        g_db = 10 * np.log10(g)
        rx_p = g_db + BASE_P + TX_G + RX_G
        snr = rx_p - noise_db
        snr_list.append(snr)
        dis_list.append(dis)
    plt.plot(dis_list, snr_list)
    plt.xlabel("Distance")
    plt.ylabel("SNR")
    plt.savefig('./fig1_2.jpg')
    plt.close()

def prob_21():
    ############# Problem 2-1 #############
    rx_list = []
    dis_list = []
    rx_avg_list = []
    for dis in range(1, DIS):
        g = (B_H * UE_H) ** 2 / (dis ** EX)
        g_db = 10 * np.log10(g)
        ran = np.random.normal(0, SIGMA)
        rx_p = g_db + BASE_P + TX_G + RX_G
        rx_avg_list.append(rx_p)
        rx_p_avg = rx_p + ran
        rx_list.append(rx_p_avg)
        dis_list.append(dis)
    plt1, = plt.plot(dis_list, rx_list, label='With Shadowing')
    plt2, = plt.plot(dis_list, rx_avg_list, label='Without Shadowing')
    plt.legend(handles=[plt1, plt2])
    plt.xlabel("Distance")
    plt.ylabel("Power")
    plt.savefig('./fig2_1.jpg')
    plt.close()

def prob_22():
    ############# Problem 2-2 #############
    dis_list = []
    snr_list = []
    snr_avg_list = []
    noise = BOLTZ_CONST * TEMP * BW
    noise_db = 10 * np.log10(noise)
    for dis in range(1, DIS):
        g = (B_H * UE_H) ** 2 / (dis ** EX)
        g_db = 10 * np.log10(g)
        ran = np.random.normal(0, SIGMA)
        rx_p = g_db + BASE_P + TX_G + RX_G
        snr = rx_p - noise_db
        snr_ran = snr + ran
        snr_list.append(snr_ran)
        snr_avg_list.append(snr)
        dis_list.append(dis)
    plt1, = plt.plot(dis_list, snr_list, label='With Shadowing')
    plt2, = plt.plot(dis_list, snr_avg_list, label='Without Shadowing')
    plt.legend(handles=[plt1, plt2])
    plt.xlabel("Distance")
    plt.ylabel("SNR")
    plt.savefig('./fig2_2.jpg')
    plt.close()

if __name__ == "__main__":
    prob_11()
    prob_12()
    prob_21()
    prob_22()



