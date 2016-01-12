var graphInfo = function(){
	this.graph_file = null;
	this.graph_num = null;
	this.graph_count = null;
	this.y_min = 0.0;
	this.y_max = 0.0;
	this.points = []
};

graphInfo.prototype = {
	setData : function(graph_file, graph_num, graph_count, y_min, y_max){
		this.graph_file = graph_file;
		this.graph_num = graph_num;
		this.graph_count = graph_count;
		this.y_min = y_min;
		this.y_max = y_max;
	},

	callNext : function(){
		var self = this;
		var url = "/galaxy/"+this.graph_file+"/"+this.graph_num+"/"+this.graph_count;
		this.callAjax(url, self);

		this.clearData();
	},

	checkGraph : function(){
		if(parseInt(this.graph_num) == parseInt(this.graph_count)){
			$(".btn-save").attr("disabled", "disabled");
			location.href = "/galaxy";
			return ;
		}
	},

	callAjax : function(url, self){
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			success: function(data){
				console.log(data);
				$("#distance-graph").css("background", "url('/static/data_image/"+data.distance_graph+"') no-repeat -55px -15px");
				$("#distance-graph").css("background-size", "435px");
				$("#graph-count").html(data.graph_count);
				$("#graph-num").html(data.graph_num);
				self.setData(data.image_file, data.graph_num, data.graph_count, data.y_min, data.y_max);
			}
		});
	},

	setGraph : function(){
		var self = this
		var url = "/galaxy/data";
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			success: function(data){
				console.log(data);
				$("#galaxy-image").css("background", "url('/static/data_image/"+data.galaxy_image+"') no-repeat -255px -150px");
				$("#distance-graph").css("background", "url('/static/data_image/"+data.distance_graph+"') no-repeat -55px -15px");
				$("#distance-graph").css("background-size", "435px");
				$("#graph-count").html(data.graph_count);
				$("#graph-num").html(data.graph_num);
				self.setData(data.image_file, data.graph_num, data.graph_count, data.y_min, data.y_max);
			}
		});
	},

	callSave : function(){
		var self = this;
		var point_1 = this.points[0]
		var point_2 = this.points[1]

		x_value_1 = (2 * Math.PI / 300) * point_1.x;
		y_value_1 = (this.y_max - this.y_min) / 260 * (260 - point_1.y) + this.y_min;
		x_value_2 = (2 * Math.PI / 300) * point_2.x;
		y_value_2 = (this.y_max - this.y_min) / 260 * (260 - point_2.y) + this.y_min;
		
		x_value_1 = (Math.round(x_value_1 * 100) / 100).toFixed(2);
		y_value_1 = (Math.round(y_value_1 * 100) / 100).toFixed(2);
		x_value_2 = (Math.round(x_value_2 * 100) / 100).toFixed(2);
		y_value_2 = (Math.round(y_value_2 * 100) / 100).toFixed(2);

		var url = "/galaxy/" + this.graph_file + "/" + this.graph_num + "/" + this.graph_count + "/" +
				x_value_1 + "/" + y_value_1 + "/" + x_value_2 + "/" + y_value_2;

		this.callAjax(url, self);

		this.clearData();
	},

	clearGraph : function(){
		$(".cover-wrap").empty();
		this.clearData();
	},

	drawMarker : function(e){
		var posX = $(".cover-wrap").offset().left;
		var posY = $(".cover-wrap").offset().top;
		var xPoint = e.pageX - posX;
		var yPoint = e.pageY - posY;
		var point = {x: Math.ceil(xPoint), y: Math.ceil(yPoint)};
		var marker = '<div class="marker" style="width: 10px; height: 10px; border:1px solid black; border-radius: 10px;background: yellow;position: absolute; top:'+(yPoint-5)+';left:'+(xPoint-5)+'"></div>';
		$(".cover-wrap").append(marker);
		this.saveData(point);
	}, 

	saveData : function(point){
		this.points.push(point)
	},

	clearData : function(){
		this.points = [];
	}

};