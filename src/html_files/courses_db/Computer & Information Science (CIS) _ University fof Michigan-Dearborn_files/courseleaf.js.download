//Default template js
//Store custom client js in /js/custom.js, and import to template.
var edition = edition;
var bubblewidth = 450;
function showCourse(domobj, which) {
	if (typeof coursebubblewidth == "undefined") {
		if(typeof bubblewidth == "undefined")
			var coursebubblewidth = 400;
		else
			var coursebubblewidth = bubblewidth;
	}
	function showCourseReady(req) {
		if($(req).find("course").length) {
			var html = $(req).find("course").text();
		} else {
			var html = "<p>Course information cannot be found. This course may " +
				"no longer be offered. If you believe there is an error or " +
				"require more information, please contact the course " +
				"department.</p>";
		}
		lfjs.bubble(domobj, html, {width:coursebubblewidth});
	}
	function showCourseError(req) {
		var html = "<p>An error occurred trying to load course information.  Please try your request again later. (" + req.status + " - " + req.statusText + ")</p>";
		lfjs.bubble(domobj, html, {
			width: coursebubblewidth
		});
	}
	domobj.blur();
	if(typeof ribbiturl == "undefined" ||
			window.location.host.indexOf(".leepfrog.com") >= 0 ||
			window.location.host.indexOf(".editcl.com") >= 0) {
		ribbiturl = "/ribbit/index.cgi";
	}
	var gcurl = ribbiturl + "?page=getcourse.rjs&code=" + encodeURIComponent(which);
	//if there is an edition var defined, use that in the getCourse call
	if(typeof edition == "string" && edition.length) {
		gcurl += "&edition=" + encodeURIComponent(edition);
	}
	$.ajax({
		url:gcurl,
		success:showCourseReady,
		error:showCourseError
	});
	lfjs.bubble(domobj, "Loading course description...", {width:coursebubblewidth});
	return false;
}

function showCourseEco(domobj, which) {
	if (typeof ecobubblewidth == "undefined") {
		if(typeof bubblewidth == "undefined")
			var ecobubblewidth = 600;
		else
			var ecobubblewidth = bubblewidth;
	}
	function showCourseEcoReady(req) {
		if($(req).find("courseeco").length) {
			var html = $(req).find("courseref").text();
		} else {
			var html = "<p>Unable to load course ecosystem.</p>";
		}
		lfjs.bubble(domobj, html, {width:ecobubblewidth});
	}
	function showCourseEcoError(req) {
		var html = "<p>An error occurred trying to load the course ecosystem." +
				"  ( " + req.status + " - " + req.statusText + ")</p>";
		lfjs.bubble(domobj, html, {
			width: ecobubblewidth
		});
	}
	domobj.blur();
	if(typeof ribbiturl == "undefined" || window.location.host.indexOf(".leepfrog.com") >= 0)
		ribbiturl = "/ribbit/index.cgi";
	$.ajax({
		url: ribbiturl + "?page=getcourseeco.rjs&" +
			(typeof lf === "object" && ! lf.progname ? "prod=true&" : '') +
			"code=" + encodeURIComponent(which),
		success:showCourseEcoReady,
		error:showCourseEcoError
	});
	lfjs.bubble(domobj, "Loading course ecosystem...", {width:ecobubblewidth});
	return false;
}

function printParent(el, removeel) {
	if (typeof removeel == "undefined")
		removeel = true;
	var html = $(el).parents("div:first").html();
	//strip out el
	if (removeel) {
		var outhtml = $("<p>").append($(el).clone()).html();
		html = html.replace(outhtml, "");
	}
	var new_win = window.open("","ppwin","resizable,height=300,width=450,scrollbars");
	new_win.document.write('<html><head><title>Course Detail</title></head><body>' +
		html + '</body></html>');
	new_win.document.close();
	$("link").each(function() {
		if(this.rel == "stylesheet") {
			$(new_win.document).find("head").append($(this).clone());
			$(new_win.document).find("body").css({"background-image": "none", "background-color": "white", "padding": "5px"});
		}
	})
	new_win.focus();
	new_win.print();
	new_win.close();
}

function showGenedCourselist(aEl) {
	var par = $(aEl).parents("table:first");
	if(!par.length)
		return;
	var head = $(aEl).attr("id").replace(/link$/, "");
	if (par.find('#' + head + 'courselist').length) {
		par.find('#' + head + 'courselist').slideToggle()
	} else {
		$(aEl).append('<div id="' + head + '" class="hiddencourselist">No Courses Defined For This Area</div>').slideDown();
	}
	$(aEl).parent("td").toggleClass("expanded");
	return false;
}

