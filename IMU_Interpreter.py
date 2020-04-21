import argparse

from cycler import cycler
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv


class real_time_peak_detection():
    def __init__(self, array, lag, threshold, influence):
        self.y = list(array)
        self.length = len(self.y)
        self.lag = lag
        self.threshold = threshold
        self.influence = influence
        self.signals = [0] * len(self.y)
        self.filteredY = np.array(self.y).tolist()
        self.avgFilter = [0] * len(self.y)
        self.stdFilter = [0] * len(self.y)
        self.avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag]).tolist()
        self.stdFilter[self.lag - 1] = np.std(self.y[0:self.lag]).tolist()

    def thresholding_algo(self):
        i = len(self.y) - 1
        self.length = len(self.y)
        if i < self.lag:
            return 0
        elif i == self.lag:
            self.signals = [0] * len(self.y)
            self.filteredY = np.array(self.y).tolist()
            self.avgFilter = [0] * len(self.y)
            self.stdFilter = [0] * len(self.y)
            self.avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag]).tolist()
            self.stdFilter[self.lag - 1] = np.std(self.y[0:self.lag]).tolist()
            return 0

        self.signals += [0]
        self.filteredY += [0]
        self.avgFilter += [0]
        self.stdFilter += [0]

        if abs(self.y[i] - self.avgFilter[i - 1]) > self.threshold * self.stdFilter[i - 1]:
            if self.y[i] > self.avgFilter[i - 1]:
                self.signals[i] = 1
            else:
                self.signals[i] = -1

            self.filteredY[i] = self.influence * self.y[i] + (1 - self.influence) * self.filteredY[i - 1]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])
        else:
            self.signals[i] = 0
            self.filteredY[i] = self.y[i]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])

        return self.signals


def main(csv_file):
    gyroX = []
    gyroY = []
    gyroZ = []
    accX = []
    accY = []
    accZ = []
    magX = []
    magY = []
    magZ = []

    time = []

    with open(csv_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:

            real_row = row[0].split(",")

            time.append(real_row[0])

            ## Unfiltered data
            gyroX.append(float(real_row[1]))
            gyroY.append(float(real_row[2]))
            gyroZ.append(float(real_row[3]))

            accX.append(float(real_row[4]))
            accY.append(float(real_row[5]))
            accZ.append(float(real_row[6]))

            magX.append(real_row[7])
            magY.append(real_row[8])
            magZ.append(real_row[9])

    est_x = [0.0, 0.0]
    est_y = [0.0, 0.0]
    est_z = [0.0, 0.0]
    gain_x = []
    gain_y = []
    gain_z = []

    i = 1

    for val in accX:
        if i == 1:
            gain_x.append(1)
            est_x.append(0.0 + 1.0 * (val - 0.0))
            i = i + 1
            #avg_list.append([val, 0.0])
        else:
            last_est = est_x[-1]
            gain_x.append(1 / i)
            est_x.append(last_est + (1 / i) * (val - last_est))
            i = i + 1
            #avg_list.append([val, last_est + (1 / i) * (val - last_est)])

    i = 1
    for val in accY:
        if i == 1:
            gain_y.append(1)
            est_y.append(0.0 + 1.0 * (val - 0.0))
            i = i + 1
            #avg_list.append([val, 0.0])
        else:
            last_est = est_y[-1]
            gain_y.append(1 / i)
            est_y.append(last_est + (1 / i) * (val - last_est))
            i = i + 1
            #avg_list.append([val, last_est + (1 / i) * (val - last_est)])

    i = 1
    for val in accZ:
        if i == 1:
            gain_z.append(1)
            est_z.append(0.0 + 1.0 * (val - 0.0))
            i = i + 1
            #avg_list.append([val, 0.0])
        else:
            last_est = est_z[-1]
            gain_z.append(1 / i)
            est_z.append(last_est + (1 / i) * (val - last_est))
            i = i + 1
            #avg_list.append([val, last_est + (1 / i) * (val - last_est)])

    print(est_z)

    plt.style.use('dark_background')

    fig, axs = plt.subplots(3)
    fig.suptitle('Sharing both axes')

    thres = real_time_peak_detection(array=accX, lag=30, threshold=3, influence=0)

    axs[0].plot(accX, label='Acceleration X', linewidth=0.5, color='red')
    axs[0].plot(est_x[2:-1], label='Estimates AccX', linewidth=2.5, color='gold')
    axs[0].plot(thres.thresholding_algo(), label='Estimates AccX', linewidth=0.5, dashes=[6, 2], color='white')

    axs[1].plot(accY, label='Acceleration Y', linewidth=0.5, color='lime')
    axs[1].plot(est_y[2:-1], label='Estimates AccY', linewidth=2.5, color='gold')

    axs[2].plot(accZ, label='Acceleration Z', linewidth=0.5, color='blue')
    axs[2].plot(est_z[2:-1], label='Estimates AccZ', linewidth=2.5, color='gold')

    axs[0].set_xlabel('iterations')
    axs[0].set_ylabel('Acceleration (m/s/s)')
    axs[0].grid(True)
    axs[1].set_xlabel('iterations')
    axs[1].set_ylabel('Acceleration (m/s/s)')
    axs[1].grid(True)
    axs[2].set_xlabel('iterations')
    axs[2].set_ylabel('Acceleration (m/s/s)')
    axs[2].grid(True)

    axs[0].legend()
    axs[1].legend()
    axs[2].legend()

    fig.canvas.set_window_title('Kalman Filter Test')

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--csv-file', metavar='path', required=True,
                        help='the path to workspace')
    args = parser.parse_args()
    main(csv_file=args.csv_file)
