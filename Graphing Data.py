import scipy.io
import os
import time
import numpy as np
from pylab import plot, xlabel, ylabel, show, title, imshow, colorbar, savefig, close, pcolor, gca, axis, xlim, ylim


class getFolderList():
    def __init__(self, folder_dir, folder_prefix_list):
        self.folder_dir = folder_dir
        self.folder_prefix_list = folder_prefix_list

    def get_folders(self):
        """
        Update:
        This function stores the names of the folders where the .mat data files are located.
        :return: folder list.
        """
        # Using the folder prefixes loop through the given directory where the folders are stored
        # appending them to the folder list.
        # Initialize a empty list.
        folder_list = []
        for folder in os.listdir(folder_dir):
            for dnum in folder_prefix_list:
                for gfnum in range(0, 12, 2):
                    folder_name = str(dnum) + '-gf' + str(gfnum)
                    if folder_name in folder:
                        folder_list.append(folder)
        return folder_list


class MakeDataPlots():
    def __init__(self, folder_dir, file_list, folder_list, time_step, dim1, dim2):
        self.folder_dir = folder_dir
        self.file_list = file_list
        self.folder_list = folder_list
        self.time_step = time_step
        self.dim1 = dim1
        self.dim2 = dim2

    def get_data_and_plot(self):
        """
        This function creates a 3-D array that stores the given data files at any one given time step. This function
        also calls various functions to preform further calculations as well as plot.
        """
        # initialize a 3-D array, to the size of the data stored in each file
        # The first dimension corresponds to the file, the second and third dimensions correspond to the first and
        # second dimensions of the array of coordinates.
        data = np.zeros((len(file_list), dim1, dim2))

        # Get the correct address to the folder.
        dir = folder_dir + folder
        print(dir)
        # Counter for taking care of what file we are working with
        counter = 0


        # Loop for finding the files.
        for item in file_list:
            current_dir = dir + '/' + item + '_' + str(time_step) + '.mat'
            # A list of the dictionary key names for the data files P1, P2, and Pp. The data for these files are
            # stored in a different manner than the others.
            p_list = ['Pperp1e', 'Pperp2e', 'Ppare']
            # Check if the file exists, if it does store the data at that file to to the data 3-D array.
            if os.path.isfile(current_dir):
                # For P1.
                if counter == 14:
                    raw_data = scipy.io.loadmat(current_dir)
                    data[counter, :, :] = raw_data[p_list[0]]
                # For P2.
                elif counter == 15:
                    raw_data = scipy.io.loadmat(current_dir)
                    data[counter, :, :] = raw_data[p_list[1]]
                # For Pp.
                elif counter == 16:
                    raw_data = scipy.io.loadmat(current_dir)
                    data[counter, :, :] = raw_data[p_list[2]]
                # For all other cases
                else:
                    raw_data = scipy.io.loadmat(current_dir)
                    data[counter, :, :] = raw_data[item]
                # Plot each file at the 60 time step
                # if time_step == 60:
                #     self.plot_others(data[counter, :, :], folder, time_step, 'Collection I/', item, data)
            counter = counter + 1
        # After all of the data is stored, check the current time step, if at 60 find and plot temperature and p average
        if time_step == 60:
            self.time60(data, folder, time_step)
        self.get_norms(data, folder, time_step)
        # self.time60(data, folder, time_step)

    def time60(self, data, folder, time_step):
        """

        :param data: 3-D array that holds the data points, sorted by file.
        :param folder: current folder being used, contains .mat files.
        :param time_step: current time step.
        """
        temperature = (data[14] + data[15] + data[16]) / (data[12] * 3)
        tperp = (data[14] + data[15]) / (2 * data[12])
        tpara = data[16] / data[12]
        kineticx = data[9] ** 2 / data[12]
        kineticy = data[10] ** 2 / data[12]
        kineticz = data[11] ** 2 / data[12]
        kineticTot = kineticx + kineticy + kineticz

        self.plot_others(kineticTot, folder, time_step, 'INSERT FOLDER HERE/', "kinetic", data)
        self.plot_others(temperature, folder, time_step, 'INSERT FOLDER HERE/', "temperature ", data)
        self.plot_others(tperp, folder, time_step, 'INSERT FOLDER HERE/', "tperp ", data)
        self.plot_others(tpara, folder, time_step, 'INSERT FOLDER HERE/', "tpara ", data)

    def get_norms(self, data, folder, time_step):
        """
        This function performs calculations on the data to find znormz, onormz, znormo, onormo, as well as calls
        plot_norm.
        :param data: 3-D array that holds the data points, sorted by file.
        :param folder: current folder being used, contains .mat files.
        :param time_step: current time step.
        """
        # For each folder perform calculations.
        nix = data[13] * data[0]
        niy = data[13] * data[1]
        niz = data[13] * data[2]
        nig = data[13] * np.sqrt(1 - data[0] ** 2 - data[1] ** 2 - data[2] ** 2)
        nex = nix - data[9]
        ney = niy - data[10]
        nez = niz - data[11]
        neg = np.sqrt(data[12] ** 2 - nex ** 2 - ney ** 2 - nez ** 2)

        Fe0 = nex * data[6] + ney * data[7] + nez * data[8]
        Fe1 = data[12] * data[6] + ney * data[5] - nez * data[4]
        Fe2 = data[12] * data[7] - nex * data[5] + nez * data[3]
        Fe3 = data[12] * data[8] + nex * data[4] - ney * data[3]

        [T0, T1, T2, T3, sqrtW] = self.contractT(data, nix, niy, niz)
        denom = sqrtW * (data[13] ** 2 - nix ** 2 - niy ** 2 - niz ** 2) + (
                T0 * data[13] - T1 * nix - T2 * niy - T3 * niz)

        Us0 = (sqrtW * data[13] + T0) / denom
        Us1 = (sqrtW * nix + T1) / denom
        Us2 = (sqrtW * niy + T2) / denom
        Us3 = (sqrtW * niz + T3) / denom
        GAM = 1. / np.sqrt(Us0 ** 2 - Us1 ** 2 - Us2 ** 2 - Us3 ** 2)

        Us0 = nig * GAM * Us0
        Us1 = nig * GAM * Us1
        Us2 = nig * GAM * Us2
        Us3 = nig * GAM * Us3

        znormz = -(data[13] * Fe0 - nix * Fe1 - niy * Fe2 - niz * Fe3) / neg
        onormz = -(Us0 * Fe0 - Us1 * Fe1 - Us2 * Fe2 - Us3 * Fe3) / neg
        znormo = znormz * neg / nig
        onormo = onormz * neg / nig

        self.plot_norm(znormz, folder, time_step, 'INSERT FOLDER HERE/', "znormz ", data)
        self.plot_norm(onormz, folder, time_step, 'INSERT FOLDER HERE/', "onormz ", data)
        self.plot_norm(znormo, folder, time_step, 'INSERT FOLDER HERE/', "znormo ", data)
        self.plot_norm(onormo, folder, time_step, 'INSERT FOLDER HERE/', "onormo ", data)

    def contractT(self, data, nix, niy, niz):
        Sx = data[7] * data[5] - data[8] * data[4]
        Sy = data[8] * data[3] - data[6] * data[5]
        Sz = data[6] * data[4] - data[7] * data[3]
        T00 = .5 * (data[6] ** 2 + data[7] ** 2 + data[8] ** 2) + .5 * (data[3] ** 2 + data[4] ** 2 + data[5] ** 2)
        edu = data[6] * nix + data[7] * niy + data[8] * niz
        bdu = data[3] * nix + data[4] * niy + data[5] * niz

        T0 = T00 * data[13] - (Sx * nix + Sy * niy + Sz * niz)
        T1 = Sx * data[13] - T00 * nix + data[6] * edu + data[3] * bdu
        T2 = Sy * data[13] - T00 * niy + data[7] * edu + data[4] * bdu
        T3 = Sz * data[13] - T00 * niz + data[8] * edu + data[5] * bdu

        sqrtW = np.sqrt(T00 ** 2 - Sx ** 2 - Sy ** 2 - Sz ** 2)
        return T0, T1, T2, T3, sqrtW

    def find_center(self, data):
        """
        This function finds the center of the graph, where the magnetic reconnection occurs.
        :param data: 3-D array that holds the data points, sorted by file.
        :return: returns the x and z values of the center point.
        """
        abs_data = np.absolute(data)
        xval_sum = np.sum(abs_data, 0)  # line of x vals, the zero here takes care of the vertical-ness
        # sum along vertical lines, the min sum is the assumed x location of the x line
        # assuming you can bend data vertical sum magnetic field and find min
        x_pos_of_xline = np.argmin(xval_sum)  # first index
        zcut_of_xline = abs_data[:, x_pos_of_xline]
        z_pos_of_xline = np.argmin(zcut_of_xline)  # zeroth index

        return x_pos_of_xline, z_pos_of_xline

    def plot_norm(self, plot_data, folder, time_step, where_to_save, plot_data_str, data):
        """
        This function is used to plot znormz, onormz, znormo, onormo. It uses a blue white red color bar, with
        zero being white, red represents particles gaining energy, blue losing.
        :param plot_data: what data is to be plotted.
        :param folder: current folder being used, contains .mat files.
        :param time_step: current time step.
        :param where_to_save: name of the folder that the graphs are to be saved to.
        :param plot_data_str: string containing the name of the data that is being plotted.
        :param data: 3-D array that holds the data points, sorted by file.
        """
        # Set axis with val
        val = .001
        [xpos, zpos] = self.find_center(data[3])
        # print(xpos, zpos)
        if 1800 >= xpos >= 1400:
            xlim(xpos - 200, xpos + 200)
        else:
            xlim(1400, 1800)

        if 950 >= zpos >= 650:
            ylim(zpos - 150, zpos + 150)
        else:
            ylim(650, 950)

        fig = imshow(plot_data, cmap="bwr", clim=(-val, val))
        title(plot_data_str + folder + '_' + str(time_step))
        colorbar()
        print('/media/sophianowak/My Passport/' + where_to_save + plot_data_str + folder + '_' + str(time_step))
        # savefig('/media/sophianowak/My Passport/' + where_to_save + plot_data_str + folder + '_' + str(time_step) + '.png')
        # close()
        show()

    def plot_others(self, plot_data, folder, time_step, where_to_save, plot_data_str, data):
        """
        This function plots temperature, tperp, as well as each data file. It uses inferno.
        :param plot_data: what data is to be plotted.
        :param folder: current folder being used, contains .mat files.
        :param time_step: current time step.
        :param where_to_save: name of the folder that the graphs are to be saved to.
        :param plot_data_str: string containing the name of the data that is being plotted.
        :param data: 3-D array that holds the data points, sorted by file.
        """
        [xpos, zpos] = self.find_center(data[3])
        plot_data = plot_data[(zpos-150):(zpos+150), (xpos-200):(xpos+200)]
        fig = imshow(plot_data, cmap="inferno", extent=[(xpos - 200), (xpos + 200), (zpos - 150), (zpos + 150)],
                     origin='lower')
        title(plot_data_str + folder + '_' + str(time_step))
        colorbar()
        print('/media/sophianowak/My Passport/' + where_to_save + plot_data_str + folder + '_' + str(time_step))
        # savefig('/media/sophianowak/My Passport/' + where_to_save + plot_data_str + folder + '_' + str(time_step) + '.png')
        # close()
        show()


