// Hello, I'm sorry about this code.
// We were originally using polymer but it turns out it's more or less incompatible with
// jQuery UI and a lot of our pre-made CSS stuff. So we ditched it.
// And now we have this. Ugly code that works.
// I hope.
// -- Keaton

// PUBLISHED EVENTS
//   edited: Runs when the content of a bunny changes
//    added: Runs when a new bunny is added to either list
//  created: Runs when a new bunny is created in either list
//  removed: Runs when a bunny is deleted
//   pulled: Runs when another user's bunny is dragged in

function editor(bunnies, mainUL, suggestUL){
	var edit = this;
	
	// EDITING UI METHODS
	
	// Turns a static element into an editable box
	this.startEdit = function(pObject){
        if(pObject === undefined)return;
		if("target" in pObject)pObject=pObject.target;
		console.log(pObject);
		if($(pObject).hasClass("ph")){$(pObject).html("");$(pObject).removeClass("ph");}
		$(pObject).parent().removeAttr("static");
		var newObject = $("<textarea onkeyup=\"autoResize(this)\" class='"+$(pObject).attr("class")+"'>"+$(pObject).html()+"</textarea>");
		$( pObject ).replaceWith(newObject);
		$( newObject ).height($(newObject)[0].scrollHeight);
		$( newObject ).focus();	
	}
	
	// Takes an editable box and turns it back into a static element
	this.finishEdit = function(taObject){
        if(taObject === undefined)return;
		if("target" in taObject)taObject=taObject.target;
		$(taObject).parent().attr("static","true");
		if($(taObject).val()==""||$(taObject).val()==" "){$(taObject).val("Double-click to edit");$(taObject).addClass("ph");}
		var pObject = $("<p class='"+$(taObject).attr("class")+"'>"+$(taObject).val()+"</p>");
		$( taObject ).replaceWith(pObject);
		$( pObject ).parent().trigger("edited");
	}
	
	// BUNNY MANAGEMENT

	this.main = mainUL;
	this.suggest = suggestUL;
	
	// Add a bunny given its HTML representation as text
	this.addBunnyInternal = function(ulList,nodeText,shouldEdit){
		if(ulList === undefined)ulList = $(this.main);
		var newNode = $(nodeText);
		$(ulList).append(newNode);
		if(shouldEdit)edit.startEdit($(ulList.lastChild).children(".ti")[0]);
		$(ulList).last().children("textarea.ti").focus();
	}
	
	// Add a bunny from data
	this.addBunny = function(ulList,bunnyObject){
		if(bunnyObject===undefined)return;
		edit.addBunnyInternal(ulList,'<li id="bunny-'+bunnyObject.id+'" bunny-id="'+bunnyObject.id+'"\
		class="span12 bunny '+((bunnyObject.creator==1)?'mine':'other')+'" style="-webkit-animation: add 300ms;" static="true">\
		'+((bunnyObject.head)?'<p class="ti head">'+bunnyObject.head+'</p>':'<p class="ti head ph">Double-click to add header</p>')+'\
		<p class="ti ct">'+bunnyObject.body+'</p>\
		<div class="close">X</div></li>',false);
		$(ulList).children().last().trigger("added");
	}
	
	// Add a new blank bunny
	this.newBunny = function(ulList){
        if(ulList === undefined || ulList.target !== undefined)ulList = $(this.main);
		edit.addBunnyInternal(ulList,'<li class="span12 bunny mine" style="-webkit-animation: add 300ms;">\
		<p class="ti head ph">Double click to add title</p><p class="ti ct ph">Edit content</p>\
		<div class="close">X</div></li>',true);
		setTimeout(function(){$(ulList).children().last().trigger("created");},10);
	}
	
	// Add multiple bunnies to a list
	this.setBunniesInternal = function(ulList,bunnies){
		for(bid in bunnies){
			edit.addBunny(ulList,bunnies[bid]);	
		}
	}
	
	// Set our main bunnies	
	this.setBunnies = function(bunnies){
		edit.data = bunnies;
		edit.setBunniesInternal(this.main,bunnies);
	}
	this.setBunnies(bunnies);
	
	// Set out bunny suggestions
	this.setSuggestions = function(bunnies){
		edit.setBunniesInternal(edit.suggest,bunnies);
	}
	
	
	// Remove a bunny from its list
	this.deleteBunny = function(element){
		if($(element).hasClass("toDelete")){
			$(element).trigger("removed");
			$(element).remove();
		}else{
			$(element).css('-webkit-animation', 'remove 300ms');
			$(element).bind('webkitAnimationEnd',function(){
				$(element).trigger("removed");
				$(element).remove();
			});
		}
	}
	
	// Update the text of a bunny, if it exists
	this.updateBunny = function(bunnyObject){
		var elem = $("#bunny-"+bunnyObject.id);
		if(elem.length==0)return;
		$("#bunny-"+bunnyObject.id+" .head").html(bunnyObject.head);
		$("#bunny-"+bunnyObject.id+" .ct").html(bunnyObject.body);
	}
	
	// Helper function gets data from a DOM object
	this.dataFromDOMBunny = function(domBunny){
		var bunnyData = this.data[$(domBunny).attr("bunny-id")];
		if(!bunnyData)return;
		bunnyData.head = $(domBunny).children(".head").html();
		bunnyData.body = $(domBunny).children(".ct").html();
		return bunnyData;
	}
	
	// EVENT BINDING
	this.start = function(){
		// Helper method for jQuery UI Drag-n-drop deletion
		var dontDelete = function(e,obj){
			$(".toDelete").removeClass("toDelete");
			setTimeout(function(){$(".toDelete").removeClass("toDelete");},10);
		}
		
		// jQuery UI Drag-n-Drop setup
		$( "#myBunnies" ).sortable({
			dropOnEmpty: true,
			distance: 15,
			
			// Handles drag-to-delete
			out: function(e,obj){$(obj.item[0]).addClass("toDelete");},
			over: dontDelete, stop: dontDelete,
			
			beforeStop: function(e,obj){
				if($(obj.item[0]).hasClass("toDelete")){
					$(obj.item[0]).trigger("removed");
					return $(obj.item[0]).remove();
				}
				if($(obj.item[0]).hasClass("other") && !$(obj.item[0]).hasClass("pulled")){
					$(obj.item[0]).addClass("pulled");
					$(obj.item[0]).trigger("pulled");
				}
			},
			update: function(e,obj){
				dontDelete();
				var j = $(obj.item[0]);
				j.trigger("order");
				if(j.hasClass("other") && j.attr("bound")==undefined){
					j.trigger("bind");
				}
			}
		});
		$( "#otherBunnies" ).sortable({
			connectWith: "#myBunnies",
			dropOnEmpty: true,
		});
		$( "#myBunnies,#otherBunnies" ).disableSelection();
		 
		// Setup basic event handlers
		$( "body" ).on("dblclick","p.ti",this.startEdit);
		$( "body" ).on("change blur focusout","textarea.ti,input.ti",this.finishEdit);
		 
		// Setup tab handlers
		$( "body" ).on("keydown","textarea.ti",function(e){
			if(e.keyCode == 9){ // User tabbed to next field
				e.preventDefault();
				if(!event.shiftKey){
					// Forwards tabbing
					if($(this).next(".ti")[0]!=undefined){
						edit.startEdit($(this).next(".ti")[0]);
						$(this).next("textarea.ti").focus();
					}else if($(this).parent().nextAll(".mine")[0]!=undefined){
						edit.startEdit($(this).parent().nextAll(".mine").children(".ti")[0]);
						$(this).parent().nextAll(".mine").children("textarea.ti").focus();
					}else{edit.newBunny($(this).parents("ul")[0]);}
				}else{
					// Backwards tabbing
					if($(this).prev(".ti")[0]!=undefined){
						edit.startEdit($(this).prev(".ti")[0]);
						$(this).prev("textarea.ti").focus();
					}else if($(this).parent().prevAll(".mine").first()!=undefined){
						edit.startEdit($(this).parent().prevAll(".mine").first().children(".ti").last()[0]);
						$(this).parent().prevAll(".mine").first().children("textarea.ti").last().focus();
					}
				}
			}
		});
		
		$("body").on("click",".close",function(e){
			edit.deleteBunny(e.target.parentElement);
		});
		
		$("body").on("webkitAnimationEnd","li",function(event){
			$(event.target).removeAttr("style");
		});
		
		// GLUE CODE TO UPDATE THE MODEL
		$("body").on("edited",".bunny",function(event){
			console.log(edit.dataFromDOMBunny(event.target));
		});
	}
}

// Special behavior to resize text areas to fit content
function autoResize(ta){
	ta.style.height = "1px";
	ta.style.height = (20+ta.scrollHeight)+"px";
};