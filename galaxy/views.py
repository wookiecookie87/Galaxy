from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import Galaxy_Image
from .models import Graph_Info
from os import listdir
from django.conf import settings
from random import randint
import os


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
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
	y_axis_min = []
	y_axis_max = []
	graph_name = []
	for i in range(len(ctr.allsegs)):
		draw_dgree_distance(i, ctr, ct);
		graph_num = "/distance_graph_"+str(i)
		plt.savefig(saveUrl + graph_num + ".png");
		axes = plt.gca()
		clearPlot(plt)
		graph_name.append(graph_num)
		y_axis_min.append(axes.get_ylim()[0])
		y_axis_max.append(axes.get_ylim()[1])
	return {"y_min" : y_axis_min, "y_max" : y_axis_max, "graph_name" : graph_name}



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
	graph_info = createGraph(ctr, saveUrl)
	y_min = graph_info["y_min"]
	y_max = graph_info["y_max"]
	graph_name = graph_info["graph_name"]
	return {"len" : len(ctr.allsegs), "graph_name" : graph_name, "y_min" : y_min, "y_max" : y_max}

def index(request):
	CURR_PATH = os.path.dirname(os.path.realpath(__file__))
	data_path = os.path.dirname(os.path.realpath(__file__))+"/data"
	# for f in listdir(CURR_PATH+"/data"):
	# 	fileName = f.split(".")
	# 	image = Galaxy_Image(file_name = fileName[0], computed = "false")
	# 	image.save()
	randNum = randint(3224, 4692)
	image_file = Galaxy_Image.objects.get(id=randNum).file_name
	file_url = data_path+"/"+image_file+".fits"
	save_url = CURR_PATH+"/static/data_image/"+image_file
	graph_count = 0

	if(Graph_Info.objects.filter(file_name=image_file)):
		print("it is already computed")
	else:
		print(save_url)
		graph_info = computeData(save_url, file_url)
		y_min = graph_info["y_min"]
		y_max = graph_info["y_max"]
		graph_name = graph_info["graph_name"]
		graph_count = graph_info["len"]
		for i in range(graph_info["len"]):
			graph = Graph_Info(file_name=image_file, graph_count=graph_count, graph_name=graph_name[i], y_min=y_min[i], y_max=y_max[i])
			graph.save()
	
	galaxy_image = image_file+"/galaxy_rgb.png"
	distance_graph = image_file+"/distance_graph_0.png"
	context = {
		'galaxy_image' : galaxy_image,
		'distance_graph' : distance_graph,
		'image_file' : image_file,
		'graph_num' : 1,
		'graph_count' : graph_count
	}

	return render(request, 'galaxy/index.html', context)


def next(request, image_file, graph_num, graph_count):
	galaxy_image = image_file+"/galaxy_rgb.png"
	distance_graph = image_file+'/distance_graph_'+str(graph_num)+".png"
	
	context = {
		'galaxy_image' : galaxy_image,
		'distance_graph' : distance_graph,
		'image_file' : image_file,
		'graph_num' : int(graph_num) + 1,
		'graph_count' : graph_count
	}
	return HttpResponse(json.dumps(context), content_type="application/json")

def actionData(request, image_file, graph_num, graph_count, point_1_x, point_1_y, point_2_x, point_2_y):
	galaxy_image = image_file+"/galaxy_rgb.png"
	graph_name = '/distance_graph_'+str(graph_num);
	distance_graph = image_file+graph_name+".png"
	graph_data = Graph_Info.objects.filter(file_name = image_file, graph_name = graph_name)
	if graph_data:
		print(graph_data.y_min)

	context = {
		'galaxy_image' : galaxy_image,
		'distance_graph' : distance_graph,
		'image_file' : image_file,
		'graph_num' : int(graph_num) + 1,
		'graph_count' : graph_count
	}


	return HttpResponse(json.dumps(context), content_type="application/json")

