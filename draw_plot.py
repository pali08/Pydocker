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

    fig, (ax1, ax3, ax2) = plt.subplots(ncols=3)

    data = diff_matrix
    data2 = pdb_aligned_matrix
    data3 = bcr_matrix

    fig.suptitle('Correlation score is {0:.3f}'.format(score))

    img1 = ax1.imshow(data)
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(img1, cax=cax1)

    img3 = ax3.imshow(data3)
    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(img3, cax=cax3)

    img2 = ax2.imshow(data2)
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

    graph = os.path.join(subfolder, "{0}_graph_{1:02d}.png".format(os.path.split(subfolder)[1], num_of_graph))

    plt.savefig(graph)
    plt.close()
    #plt.show()
    return(0)


