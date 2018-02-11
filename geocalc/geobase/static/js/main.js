		var map = L.map('map').setView([51.505, 71.00], 7);

		var hybridMutant = L.gridLayer.googleMutant({maxZoom: 24, type:'hybrid'});
		var roadMutant = L.gridLayer.googleMutant({maxZoom: 24, type:'roadmap'}).addTo(map);
	    var satMutant = L.gridLayer.googleMutant({maxZoom: 24, type:'satellite'});
	    L.control.layers({'Гибрид': hybridMutant, 'Карта': roadMutant, 'Спутник': satMutant}, {}, {collapsed: false}).addTo(map);

	    var grid = L.gridLayer({attribution: 'Grid Layer',});

	    grid.createTile = function (coords) {
	      var tile = L.DomUtil.create('div', 'tile-coords');
	      tile.innerHTML = [coords.x, coords.y, coords.z].join(', ');

	      return tile;
	    };

	    map.addLayer(grid);

	    function NEHtoWGS84(point_set){
	    	var NEH = new tNEH(point_set.X, point_set.Y, 0.0);
	    	var csset = pointtable.cssets[point_set.csid]
	    	var wgs84 = new datum (csset.datum);
	    	var pr = new proj (csset.proj);
	    	var mBLH = NEHtoBLH(wgs84, pr, NEH);
	    	var mXYZ = BLHtoXYZ(wgs84, mBLH);
	    	var wXYZ = XYZ2toXYZ1(wgs84, mXYZ);
	    	return XYZtoBLH(wgs84, wXYZ);
	    	//return mBLH;
	    }

	    function getCoord(){
	    	var coord = {};
	    	coord.pointname = document.getElementById("point_name").value;
	    	document.getElementById("point_name").value = '';
	    	coord.csid = document.getElementById("csset").value;
	    	coord.X = parseFloat(document.getElementById("north").value);
	    	document.getElementById("north").value = '';
	    	coord.Y = parseFloat(document.getElementById("east").value);
	    	document.getElementById("east").value = '';
	    	return coord;
	    }

	    var pointtable = new Vue({
	    	el: '#pointtable',
	    	delimiters: ['<<', '>>'],
	    	data: {
	    		points: [],
	    		cssets: cstable
	    	},
	    	methods:{
	    		addPointItem: function(){
	    			this.addPoints(getCoord());
	    		},
	    		removePointItem: function(index){
	    			map.removeLayer(this.points[index].marker);
	    			this.points.splice(index, 1);
	    		},
	    		zoomPointItem: function(index){
	    			var BLH = NEHtoWGS84(this.points[index]);
	    			map.setView([BLH.B, BLH.L], 21);
	    		},
	    		addPoints: function(point_set){
	    			var BLH = NEHtoWGS84(point_set);
	    			var marker = L.marker([BLH.B, BLH.L]);
	    			map.addLayer(marker);
	    			point_set.marker = marker;
	    			this.points.push(point_set);
	    		},
	    		closeProject: function(){
	    			document.getElementById('pointtable').style.display = "none";
	    		}
	    	}
	    });

	    for(var i = 0; i<pointbase.length; i++){
	    	pointtable.addPoints(pointbase[i]);
	    }

	    $("#projectform").submit(function (event) { //устанавливаем событие отправки для формы с id=appl-form
                event.preventDefault();
                var pointdata = JSON.stringify(pointtable.points, ["pointname", "csid", "X", "Y"])
                var form_data = $("#projectform").serialize() +'&project_points='+pointdata; //собераем все данные из формы
                $.post('', form_data, function (data) {
                    alert(data.project_url);
                    location = data.project_url;
                    });
            });

	    var saveclass = null;

		function saveTheme(cookieValue)
		{
		    var sel = document.getElementById('csset');

		    saveclass = saveclass ? saveclass : document.body.className;
		    document.body.className = saveclass + ' ' + sel.value;

		    setCookie('csset', cookieValue, 365);
		}

		function setCookie(cookieName, cookieValue, nDays) {
		    var today = new Date();
		    var expire = new Date();

		    if (nDays==null || nDays==0)
		        nDays=1;

		    expire.setTime(today.getTime() + 3600000*24*nDays);
		    document.cookie = cookieName+"="+escape(cookieValue) + ";expires="+expire.toGMTString();
		}

		function readCookie(name) {
		  var nameEQ = name + "=";
		  var ca = document.cookie.split(';');
		  for(var i = 0; i < ca.length; i++) {
		    var c = ca[i];
		    while (c.charAt(0) == ' ') c = c.substring(1, c.length);
		    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
		  }
		  return null;
		}

		document.getElementById('csset').value = readCookie('csset');