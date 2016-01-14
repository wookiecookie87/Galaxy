var graphInfo = function(){
	this.graph_file = null;
	this.graph_num = null;
	this.graph_count = null;
	this.y_min = 0.0;
	this.y_max = 0.0;
	this.x_min = 0;
	this.x_max = 0;
	this.points = [];
	this.xy_values = [];
	this.x_value = 0.0;
	this.y_value = 0.0;
	// this.x_value_1 = 0.0;
	// this.y_value_1 = 0.0;
	// this.x_value_2 = 0.0;
	// this.y_value_2 = 0.0;
};

graphInfo.prototype = {
	init : function(){
		var self = this;
		self.setGraph();
		$(".btn-skip").on("click", function(){
			self.clearGraph();
			if(parseInt(self.graph_num) == parseInt(self.graph_count)){
				if(confirm("Data set completed. Would you like to go to next data set?")){
					$(".btn-skip").attr("disabled", "disabled");
					location.href = "/galaxy";
					return ;
				}	
			}

			self.callNext();

		});

		$(".btn-save").on("click", function(){
			if($(".marker").length < 2){
				alert("You must pick 2 highest points.");
				return ;
			}

			if(parseInt(self.graph_num) == parseInt(self.graph_count)){
				if(confirm("Data set completed. Would you like to go to next data set?")){
					$(".btn-save").attr("disabled", "disabled");
					location.href = "/galaxy";
					return ;
				}
			}
			self.callSave();
			self.clearGraph();
		});

		$(".cover-wrap").on("click", function(e){
			if($(".marker").length >=2 ){
				alert("You must pick 2 highest points.");
				return ;
			}
			self.drawMarker(e);
			// if($(".marker").length ===2 ){
			// 	self.convertPoints();
			// }
		});

		$(".btn-retry").on("click", function(){
			self.clearGraph();
		})
	},

	setData : function(graph_file, graph_num, graph_count, y_min, y_max, x_min, x_max){
		this.graph_file = graph_file;
		this.graph_num = graph_num;
		this.graph_count = graph_count;
		this.y_min = y_min;
		this.y_max = y_max;
		this.x_min = x_min;
		this.x_max = x_max;
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
				$("#distance-graph").css("background", "url('/static/data_image/"+data.distance_graph+"') no-repeat -49px 5px");
				$("#distance-graph").css("background-size", "388px");
				$("#graph-count").html(data.graph_count);
				$("#graph-num").html(data.graph_num);
				self.setData(data.image_file, data.graph_num, data.graph_count, data.y_min, data.y_max, data.x_min, data.x_max);
			}
		});
	},

	setGraph : function(){
		var self = this
		self.loading();
		var url = "/galaxy/data";
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			success: function(data){
				console.log(data);
				$("#galaxy-image").css("background", "url('/static/data_image/"+data.galaxy_image+"') no-repeat -255px -150px");
				$("#distance-graph").css("background", "url('/static/data_image/"+data.distance_graph+"') no-repeat -49px 5px");
				$("#distance-graph").css("background-size", "388px");
				$("#graph-count").html(data.graph_count);
				$("#graph-num").html(data.graph_num);
				self.setData(data.image_file, data.graph_num, data.graph_count, data.y_min, data.y_max, data.x_min, data.x_max);
				self.loadingComplete()
			}
		});
	},

	callSave : function(){
		var self = this;
		var point_1 = this.points[0]
		var point_2 = this.points[1]

		var heightX = 300
		var heightY = 233;
		var url = "/galaxy/" + this.graph_file + "/" + this.graph_num + "/" + this.graph_count + "/" +
				this.xy_values[0].x + "/" + this.xy_values[0].y + "/" + this.xy_values[1].x + "/" + this.xy_values[1].y;

		this.callAjax(url, self);

		this.clearData();
	},

	convertPoints : function(point){
		// var point_1 = this.points[0]
		// var point_2 = this.points[1]
		var heightX = 300
		var heightY = 233;

		var x_value = (this.x_max - this.x_min)/ heightX * point.x;
		var y_value = (this.y_max - this.y_min) / heightY * (heightY - point.y) + this.y_min;
		
		this.x_value= (Math.round(x_value * 100) / 100).toFixed(2);
		this.y_value = (Math.round(y_value * 100) / 100).toFixed(2);
		
		this.xy_values.push({x: this.x_value, y: this.y_value})

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
		this.convertPoints(point);
		var rad = this.x_value * Math.PI / 180;

		var x = this.y_value * Math.sin(rad);
		var y = this.y_value * Math.cos(rad);

		alert(rad+"  " +x+"  "+y);
		//var contourmarker = '<div class="contour-marker" style="width: 10px; height: 10px; border:1px solid black; border-radius: 10px;background: yellow;position: absolute; top:'+(yPoint-5)+';left:'+(xPoint-5)+'"></div>';
		//$(".cover-wrap").append(marker);
	}, 

	saveData : function(point){
		this.points.push(point)
	},

	clearData : function(){
		this.points = [];
		this.xy_values = [];
	},

	loading : function(){
		$(".loading-bar").addClass("show");
	},

	loadingComplete : function(){
		$(".loading-bar").removeClass("show");
	}
};