function escXML(str) {
	if(typeof str == "undefined")
		return "";
	var newStr = str.replace(/\&/g,'&amp;');
	newStr = newStr.replace(/\"/g,'&quot;');
	newStr = newStr.replace(/\</g,'&lt;');
	newStr = newStr.replace(/\>/g,'&gt;');

	return newStr;
}

//Tabs
$(function() {
	$(".tab_content").each(function() {
		var name = this.id.replace(/container$/, "")
		$(this).find("a[name='" + name + "']").remove();
	});
	if(typeof defshow != 'undefined')
		updateTabs(defshow);
	var page = window.location.href.replace(/\#.*$/, "").replace(/\/[^\/]*$/, "/");
	if(typeof bodycontainer == 'undefined')
		var bodycontainer = '#content';
	if(typeof validhashes == 'undefined')
		var validhashes = '';
	$(bodycontainer).find("a").each(function() {
		var href = $(this).attr("href");
		if(href) {
			var cleanhref = href.replace(page, "").replace(/^\#/, "");
			$(this).data("cleanhref", cleanhref);
			if(href.indexOf("#") == 0 && validhashes.indexOf("," + cleanhref + ",") != -1) {
				$(this).click(function(event) {
					showSection($(this).data("cleanhref"));
				});
			}
		}
	});

	// arrow key funtionality added to tabs
	$("#tabs a").keydown(function(e) {
		var key = lfjs.keypress.getNonPrintableChar(e);
		overflowTabs.keynav = true;
		switch(key) {
			case "LEFT":
			case "UP":
				var $tabParents = $(this).parents("li");
				if($tabParents.first().hasClass("tab-isoverflow")
						&& !$tabParents.first().is(":first-child")) {
					$tabParents.first().prev().find("a").click();
				} else {
					overflowTabs.hide();
					$tabParents.last().prev().find("a").click();
				}
				e.preventDefault();
				break;
			case "RIGHT":
			case "DOWN":
				if($(this).parent("li").next("li").hasClass("tab-overflow")
						|| $(this).parent("li").hasClass("tab-isoverflow")) {
					overflowTabs.show();
				} else {
					overflowTabs.hide();
				}
				$(this).parent("li").next().find("a").first().click();
				e.preventDefault();
				break;
			case "HOME":
				$(this).parents("ul").last().children("li").first().find("a").first().click();
				e.preventDefault();
				break;
			case "END":
				$(this).parents("ul").children("li").last().find("a").last().click();
				e.preventDefault();
				break;
			case "ENTER":
				$(this).click();
				e.preventDefault();
				break;
			case "TAB":
				overflowTabs.hide();
				//purposefully no break

			default:
				overflowTabs.keynav = false;
				return true;
		}
	});

	//ctrl+page up/down functionality to switch to prev or next tab within .tab_content
	//only supported by Windows FF as of July 2017
	$(".tab_content").keydown(function(e) {
		var key = lfjs.keypress.getNonPrintableChar(e);
		switch(key) {
			case "Ctrl+PGUP":
				$("#tabs li.active").prev("li").find("a").click();
				e.preventDefault();
				break;
			case "Ctrl+PGDN":
				$("#tabs li.active").next("li").find("a").click();
				e.preventDefault();
				break;
		}
	});

	overflowTabs.init();

	var $window = $(window);
	var windowWidth = $window.width();
	$window.resize(function() {
		if($window.width() != windowWidth) {
			overflowTabs.init();
			windowWidth = $window.width();
		}
	});
});

var _showsectclick = false;
var _currotp = false;

$(function () {
	var dest = window.location.hash.replace(/^\#/, '');
	var isTab = (dest) ? $("#" + escXML(dest) + "container").length > 0 : false ;
	// If destination is defined and is not a tab, take control of scrolling
	// else make sure scrollRestoration = auto
	if (dest && !isTab && 'scrollRestoration' in history) {
		history.scrollRestoration = 'manual'
		// lf.noscroll is used by pwtoolbar to set the scroll to the last scroll
		// position. This happens after the scroll here, so we turn it off.
		if (lf) lf.noscroll = true;
	} else if ('scrollRestoration' in history) {
		history.scrollRestoration = 'auto';
	}
	navigateToHash(dest, true);
});

function navigateToHash(dest, isOnReadyNavigation) {
	dest = dest || window.location.hash.replace(/^\#/, '');
	if (!dest) return false;
	// Tab navigation
	if( $("#" + escXML(dest) + "container").length &&
		$("#" + escXML(dest) + "container").hasClass("tab_content") &&
		$("#" + escXML(dest) + "container").is(":hidden")) {
		showSection(dest);
		return true;
	}

	// On This Page navigation
	if (/(.*)-otp(\d+)$/.test(dest)) {
		showSection(RegExp.$1, { otp: RegExp.$2} );
		return true;
	}

	// Inner Tab navigation
	// Try by id first, fall back to anchor with name
	var $innerTab = $("#" + escXML(dest));
	if ($innerTab.length === 0) {
		$innerTab = $('a[name="'+escXML(dest)+ '"]');
	}
	if ($innerTab.length) {
		// Find parent tab
		var $parentTab = $innerTab.closest('div[role="tabpanel"]');
		var section = '';
		// If can't find parent tab, it's probably because there is only one tab. If there *are* tabs, it means we didn't find one successfully; bail.
		if ($parentTab.length === 0 && $('div[role="tabpanel"]').length) return;
		// If we found the parent tab, set that tab as our section. showSection will activate that tab and scroll to context.
		if ($parentTab.length) section = $parentTab.attr('id').replace(/container$/, '');
		// If we have only one tab, then section==='' still. That's intended, showSection will leave tabs alone and simply scroll the anchor into view.
		var context = {
			innerTab: {
				target: $innerTab[0], isOnReadyNavigation: isOnReadyNavigation
			}
		};
		showSection(section, context);
		return true;
	}

	return false;
}

window.onhashchange = function () {
	navigateToHash();
};

function cleanHash(str) {
	return str.replace(/^\#/, "");
}
var anchorOffset = 0;
function showSection(section, context) {
	_showsectclick = true;
	var sectionchange = false;
	$("#" + escXML(section) + "tab").find("a").blur();
	$("#" + escXML(section) + "tab").find("a").attr("target", "");

	var loc = window.location.href;
	var overrideLoc = true;
	// if changing tabs
	if(!$("#" + escXML(section) + "tab").hasClass("active")) {
		$(".tab_content").not("#" + escXML(section) + "container").hide();
		$("#" + escXML(section) + "container").show();
		updateTabs(section);
		loc = loc.replace(/\#[^\#]*$/, "") + "#" + section;
		sectionchange = true;
		$("li#" + escXML(section) + "tab a").focus();
	} else {
		//give focus anyway
		$("#" + escXML(section) + "tab a").focus();
	}

	// scroll to element if calling link has nav-id attribute
	// special case for otp-id attribute on same page
	var navid = false;
	var otpid = false;
	if (context) {
		if ("otp" in context) {
			loc = loc.replace(/\#[^\#]*$/, "") + "#" + section;
			var el = document.getElementsByName("otp" + context.otp);
				if(el[0]) {
					var pos = findPos(el[0]);
					pos[0] -= anchorOffset;
					window.scrollTo(0,pos);
				}
		} else if ("innerTab" in context) {
			overrideLoc = false;
			var target = context.innerTab.target;
			var isOnReadyNavigation = context.innerTab.isOnReadyNavigation;
			var pos = findPos(target);
			pos[0] -= anchorOffset;
			var ua = window.navigator.userAgent;
			if (isOnReadyNavigation &&
				(ua.indexOf('MSIE ') > 0 || ua.indexOf('Trident/') > 0)) {
				// Internet explorer insists on resetting the scroll position
				// but only when we are logged in. If this is onReadyNavigation,
				// and we are logged in, and this is internet explorer,
				// we'll insist on setting the scroll position three times before
				// quitting.
				var resets = 0;
				var maxResets = 2;
				var insistPos = function () {
					if (resets > 0 && document.cookie.indexOf("wizauth=") < 0) {
						return;
					}
					pos = findPos(target);
					pos[0] -= anchorOffset;
					window.scrollTo(0, pos);
					resets++;
					if (resets <= maxResets) {
						$(window).one('scroll', function () {
							setTimeout(insistPos, 10);
						});
					}
				}
				insistPos();
			} else {
				window.scrollTo(0, pos);
			}
		} else {
			navid = context.getAttribute("nav-id");
			otpid = context.getAttribute("otp-id");
			// if referenced from different otp element, add to browser history
			if (!sectionchange && otpid != _currotp && typeof history.pushState == 'function') {
				history.replaceState({}, "", "#" + section + "-otp" + otpid);
			}
			_currotp = otpid;
			if (navid && navid != -1) {
				var els = document.getElementsByName(section);
				for (var i = 0; i < els.length; i++) {
					if (els[i].getAttribute("headerid") == navid) {
						var pos = findPos(els[i]);
						pos[0] -= anchorOffset;
						window.scrollTo(0,pos);
						break;
					}
				}
			}
		}
	}

	// push to history if HTML5 supported browser
	if (window.onhashchange) {
		if (sectionchange && overrideLoc) {
			window.location.assign(loc);
		}
	} else if (overrideLoc) {
		window.location.replace(loc);
	}
	if(typeof resizeMe == "function")
		resizeMe();

	return false;
}
function updateTabs(section) {
	$("#tabs li").not("#" + escXML(section) + "tab").removeClass("active");
	$("#tabs li a").not("#" + escXML(section) + "tab").attr({"aria-selected":"false","tabindex":"-1"});
	$(".tab_content").attr("aria-hidden","true");

	$("#" + escXML(section) + "tab").addClass("active");
	$("#" + escXML(section) + "tab a").attr({"aria-selected":"true","tabindex":"0"});
	$(".tab_content#" + escXML(section) + "container").attr("aria-hidden","false");

	//deal with overflow tabs
	if($("#" + escXML(section) + "tab").hasClass("tab-isoverflow")) {
		$("#" + escXML(section) + "tab").closest("li.tab-overflow").addClass("active-sub");
	} else {
		$("#tabs li.tab-overflow").removeClass("active-sub");
	}

	if(!overflowTabs.keynav)
		overflowTabs.hide();
}

var overflowTabs = {
	//global vars
	enabled: false,
	label: "More",
	label_solo: "Page sections",
	keynav: false,
	curSoloTab: false,
	base: function() {
		return $("#tabs > ul > li").position().top;
	},
	initTabsHeight: function() {
		return $("#tabs").outerHeight();
	},

	//functions
	hide: function() {
		$("#tabs li.tab-overflow").removeClass("open");
		if(!this.curSoloTab)
			$("#tabs").removeClass("condense");
		return false;
	},
	show: function() {
		$("#tabs li.tab-overflow").addClass("open");
		if($("#overflowtabs").offset().left < 0) {
			$("#tabs").addClass("condense");
		}
		$(document.body).click(function(e) {
			if($(e.target).closest("#tabs li.tab-overflow").length < 1) {
				overflowTabs.hide();
			}
		});
	},
	click: function() {
		if($("#tabs li.tab-overflow").hasClass("open")) {
			overflowTabs.hide();
		} else {
			overflowTabs.show();
		}
		return false;
	},
	keypress: function(e) {
		overflowTabs.keynav = true;
		$("#overflowTabsButton").unbind('keydown').bind('keydown',function(e) {
			var key = lfjs.keypress.getNonPrintableChar(e);
			switch(key) {
				case "LEFT":
				case "UP":
					$(this).parent("li").prev("li").find("a").click();
					e.preventDefault();
					break;
				case "RIGHT":
				case "DOWN":
					overflowTabs.show();
					$(this).next("ul").children("li").first().find("a").click();
					e.preventDefault();
					break;
				case "HOME":
					$(this).parents("ul").last().children("li").first().find("a").click();
					e.preventDefault();
					break;
				case "END":
					$(this).parents("ul").children("li").last().find("a").last().click();
					e.preventDefault();
					break;
				case "ENTER":
					$(this).click();
					e.preventDefault();
					break;
				default:
					overflowTabs.keynav = false;
					return true;
			}
		});
	},
	create: function() {
		//insert area
		$("#tabs ul").append("<li class='tab-overflow' role='presentation'><button id='overflowTabsButton' tabindex='-1' aria-hidden='true'>" + overflowTabs.label + "</button><ul role='presentation' id='overflowtabs'></ul></li>");
		//bind keypress events
		overflowTabs.keypress();
		//bind click event
		$("#overflowTabsButton").click(overflowTabs.click);
		//when focus is brought back from content area
		$("#overflowtabs").focusin(function() {
			if(!$("#tabs li.tab-overflow").hasClass("open")) {
				overflowTabs.show();
			}
		});
	},
	remove: function() {
		$("#tabs li.tab-overflow").remove();
		$("#tabs").removeClass("overflow-active");
	},
	initSolo: function() {
		$("#overflowTabsButton").text(this.label_solo);
		$("#overflowTabsButton").parent("li").addClass("tab-solo");
		$("#tabs").addClass("condense");
		this.curSoloTab = true;
	},
	termSolo: function() {
		$("#overflowTabsButton").text(overflowTabs.label);
		$("#overflowTabsButton").parent("li").removeClass("tab-solo");
		$("#tabs").removeClass("condense");
		this.curSoloTab = false;
	},
	process: function() {
		//indentify overflowed tabs and place into overflow container
		$($("#tabs > ul > li").not(".tab-overflow").get().reverse()).each(function() {
			var offsetTop = $(this).position().top;
			if(offsetTop > overflowTabs.base()) {
				if(!$("#tabs li.tab-overflow").length) {
					overflowTabs.create();
				}
				$(this).addClass("tab-isoverflow");
				$("#overflowtabs").prepend($(this));
			} else {
				$(this).removeClass("tab-isoverflow"); //needed?
				return false;
			}
		});
		//check to see if overtab tab has overflowed
		if($("li.tab-overflow").position().top > overflowTabs.base()) {
			overflowPrevious();

			if($("li.tab-overflow").position().top > overflowTabs.base() || $("#tabs > ul > li").length === 1) {
				overflowPrevious();
				//this is the only remaining one
				this.initSolo();
			} else {
				this.termSolo();
			}
		}

		$("#tabs").addClass("overflow-active");
		if($("#overflowtabs").children("li.active").length) {
			$("li.tab-overflow").addClass("active-sub");
		}
		this.initTabsHeight = $("#tabs").outerHeight();

		function overflowPrevious() {
			var lastNormal = $("#tabs > ul > li.tab-overflow").prev()[0];
			$(lastNormal).addClass("tab-isoverflow");
			$("#overflowtabs").prepend($(lastNormal));
		}
	},
	watchChanges: function() {
		var isOverflow = false;
		$("#tabs > ul > li").each(function() {
			if($(this).position().top > overflowTabs.base()) {
				isOverflow = true;
				return false;
			}
		});
		if(isOverflow) {
			overflowTabs.process();
		} else if($("#overflowtabs").length > 0) {
			var tmpSolo = false;
			if(overflowTabs.curSoloTab) {
				tmpSolo = true;
				this.termSolo();
			}
			$("#overflowtabs li").each(function() {
				$(this).detach();
				$(this).insertBefore("#tabs li.tab-overflow");

				if(!$("#overflowtabs").children().length) {
					var btn = $("#tabs li.tab-overflow").detach();
					if($("#tabs").outerHeight() > overflowTabs.initTabsHeight) {
						$("#tabs > ul").append(btn);
						$("#overflowtabs").prepend($(this));
						return false;
					} else {
						$("#tabs > ul").append(btn);
					}
				} else {
					if($("#tabs").outerHeight() > overflowTabs.initTabsHeight) {
						$("#overflowtabs").prepend($(this));
						return false;
					} else {
						$(this).removeClass("tab-isoverflow");
						tmpSolo = false;
					}
				}
			});
			if(tmpSolo) {
				this.initSolo();
			} else {
				$("#tabs").removeClass("condense");
			}
			if(!$("#overflowtabs").children().length) {
				this.remove();
			}
		}
	},
	init: function() {
		if(this.enabled) {
			setTimeout(function() { overflowTabs.watchChanges(); }, 35);
		}
	}
}
//end tabs

// Toggle Headers
$(function() {
	var toggleBreakElems = [];
	var i = 0;
	$('#content :header.toggle,.page_content :header.toggle').each(function(i){
		var groupedElems = [];
		var headerLevel = parseInt($(this).attr("tagName").replace(/\D+/g, '')); //replace .attr with .prop for new jquery
		for(var j = headerLevel; j>1; j--) {
			toggleBreakElems.push("H"+j);
		}
		var next = $(this).next();
		while(next.length > 0 && $.inArray($(next[0]).attr("tagName"),toggleBreakElems) < 0) {
			var end = false;
			toggleBreakElems.forEach(function(tag) {
				if($(next).find(tag).length > 0 || $(next).hasClass("togglebreak")) {
					end = true;
				}
			});
			if(end === true)
				break;
			groupedElems.push($(next)[0]);
			next = next.next();
		}
		//wrap the elements
		$(groupedElems).wrapAll("<div class='toggle-content' />");
		//wrap the .toggle heading + the content
		$(this).next('.toggle-content').andSelf().wrapAll("<div class='toggle-wrap' />");
		//assign an id to the content wrap for a11y
		var id = 'tgl' + i;
		$(this).next('.toggle-content').attr({'aria-hidden':'true','id':id});
		var panel = $(this).next('.toggle-content');
		// Add the button inside the <h2> so both the heading and button semanics are read
		$(this).wrapInner('<button aria-expanded="false" aria-controls="'+ id +'">');
		//toggle the content and related attrs
		var button = $(this).children('button');
		button.click(function(){
			$(this).parent().toggleClass('expanded');
			flipAria($(this),panel);
		});
		toggleBreakElems = []; //reset list of headers to break on
		i++;
	});
	
	//group each set of toggle headers
	$('#content :not(.toggle-wrap) + .toggle-wrap,.page_content :not(.toggle-wrap) + .toggle-wrap').each(function() {
		$(this).nextUntil(':not(.toggle-wrap)').andSelf().wrapAll('<div class="toggle-group" />');
	});

	// expand content corresponding to any anchor tag in URL visited
	if(window.location.hash) {
		var hash = escXML(window.location.hash.slice(1));
		toggleHeaderAnchor(hash);
	}
	$(window).bind('hashchange', function(e) {
		var hash = escXML(window.location.hash.slice(1));
		toggleHeaderAnchor(hash);
	});
	function toggleHeaderAnchor(hash) {
		var target = "";
		if($(":header#"+hash+".toggle").length > 0) {
			target = $(":header#"+hash+".toggle");
		} else if($("a#"+hash).length > 0) {
			target = $("a#"+hash).parent("button");
		}
		if(target.length) {
			$(target).click();
			$('html,body').animate({scrollTop: $("#" + hash).offset().top},'fast');
		}
	}
});
// end Toggle Headers

//Search Form Helper
//Ensure caturl parameter is useful in combination with pagebasedir
$(function() {
	var param = getURLParameter("caturl");
	var catURLFields = document.querySelectorAll('input[name="caturl"],input[name="gscaturl"],input[name="fscaturl"]');
	if(catURLFields.length) {
		for(var i = 0; i < catURLFields.length; i++) {
			var field = catURLFields[i];
			if(field.value === "/search" || field.value === "/") {
				if(param && param.length)
					field.value = param;
				else
					field.parentNode.removeChild(field);
			}
		};
	}
	function getURLParameter(param) {
		var sPageURL = window.location.search.substring(1),
			sURLVariables = sPageURL.split('&'),
			sParameterName,
			i;
		for (i = 0; i < sURLVariables.length; i++) {
			sParameterName = sURLVariables[i].split('=');
			if (sParameterName[0] === param) {
				return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
			}
		}
	}
});

function flipAria(elem,target,state) {
	if(state === undefined) {
		var state = $(elem).attr('aria-expanded') === 'false' ? true : false;
	}
	$(elem).attr('aria-expanded', state);
	$(target).attr('aria-hidden', !state);
}

function dataToggle(elem,state) {
	if(state === undefined) {
		var state = $(elem).attr('aria-expanded') === 'false' ? true : false;
	}
	var target = $(elem).attr("data-toggle");
	var animate = false;
	if($(elem).attr("data-toggle-animate") === "true")
		animate = true;
	
	if(state) {
		$(elem).addClass("active");
		$(target).addClass("active");
		if(animate)
			$(target).slideDown(true);
	} else {
		$(elem).removeClass("active");
		$(target).removeClass("active");
		if(animate)
			$(target).slideUp(true);
	}
	
	flipAria(elem,target,state);
}

function showPrintDialog() {
	var pd = $('#print-dialog');
	if (!pd || !pd[0])
		return;
	pd[0].activate({
		keyhandler: lfjs.window.defaultKeyHandler,
		focus: 'a:eq(0)'
	});
}
function hidePrintDialog() {
	if($("#print-dialog").length)
		$('#print-dialog')[0].deactivate();
}
function findPos(obj) {
	var curtop = 0;
	if (obj.offsetParent) {
		do {
			curtop += obj.offsetTop;
		} while (obj = obj.offsetParent);
	}
	return [curtop];
}
