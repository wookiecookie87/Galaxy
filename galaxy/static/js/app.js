var graphInfo = function(){
	this.graph_file = null,
	this.graph_num = null,
	this.graph_count = null,
	this.points = []
};

graphInfo.prototype = {
	setData : function(graph_file, graph_num, graph_count){
		this.graph_file = graph_file;
		this.graph_num = graph_num;
		this.graph_count = graph_count;
	},

	callNext : function(){
		var self = this;
		var url = "/galaxy/"+this.graph_file+"/"+this.graph_num+"/"+this.graph_count;
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			success: function(data){
				console.log(data);
				$("#distance-graph").css("background", "url('/static/data_image/"+data.distance_graph+"') no-repeat -55px -15px");
				$("#distance-graph").css("background-size", "435px");
				$("#graph-num").html(data.graph_num);
				self.setData(data.image_file, data.graph_num, data.graph_count);
			}
		});
	},

	checkGraph : function(){
		if(parseInt(this.graph_num) == parseInt(this.graph_count)){
			$(".btn-save").attr("disabled", "disabled");
			location.href = "/galaxy";
			return ;
		}
	},

	callSave : function(){
		var self = this;
		var point_1 = this.points[0]
		var point_2 = this.points[1]
		var url = "/galaxy/"+this.graph_file+"/"+this.graph_num+"/"+this.graph_count+"/"+
				point_1.x+"/"+point_1.y+"/"+point_2.x+"/"+point_2.y;

		$.ajax({
			type: "GET",
			url: url,
			//data: {point_1 : JSON.stringify(point_1), point_2 : JSON.stringify(point_2)},
			dataType: "json",
			success: function(data){
				console.log(data);
				$("#distance-graph").css("background", "url('/static/data_image/"+data.distance_graph+"') no-repeat -55px -15px");
				$("#distance-graph").css("background-size", "435px");
				$("#graph-num").html(data.graph_num);
				self.setData(data.image_file, data.graph_num, data.graph_count);
			}
		});
	},

	clearGraph : function(){
		$(".cover-wrap").empty();
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
	}

};