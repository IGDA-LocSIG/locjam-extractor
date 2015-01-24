jQuery(function(){
	var __data = [];
	var lang = langs[0];
	
	window.twine_trans = function(row){
		return __data[row];
	}

	function load_lang(lang){
		jQuery.get(lang+".txt", function(data){
			__data = data.split("\n");
			jQuery("div#storeArea").find("div").each(function(e,i){
				var msg = jQuery(this).data("trans");
				var splat = jQuery(this).data("split");
				if (msg !== undefined){
					if (msg.indexOf("twine_trans")>=0){
						try{
							msg = eval(msg);
						} catch (e){}
						if (splat !== undefined){
							msg = msg + __data[splitline] + __data[splitline+1+splat]
						}
						jQuery(this).text(msg);
					}
				}
			});
		});

		setTimeout(
			function(){
				jQuery(window.document.body).trigger("load");
			}, 1000);
	}

	load_lang(langs[0]);

	if (langs.length>1){
		var appendable = jQuery("<li id='lang'><select id='t_select'></select></li>");
		for (var i in langs){
			appendable.find("#t_select").append("<option value='"+langs[i]+"'>"+langs[i]+"</option>");
		}
		jQuery("#sidebar").append(appendable);
		jQuery(window.document).on("change", "#t_select", function(){
			load_lang(jQuery("#t_select").val());
		});
	}
	
});
