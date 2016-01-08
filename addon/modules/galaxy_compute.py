import os
import numpy as np
import pandas as pd

# Set up matplotlib and use a nicer set of plot parameters
#config InlineBackend.rc = {}
import matplotlib
#matplotlib.rc_file("../../templates/matplotlibrc")
import matplotlib.pyplot as plt
#matplotlib inline

from astropy.utils.data import download_file
from astropy.io import fits
from os import listdir


def clearPlot(plt):
	plt.cla()
	plt.clf()

def get_center(ctr):
	return np.mean(ctr.allsegs[len(ctr.allsegs)-1], axis=1)[0]

#ct = get_center(ctr)

def get_radian(center, point):
	x = point[0] - center[0]
	y = point[1] - center[1]
	rad = np.arctan2(y, x);
	return rad if rad > 0 else np.pi * 2 + rad

def get_distance(center, point):
	return np.sqrt(np.square(center[0] - point[0]) + np.square(center[1]-point[1]))

# def draw_degree_distance(n):
# 	for s in ctr.allsegs[n]:
# 		for d in s:
# 			plt.plot(get_radian(ct, d), get_distance(ct, d), '.')
# 	plt.show

def draw_dgree_distance(n, ctr, ct):
	x = []
	y = []
	for s in ctr.allsegs[n]:
		for d in s:
			x.append(get_radian(ct,d))
			y.append(get_distance(ct,d))
		df = pd.DataFrame({"x":x, "y":y}).sort_values("x")
		plt.plot(df["x"], df["y"])

def createGraph(ctr, saveUrl):
	ct = get_center(ctr)
	for i in range(len(ctr.allsegs)):
		draw_dgree_distance(i, ctr, ct);
		plt.savefig(saveUrl + "/distance_graph_"+str(i)+".png");
		clearPlot(plt)
# plt.show();



def computeData(saveUrl, fileUrl):
	hdu_list = fits.open(fileUrl)
	os.mkdir(saveUrl)
	image_data = hdu_list[1].data
	hdu_list.close()
	data = image_data.GALAXY[0]
	ctr = plt.contour(image_data['GALAXY'][0], 25, linewidth=0.3)
	plt.savefig(saveUrl + "/galaxy_contour.png");
	clearPlot(plt)
	plt.imshow(data);
	plt.savefig(saveUrl + "/galaxy_rgb.png");
	clearPlot(plt)
	createGraph(ctr, saveUrl)


computeData("test_2", "data/refined_0034.fits")
