from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from pdb_bins import pdb_to_bins
import os


def draw_points(diff_matrix, num_of_graph, subfolder, score, bin_size, pdb_aligned_matrix, bcr_matrix):
    plt.switch_backend('agg') #default backend is 'agg' and it can only draw png file. I use 'Qt4Agg' for interactive 3D graph. 

    #x_ar_bcr, y_ar_bcr, z_ar_bcr = fill_coord_lists(bcr_matrix)

    #x_ar_pdb, y_ar_pdb, z_ar_pdb = fill_coord_lists(pdb_matrix)

    #fig = plt.figure(1)
    '''
    ax = fig.add_subplot(211, projection='3d')

    ax.scatter(x_ar_bcr, y_ar_bcr, z_ar_bcr, color='red')
    ax.scatter(x_ar_pdb, y_ar_pdb, z_ar_pdb, color='green')

    ax.set_xlabel('')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title('Correlation score is {}'.format(score))
    '''
    fig, (ax1, ax3, ax2) = plt.subplots(ncols=3)

    data = diff_matrix
    data2 = pdb_aligned_matrix
    data3 = bcr_matrix

    fig.suptitle('Correlation score is {0:.3f}'.format(score))

    img1 = ax1.imshow(data, cmap='afmhot')
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(img1, cax=cax1)

    img3 = ax3.imshow(data3, cmap='afmhot')
    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(img3, cax=cax3)

    img2 = ax2.imshow(data2, cmap='afmhot')
    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(img2, cax=cax2)

    ax1.set_title('Subtracted matrices')
    ax2.set_title('Pdb surface')
    ax3.set_title('Afm image')

    ax1.set_xlabel("px")
    ax1.set_ylabel("px")
    ax2.set_xlabel("px")
    ax2.set_ylabel("px")
    ax3.set_xlabel("px \n 1 px = {0:.3f}nm".format(bin_size))
    ax3.set_ylabel("px")

    plt.tight_layout(h_pad=1)

    #cax1 = ax1.imshow(data, interpolation='nearest', cmap=cm.afmhot)
    #ax1.set_title('Correlation score is {0:.3f}'.format(score))
    #ax1.set_xlabel("px \n 1 px = {0:.3f}nm".format(bin_size))
    #ax1.set_ylabel("px")

    #cbar1 = fig.colorbar(cax1, ax = ax1, ticks=[lowest,average,highest], orientation='vertical')
    #cbar1.ax.set_xticklabels(["{0:.3f}nm".format(lowest),"{0:.3f}nm".format(average),"{0:.3f}nm".format(highest)])  # horizontal colorbar

    #cax2 = ax2.imshow(data2, interpolation='nearest', cmap=cm.afmhot)
    #ax2.set_title('Pdb matrix')
    #ax2.set_xlabel("px \n 1 px = {0:.3f}nm".format(bin_size))
    #ax2.set_ylabel("px")

    #cbar2 = fig.colorbar(cax2, ax = ax2,ticks=[lowest_pdb,avg_pdb,highest_pdb], orientation='vertical')
    #cbar2.ax.set_xticklabels(["{0:.3f}nm".format(lowest_pdb),"{0:.3f}nm".format(avg_pdb),"{0:.3f}nm".format(highest_pdb)])  # horizontal colorbar

    #ax.figtext(1,20,"1 px = {0:.3f}nm".format(bin_size),horizontalalignment='center', verticalalignment='bottom')
    '''
    #and now second graph: matrix of differences
    ax2 = fig.add_subplot(211)
    ax2.set_title('Correlation score is {}'.format(score))
    cax = ax2.imshow(diff_matrix)
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
    cbar.ax2.set_xticklabels(['Low', 'Medium', 'High'])  # horizontal colorbar
    '''
    graph = os.path.join(subfolder, "{0}_graph_{1:02d}.png".format(os.path.split(subfolder)[1], num_of_graph))
    plt.savefig(graph)
    plt.close()
    #plt.show()
    return(0)

# TODO: picture name and folder in argument or by joining name of bcr and pdb files

