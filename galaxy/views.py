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
	return len(ctr.allsegs)

def index(request):
	CURR_PATH = os.path.dirname(os.path.realpath(__file__))
	data_path = os.path.dirname(os.path.realpath(__file__))+"/data"
	# for f in listdir(CURR_PATH+"/data"):
	# 	fileName = f.split(".")
	# 	image = Galaxy_Image(file_name = fileName[0], computed = "false")
	# 	image.save()
	randNum = randint(3224, 4692)
	image_file = Galaxy_Image.objects.get(id=randNum).file_name
	#file_name = image_file+".fits"
	file_url = data_path+"/"+image_file+".fits"
	save_url = CURR_PATH+"/static/data_image/"+image_file
	graph_count = 0

	if(Graph_Info.objects.filter(file_name=image_file)):
		print("it is already computed")
	else:
		print(save_url)
		graph_count = computeData(save_url, file_url)
		graph = Graph_Info(file_name=image_file, graph_count=graph_count)
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

	# latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# context = {
	# 	'latest_question_list' : latest_question_list,
	# }
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

def actionData(request, image_file, graph_num, graph_count):
	galaxy_image = image_file+"/galaxy_rgb.png"
	distance_graph = image_file+'/distance_graph_'+str(graph_num)+".png"
	
	#points = json.loads(request.POST.get('points'))

	context = {
		'galaxy_image' : galaxy_image,
		'distance_graph' : distance_graph,
		'image_file' : image_file,
		'graph_num' : int(graph_num) + 1,
		'graph_count' : graph_count
	}


	return HttpResponse(json.dumps(context), content_type="application/json")