if __name__ == '__main__':
    start = time.time()
    # Change the file directory variable depending on where the data is currently stored.
    folder_dir = '/media/sophianowak/My Passport/AsymmetricScan400/'
    # List of the file names, though these names may not necessarily correspond to the correct dictionary key where
    # the data is located.
    file_list = ['uix', 'uiy', 'uiz', 'bx', 'by', 'bz', 'ex', 'ey', 'ez', 'jx', 'jy', 'jz', 'ne', 'ni', 'P1', 'P2', 'Pp']
    # Store the folder prefixes to later loop through storing all of the folders.
    folder_prefix_list = ['d10', 'd10.5', 'd11', 'd12', 'd14', 'd16', 'd20', 'd27', 'd74', 'd200']

    # Call the getFolderList class to create the list of the folders
    folders = getFolderList(folder_dir, folder_prefix_list)
    folder_list = folders.get_folders()
    print(folder_list)

    # Dimensions of the data in each file.
    dim1 = 1680
    dim2 = 3360
    # Loop over all of the folders
    folder_list = ['d200-gf4']
    for folder in folder_list:
        for time_step in range(60, 61):
            graphs = MakeDataPlots(folder_dir, file_list, folder_list, time_step, dim1, dim2)
            graphs.get_data_and_plot()
            del graphs

    end = time.time()
    print(end - start + "seconds")
