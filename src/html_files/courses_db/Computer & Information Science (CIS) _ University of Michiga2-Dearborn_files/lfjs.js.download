/**
 * LFJS
 * Version: 20150520
 * Build: 20150520110720
 * Commit: 316d36dd1f39e4aadfaa00a61273f1d5f090a31c
 * Branch: master
 */

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind
if (!Function.prototype.bind) {
	Function.prototype.bind = function (oThis) {
		if (typeof this !== 'function') {
			// closest thing possible to the ECMAScript 5
			// internal IsCallable function
			throw new TypeError('Function.prototype.bind - what is trying to be bound is not callable');
		}

		var aArgs = Array.prototype.slice.call(arguments, 1),
			fToBind = this,
			fNOP = function () {
			},
			fBound = function () {
				return fToBind.apply(this instanceof fNOP
						? this
						: oThis,
					aArgs.concat(Array.prototype.slice.call(arguments)));
			};

		fNOP.prototype = this.prototype;
		fBound.prototype = new fNOP();

		return fBound;
	};
}
var lfjs = {};

// Utility functions

lfjs.isdocumentready = false;
lfjs.path = '';
lfjs.version = 20150520;
$(function() {
	lfjs.isdocumentready = true;
	lfjs.path = $("script[src$='lfjs.js']:first").attr("src").replace(/\/[^\/]*$/, "");
});

lfjs.rfcdate2jsdate = function(in_date) {
	var work_arr = in_date.split(' ');
	var ret_date = new Date(work_arr[2] + " " + work_arr[1] + ", " +
		work_arr[3] + " " + work_arr[4]);
	ret_date.setHours(ret_date.getHours() - ret_date.getTimezoneOffset() / 60);
	return ret_date;
};

lfjs.displayDate = function(in_date, format) {
	var month_arr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
						'Sep', 'Oct', 'Nov', 'Dec'];
	if (!in_date)
		return "";
	var showtime = true;
	if(format == "notime")
		showtime = false;
	var work_str = "";
	if (format && format == "nice") {
		return month_arr[in_date.getMonth()] + " " + in_date.getDate() +
			", " + in_date.getFullYear() + " " + (in_date.getHours() % 12 == 0 ?
			"12" : in_date.getHours() % 12) +  ":" +
			(100 + in_date.getMinutes()).toString().substring(1) +
			(in_date.getHours() < 12 ? "am" : "pm");
	}
	//support for any format containing %y,%Y,%m,  and %d (i.e. %m/%d/%Y or %Y-%m-%d), %F (full date %Y-%m-%d),
	//		%D (full date %m/%d/%y), %H (hour 00-23), %I (hour 01-12), %k (hour 0-23), %l (hour 1-12),
	//		%M (minute 00-59), %S (seconds 00-60), %p (AM or PM), %P (am or pm);
	if(format && /\%[yYmdFDHIklM]{1}/.test(format)) {
		var shortmonth, shortday, shorthour, hour12hr, shorthour12hr, shortmin;
		var year = in_date.getFullYear();
		var shortyear = (year + "").replace(/.*(\d{2})$/, "$1");
		var month = shortmonth = in_date.getMonth() + 1;
		var hour = shorthout = hour12hr = shorthour12hr = in_date.getHours();
		var minutes = in_date.getMinutes();
		var secs = in_date.getSeconds();
		if(hour < 12)
			var ampm = "AM";
		else
			var ampm = "PM"

		if(hour % 12 == 0)
			var hour12hr = shorthour12hr = 12;
		else
			var hour12hr = shorthour12hr = hour % 12;
		if(hour12hr < 10)
			hour12hr = "0" + hour12hr;
		if(month < 10)
			month = "0" + month;
		var day = shortday = in_date.getDate();
		if(day < 10)
			day = "0" + day;
		if(hour < 10)
			hour = "0" + hour;
		if (minutes < 10)
			minutes = "0" + minutes;
		if(secs < 10)
			secs = "0" + secs;
		var retval = format;
		retval = retval.replace(/%F/g, year + "-" + month + "-" + day).replace(/%D/g, month + "/" + day + "/" + shortyear);
		retval = retval.replace(/%Y/g, year).replace(/%y/g, shortyear).replace(/%m/g, month).replace(/%d/g, day);
		retval = retval.replace(/%H/g, hour).replace(/%I/g, hour12hr).replace(/%k/g, shorthour).replace(/%l/g, shorthour12hr);
		retval = retval.replace(/%M/g, minutes).replace(/%M/g, minutes).replace(/%S/g, secs);
		retval = retval.replace(/%p/g, ampm).replace(/%P/g, ampm.toLowerCase());
		return retval;
	}
	var now = new Date();
	var hours_old = Math.abs((now - in_date.getTime()) / 1000 / 60 / 60);
	if ((hours_old < 9 ||
			(hours_old < 24 && now.getDate() == in_date.getDate())) && showtime) {
		if (in_date.getHours() % 12 == 0)
			work_str += "12";
		else
			work_str += in_date.getHours() % 12;
		work_str += ":" +
			(100 + in_date.getMinutes()).toString().substring(1);
		if (in_date.getHours() < 12)
			work_str += "am";
		else
			work_str += "pm";
	} else if (hours_old > (24*30*6) && !showtime) {
		work_str += month_arr[in_date.getMonth()] + " " +
			in_date.getFullYear();
	} else {
		work_str += month_arr[in_date.getMonth()] + " " +
			in_date.getDate();
	}
	return work_str;
};

lfjs.toDate = function(in_datestr) {
	// yyyy-mm-dd
	var format1 = /^(\d{4})\-(\d{1,2})\-(\d{1,2})$/;
	// mm/dd/yyyy
	var format2 = /^(\d{1,2})\/(\d{1,2})\/(\d{2,4})$/;

	if(format1.test(in_datestr)) {
		var res = format1.exec(in_datestr);
		return new Date(parseInt(res[1],10), (parseInt(res[2],10)-1), parseInt(res[3], 10));
	} else if(format2.test(in_datestr)) {
		var res = format2.exec(in_datestr);
		var thisyear = new Date().getFullYear() + "";
		var year = res[3];
		if(year.length == 2) {
			//use this year as a cutoff for 2000 vs. 1900
			var test = parseInt(thisyear.replace(/.*(\d{2})$/, "$1"),10);
			if(parseInt(year,10) <= test)
				year = "20" + year;
			else
				year = "19" + year;
		} else if (year.length != 4) {
			year = thisyear;
		}
		return new Date(parseInt(year,10), (parseInt(res[1],10)-1), parseInt(res[2], 10));
	}
	return new Date(in_datestr);
};

lfjs.makeTextDiv = function(in_contents, in_class) {
	var div = document.createElement("div");
	if (in_class && in_class.length)
		div.className = in_class;
	div.appendChild(document.createTextNode(in_contents));
	return div;
}

lfjs.cleanHTML = function(in_str) {
	return in_str.replace(/&/g, "&amp;").replace(/</g, "&lt;");
};

lfjs.addEvent = function(el, evname, func) {
	if (typeof el.addEventListener == "function") {
		el.addEventListener(evname, func, true);
	} else {
		el.attachEvent("on" + evname, func);
	}
};

lfjs.removeEvent = function(el, evname, func) {
	if (typeof el.removeEventListener == "function") {
		el.removeEventListener(evname, func, true);
	} else {
		el.detachEvent("on" + evname, func);
	}
};

lfjs.getStyleValue = function (el, property) {
	var cs, val = false;
	// Webkit, Firefox, IE9+
	if (window.getComputedStyle) {
		cs = getComputedStyle(el, null);
		val = cs[property];
	} else if (el.currentStyle) {
		// < IE9
		val = el.currentStyle[property];
	}
	return val;
};


lfjs.scrollToShow = function(selEl, parentEl) {
	//Only works in FF if position is set to "relative" of "absolute"
	// Step 1: position item in the parent div
	// Step 2: if item is offscreen, scroll screen
	if(typeof selEl == "string")
		selEl = document.getElementById(selEl);

	var scrollGap = selEl.clientHeight / 2;
	if(typeof parentEl == "undefined") {
		// Find the first parent who has overflow set to "scroll"
		for (parentEl = selEl.parentNode;
				parentEl.tagName.toLowerCase() != "body";
				parentEl = parentEl.parentNode) {
         var overflow = lfjs.getStyleValue(parentEl, 'overflow');
         if (overflow.indexOf("scroll") >= 0 ||
               overflow.indexOf("auto") >= 0) {
            break;
         }
      }
	} else if(typeof parentEl == "string")
		parentEl = document.getElementById(parentEl);

	if (parentEl == document.body) {
		var selOffset = $(selEl).offset();
		var selHeight = $(selEl).outerHeight();
		var winHeight = $(window).height();
		var curScroll = $(document).scrollTop();

		if (selOffset.top + selEl.offsetHeight > winHeight + curScroll) {
			$(document).scrollTop(
					selOffset.top + selHeight - winHeight + scrollGap);
			return;
		}
		if (selOffset.top < curScroll)
			$(document).scrollTop(selOffset.top - scrollGap);
	} else {
		if(selEl.offsetTop + selEl.offsetHeight >
				parentEl.scrollTop + parentEl.clientHeight) {
			parentEl.scrollTop = selEl.offsetTop + selEl.offsetHeight -
					parentEl.clientHeight + scrollGap;
		} else if(selEl.offsetTop < parentEl.scrollTop) {
			parentEl.scrollTop = selEl.offsetTop - scrollGap;
		}
	}
};

lfjs.setSelectedIndex = function(domobj, value) {
	for (var i=0; i < domobj.options.length; i++) {
		if (domobj.options[i].value == value) {
			domobj.selectedIndex = i;
			return true;
		}
	}
	return false;
}
/*global lfjs*/

/**
 * Base64 Encoding and decoding functions
 */
lfjs.base64 = (function base64IIFE() {
	'use strict';

	var base64 = {};
	var chars = [
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
		'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '/'
	];

	/**
	 * Decode a base 64 encoded string
	 *
	 * @param {string} which The base 64 encoded string
	 * @returns {string} The decoded string
	 */
	base64.decode = function base64Decode(which) {
		var binary = '', result = '';

		for (var x = 0; x < which.length; x++) {
			for (var y = 0; y < chars.length; y++) {
				if (which.charAt(x) === chars[y]) {
					binary += String('000000' + y.toString(2)).
						substring(y.toString(2).length);
				}
			}
		}

		for (var i = 0; i < binary.length; i += 8) {
			var number = 0, counter = 0;
			for (var j = 0; j < binary.substring(i, i + 8).length; j++) {
				for (var k = 128; k >= 1; k -= (k / 2)) {
					if (binary.substring(i, i + 8).charAt(counter++) === '1') {
						number += k;
					}
				}
			}
			if (number > 0) {
				result += String.fromCharCode(number);
			}
		}

		return result;
	};

	/**
	 * Base 64 encode a string
	 *
	 * @param {string}  which The string to encode
	 * @returns {string} The encoded string
	 */
	base64.encode = function base64Encode(which) {
		var binary = '', result = '';

		for (var x = 0; x < which.length; x++) {
			binary += String('00000000' + which.charCodeAt(x).
				toString(2)).substring(which.charCodeAt(x).
					toString(2).length);
		}

		for (var i = 0; i < binary.length; i += 6) {
			var number = 0, counter = 0;
			for (var j = 0; j < binary.substring(i, i + 6).length; j++) {
				for (var k = 32; k >= 1; k -= (k / 2)) {
					if (binary.substring(i, i + 6).charAt(counter++) === '1') {
						number += k;
					}
				}
			}
			result += chars[number];
		}

		return result;
	};

	return base64;
})();
// lfjs.keypress.installhandler(func)
// lfjs.keypress.stuff(keystring)

lfjs.keypress = {
	installhandler: function(func) {
		var oldhandler;
		if (document.onkeypress) {
			var tmpfunc = document.onkeypress;
			oldhandler = tmpfunc("GETFUNC");
		}
		if (!func) {
			document.onkeypress = null;
			if (document.all || $.browser.webkit)
				document.onkeydown = null;
			return oldhandler;
		}
		var keyhandler = func;
		document.onkeypress = function(in_key) {
			if (in_key && in_key == "GETFUNC")
				return keyhandler;
			return lfjs.keypress.keypresshandler(in_key, keyhandler);
		};
		if (document.all || $.browser.webkit) {
			document.onkeydown = function(in_key) {
				return lfjs.keypress.keydownhandler(in_key, keyhandler);
			};
		}
		return oldhandler;
	},

	stuff: function(keystr) {
		if (document.onkeypress) {
			var handler = document.onkeypress;
			return handler(keystr);
		} else {
			return false;
		}
	},

	// Remaining functions are private
	getNonPrintableChar: function(event) {
		var keyCode = event.keyCode;
		var keyStr = "";
		switch (keyCode) {
			case 112: keyStr += "F1"; break;
			case 113: keyStr += "F2"; break;
			case 114: keyStr += "F3"; break;
			case 115: keyStr += "F4"; break;
			case 116: keyStr += "F5"; break;
			case 117: keyStr += "F6"; break;
			case 118: keyStr += "F7"; break;
			case 119: keyStr += "F8"; break;
			case 120: keyStr += "F9"; break;
			case 121: keyStr += "F10"; break;
			case 122: keyStr += "F11"; break;
			case 123: keyStr += "F12"; break;
			case 38: keyStr += "UP"; break;
			case 40: keyStr += "DOWN"; break;
			case 37: keyStr += "LEFT"; break;
			case 39: keyStr += "RIGHT"; break;
			case 33: keyStr += "PGUP"; break;
			case 34: keyStr += "PGDN"; break;
			case 36: keyStr += "HOME"; break;
			case 35: keyStr += "END"; break;
			case 13: keyStr += "ENTER"; break;
			case 9: keyStr += "TAB"; break;
			case 27: keyStr += "ESC"; break;
			case 8: keyStr += "BACKSPACE"; break;
			case 46: keyStr += "DEL"; break;
			//ignore these here
			case 16: //shift 
			case 17: //ctrl  
			case 18: //alt   
			case 20: //caps lock
				keyStr = "";
				break;
		}
		
		if(keyStr != "") {
			if(event.shiftKey)
				keyStr = "Shift+" + keyStr;
			if(event.ctrlKey || event.ctrlLeft)
				keyStr = "Ctrl+" + keyStr;
			if(event.altKey || event.altLeft)
				keyStr = "Alt+" + keyStr;
		}
			
		return keyStr;
	},

	keystring: function(in_key) {
		if (typeof in_key == "string")
			return in_key;
		if (typeof in_key == "undefined")
			in_key = window.event;

		var keyStr = "";
		var key_code = in_key.keyCode;
		if (!key_code)
			key_code = in_key.charCode;
		if (typeof in_key.charCode == "undefined")
			in_key.charCode = in_key.keyCode;
		if (in_key.charCode != null && in_key.charCode != 0 && key_code > 30) {
			if (in_key.ctrlKey || in_key.ctrlLeft || in_key.metaKey)
				keyStr += "Ctrl+";
			if (in_key.altKey || in_key.altLeft)
				keyStr += "Alt+";
			keyStr += String.fromCharCode(key_code);
		} else {
			keyStr += lfjs.keypress.getNonPrintableChar(in_key);
		}
		return keyStr;
	},

	keydownhandler: function(event, funcname) {
		// IE uses keydown to catch unprintable characters; ignore the
		//    function if keydown was not unprintable
		if (typeof event == "undefined")
			event = window.event;
		var which = lfjs.keypress.getNonPrintableChar(event);
		if (which.length && !funcname(which)) {
			event.returnValue = false;
			event.cancelBubble = true;
			event.keyCode = 0;
			return false;
		}
		return true;
	},

	keypresshandler: function(in_key, funcname) {
		// Check to see if keypress was lfjs.keypress.stuff'd
		if (typeof in_key == "string")
			return funcname(in_key);
		// Mozilla and IE (for regular keys) use keypress
		if (!funcname(lfjs.keypress.keystring(in_key))) {
			if (!in_key) {
				in_key = window.event;
				in_key.returnValue = false;
				in_key.cancelBubble = true;
				in_key.keyCode = 0;
			}
			if (in_key.stopPropagation)
				in_key.stopPropagation();
			if (in_key.preventDefault)
				in_key.preventDefault();
			in_key.returnValue = false;
			return false;
		}
		return true;
	}
};
lfjs.window = function(domobj) {
	domobj.mvc = this;
	domobj.activate = function (a) { return this.mvc.activate(a); };
	domobj.deactivate = function () { return this.mvc.deactivate(); };
	$(domobj).addClass("inactivescreen");
	var role = $(domobj).attr('role');
	if (!role) {
		$(domobj).attr('role', 'dialog');
	}
	this.win = domobj;
	document.body.appendChild(domobj.parentNode.removeChild(domobj));
};

lfjs.window.stack = [];

lfjs.window.zcounter = 100;

lfjs.window.prototype.activate = function(args) {
	if (lfjs.window.stack.length > 0) {
		var last_win = lfjs.window.stack[lfjs.window.stack.length-1].win;
		$(last_win).removeClass("activescreen");
		$(last_win).addClass("inactivescreen");
	} else {
		// Make the body an inactive screen
		$(document.body).addClass("inactivescreen");
	}
	$(this.win).removeClass("inactivescreen");
	$(this.win).addClass("activescreen");
	if (args && args.title) {
		var titlediv = $(this.win).find('.screentitle');
		if (titlediv.size() > 0) {
			titlediv.text(args.title);
		} else {
			var title = lfjs.makeTextDiv(args.title, "screentitle");
			this.win.insertBefore(title, this.win.firstChild);
			new lfjs.dragable(title);
		}
	}
	if (args && args.onactivate)
		this.win.onactivate = args.onactivate;
	if ($(this.win).css("visibility") == "hidden" ||
			$(this.win).css("display") == "none") {
		$(this.win).css("visibility", "hidden");
		$(this.win).css("display", "block");
		var screensize = new Object;
		if (window.innerWidth) {
			screensize.width = window.innerWidth;
			screensize.height = window.innerHeight;
		} else {
			//size appropriately for IE for Quirks vs. Standards mode
			if (document.documentElement &&
						document.documentElement.clientHeight) {
				screensize.width = document.documentElement.clientWidth;
				screensize.height = document.documentElement.clientHeight;
			} else {
				screensize.width = document.body.clientWidth;
				screensize.height = document.body.clientHeight;
			}
		}
		//Position appropriately for IE for Quirks vs. Standards mode
		var scroll = document.body.scrollTop;
		if (!scroll && document.documentElement &&
					 document.documentElement.scrollTop)
			scroll = document.documentElement.scrollTop;
		$(this.win).css({
			left: $(this.win).width() > screensize.width ? 0 :
				parseInt((screensize.width - $(this.win).width()) / 2),
			top:  $(this.win).height() > screensize.height ? scroll :
				parseInt((screensize.height - $(this.win).height()) / 3) + scroll
		});
	}
	// size and activate the modallayer
	if (!lfjs.window.modaldiv) {
		lfjs.window.modaldiv = document.createElement("div");
		//$(lfjs.window.modaldiv).text("modal");
		//document.body.insertBefore(lfjs.window.modaldiv, null);
		document.body.appendChild(lfjs.window.modaldiv);
		lfjs.window.modaldiv.id = "lfjs_modaldiv";
		$(lfjs.window.modaldiv).css(
				{position:"absolute", top:"0px", left:"0px" });
		lfjs.window.modaldiv.onclick = function() { return false; };
		lfjs.addEvent(window, "resize", lfjs.window.resizeModalDiv);
	}
	lfjs.window.resizeModalDiv();
	$(lfjs.window.modaldiv).css(
		{visibility:"visible", display:"block", zIndex:lfjs.window.zcounter++});

	if ((args && args.keyhandler) || this.win.keyhandler) {
		if (args.keyhandler === lfjs.window.defaultKeyHandler) {
			args.keyhandler = lfjs.window.defaultKeyHandler.bind(this.win);
		}

		// Don't save prior key handler if activate is called because a
		//	window on top was deactivated
		if (!this.lastkeyhandler) {
			this.lastkeyhandler =
				lfjs.keypress.installhandler((args && args.keyhandler) ?
					args.keyhandler : this.win.keyhandler);
		} else {
			lfjs.keypress.installhandler((args && args.keyhandler) ?
				args.keyhandler : this.win.keyhandler);
		}
	}
	$(this.win).css("zIndex", lfjs.window.zcounter++);
	$(this.win).css("visibility", "visible");
	lfjs.window.stack[lfjs.window.stack.length] = { win: this.win, args: args };

	if (args && args.focus) {
		this.lastFocusedElement = document.activeElement;
		$(this.win).find(args.focus).focus();
	}

	if (this.win.onactivate)
		this.win.onactivate();
};

lfjs.window.prototype.deactivate = function(args) {
	if (lfjs.window.stack.length < 1)
		return;
	$(this.win).removeClass("activescreen");
	$(this.win).addClass("inactivescreen");
	$(this.win).css("display", "none");
	var ourargs = lfjs.window.stack[lfjs.window.stack.length-1].args;
	if (this.lastkeyhandler) {
		lfjs.keypress.installhandler(this.lastkeyhandler);
		this.lastkeyhandler = null;
	} else if (ourargs && ourargs.keyhandler) {
		lfjs.keypress.installhandler(null);
	}
	lfjs.window.stack.length--;
	if (lfjs.window.stack.length > 0) {
		var prior = lfjs.window.stack[lfjs.window.stack.length-1];
		lfjs.window.stack.length--;
		prior.win.activate(prior.args);
	} else {
		$(document.body).removeClass("inactivescreen");
		$(lfjs.window.modaldiv).css("display", "none");
		lfjs.removeEvent(window, "resize", lfjs.window.resizeModalDiv);
	}

	if (this.lastFocusedElement) {
		$(this.lastFocusedElement).focus();
	}
};

// Static methods

/**
 * A default keypress handler for windows
 * De-activates the window when the user presses the ESC key
 *
 * @param {string} key
 */
lfjs.window.defaultKeyHandler = function (key) {
	switch (key) {
		case 'ESC':
			this.deactivate();
			return false;
	}

	return true;
};

lfjs.window.wait = function() {
	if (!lfjs.window.waitdiv) {
      lfjs.window.waitdiv = document.createElement("div");
      document.body.appendChild(lfjs.window.waitdiv);
      lfjs.window.waitdiv.id = "lfjs_waitdiv";
      $(lfjs.window.waitdiv).css(
            {position:"absolute", top:"0px", left:"0px", cursor:"wait" });
      lfjs.window.waitdiv.onclick = function() { return false; };
		if (lfjs.window.stack.length == 0)
			lfjs.addEvent(window, "resize", lfjs.window.resizeWaitDiv);
   }
  	lfjs.window.resizeWaitDiv();
   $(lfjs.window.waitdiv).css(
      {visibility:"visible", display:"block", zIndex:lfjs.window.zcounter++});
	lfjs.window.waitpriorhandler =
			lfjs.keypress.installhandler(lfjs.window.waitkeyhandler);
};

lfjs.window.nowait = function() {
	$(lfjs.window.waitdiv).css("display", "none");
	if (lfjs.window.stack.length == 0)
		lfjs.removeEvent(window, "resize", lfjs.window.resizeWaitDiv);
	if (lfjs.window.waitpriorhandler)
		lfjs.keypress.installhandler(lfjs.window.waitpriorhandler);
};

// Internal static functions
lfjs.window.resizeFullDiv = function(which) {
	// Remove div to let body size be what it wants
	var div = $(which);
	div.css({display:"none"});
	if(document.compatMode && document.compatMode == "CSS1Compat")
		var refEl = document.documentElement;
	else
		var refEl = document.body;
	if (refEl.scrollHeight > $(window).height())
		div.css( {height:refEl.scrollHeight, width: "100%" } );
	else
		div.css( { height:$(window).height(), width: "100%" } );
	div.css({display:"block"});
};


lfjs.window.resizeModalDiv = function() {
	lfjs.window.resizeFullDiv(lfjs.window.modaldiv);
};

lfjs.window.resizeWaitDiv = function() {
	lfjs.window.resizeFullDiv(lfjs.window.waitdiv);
};

lfjs.window.waitkeyhandler = function(in_key) {
	if (in_key == "TAB" || (in_key.length == 1 && in_key >= ' ' &&
				in_key <= '~'))
		return false;           // Ignore al-nums; allow control keys
	return true;
};

// Initialize code
$(function() {
	$('.screen').each(function(i) { new lfjs.window(this); });
	$('.screentitle').each(function(i) {
		if (!$(this).hasClass("dragable")) {
			new lfjs.dragable(this);
		}
	});
});
// automatically turn any div of type "selectgrid" into a selectgrid object
// functions: addrow, removerow, getselected, empty
// addRow(id, cols[html], args{})
//		ondblclick: function(id)
//		onclick: function(id) (default: select current row)
//		classname: classname
//		title: title

lfjs.grid = function(domobj) {
	this.div = domobj;
	this.allowHTML = true;
	domobj.mvc = this;
	domobj.addRow = function (a, b, c) { return this.mvc.addRow(a, b, c); };
	domobj.setHeaders = function (a) { return this.mvc.setHeaders(a); };
	domobj.removeRow = function (a) { return this.mvc.removeRow(a); };
	domobj.empty = function () { return this.mvc.empty(); };
	domobj.getSelectedTR = function() { return this.mvc.getSelectedTR(); }
	domobj.getSelectedIndex = function() { return this.mvc.getSelectedIndex(); }
	domobj.getSelectedId = function() { return this.mvc.getSelectedId(); }
	domobj.getSelectedData = function() { return this.mvc.getSelectedData(); }
	domobj.selectRow = function(inrow) { return this.mvc.selectRow(inrow); }
	domobj.selectNext = function(dir) { return this.mvc.selectNext(dir); }
	domobj.setData = function(a, b) { return this.mvc.setData(a, b); }
	domobj.pause = function(a) { return this.mvc.pause(a); }
	domobj.setColWidths = function(a, b) { return this.mvc.setColWidths(a, b); }
	if ($(domobj).find("table").size() < 1) {
		this.table = document.createElement("table");
		domobj.appendChild(this.table);
	} else {
		this.table = $(domobj).find("table")[0];
	}
	this.table.width = "100%";
	this.table.cellSpacing = 0;
	if ($(domobj).find("colgroup").size() < 1) {
		this.colgroup = document.createElement("colgroup");
		this.table.appendChild(this.colgroup);
	}
	if ($(domobj).find("tbody").size() < 1) {
		this.tbody = document.createElement("tbody");
		this.table.appendChild(this.tbody);
	} else {
		this.tbody = $(domobj).find("tbody")[0];
	}
	if ($(domobj).find("thead").size() < 1) {
		this.thead = document.createElement("thead");
		this.table.insertBefore(this.thead, this.tbody);
	} else {
		this.thead= $(domobj).find("thead")[0];
	}
}

// Times: 11/51 (createElement, .append())
lfjs.grid.prototype.addRow = function(id, cols, args) {
	var filter = this.filter ? this.filter : this.div.filter;
	if (filter) {
		var addrow = false;
		for (var i=0; i < cols.length; i++) {
			if (filter.test(cols[i])) {
				addrow = true;
				break;
			}
		}
		if (!addrow)
			return false;
	}
	var tr = null, doappend = true;
	if (!args || !args.fastadd) {
		$(this.tbody).children().each(function (i) {
			if (this.selectid == id) {
				tr = this;
				doappend = false;
				$(this).empty();
				return false;
			}
		});
	}
	if (!tr) {
		tr = document.createElement("tr");
		if (!(this.tbody.childNodes.length % 2))
			tr.className = "odd";
	}
	tr.selectid = id;
	tr.gridobj = this;
	var gridobj = this;
	if (args && args.data)
		tr.data = args.data;
	if (args && args.classname)
		$(tr).addClass(args.classname);
	if (args && args.onclick) {
		var clickfunc = args.onclick;
		tr.onclickfunc = clickfunc;
		tr.onclick = function() {
			var funcval = clickfunc(this.selectid, this);
			if (typeof funcval == "undefined" || funcval)
				gridobj.selectRow(this); };
	} else {
		tr.onclick = function() { gridobj.selectRow(this); };
	}
	if (args && args.ondblclick) {
		var dblfunc = args.ondblclick;
		tr.ondblclick = function() { dblfunc(this.selectid, this); };
	}
	if (args && args.title)
		tr.title = args.title;
	for (var i=0; i < cols.length; i++) {
		var td = document.createElement("td");
		if (!i && cols.length == 1)
			td.className = "firstcolumn lastcolumn";
		else if (!i)
			td.className = "firstcolumn";
		else if (i == cols.length - 1)
			td.className = "lastcolumn";
			
		if(args && args.html)
			td.innerHTML = cols[i];
		else
			td.appendChild(document.createTextNode(cols[i]));
		tr.appendChild(td);
	}
	if (doappend) {
		if (args && args.insertAfter && args.insertAfter.nextSibling)
			this.tbody.insertBefore(tr, args.insertAfter.nextSibling);
		else
			this.tbody.appendChild(tr);
	}
	return tr;
}

lfjs.grid.prototype.setHeaders = function(colobjs, args) {
	$(this.thead).empty();
	tr = document.createElement("tr");
	$(this.thead).append(tr);
	for (var i=0; i < colobjs.length; i++) {
		var th = $(document.createElement("th"));
		th.text(colobjs[i].name);
		if (colobjs[i].classname)
			th.addClass(colobjs[i].classname);
		if (colobjs[i].onclick) {
			lfjs.grid.setClickFunc(th[0], colobjs[i].onclick,
					colobjs[i].id ? colobjs[i].id : colobjs[i].name, i,
					colobjs[i].name, this.div);
		}
		if (colobjs[i].title)
			th[0].title = colobjs[i].title;
		$(tr).append(th);
	}
}

// Private function; used to get enclosures inside of loops
lfjs.grid.setClickFunc = function(in_obj, in_func, in_id, in_index,
			in_name, in_divobj) {
	var func = in_func;
	var id = in_id;
	var index = in_index;
	var name = in_name;
	var divobj = in_divobj;
	var obj = in_obj;
	obj.onclick = function() { func(id, index, name, obj, divobj) };
}

lfjs.grid.prototype.removeRow = function(which) {
	var thisobj = this;
	$(this.tbody).children().each(function(i) {
		if (this.selectid == which) {
			if ($(this).hasClass("selected") &&
						$(thisobj.tbody).children().length > 1) {
				thisobj.selectNext();
			}
			this.parentNode.removeChild(this);
			return false;
		}
	});
}

lfjs.grid.prototype.empty = function() {
	//$(this.tbody).html("");		// This was very slow; so was ".empty()"
	while (this.tbody.lastChild)
		this.tbody.removeChild(this.tbody.lastChild);
	this.div.data = null;
}

lfjs.grid.prototype.selectRow = function(which) {
	if (!which) {
		$(this.tbody).children().removeClass("selected");
		return;
	}
	if (typeof which != "object") {
		// Find the row with this ID
		var trobj = null;
		$(this.div).find("tr").each( function(i) {
			if (this.selectid == which) {
				trobj = this;
				return false;
			}
		});
		if (!trobj)
			return;
		which = trobj;
	}
	var row = $(which);
	// Shortcut to the data block
	this.div.data = row[0].data;
	row.siblings().removeClass("selected");
	row.addClass("selected");
	// Scroll up to keep header in view
	if (!which.previousSibling && this.thead.firstChild)
		which = this.thead.firstChild;
	lfjs.scrollToShow(which, this.div);
}

lfjs.grid.prototype.getSelectedAttribute = function(which) {
	var selrow = $(this.tbody).children().filter(".selected");
	if (selrow.size() == 1)
		return selrow[0][which];
	else
		return null;
}

lfjs.grid.prototype.getSelectedTR = function() {
	var selrow = $(this.tbody).children().filter("TR.selected");
	if (selrow.size() == 1)
		return selrow[0];
	else
		return null;
} 

lfjs.grid.prototype.getSelectedIndex = function() {
	var tr = $(this.tbody).children("tr.selected:first");
	if(!tr.length)
		return -1;
	return $(this.tbody).children("tr").index(tr[0]);
} 

lfjs.grid.prototype.getSelectedId = function() {
	return this.getSelectedAttribute("selectid");
}

lfjs.grid.prototype.getSelectedData = function() {
	return this.getSelectedAttribute("data");
}

lfjs.grid.prototype.selectNext = function(direction) {
	var rows = $(this.tbody).children();
	if (rows.size() == 0)		// Nothing to select
		return false;
	if (rows.size() == 1) {
		if (rows[0].onclickfunc) {
			var clickfunc = rows[0].onclickfunc;
			clickfunc(rows[0].selectid, rows[0]);
		}
		this.selectRow(rows[0]);
		return true;
	}
	var newrow = null;
	rows.each(function(i) {
		if ($(this).hasClass("selected")) {
			if (!direction || direction > 0)
				i++;
			else
				i--;
			if (i < 0)
				i = 0;
			if (i >= rows.size())
				i = rows.size() - 1;
			newrow = rows[i];
			return false;
		}
	});
	if (!newrow && (!direction || direction > 0))
		newrow = rows[0];
	else if (!newrow)
		newrow = rows[rows.size()-1];
	this.selectRow(newrow);
	if (newrow.onclickfunc) {
		var clickfunc = newrow.onclickfunc;
		clickfunc(newrow.selectid, newrow);
	}
	return true;
}

lfjs.grid.prototype.setColWidths = function(widths, args) {
	if (args && args.runonce && $(this.colgroup).children().size() > 0)
		return;
	$(this.colgroup).empty();
	for (var i=0; i < widths.length; i++) {
		var newcol = document.createElement("col");
		newcol.width = widths[i];
		$(this.colgroup).append(newcol);
	}
}

lfjs.grid.generation_counter = 0;

lfjs.grid.prototype.setData = function(rows, args) {
	// If there is a "setinfo", then we let that timer do our work
	var skipcall = true;
	if (!this.setinfo)
		skipcall = false;
	if (!args)
		args = new Object();
	this.setinfo = { rows: rows, insfunc: args.insfunc,
			donefunc: args.donefunc, offset: 0, fetchoffset:0,
			fetchurl: args.fetchurl, fetchdisplay:args.fetchdisplay,
			started: new Date() };
	if (!args.append)
		this.empty();
	if (args.fetchurl && args.fetchurl.length && !rows.length) {
		if (!args.fetchoffset)
			this.setinfo.fetchoffset = 0;
		delete this.setinfo.rows;
		this.setinfo.fetch_generation = ++lfjs.grid.generation_counter;
		this.setDataFetch();
	} else if (!skipcall) {
		this.setDataWork();
	}
}

lfjs.grid.prototype.pause = function(dopause) {
	if (!this.setinfo)
		return false;
	var retval = this.setinfo.paused;
	if (!dopause && (typeof dopause != "undefined" || this.setinfo.paused))
		delete this.setinfo.paused;
	else 
		this.setinfo.paused = true;
	if (!this.setinfo.paused && this.setinfo.rows)
		this.setDataWork();
	return retval;
}

lfjs.grid.prototype.setDataFetch = function() {
	var me = this;
	var locgen = this.setinfo.fetch_generation;
	this.setinfo.httpreq = $.ajax({url:this.setinfo.fetchurl +
		"&offset=" + this.setinfo.fetchoffset,
		success:function(req) { me.setDataFetched(req, locgen); } });
}

lfjs.grid.prototype.setDataFetched_delayed = function(req, genid) {
	var me = this, locreq = req, locgen=genid;
	setTimeout(function() { me.setDataFetched_real(locreq, locgen); }, 3000);
}

lfjs.grid.prototype.setDataFetched = function(req, genid) {
	// Check to see if this data request is from the currently pending request
	if (!this.setinfo || this.setinfo.fetch_generation != genid)
		return;
	delete this.setinfo.httpreq;
	this.setinfo.fetchoffset = parseInt($(req).find("fetchbatch").attr("next"));
	var currrows = $(req).find(this.setinfo.fetchdisplay);
	if (!this.setinfo.rows) {
		// Show this and fetch a new batch
		this.setinfo.rows = currrows;
		this.setinfo.offset = 0;
		if (this.setinfo.fetchoffset)
			this.setDataFetch();
		this.setDataWork();
	} else {
		// Save this batch until we are done showing the prior batch
		this.setinfo.nextrows = currrows;
	}
}

lfjs.grid.showthreadsize = 50;
lfjs.grid.showthreadpause = 25;

lfjs.grid.prototype.setDataWork = function() {
	if (!this.setinfo || this.setinfo.paused || !this.setinfo.rows)
		return;

	var maxrows = lfjs.grid.showthreadsize;
	var stoprow = this.setinfo.offset + maxrows;
	if (stoprow > this.setinfo.rows.length)
		stoprow = this.setinfo.rows.length;
	var i;
	for (i=this.setinfo.offset; i < stoprow; i++) {
		if (this.setinfo.insfunc)
			this.setinfo.insfunc(this, this.setinfo.rows, i);
		else
			this.addRow(0, this.setinfo.rows[i], {fastadd:true});
	}
	if (stoprow < this.setinfo.rows.length) {
		// More to show in this set
		this.setinfo.offset = stoprow;
		var where = this;
		setTimeout(function() { where.setDataWork() }, lfjs.grid.showthreadpause);
		return true;
	}
	if (this.setinfo.fetchurl && this.setinfo.nextrows) {
		// More to show in next set
		this.setinfo.rows = this.setinfo.nextrows;
		this.setinfo.offset = 0;
		delete this.setinfo.nextrows;
		if (this.setinfo.fetchoffset)
			this.setDataFetch();
		this.setDataWork();		// Show next batch
	} else if (!this.setinfo.fetchurl || !this.setinfo.httpreq) {
		if (this.setinfo.donefunc) {
			var oldsetinfo = this.setinfo;
			delete this.setinfo;
			oldsetinfo.donefunc(this.div, "done", oldsetinfo);
		} else {
			delete this.setinfo;
		}
	} else {
		delete this.setinfo.rows;
	}
}

// Initialize code
$(function() {
	$('.selectgrid').each(function(i) { 
		new lfjs.grid(this);
		this.onselectstart = function() { return false; }
	});
});
// Synchronize form fields with data from an XML document

lfjs.dbForm = function(viewdefs, xmldoc, args) {
	this.viewdefs = viewdefs;
	this.show(xmldoc);
}

lfjs.dbForm.prototype.show = function(in_xml) {
	var warnings = [];
	if (in_xml)
		this.xmldoc = in_xml;
	for (var i=0; i < this.viewdefs.length; i++) {
		var val = this.getFieldVal(i);
		if(this.viewdefs[i].dom.indexOf("[") != -1)
			var dom = $(this.viewdefs[i].dom.
					substr(1, this.viewdefs[i].dom.length-2));
		else
			var dom = $('#' + this.viewdefs[i].dom);
		if (dom.size() < 1) {
			warnings.push("cannot find dom:" + this.viewdefs[i].dom);
			continue;
		}
		switch (dom[0].nodeName.toLowerCase()) {
			case "select":
				var delim = ",";
				if(this.viewdefs[i].options && this.viewdefs[i].options.delimiter)
					delim = this.viewdefs[i].options.delimiter;
				var vals = val.split(delim);
				if(vals.length == 1)
					lfjs.setSelectedIndex(dom[0], val);
				else {
					var searchstr = delim + vals.join(delim) + delim;
					for (var j=0; j < dom[0].options.length; j++) {
						if (searchstr.indexOf(delim + dom[0].options[j].value + delim) >= 0) {
							dom[0].options[j].selected = true;
						} else
							dom[0].options[j].selected = false;
					}
				}
				break;
			case "textarea":
				dom[0].value = val;
				break;
			case "input":
				switch (dom[0].type) {
					case "text":
					case "password":
					case "hidden":
						dom[0].value = val;
						break;
					case "checkbox":
					case "radio":
						if(dom.length == 1) {
							if (val.length > 0)
								dom[0].checked = true;
							else
								dom[0].checked = false;
						} else {
							var vals = val.split(",");
							dom.each(function() {
								this.checked = false;
							});
							for(var j=0; j < vals.length; j++) {
								var el = dom.filter("[value='" + vals[j] + "']");
						
								if(el.length == 1)
									el[0].checked = true;
							}
						}
						break;
					default:
						warnings.push("unknown field type: " + dom[0].type);
				}
				break;
			default:
				if (dom.hasClass("selectgrid") && dom[0].addRow) {
					dom[0].empty();
					var val_arr = val.split('\n');
					for (var val_ctr=0; val.length && val_ctr < val_arr.length;
									val_ctr++) {
						var griddata = val_arr[val_ctr].split('|');
						if (griddata.length == 1) {
							dom[0].addRow(griddata[0], [griddata[0]], {fastadd:true});
						} else if (griddata.length > 1) {
							dom[0].addRow(griddata[0], griddata.slice(1),
										{fastadd:true});
						}
					}
				} else if (this.viewdefs[i].options &&
								this.viewdefs[i].options.ishtml) {
					dom.html(val);
				} else {
					dom.text(val);
				}
				break;
		}
	}
	if (warnings.length && typeof(console) != "undefined") {
		for (var i=0; i < warnings; i++)
			console.log("dbform.show: " + warnings[i]);
	}
	return warnings;
}


lfjs.dbForm.prototype.clear = function(in_xml) {
	this.xmldoc = null;
	this.show();
}
lfjs.dbForm.prototype.gather = function(args) {
	var retobj = new Object;
	for (var i=0; i < this.viewdefs.length; i++) {
		var oldval = this.getFieldVal(i);
		if(this.viewdefs[i].dom.indexOf("[") != -1)
			var dom = $(this.viewdefs[i].dom.
					substr(1, this.viewdefs[i].dom.length-2));
		else
			var dom = $('#' + this.viewdefs[i].dom);
		if(dom.length < 1)
			continue;
		var newval = "";
		switch (dom[0].nodeName.toLowerCase()) {
			case "select":
				if (dom[0].selectedIndex >= 0) {
					//newval = dom[0].options[dom[0].selectedIndex].value;
					var delim = ",";
					if(this.viewdefs[i].options && this.viewdefs[i].options.delimiter)
						delim = this.viewdefs[i].options.delimiter;
					var items = dom.val();
					if(typeof items == "string")
						newval = items;
					else
						newval = items.join(delim);
				}
				break;
			case "textarea":
				newval = dom[0].value.replace(/\r\n/g, "\n");
				break;
			case "input":
				switch (dom[0].type) {
					case "text":
					case "password":
					case "hidden":
						newval = dom[0].value;
						break;
					case "checkbox":
					case "radio":
						// How do we handle "hasno"?
						
						if(dom.length == 1) {
							if (dom[0].checked) {
								var hasstr = this.viewdefs[i].xml;
								if (hasstr.indexOf(" has ") >= 0)
									newval = hasstr.substr(hasstr.indexOf(" has ")+5);
								else if (hasstr.indexOf(" hasno ") >= 0)
									newval = "";
								else if (dom[0].value.length)
									newval = dom[0].value;
								else
									newval = "true";
							}
						} else {
							var vals = [];
							dom.each(function() {
								if(this.checked) 
									vals[vals.length] = this.value;
							});
							newval = vals.sort().join(",");
							if (args && args.changedonly &&
									oldval.split(',').sort().join(",") == newval)
								newval = oldval;
						}
						break;
					default:
						newval = oldval;
						if (typeof(console) != "undefined")
							console.log("dbForm.gather: unknown field type: " + 
								dom[0].type + "; setting to " + newval);
				}
				break;
			default:
				if (dom.hasClass("selectgrid") && dom[0].addRow) {
					newval = [];
					$(dom).find("tr").each(function(i, row) {
						newval.push(row.selectid + '|' + $(row).text());
					});
					newval = newval.join("\n");
				} else if (this.viewdefs[i].options &&
								this.viewdefs[i].options.ishtml) {
					newval = dom.html();
				} else {
					newval = dom.text();
				}
				break;
		}
		if (newval != oldval || !args || !args.changedonly) {
			if (this.viewdefs[i].gatherVal)
				newval = this.viewdefs[i].gatherVal(this.viewdefs[i].dom, newval);
			var domname = this.viewdefs[i].dom;
			if (this.viewdefs[i].gatherName) {
				domname = this.viewdefs[i].gatherName;
			} else {
				if (args && args.domprefix && args.domprefix.length > 0 &&
						domname.indexOf(args.domprefix) == 0)
					domname = domname.substr(args.domprefix.length);
				if (args && args.formprefix && args.formprefix.length > 0)
					domname = args.formprefix + domname;
			}
			if (!retobj[domname]) {
				retobj[domname] = newval;
			} else {
				if (typeof retobj[domname] != "array")
					retobj[domname] = [retobj[domname]];
				retobj[domname][retobj[domname].length] = newval;
			}
			if (args && args.firstonly)
				return retobj;
		}
	}
	return retobj;
}

lfjs.dbForm.prototype.hasChanges = function() {
	var changes = this.gather({firstonly:true, changedonly:true});
	for (change in changes)
		return true;
	return false;
}

// Private functions
lfjs.dbForm.prototype.getFieldVal = function(offset) {
	var val = "";
	var xmlfunc;
	if (this.xmldoc && this.viewdefs[offset].xml) {
		var xmlname = this.viewdefs[offset].xml;
		var xmlattr;
		if (xmlname.indexOf(' ') > 0) {
			xmlfunc = xmlname.substr(xmlname.indexOf(' ')+1);
			xmlname = xmlname.substr(xmlname, xmlname.indexOf(' '));
		}
		if (xmlname.indexOf('.') > 0) {
			xmlattr = xmlname.substr(xmlname.indexOf('.')+1);
			xmlname = xmlname.substr(xmlname, xmlname.indexOf('.'));
		}
		if (xmlname == "this")
			xmlnode = $(this.xmldoc);
		else if (xmlname.indexOf("[") == 0)
			xmlnode = $(this.xmldoc).find(xmlname);
		else
			xmlnode = $(this.xmldoc).children(xmlname);
		if (xmlattr && xmlnode.size() > 0) {
			val = xmlnode[0].getAttribute(xmlattr);
			if (!val)
				val = "";
		} else {
			val = xmlnode.text();
		}
	}
	// TODO: make this word-boundary matching
	if (this.viewdefs[offset].showVal) {
		val = this.viewdefs[offset].
				showVal(this.viewdefs[offset].dom, val, xmlfunc);
	} else if (xmlfunc && xmlfunc.indexOf("has ") == 0) {
		if (RegExp("\\b" + xmlfunc.substr(4) + "\\b").test(val))
			val = xmlfunc.substr(4);
		else
			val = "";
	} else if (xmlfunc && xmlfunc.indexOf("hasno ") == 0) {
		if (RegExp("\\b" + xmlfunc.substr(4) + "\\b").test(val))
			val = "";
		else
			val = xmlfunc.substr(4);
	} else if (xmlfunc && xmlfunc == "grid") {
		var val = [];
		xmlnode.children().each(function() {
			val.push($(this).attr("id") + "|" + $(this).text());
		});
		val = val.join('\n');
	}
	return val;
}

lfjs.dragable = function(in_domobj) {
	var domobj = in_domobj;
	domobj.mvc = this;
	this.div = domobj;
	this.container = domobj.parentNode;
	lfjs.dragable.activedrag = {};
	domobj.dragStart = function(ev) { return domobj.mvc.dragStart(ev); };
	lfjs.addEvent(domobj, "mousedown", domobj.dragStart);
}

lfjs.dragable.prototype.dragStart = function(event) {
	var el, evObj;
	var left, top;

	lfjs.dragable.activedrag = {};

	evObj = (typeof window.event == "undefined") ? event : window.event;
	lfjs.dragable.activedrag.dragEl = this.container;
	this.container.style.cursor = "move";
		
	// Get cursor position with respect to the page.
	if (typeof evObj.clientX != "undefined" &&
				typeof document.body.scrollLeft != "undefined") {
		left = evObj.clientX + document.body.scrollLeft;
		top = evObj.clientY + document.body.scrollTop;
	} else if (typeof winodw.scrollX != "undefined") {
		left = evObj.clientX + window.scrollX;
		top = evObj.clientY + window.scrollY;
	} else {
		return;
	}

	// Save starting positions of cursor and element.
	lfjs.dragable.activedrag.startCursX = left;
	lfjs.dragable.activedrag.startCursY = top;
	

	if(lfjs.dragable.activedrag.dragEl.style.left == "") {
		if (document.defaultView && document.defaultView.getComputedStyle) {
			lfjs.dragable.activedrag.dragEl.style.left = parseInt(
					document.defaultView.getComputedStyle(
					lfjs.dragable.activedrag.dragEl, '').getPropertyValue('left'));
		} else if(document.all && document.getElementById &&
					lfjs.dragable.activedrag.dragEl.currentStyle) {
			var elLeft = lfjs.dragable.activedrag.dragEl.currentStyle.left;
			if(elLeft == "auto") {
				lfjs.dragable.activedrag.dragEl.style.left =
					lfjs.dragable.activedrag.dragEl.offsetLeft;
			} else
				lfjs.dragable.activedrag.dragEl.style.left = parseInt(
						lfjs.dragable.activedrag.dragEl.currentStyle.left);
		}
	}
	lfjs.dragable.activedrag.elStartLeft =
			(typeof lfjs.dragable.activedrag.dragEl.style.left != "number") ?
					parseInt(lfjs.dragable.activedrag.dragEl.style.left) : 0;
	
	if(lfjs.dragable.activedrag.dragEl.style.top == "") {
		if (document.defaultView && document.defaultView.getComputedStyle) {
			lfjs.dragable.activedrag.dragEl.style.top = parseInt(
					document.defaultView.getComputedStyle(
						lfjs.dragable.activedrag.dragEl, '').getPropertyValue('top'));
		} else if(document.all && document.getElementById &&
					lfjs.dragable.activedrag.dragEl.currentStyle) {
			var elTop = lfjs.dragable.activedrag.dragEl.currentStyle.top;
			if(elTop == "auto") {
				lfjs.dragable.activedrag.dragEl.style.top =
					lfjs.dragable.activedrag.dragEl.offsetTop;
			} else
				lfjs.dragable.activedrag.dragEl.style.top =
					parseInt(lfjs.dragable.activedrag.dragEl.currentStyle.top);
		}
	} 
	lfjs.dragable.activedrag.elStartTop =
			(typeof lfjs.dragable.activedrag.dragEl.style.top != "number") ?
			 parseInt(lfjs.dragable.activedrag.dragEl.style.top) : 0;
	
	// Capture mousemove and mouseup events on the page.
	lfjs.addEvent(document, "mousemove", lfjs.dragable.dragMove);
	lfjs.addEvent(document, "mouseup", lfjs.dragable.dragEnd);
	
	if (typeof evObj.preventDefault == "function") {
		evObj.preventDefault();
	} else {
		evObj.cancelBubble = true;
		evObj.returnValue = false;
	}
}

lfjs.dragable.dragMove = function(ev) {
	var left, top, evObj;
	evObj = (typeof window.event == "undefined") ? ev : window.event;
	
	//only for Firefox - make sure draggable obj stays in window
	//  NOTE: IE seems to handle this fine
	if(window.innerWidth) {
		if((evObj.clientX < 3) || (evObj.clientX > (window.innerWidth -20)))
			return;
		if((evObj.clientY < 3) || (evObj.clientY > (window.innerHeight-20)))
			return;
	}
	// Get cursor position with respect to the page.
	if (typeof evObj.clientX != "undefined" &&
				typeof document.body.scrollLeft != "undefined") {
		left = evObj.clientX + document.body.scrollLeft;
		top = evObj.clientY + document.body.scrollTop;
	} else if (typeof winodw.scrollX != "undefined") {
		left = evObj.clientX + window.scrollX;
		top = evObj.clientY + window.scrollY;
	} 
	
	// Move drag element by the same amount the cursor has moved.
	var tmpEl = lfjs.dragable.activedrag.dragEl;
	lfjs.dragable.activedrag.dragEl.style.left =
			(lfjs.dragable.activedrag.elStartLeft + left -
			lfjs.dragable.activedrag.startCursX) + "px";
	lfjs.dragable.activedrag.dragEl.style.top =
			(lfjs.dragable.activedrag.elStartTop  + top -
			lfjs.dragable.activedrag.startCursY) + "px";
	if (typeof(tmpEl.drag_minleft) != "undefined" &&
			parseInt(tmpEl.style.left) < tmpEl.drag_minleft)
		tmpEl.style.left = tmpEl.drag_minleft + "px";
	if (typeof(tmpEl.drag_maxleft) != "undefined" &&
			parseInt(tmpEl.style.left) > tmpEl.drag_maxleft)
		tmpEl.style.left = tmpEl.drag_maxleft + "px";
	if (typeof(tmpEl.drag_mintop) != "undefined" &&
			parseInt(tmpEl.style.top) < tmpEl.drag_mintop)
		tmpEl.style.top = tmpEl.drag_mintop + "px";
	if (typeof(tmpEl.drag_maxtop) != "undefined" &&
			parseInt(tmpEl.style.top) > tmpEl.drag_maxtop)
		tmpEl.style.top = tmpEl.drag_maxtop + "px";

	if (typeof evObj.preventDefault == "function") {
		evObj.preventDefault();
	} else {
		evObj.cancelBubble = true;
		evObj.returnValue = false;
	}
}

lfjs.dragable.dragEnd = function(ev) {
	lfjs.dragable.activedrag.dragEl.style.cursor = "default";
	// Stop capturing mousemove and mouseup events.
	lfjs.removeEvent(document, "mousemove", lfjs.dragable.dragMove);
	lfjs.removeEvent(document, "mouseup", lfjs.dragable.dragEnd);
}

// Initialize code
$(function() {
   $('.dragable').each(function(i) { new lfjs.dragable(this); });
});
lfjs.prompt = function(prompt, func, args) {
	if (!lfjs.prompt.win && $('#promptwin').size() > 0)
		lfjs.prompt.win = $('#promptwin')[0];
	if (!lfjs.prompt.win) {
		// Create a prompt window
		lfjs.prompt.win = document.createElement("div");
		lfjs.prompt.win.id = "promptwin";
		lfjs.prompt.win.className = "screen";
      document.body.appendChild(lfjs.prompt.win);
		new lfjs.window(lfjs.prompt.win);
		var html = "<div class=\"prompt\">Enter value:</div>" +
				"<input id=\"prompt_input\" type=\"text\"";
		if(args && args.maxlength)
			html += " maxlength=\"" + args.maxlength + "\"";
		html += " /><br>" +
				"<div class=\"buttonbar\">" +
				"<a href=\"#\" class=\"button\" onClick=\"lfjs.keypress.stuff(" +
					"'CTRL+ENTER'); return false;\"> OK </a>&nbsp; " +
				" <a href=\"#\" class=\"button\" onClick=\"lfjs.keypress.stuff(" +
					"'ESC'); return false;\">Cancel</a>" +
				"</div>";
				
		$(lfjs.prompt.win).html(html);
	}
	lfjs.prompt.func = func;
	var title = prompt;
	if (args && args.title)
		title = args.title;
	$(lfjs.prompt.win).find(".prompt").text(prompt);
	if (args && args.defaultvalue)
		$(lfjs.prompt.win).find("input")[0].value = args.defaultvalue;
	else
		$(lfjs.prompt.win).find("input")[0].value = "";
	lfjs.prompt.win.activate(
			{ title: title, keyhandler: lfjs.prompt.keyhandler });
	var inpval = $(lfjs.prompt.win).find("input")[0];
	inpval.select();
	inpval.focus();
}

lfjs.prompt.keyhandler = function(in_key) {
	if (in_key == "ESC") {
		lfjs.prompt.win.deactivate();
		lfjs.prompt.func();
		return false;
	} else if (in_key == "CTRL+ENTER" || in_key == "ENTER") {
		var val = $(lfjs.prompt.win).find("input")[0].value;
		if (val && val.length > 0) {
			lfjs.prompt.win.deactivate();
			lfjs.prompt.func(val);
		}
		return false;
	}
	return true;
}

lfjs.promptync = function(func, args) {
	if (!lfjs.promptync.win && $('#yncwin').size() > 0)
		lfjs.promptync.win = $('#yncwin')[0];
	if (!lfjs.promptync.win) {
		// Create a ync window
		lfjs.promptync.win = document.createElement("div");
		lfjs.promptync.win.id = "yncwin";
		lfjs.promptync.win.className = "screen";
      document.body.appendChild(lfjs.promptync.win);
		new lfjs.window(lfjs.promptync.win);
		$(lfjs.promptync.win).html(
			"<div class=\"ync\">Save changes?</div><div style=\"float:left\">" +
			"<a href=\"#no\" class=\"button\" onClick=\"" +
				"lfjs.keypress.stuff('n'); return false;\">No</a>" +
			"</div><div style=\"float:right\">" +
			"<a href=\"#cancel\" class=\"button\" onClick=\"" +
				"lfjs.keypress.stuff('ESC'); return false;\">Cancel</a>" +
			"<a href=\"#yes\" class=\"button\" onClick=\"" +
				"lfjs.keypress.stuff('CTRL+ENTER'); return false;\">Yes</a>" +
			"</div>"
		);
	}
	lfjs.promptync.func = func;
	lfjs.promptync.yesfunc = args.yesfunc;
	lfjs.promptync.nofunc = args.nofunc;
	var title = (args.title ? args.title :
			(args.prompt ? args.prompt : "Confirm"));
	$(lfjs.promptync.win).find(".ync").text(
			args.prompt ? args.prompt : "Save changes?");
	var buttons = $(lfjs.promptync.win).find(".button");
	$(buttons[0]).text(args.noprompt ? args.noprompt : "No");
	$(buttons[1]).text(args.cancelprompt ? args.cancelprompt : " Cancel ");
	$(buttons[2]).text(args.yesprompt ? args.yesprompt : " Yes ");
	lfjs.promptync.win.activate({ keyhandler: lfjs.promptync.keyhandler,
		title: title });
}

lfjs.promptync.keyhandler = function(in_key) {
	if (in_key == "ESC") {
		lfjs.promptync.win.deactivate();
		lfjs.promptync.func();
		return false;
	} else if (in_key == "CTRL+ENTER" || in_key == "y" || in_key == "Y") {
		lfjs.promptync.win.deactivate();
		if (lfjs.promptync.yesfunc)
			lfjs.promptync.yesfunc();
		lfjs.promptync.func("yes");
	} else if (in_key == "n" || in_key == "N") {
		lfjs.promptync.win.deactivate();
		if (lfjs.promptync.nofunc)
			lfjs.promptync.nofunc();
		lfjs.promptync.func("no");
	}
	return true;
}
//-----------------------------
//   Tab Functions
//----------------------------- 


$(function() {
	$('.tabset').each(function(i) {
		var args = {};
		
		if($(this).find(".tabnav").length == 1 && $(this).find(".tabnav").find("a").length > 1) {
			args.tabnav = $(this).find(".tabnav")[0];
			 $(this).find(".tabnav").remove();
		}
		var ts = new lfjs.tabset(this, args);	   
		var tabs = $(this).children(".tab");
		tabs.each(function(i) {
			if($(this).next(".tabcontent")[0])
				var content = $(this).next(".tabcontent")[0];
			else
				var content = null;
			var targs = {};
			if($(this).attr("id").length)
				targs["id"] = $(this).attr("id");
			if(this.className.length)
				targs["classname"] = this.className;
			targs["contents"] = $(this).next(".tabcontent")[0];
			var tab = ts.addTab($(this).html(), targs );
			if($(this).hasClass("selected"))
				tab.show();
				
			$(this).remove();
		});
		ts.displayTabNav();
		//size content div appropriately
		if($(ts.mainContentEl).children().length) {
			var pad = parseInt($(ts.tabContainerEl).css("padding-top"));
			
			var height = $(ts.domobj).height() - $(ts.tabContainerEl).height();
			
			if(!isNaN(pad))
				height -= pad;
			height -= 3;
			$(ts.mainContentEl).height(height);
		}
   });
		   
});

lfjs.tabset = function(domobj, args) {
	if(!args)
		var args = {};
	var self = this;
	domobj.tabset = this;
	this.domobj = domobj;
	//internal array of all tab objects
	this.tabs = [];
	//variable to track the currently shown tab
	this.currActive;
	//array to track the previously shown tabs
	this.prevActive = [];
	//timerID used for scrolling using the arrows
	this.tabScrollTimer = 0;
	
	//create the container div for the actual tabs
	var container = document.createElement("div");
	$(container).addClass('tabcontainer').css( {  width: "100%"});
	
	//add nobr element to avoid tabs breaking if window is shrunk
	var nobr = document.createElement("nobr");
	
	
	//create a navigation div for scrolling tabs
	function end(event) {
		var el = event.target
		el.blur();
		self.endScroll();
		event.stopPropagation();
	}
	//add the scroll navigation div and links
	if(args.tabnav && $(args.tabnav).children("a").length > 1) {
		var nav = args.tabnav;
		var left = $(args.tabnav).find("a")[0];
		var right = $(args.tabnav).find("a")[1];
	} else {
		var nav = document.createElement("div");
		var left = document.createElement("a");
		var lefthtml = "&laquo;";
		$(left).html(lefthtml).attr("title", "Scroll Left");
		var right = document.createElement("a");
		var righthtml = "&raquo;";
		$(right).html(righthtml).attr("title", "Scroll Right");
		$(nav).append(left).append("&nbsp;").append(right);
	}
	$(nav).addClass("tabnav").css( { display: "none", float: "right" } );
	
	$(left).addClass("left").attr( { href: "#" } ).mousedown(
		function(event) { self.scroll(-1); event.stopPropagation(); return false; }
	).mouseup(
		function(event) { end(event); return false; }
	).mouseout(
		function(event) { end(event); return false; }
	).click(
		function(event) { end(event); return false; }
	);
	
	$(right).addClass("right").attr( { href: "#" } ).mousedown(
		function(event) { self.scroll(1); event.stopPropagation(); return false; }
	).mouseup(
		function(event) { end(event); return false; }
	).mouseout(
		function(event) { end(event); return false; }
	).click(
		function(event) { end(event); return false; }
	);
	
	
	function resizeMe() {
		self.displayTabNav();
	}
	//create the content div for the content of each tab
	var content = document.createElement("div");	
	$(content).addClass('tabcontents');
	
	//add an event to handle displaying/hiding navigation on window resize
	//doesn't work right in IE, since IE fires multiple resize events, if fact
	//   it crashes IE6 on Win@k in Quirks Mode
	if(!$.browser.msie) {
		$(window).resize(function() { resizeMe() });
	}
	$(nobr).append(nav).append(container);
	$(domobj).append(nobr).append(content);
	//$(nobr).append(container);
	//$(domobj).append(nav).append(nobr).append(content);
	

	
	this.tabContainerEl = container;	
	this.mainTabEl = domobj;	
	this.mainContentEl = content;	
	this.navEl = nav;
	
	//Add a scroll wheel handler (jQuery does not support teh mousewheel event, so add it old school)
	if (typeof this.tabContainerEl.addEventListener == "function") {
		this.tabContainerEl.addEventListener("DOMMouseScroll", function(event) { self.tabMouseWheel(event); }, true);
	} else {
		this.tabContainerEl.attachEvent("onmousewheel", function(event) { self.tabMouseWheel(event); });
	}
	
	domobj.getTabs = function() { return this.tabset.getTabs(); };
	domobj.getShownTab = function() { return this.tabset.getShownTab(); };
	domobj.show = function(tab) { return this.tabset.show(tab); };
	domobj.remove = function(tab) { return this.tabset.remove(tab); };
	domobj.addTab = function(label, args) { return this.tabset.addTab(label, args); };
	
	return this;
	//domobj.activate = function (a) { return this.mvc.activate(a); };
	//domobj.deactivate = function () { return this.mvc.deactivate(); };
	//$(domobj).addClass("inactivescreen");
}

lfjs.tab = function(label, args) {
	if(!args)
		var args = {};
	this.tabset;
	this.tabDiv = null;
	this.contents = null;
	this.label = label;
	this.canclose = false;
	this.canmove = false;
	this.isActive = false;
	//variable to remember the vertical scroll position for each tab
	this.scrollTop = 0;
	if(args.id)
		this.id = args.id;
	if(args.classname)
		this.classname = args.classname;
	if(args.showfunc)
		this.showfunc = args.showfunc;
	if(args.hidefunc)
		this.hidefunc = args.hidefunc;
	if(args.closefunc)
		this.closefunc = args.closefunc;
	if(args.dropfunc)
		this.dropfunc = args.dropfunc;
	if(args.canclose)
		this.canclose = args.canclose;
	if(args.data)
		this.data = args.data;
	if(args.canmove)
		this.canmove = args.canmove;
	
	if(args.contents) {
		if(typeof args.contents == "string" && $("#" + args.contents).length)
			this.contents = $("#" + args.contents)[0];
		else if($(args.contents).length) {
			//this.contents = $(args.contents).remove().get(0);
			this.contents = args.contents;
		}
		$(this.contents).css({display: "none"});
		
		
	} 
	
	return this;
}
//create the actual tab element
lfjs.tab.prototype.drawTab = function () {
	var self = this;
	
	if(this.tabDiv && $(this.tabDiv).length) {
		var tabDiv = $(this.tabDiv).empty().get(0);
	} else {
		var tabDiv = document.createElement("span");
		this.tabDiv = tabDiv;
	
		$(this.tabset.tabContainerEl).append(tabDiv);
		$(tabDiv).css(
			{ display: "inline" }
		).addClass("tab").addClass((this.isActive) ? 'tabactive' : 'tabinactive').mouseover(
			function(event) { self.tabMouseOver(); }
		).mouseout(
			function(event) { self.tabMouseOut(); }
		).click(
			function(event) { self.show(); }
		);
		if(this.id)
			$(tabDiv).attr("id", this.id)
		if(this.classname)
			$(tabDiv).addClass(this.classname)
		
		if(typeof tabDiv.onselectstart != "undefined") {
			//tabDiv.onselectstart = function() { return false; };	
		}
	}
	tabDiv.tab = this;
	$(tabDiv).html(this.label);
	if(this.canclose) {
		var close = document.createElement("span");
		var a = document.createElement("a");
		$(a).html("x").attr( {title: "Close Tab"} ).click(
			function() { self.remove(); }
		);
		$(close).addClass('closetab').append(a);
		$(tabDiv).append(close);
	}
	
	
	if(this.isActive) {
		this.tabset.currActive = this;
	}
}

lfjs.tabset.prototype.addTab = function(label, args) {
	var tabObj = new lfjs.tab(label, args);
	tabObj.tabset = this;
	
	if(tabObj.contents) {
		if(tabObj.contents.parentNode) {
			var node = tabObj.contents.parentNode.removeChild(tabObj.contents);
		} else {
			var node = tabObj.contents;
		}
		$(this.mainContentEl).append(node);
	}
	
	tabObj.tabset.tabs[tabObj.tabset.tabs.length] = tabObj;
	tabObj.drawTab();
	//show tab navigation, if necessary
	this.displayTabNav();
	
	return tabObj;
}

lfjs.tab.prototype.updateArgs = function(args) {
	for(var i in args) {
		if(typeof this[i] != "undefined" && this[i] != null) {
			this[i] = args[i];	
		}
	}
	this.drawTab();
}
lfjs.tabset.prototype.getTabs = function() {
	var tabs = [];
	for(var i=0; i < this.tabs.length; i++) {
		tabs[tabs.length] = this.tabs[i];
	}
	return tabs;
}

lfjs.tabset.prototype.getShownTab = function() {
	if(this.currActive)
		return this.currActive;
	return null;
}

lfjs.tabset.prototype.show = function(tabObj) {
	tabObj.show();	
}
//show a tab
lfjs.tab.prototype.show = function() {
	var content = this.tabset.mainContentEl;
	
	if(this == this.tabset.currActive)
		return;
	if(this.tabset.currActive) {
		if(this.tabset.currActive.hidefunc) {
			var ret = this.tabset.currActive.hidefunc(this.tabset.currActive);
			if(ret == false)
				return false;
		}
		this.tabset.prevActive[this.tabset.prevActive.length] = this.tabset.currActive;
		$(this.tabset.currActive.tabDiv).addClass('tabinactive').removeClass('tabactive');
	}
		
	$(this.tabDiv).addClass('tabactive').removeClass('tabinactive');
	var show = true;
	if(this.showfunc) {
		show = this.showfunc(this);
	}
	if(this.contents && show != false) {
		if(this.tabset.currActive && this.tabset.currActive.contents) {
			this.tabset.currActive.scrollTop = this.tabset.mainContentEl.scrollTop;
			$(this.tabset.currActive.contents).css( { display: "none" });
		}
		$(this.contents).css( { display: "block" } );
		this.tabset.mainContentEl.scrollTop = this.scrollTop;
	}
	
	//Set this as the currently active tab
	this.tabset.currActive = this;
	
	this.scrollToView();
	
}
lfjs.tab.prototype.scrollToView = function() {
	//if it is scrolled out of view, scroll into view
	if(this.tabset.tabContainerEl.clientWidth < this.tabset.tabContainerEl.scrollWidth) {
		var offL = this.tabDiv.offsetLeft;
		var scrL = this.tabset.tabContainerEl.scrollLeft;
		var offR = this.tabDiv.offsetLeft + this.tabDiv.offsetWidth;
		var scrR = this.tabset.tabContainerEl.scrollLeft + this.tabset.tabContainerEl.clientWidth;
		if(offL < scrL) 
			this.tabset.tabContainerEl.scrollLeft = offL - 8;
		else if (offR > scrR)
			this.tabset.tabContainerEl.scrollLeft = offR - this.tabset.tabContainerEl.clientWidth;
	}
	
}
lfjs.tabset.prototype.remove = function(tabObj) {
	tabObj.remove();	
}

lfjs.tab.prototype.remove = function(forceclose) {
	if(typeof forceclose == "undefined")
		var forceclose = false;
	var exists = false;
	if(this.tabset.tabs.length > 1 || forceclose) {
		for(var i=0; i < this.tabset.tabs.length; i++) {
			if(this.tabset.tabs[i] == this) {
				//check if it is the last tab, if it is, select the last tab
				//  otherwise, select the next tab after removal
				if(i == (this.tabset.tabs.length-1)) 
					var nextTab = i-1;
				else
					var nextTab = i;
					
				this.tabset.tabs.splice(i,1);
				exists = true;
				break;
			}
		}
		if(exists) {
			if(this.closefunc) {
				var ret = this.closefunc(this);
				if(ret == false)
					return false;
			}
			this.tabset.tabContainerEl.removeChild(this.tabDiv);
			var isCurrTab = false;
			if(this.tabset.currActive == this) {
				isCurrTab = true;
				this.tabset.currActive = null;
			}
			if(this.contents) {
				$(this.contents).remove();
			}
			var next = this.tabset.currActive;
			//show the previously selected tab, if exists, otherwise select by proximity
			if(this.tabset.prevActive.length) {
				//remove references to the tab closing in prevActive
				for(var i=this.tabset.prevActive.length; i >= 0; i--) {
					if(this.tabset.prevActive[i] == this)
						this.tabset.prevActive.splice(i,1);
				}
				
				if(isCurrTab) {
					var next = this.tabset.prevActive.splice(this.tabset.prevActive.length-1, 1);
					next = next[0];
				} 
			} else if (isCurrTab) {
				next = this.tabset.tabs[nextTab];
			}
			if(isCurrTab && next) 
				next.show();
			if(next)
				next.scrollToView();
			
			
			//show tab navigation, if necessary
			this.tabset.displayTabNav();
			
		}
	}
}


///////////////////////////////
//  EVENT HANDLING FUNCTIONS
//////////////////////////////
//called onClick to show the tab that was clicked on

lfjs.tab.prototype.tabMouseOut = function() {
	$(this.tabDiv).removeClass('tabhover');
}

lfjs.tab.prototype.tabMouseOver = function() {
	if(!(this == this.tabset.currActive))
		$(this.tabDiv).addClass('tabhover');
}
lfjs.tabset.prototype.tabMouseWheel = function(ev) {
	var delta = 0;

	if (!ev) 
		ev = window.event;
	//IE and Opera
	if (ev.wheelDelta) { 
		delta = ev.wheelDelta/120;
		// In Opera 9, delta differs in sign as compared to IE.
		if (window.opera)
			delta = -delta;
	// Firefox
	} else if (ev.detail) { 
		// In Firefox, sign of delta is different than in IE.  Also, delta is multiple of 3.
		delta = -ev.detail/3;
	}
	// If delta is nonzero, handle it. Basically, delta is now positive if wheel was scrolled up,
	// and negative, if wheel was scrolled down.
	if (delta) {
		var dis = delta * 20;
		this.tabContainerEl.scrollLeft -= dis;
	}
	
	if (ev.preventDefault)
		ev.preventDefault();
	ev.returnValue = false;
}

lfjs.tabset.prototype.scroll = function(dir) {
	var self = this;
	var dir = dir;
	this.tabScrollTimer = setTimeout(function() { self.scroll(dir);}, 1);
	var dis = dir * 2;
	this.tabContainerEl.scrollLeft += dis;
}
lfjs.tabset.prototype.endScroll = function() {
	
	if(typeof this.tabScrollTimer == "number") 
		clearTimeout(this.tabScrollTimer);
	return false;
}
//check to see if the tab navigation is required 
lfjs.tabset.prototype.displayTabNav = function() {
	var cliW = this.mainTabEl.clientWidth;
	var scrW = this.tabContainerEl.scrollWidth;
	//if no width is set on mainTabEl, IE reports clientWidth as 0
	if(cliW == 0) {
		this.mainTabEl.style.width = "100%";
		cliW = this.mainTabEl.clientWidth;
		this.mainTabEl.style.width = "";
	}
	if(scrW > cliW) {
		this.navEl.style.display = "block";
		this.tabContainerEl.style.width = (cliW - this.navEl.offsetWidth - 4) + "px";
		this.tabContainerEl.style.overflowX = "hidden";
	} else {
		this.navEl.style.display = "none";
		this.tabContainerEl.style.width = "100%";
	}
	//if scrollLeft + clientWidth > scrollWidth, then we need to snap the tabs to the right side
	if(this.tabContainerEl.scrollLeft + this.tabContainerEl.clientWidth > this.tabContainerEl.scrollWidth) 
		this.tabContainerEl.scrollLeft = this.tabContainerEl.scrollWidth + this.tabContainerEl.clientWidth;
		
	
	
	
	
}



// Initialize code
$(function() {
	$('.multiupload').each(function(i) { 
		new lfjs.multiupload(this);
	});
});



lfjs.multiupload = function(domobj) {
	if(parseInt(lfjs.multiupload.flashVersion(), 10) < 9) {
		try {
			domobj.onclick(domobj);
		} catch(e) {}
		return;
	}
	
	var flashsrc = $("script[src$='swfupload.js']:first").attr("src").replace(/swfupload\.js$/, "swfupload.swf");
	
	if(domobj.nodeType == 1 && (/(span|div|a|button|img)/.test(domobj.nodeName.toLowerCase()) || 
	   (domobj.nodeName.toLowerCase() == "input" && domobj.type == "button"))) {
		
	} else {
		if(window.console)
			console.log("MultiUpload element must be SPAN, DIV, A, IMG, BUTTON, or INPUT type=button.");	
		return;
	}
	//console.log(domobj.nodeType + ' ' + domobj.nodeName + ' "' + domobj.id + '" - ' + $(domobj).width() + " x " + $(domobj).height());
	//console.log(domobj.offsetWidth + " x " + domobj.offsetHeight);
	if(typeof SWFUpload == "function") {
		var placeholder = document.createElement("span");
		var ts = new Date().valueOf() + '';
		placeholder.id = "lfjsmu" + domobj.nodeName.toLowerCase() + ts.substring(Math.floor(Math.random()*ts.length));
		
		$(domobj).css({zIndex: "1"});
		var swfwidth = domobj.offsetWidth;		// Broken: $(domobj).width();
		var swfheight = domobj.offsetHeight;	// Broken: $(domobj).height();
		
		var washidden = false;
		if (swfwidth == 0 || swfwidth == 0) {
			washidden = true;
			//tweak any hidden parents so we can figure out where to put the button.
			var hiddenpar = $(domobj).parents(":hidden");
			var currpos = hiddenpar.css("position");
			
			hiddenpar.toggle().css({ visibility: "hidden", position:"absolute"});
			swfwidth = domobj.offsetWidth;		// Broken: $(domobj).width();
			swfheight = domobj.offsetHeight;	// Broken: $(domobj).height();
		}
	
		if(/(input|button|img)/.test(domobj.nodeName.toLowerCase())) {
			var buttontext = domobj.value;
			var par = document.createElement("span");
			$(par).addClass("swfuploadwrapper");
			$(domobj).wrap(par).before(placeholder);
			//console.log("OW: " + domobj.offsetWidth + " - JQ Width: " + $(domobj).width());
			if(domobj.offsetWidth) {
				//swfwidth = domobj.offsetWidth;
				//swfheight = domobj.offsetHeight;
			}
		} else {
			var buttontext = $(domobj).html();
			$(domobj).prepend(placeholder);
		}
		if (washidden)
			hiddenpar.css({ visibility: "visible", position:currpos}).toggle();
		
		var cursor = $(domobj).css("cursor").toLowerCase();
		var swfcursor = SWFUpload.CURSOR.ARROW;
		if(cursor == "pointer" || cursor == "hand" || domobj.nodeName.toLowerCase() == "a")
			swfcursor = SWFUpload.CURSOR.HAND;
			
		this.settings = { };
		domobj.uploadsettings = this.settings;
		if(domobj.onclick) {
			domobj.initfunc = domobj.onclick;
			domobj.initfunc();
			domobj.onclick = function() { return false; };
			//console.log(this.settings);
		} else 
			domobj.initfunc = function() {};
			
		var args = {
			button_placeholder_id: placeholder.id,
			flash_url: flashsrc,
			file_types: "*.*",
			file_types_description: "All Files",
			requeue_on_error: false,
			//button_text: buttontext,
			button_width: swfwidth,
			button_height: swfheight,
			button_action : SWFUpload.BUTTON_ACTION.SELECT_FILES,		
			button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
			button_cursor: swfcursor,
			
			use_query_string: false,

			debug: false
		}

		var swf = this;
		
		function addSetting(localsetting, swfsetting) {
			if(swf.settings[localsetting] && swf.settings[localsetting].length)
				args[swfsetting] = swf.settings[localsetting];
		}
		addSetting("url", "upload_url");
		addSetting("filetypes", "file_types");
		addSetting("filetypesdesc", "file_types_description");
		addSetting("filepostname", "file_post_name");
		addSetting("postparams", "post_params");
		addSetting("filepostname", "file_post_name");
		addSetting("requeueonerror", "requeue_on_error");
		addSetting("filesizelimit", "file_size_limit");
		
		
		args["swfupload_loaded_handler"] = function() { swf.flashLoaded() };
		args["file_dialog_start_handler"] = function() { swf.fileDialogStart() };
		args["file_queued_handler"] = function(a) { swf.fileQueued(a) };
		args["file_queue_error_handler"] = function(a, b, c) { swf.fileQueueError(a, b, c) };
		args["file_dialog_complete_handler"] = function(a, b, c) { swf.fileDialogComplete(a, b, c) };
		args["upload_start_handler"] = function(a) { return swf.uploadStart(a) };
		args["upload_progress_handler"] = function(a, b, c) { swf.uploadProgress(a, b, c) };
		args["upload_error_handler"] = function(a, b, c) { swf.uploadError(a, b, c) };
		args["upload_success_handler"] = function(a, b) { swf.uploadSuccess(a, b) };
		args["upload_complete_handler"] = function(a) { swf.uploadComplete(a) };
		
		this.swfupload = new SWFUpload(args);
		$(".multiupload .swfupload, SPAN .swfupload").each(function() { $(this).css({position: "absolute", "z-index": "2"}) });
		
		this.files = [];
		this.currupload = "";
		this.queuelength = 0;
		this.currfilecnt = 0;
		this.domobj = domobj;
		domobj.mvc = this;
		
		domobj.startUpload = function (a) { return this.mvc.startUpload(a); };
		domobj.cancelUpload = function (a) { return this.mvc.cancelUpload(a); };
		domobj.stopUpload = function () { return this.mvc.stopUpload(); };
		domobj.getFile = function (a) { return this.mvc.getFile(a); };
		domobj.getFiles = function () { return this.mvc.getFiles(); };
		domobj.setUploadURL = function (a) { return this.mvc.setUploadURL(a); };
		domobj.setPostParams = function (a, b) { return this.mvc.setPostParams(a, b); };
		domobj.setFilePostParams = function (a, b, c) { return this.mvc.setFilePostParams(a, b, c); };
		domobj.isIdle = function () { return this.mvc.isIdle(); };
	} else {
		if(window.console)
			console.log("Cannot find SWFUpload.  Make sure js file is included");	
	}
}

lfjs.multiupload.prototype.flashLoaded = function() {
	$(".multiuploadnoinit").hide();
	if(typeof lfjs.multiupload.onInit == "function")
		lfjs.multiupload.onInit(this.domobj);
		
	if (this.settings["flashLoaded"] && typeof this.settings["flashLoaded"] == "function") {
		this.settings["flashLoaded"](this.domobj);	
	}
}

lfjs.multiupload.prototype.fileDialogStart = function() {
	//add/update swf setting here
	
	this.domobj.initfunc();
	var swf = this;
	var swfu = this.swfupload;
	// IE errors on this, so wrap in try/catch
	try {
		swfu.movieElement.blur();
	} catch(e) { }
	function addSetting(localsetting, setfunc) {
		if(swf.settings[localsetting] && swf.settings[localsetting].length)
			setfunc(swf.settings[localsetting]);
	}
	
	if(swf.settings["url"] && swf.settings["url"].length)
		this.setUploadURL(swf.settings["url"]);
	if(swf.settings["filepostname"] && swf.settings["filepostname"].length)
		this.swfupload.setFilePostName(swf.settings["filepostname"]);
	if(swf.settings["filesizelimit"] && swf.settings["filesizelimit"].length)
		this.swfupload.setFileSizeLimit(swf.settings["filesizelimit"]);
	if(swf.settings["postparams"] && typeof swf.settings["postparams"] == "object")
		this.setPostParams(swf.settings["postparams"], true);
		
	if(swf.settings["filetypes"] && swf.settings["filetypes"].length) {
		var desc = "All Files";
		if(swf.settings["filetypesdesc"] && swf.settings["filetypesdesc"].length) {
			var desc = swf.settings["filetypesdesc"];
		}
		this.swfupload.setFileTypes(swf.settings["filetypes"], desc);
	}
	addSetting("requeueonerror", "requeue_on_error");
	
	if (this.settings["fileSelectStart"] && typeof this.settings["fileSelectStart"] == "function") {
		this.settings["fileSelectStart"](this.domobj);	
	}
}

lfjs.multiupload.prototype.fileQueued = function(file) {
	var ret = true;
	if (this.settings["fileQueued"] && typeof this.settings["fileQueued"] == "function") {
		ret = this.settings["fileQueued"](this.domobj, file);	
	}
	if(ret == false) {
		this.swfupload.cancelUpload(file.id, false);
	} else {
		var idx = this.files.length;
		this.files[idx] = file;
		this.files[idx].serverdata = "";
	}
}

lfjs.multiupload.prototype.fileQueueError = function(file, error, msg) {
	if (this.settings["fileQueueError"] && typeof this.settings["fileQueueError"] == "function") {
		var ret = this.settings["fileQueueError"](this.domobj, file, error, msg);
	}	
	for(var i=0; i < this.files.length; i++) {
		if(this.files[i].id == file.id) {
			this.files.splice(i, 1);
			break;
		}
	}
}

lfjs.multiupload.prototype.fileDialogComplete = function(numselected, numqueued, totalqueue) {
	var ret = true;
	this.queuelength += numqueued;
	//Don't fire on a cancel
	if(numselected == 0)
		return;
	if (this.settings["fileSelectComplete"] && typeof this.settings["fileSelectComplete"] == "function") {
		var ret = this.settings["fileSelectComplete"](this.domobj, this.files, numselected, numqueued);	
	}
	
	if(ret != false) {
		this.swfupload.startUpload();	
	}

}

lfjs.multiupload.prototype.uploadStart = function(file) {
	var ret = true;
	this.currfilecnt++;
	if (this.settings["uploadStart"] && typeof this.settings["uploadStart"] == "function") {
		var ret = this.settings["uploadStart"](this.domobj, file, this.currfilecnt, this.queuelength);	
	}
	this.currupload = file.id;
	if(ret == false)
		return ret;
}

lfjs.multiupload.prototype.uploadProgress = function(file, complete, total) {
	
	if (this.settings["uploadProgress"] && typeof this.settings["uploadProgress"] == "function") {
		var ret = this.settings["uploadProgress"](this.domobj, file, complete, total);	
	}
	if(complete == total) {
		if (this.settings["fileReceived"] && typeof this.settings["fileReceived"] == "function") {
			var ret = this.settings["fileReceived"](this.domobj, file);
		}
	}
}

lfjs.multiupload.prototype.uploadError = function(file, error, msg) {
	
	if (this.settings["uploadError"] && typeof this.settings["uploadError"] == "function") {
		var ret = this.settings["uploadError"](this.domobj, file, error, msg);	
	}
}

lfjs.multiupload.prototype.uploadSuccess = function(file, data) {
	for(var i=0; i < this.files.length; i++) {
		if(this.files[i].id == file.id) {
			this.files[i].serverdata = data;
			break;
		}
	}
}

lfjs.multiupload.prototype.uploadComplete = function(file) {
	var ret = true;
	var data = "";
	var delidx = -1;
	for(var i=0; i < this.files.length; i++) {
		if(this.files[i].id == file.id) {
			var data = this.files[i].serverdata;
			delidx = i;
			break;
		}
	}
	if (this.settings["uploadComplete"] && typeof this.settings["uploadComplete"] == "function") {
		var ret = this.settings["uploadComplete"](this.domobj, file, data);
	}
	if(delidx >= 0)
		this.files.splice(delidx, 1);
	
	this.currupload = "";
	if(ret != false)
		this.swfupload.startUpload();	
	if(this.isIdle())
		this.queueComplete();
	
}

lfjs.multiupload.prototype.queueComplete = function() {
	this.queuelength = 0;
	this.currfilecnt = 0;
	if (this.settings["queueComplete"] && typeof this.settings["queueComplete"] == "function") {
		var ret = this.settings["queueComplete"](this.domobj);
	}

	
}

lfjs.multiupload.prototype.startUpload = function(fileid) {
	this.swfupload.startUpload(fileid);
	
}

lfjs.multiupload.prototype.cancelUpload = function(fileid, throwerror) {
	for(var i=0; i < this.files.length; i++) {
		if(this.files[i].id == fileid) {
			this.files.splice(i, 1);
			break;
		}
	}
	this.queuelength--;
	
	this.swfupload.cancelUpload(fileid, throwerror);
	
}

lfjs.multiupload.prototype.stopUpload = function() {
	this.swfupload.stopUpload();
	
}

lfjs.multiupload.prototype.getFile = function(fileid) {
	for(var i=0; i < this.files.length; i++) {
		if(this.files[i].id == fileid || this.files[i].name == fileid)
			return this.files[i];
	}
	return null;
	
}

lfjs.multiupload.prototype.getFiles = function() {
	return this.files;
	
}

lfjs.multiupload.prototype.setUploadURL = function(url) {
	this.swfupload.setUploadURL(url);
	
}

lfjs.multiupload.prototype.setPostParams = function(paramobj, addremove) {
	if(typeof addremove == "undefined" || addremove == null) {
		this.swfupload.setPostParams(paramobj);
	} else if (addremove == true) {
		for(var i in paramobj) {
			this.swfupload.addPostParam(i, paramobj[i]);
		}
	} else if (addremove == false) {
		for(var i in paramobj) {
			this.swfupload.removePostParam(i);
		}
	}
	
}

lfjs.multiupload.prototype.setFilePostParams = function(fileid, paramobj, addremove) {
	var file = this.getFile(fileid);
	if(typeof addremove == "undefined" || addremove == null) {
		var addremove = true;
	}
	if (addremove == true) {
		for(var i in paramobj) {
			this.swfupload.addFileParam(file.id, i, paramobj[i]);
		}
	} else if (addremove == false) {
		for(var i in paramobj) {
			this.swfupload.removeFileParam(file.id, i);
		}
	}
	
}

lfjs.multiupload.prototype.isIdle = function() {
	var stats = this.swfupload.getStats();
	if(stats.in_progress == 0 && stats.files_queued == 0 && this.files.length == 0)
		return true;
	return false;
}

lfjs.multiupload.flashVersion = function() {
	var flashVer = -1;
	if (navigator.plugins != null && navigator.plugins.length > 0) {
		if (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]) {
			var swVer2 = navigator.plugins["Shockwave Flash 2.0"] ? " 2.0" : "";
			var flashDescription = navigator.plugins["Shockwave Flash" + swVer2].description;
			var descArray = flashDescription.split(" ");
			var tempArrayMajor = descArray[2].split(".");			
			var versionMajor = tempArrayMajor[0];
			var versionMinor = tempArrayMajor[1];
			var versionRevision = descArray[3];
			if (versionRevision == "") {
				versionRevision = descArray[4];
			}
			if (versionRevision[0] == "d") {
				versionRevision = versionRevision.substring(1);
			} else if (versionRevision[0] == "r") {
				versionRevision = versionRevision.substring(1);
				if (versionRevision.indexOf("d") > 0) {
					versionRevision = versionRevision.substring(0, versionRevision.indexOf("d"));
				}
			}
			flashVer = versionMajor + "." + versionMinor + "." + versionRevision;
		}
	}
	else if ( window.ActiveXObject ) {
		// NOTE : new ActiveXObject(strFoo) throws an exception if strFoo isn't in the registry
		var version;
		try {
			// version will be set for 7.X or greater players
			axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
			version = axo.GetVariable("$version");
		} catch (e) {
		}
	
		if (!version)
		{
			try {
				// version will be set for 6.X players only
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");
				
				// installed player is some revision of 6.0
				// GetVariable("$version") crashes for versions 6.0.22 through 6.0.29,
				// so we have to be careful. 
				
				// default to the first public version
				version = "WIN 6,0,21,0";
	
				// throws if AllowScripAccess does not exist (introduced in 6.0r47)		
				axo.AllowScriptAccess = "always";
	
				// safe to call for 6.0r47 or greater
				version = axo.GetVariable("$version");
	
			} catch (e) {
			}
		}
	
		if (!version)
		{
			try {
				// version will be set for 4.X or 5.X player
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
				version = axo.GetVariable("$version");
			} catch (e) {
			}
		}
	
		if (!version)
		{
			try {
				// version will be set for 3.X player
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
				version = "WIN 3,0,18,0";
			} catch (e) {
			}
		}
	
		if (!version)
		{
			try {
				// version will be set for 2.X player
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
				version = "WIN 2,0,0,11";
			} catch (e) {
				version = -1;
			}
		}
		if(version != -1)
			version = version.replace(/^[^\d]*/, "");
		flashVer = version;
	}	
	
	if(flashVer != -1)
		flashVer = flashVer.replace(/,/g, ".");
	return flashVer;
}


$(function() {
	if ($(".bubble").length) {
		lfjs.bubble.createBubble();
		$('.bubble').each(function(i){
			var title = $(this).attr("title");
			if(title) {
				$(this).attr("title", title.replace(/\<\/?[^\>]*\>/g, ""));
				args = {};
				if($(this).attr("bubblewidth"))
					args.width = parseInt($(this).attr("bubblewidth"), 10);
				$(this).data("args", args).click(function(event) {
					//console.log($(this).data("args"))
					lfjs.bubble(this, title, $(this).data("args"), event);
				});
			}
		});
	}
});
lfjs.bubble = function(domobj, message, args, event, belowContent) {
	lfjs.bubble.hide();
	if(typeof lfjs.path == "undefined")
		lfjs.path = $("script[src$='lfjs.js']:first").attr("src").replace(/\/[^\/]*$/, "");
	if(typeof message == "undefiend" || message.length == 0)
		return;
	if(typeof args == "undefined")
		var args = {};
	var closeimg = lfjs.path + "/lfjsimages/cancel.gif";
	if(args.closeimg)
		closeimg = args.closeimg;
	if(typeof lfjs.bubble.domobj == "undefined") {
		lfjs.bubble.createBubble();		
	}
	//if dom obj is not visible (i.e. gone or in an old bubble), try to use the previous dom obj
	if(!$(domobj).is(":visible")) {
		if(lfjs.bubble.prevdomobj)
			domobj = lfjs.bubble.prevdomobj;
	} else {
		lfjs.bubble.prevdomobj = domobj;
	}
	var width = 225;
	if(typeof args.width != "undefined")
		width = args.width;
	$(lfjs.bubble.domobj).width(width);
	if(!$(lfjs.bubble.domobj).find("#lfjsbubbleclose").length) {
		var img = document.createElement("img");
		$(img).attr({ id: "lfjsbubbleclose", title: "Close", src: closeimg })
			.error(function() {
				$(this).hide()
			}).click(function() {
				lfjs.bubble.hide();
			});
		$(lfjs.bubble.domobj).prepend(img);
	}
	
	$(lfjs.bubble.domobj).find(".lfjsbubblecontent").html(message);
	if (domobj) {
		var position = lfjs.bubble.calculatePosition(domobj, belowContent);
        var tail = $(".lfjsbubbletail");
        tail.show();
	
		$(lfjs.bubble.domobj).css({ position: "absolute", top: position.top, left: position.left}).show().click(function() {
			return false;
		});
	
		$(lfjs.bubble.domobj).find("a, :input").click(function(event) {
			event.stopImmediatePropagation();
			return true;
		});
		domobj.blur();
		setTimeout(function() {
			$(document.body).bind("click.hidebubble", function(event) {
				lfjs.bubble.hide();
			});
		}, 1);
	}
}
lfjs.bubble.calculatePosition = function(domobj, belowContent) {
	belowContent = (typeof belowContent != "undefined") ? belowContent : false;

    //Return object with top/left locations
    var toReturn = {};

	if (!domobj)
        return;
	
	var off = $(domobj).offset();
	var dw = $(domobj).width();

	var w = $(lfjs.bubble.domobj).width();
	var h = $(lfjs.bubble.domobj).height();

	toReturn.top = off.top - h - 5;
	toReturn.left = off.left - ((w - 70) - (dw / 2));

    //Top will be changed depending on whether we are rendering above or below the content
    var tail = $(".lfjsbubbletail");
    tail.removeClass("top left");

    if (belowContent)
    {
        toReturn.top = toReturn.top + (height) + 30;        //Calculate new top
        tail.css("top", "-5px");                //Push to 5 pixels above
        tail.addClass("top");                   //Add top class to flip the image
        return;
    }

    //Check if bubble will be out of sight (above or below)
    var windowHeight = $(window).height();
    var docTop = $(window).scrollTop();
    var docBottom = docTop + windowHeight;

    //Calculate the new bottom
    //  (add twice the height to get bottom of bubble displayed below)
    var bottom = toReturn.top + (2*h) + 20;

    if ((bottom >= docBottom) && (toReturn.top <= docTop))
    {
         //Off of top of screen completely or Off screen on both top and bottom - display based on which is off by the "least"
        if (toReturn.top < 0 || ((bottom - docBottom) < (docTop - toReturn.top)))
        {
            //Off on bottom by more than it is on top... display on top
            toReturn.top  = toReturn.top + (h) + 30;       //Calculate new top
            tail.css("top", "-5px");    //Push to 5 pixels above
            tail.addClass("top");       //Add top class to flip the image
        }
        else if ((bottom - docBottom) > (docTop - toReturn.top))
        {
            //Clear out the top value
            tail.css("top", "");
        }
    }

    //Off on top - display below
    else if (toReturn.top <= docTop)
    {
        toReturn.top  = toReturn.top + (h) + 30;       //Calculate new top
        tail.css("top", "-5px")     //Push to 5 pixels above
            .addClass("top");       //Add top class to flip the image
    }

    //Default value - clear the old top value
    else
    {
        tail.css("top", "");
    }
    
    //center bubble tail overr domobj
    if (toReturn.left < 0) {
        var right = w - (off.left + 70)
        //console.log("Right: " + right + " - Width: " + w)
        if (right > (w / 2)) {
            tail.addClass("left");
            right += 35
        }
        tail.css("right", right + "px")
        toReturn.left = 0;
    }
    else 
    {
        tail.css("right", "40px")
    }
	
    return toReturn;
};

lfjs.bubble.hide = function() {
	if (typeof lfjs.bubble.domobj != "undefined") {
		$(lfjs.bubble.domobj).hide();
	}
	$(document.body).unbind("click.hidebubble");
}
lfjs.bubble.createBubble = function() {
	if(typeof lfjs.bubble.domobj != "undefined")
		return;
	var div = document.createElement("div");
	var html = '<div class="lfjsbubbletop"></div>';
	html += '<div class="lfjsbubbletopright"></div>';
	html += '<div class="lfjsbubblemainwrapper"><div class="lfjsbubblemain">';
	html += '<div class="lfjsbubblecontent"></div></div></div>';
	html += '<div class="lfjsbubblebottom"></div>';
	html += '<div class="lfjsbubblebottomright"></div><div class="lfjsbubbletail"></div>';
	$(div).addClass("lfjsbubble").html(html).hide().appendTo(document.body);
	lfjs.bubble.domobj = div;
}
/*jshint jquery: true, browser: true, devel: true*/
/*global lfjs*/
/*exported seligo*/

lfjs.seligo = (function ($) {
	'use strict';

	var seligo = {
		CMD_CONFIG: 'config',
		CMD_DEFAULT: 'default',
		CMD_MODE_XHR: 'mode-xhr',
		CMD_MODE_INLINE: 'mode-inline',
		MODE_INLINE: 'inline',
		MODE_XHR: 'xhr',
		REGEX_FILTER: '\\b(%text%)',
		CLASS_SELECTED: 'selected',
		CLASS_SELIGO_CONTAINER: 'seligo-container',
		CLASS_SELIGO_ORIGINAL: 'seligo-original',
		CLASS_SELIGO_COVER: 'seligo-cover',
		CLASS_SELIGO_OPTIONS: 'seligo-options',
		CLASS_SELIGO_DROP: 'seligo-drop',
		CLASS_SELIGO_CURRENT: 'seligo-current',
		CLASS_SELIGO_SEARCH: 'seligo-search',
		CLASS_SELIGO_REMOVE: 'seligo-remove',
		SELECTOR_SELIGO: '.seligo',
		SELECTOR_SELIGO_CONTAINER: '.seligo-container',
		SELECTOR_SELIGO_ORIGINAL: '.seligo-original',
		SELECTOR_SELIGO_COVER: '.seligo-cover',
		SELECTOR_SELIGO_OPTIONS: '.seligo-options',
		SELECTOR_SELIGO_DROP: '.seligo-drop',
		SELECTOR_SELIGO_CURRENT: '.seligo-current',
		SELECTOR_SELIGO_SEARCH: '.seligo-search',
		SELECTOR_SELIGO_REMOVE: '.seligo-remove'
	};
	var converted = [];
	var visible = null;
	var clickStack = 0;

	/**
	 * Seligo object
	 *
	 * @param {Object} select The select DOM element being enhanced
	 * @param {Object} config The configuration settings
	 * @constructor
	 */
	var Seligo = function Seligo(select, config) {
		this.select = select;
		this.config = config;
		this.mode = seligo.MODE_INLINE;
	};

	/**
	 * Element used to resolve XHR URLs
	 *
	 * @type {HTMLElement}
	 */
	Seligo.aTag = document.createElement('a');

	/**
	 * The default filter function used by seligo
	 *
	 * @param {Object} args
	 * @param {string} args.optionIndex
	 * @param {string} args.optionText
	 * @param {string} args.optionValue
	 * @param {string} args.userText
	 * @param {RegExp} args.regExp
	 * @returns {boolean}
	 */
	Seligo.defaultFilterFunction = function defaultFilterFunction(args) {
		var match = args.optionText.match(args.regExp);
		return match === null ? false : match;
	};

	/**
	 * Get the computed CSS property value for an element
	 *
	 * @param {Object} el The DOM Element
	 * @param {String} property The CSS property to retrieve
	 * @returns {*}
	 */
	Seligo.getStyleValue = function (el, property) {
		var cs, val = false;
		// Webkit, Firefox, IE9+
		if (window.getComputedStyle) {
			cs = getComputedStyle(el, null);
			val = cs[property];
		} else if (el.currentStyle) {
			// < IE9
			val = el.currentStyle[property];
		}
		return val;
	};

	/**
	 * Handle mutation events on the original <select> element
	 *
	 * @param {Array} mutations
	 */
	Seligo.selectObserveMutations = function selectObserveMutations(mutations) {
		var childList = false;
		var attributes = false;
		var changed = false;
		var select = null;

		for (var i = 0; i < mutations.length; i++) {
			var mutation = mutations[i];

			select = mutation.target;

			switch(mutation.type) {
				case 'attributes':
					attributes = changed = true;
					break;

				case 'childList':
					childList = changed = true;
					break;
			}
		}

		if (select !== null && select.seligo) {
			if (changed) {
				select.seligo.maskSelect();
			}

			if (attributes) {
				select.seligo.updateDisabledStatus();
				select.seligo.updateDisplayStatus();
			}

			if (childList) {
				select.seligo.generateDivOptions();
			}
		}
	};

	/**
	 * Handle clicks anywhere in the document
	 *
	 * @param {Object} evt
	 */
	Seligo.documentClick = function documentClick(evt) {
		var self = evt.data;
		var onMyCover = evt.target === self.elCover;
		var onMe = evt.target === self.elDrop;
		var onMyDescendants = $.contains(self.elDrop, evt.target);

		if (!onMyCover && !onMe && !onMyDescendants) {
			self.hideDrop();
		}
	};

	/**
	 * Default configuration settings for new Seligo objects
	 *
	 * @type {Object}
	 */
	Seligo.defaultConfig = {
		xhrUrl: '',
		xhrQueryParam: 'search',
		searchPlaceholder: 'Enter your search',
		filterPlaceholder: '',
		showMode: seligo.MODE_INLINE,
		regExp: seligo.REGEX_FILTER,
		filterFunction: Seligo.defaultFilterFunction,
		onBeforeChange: null
	};

	/**
	 * Initialize the Seligo object
	 */
	Seligo.prototype.init = function init() {
		// Fall back to a default select field if MutationObserver is not
		// implemented by the browser
		if (typeof MutationObserver === 'undefined') {
			return;
		}

		this.$select = $(this.select);

		this.$select
			.addClass(seligo.CLASS_SELIGO_ORIGINAL)
			.attr('tabindex', '-1')
			.wrap('<div class="' + seligo.CLASS_SELIGO_CONTAINER + '" data-mode="' + seligo.MODE_INLINE + '">')
			.before('<div class="' + seligo.CLASS_SELIGO_COVER + '" tabindex="0">')
			.before('<div class="' + seligo.CLASS_SELIGO_OPTIONS + '">');

		this.$seligo = this.$select.parents(seligo.SELECTOR_SELIGO_CONTAINER);
		this.$cover = this.$seligo.children(seligo.SELECTOR_SELIGO_COVER);
		this.$options = this.$seligo.children(seligo.SELECTOR_SELIGO_OPTIONS);

		this.$options
			.wrap('<div class="' + seligo.CLASS_SELIGO_DROP + '" data-mode="' + seligo.MODE_INLINE + '">')
			.before('<div class="' + seligo.CLASS_SELIGO_REMOVE + '">')
			.before('<div class="' + seligo.CLASS_SELIGO_CURRENT + '">')
			.before('<input type="text" class="' + seligo.CLASS_SELIGO_SEARCH + '">');

		this.$drop = this.$seligo.children(seligo.SELECTOR_SELIGO_DROP);
		this.$remove = this.$drop.children(seligo.SELECTOR_SELIGO_REMOVE);
		this.$current = this.$drop.children(seligo.SELECTOR_SELIGO_CURRENT);
		this.$search = this.$drop.children(seligo.SELECTOR_SELIGO_SEARCH);

		this.maskSelect();
		this.generateDivOptions();
		this.updateDisabledStatus();
		this.updateDisplayStatus();

		this.$remove.click(this.removeClicked.bind(this));
		this.$select.focus(this.selectFocused.bind(this));
		this.$current.click(this.currentClicked.bind(this));

		this
			.$cover
			.click(this.coverClicked.bind(this))
			.keypress(this.coverKeyPress.bind(this))
			.keydown(this.coverKeyDown.bind(this));

		this
			.$search
			.bind('paste', this.searchKeyDown.bind(this))
			.bind('cut', this.searchKeyDown.bind(this))
			.keydown(this.searchKeyDown.bind(this));

		this
			.$options
			.delegate('div', 'mouseup', this.optionsClicked.bind(this))
			.delegate('div', 'mouseenter', this.optionsMouseEnter.bind(this));

		this.$drop.appendTo('body').keydown(this.dropKeyDown.bind(this));

		this.elOptions = this.$options[0];
		this.elCover = this.$cover[0];
		this.elDrop = this.$drop[0];
		this.lastUserText = null;

		this.observer = new MutationObserver(Seligo.selectObserveMutations);
		this.observer.observe(this.select, {attributes: true, childList: true});

		converted.push(this);
	};

	/**
	 * Register the document click handler
	 */
	Seligo.prototype.registerDocumentClick = function registerDocumentClick() {
		clickStack++;
		$(document).click(this, Seligo.documentClick);
	};

	/**
	 * Clear the document click handler
	 */
	Seligo.prototype.clearDocumentClick = function clearDocumentClick() {
		clickStack--;

		if (clickStack === 0) {
			$(document).unbind('click', Seligo.documentClick);
		}
	};

	/**
	 * Place a transparent mask over the original <select> element
	 */
	Seligo.prototype.maskSelect = function maskSelect() {
		var marginTop = parseInt(this.$select.css('marginTop'), 10);
		var marginLeft = parseInt(this.$select.css('marginLeft'), 10);
		var height = parseInt(Seligo.getStyleValue(this.select, 'height'), 10);
		var width = parseInt(Seligo.getStyleValue(this.select, 'width'), 10);

		this.$cover.css({
			height: height + 'px',
			left: (isNaN(marginLeft) ? 0 : marginLeft) + 'px',
			top: (isNaN(marginTop) ? 0 : marginTop) + 'px',
			width: width + 'px'
		});
	};

	/**
	 * Get the selected item from the original <select> element
	 *
	 * @returns {Object}
	 */
	Seligo.prototype.getBaseSelected = function getBaseSelected() {
		var $option = this.$select.children(':selected');
		return {
			value: $option.val(),
			text: $option.text()
		};
	};

	/**
	 * Handle focus events on the original <select> element
	 */
	Seligo.prototype.selectFocused = function selectFocused() {
		/*jshint validthis: true*/
		this.$select.blur();
		this.$cover.focus();
	};

	/**
	 * Re-check the display status of the original <select> element
	 */
	Seligo.prototype.updateDisplayStatus = function updateDisplayStatus() {
		if (this.$select.css('display') === 'none') {
			this.$seligo.hide();
		}
		else {
			this.$seligo.show();
		}
	};

	/**
	 * Re-check the disabled status of the original <select> element
	 */
	Seligo.prototype.updateDisabledStatus = function updateDisabledStatus() {
		this.select.statusDisabled = this.$select.attr('disabled');

		if (this.select.statusDisabled) {
			this.$cover.removeAttr('tabindex');
		}
		else {
			this.$cover.attr('tabindex', '0');
		}
	};

	/**
	 * Handle keydown events on the .seligo-cover element
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.coverKeyDown = function coverKeyDown(evt) {
		/*jshint validthis: true*/
		switch(evt.keyCode) {
			case 13: // enter
			case 32: // spacebar
			case 38: // up arrow
			case 40: // down arrow
				this.coverClicked(evt);
				return;
		}
	};

	/**
	 * Handle keypress events on the .seligo-cover element
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.coverKeyPress = function coverKeyPress(evt) {
		/*jshint validthis: true*/
		switch(evt.keyCode) {
			case 9: // tab
			case 13: // enter
			case 32: // spacebar
			case 38: // up arrow
			case 40: // down arrow
				return;

			default:
				evt.preventDefault();
				evt.stopPropagation();
				this.coverClicked(evt);
				break;
		}
	};

	/**
	 * Handle clicks on the .seligo-cover element
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.coverClicked = function coverClicked(evt) {
		if (!this.select.statusDisabled) {
			this.showDrop(evt);
		}
	};

	/**
	 * Set focus on the .seligo-cover element
	 */
	Seligo.prototype.focusCover = function focusCover() {
		this.$cover.focus();
	};

	/**
	 * Generate the unfiltered set of options
	 */
	Seligo.prototype.generateDivOptions = function generateDivOptions() {
		this.allOptions = '';

		for (var i = 0; i < this.select.options.length; i++) {
			var opt = this.select.options[i];
			this.allOptions += '<div data-value="' + opt.value + '">' + opt.text + '</div>';
		}
	};

	/**
	 * Highlight an option and make it visible in the drop down list
	 *
	 * @param {string} value The value of the option to make visible
	 */
	Seligo.prototype.highlightAndMakeVisible = function highlightAndMakeVisible(value) {
		var $highlighted = this.$options.find('[data-value="' + value + '"]');
		this.elOptions.scrollTop = 0;
		this.optionHighlight($highlighted.get(0));
		this.makeOptionVisible($highlighted.get(0));
	};

	/**
	 * Show the drop down menu
	 *
	 * @param {Object} [evt] The original event that triggered the drop down to be shown
	 */
	Seligo.prototype.showDrop = function showDrop(evt) {
		var offset = this.$cover.offset();
		var selected = this.getBaseSelected();

		this.currentSelected = selected;

		this.$drop.attr('data-current', selected.value);
		this.$current.text(selected.text);

		switch (this.config.showMode) {
			case seligo.MODE_INLINE:
				this.setModeInline();
				break;

			case seligo.MODE_XHR:
				this.setModeXhr();
				break;
		}

		this
			.$drop
			.css({
				left: offset.left + 'px',
				top: offset.top + 'px',
				minWidth: this.$cover.outerWidth() + 'px'
			})
			.show();

		var dropHeight = this.elDrop.offsetHeight;
		var optionsHeight = this.elOptions.offsetHeight;
		var deltaHeight = (offset.top - $(window).scrollTop()) + dropHeight - window.innerHeight;

		this
			.$options
			.css({
				maxHeight: Math.min(300, Math.max(30, (optionsHeight - deltaHeight) - 10)) + 'px'
			});

		this
			.$search
			.val('')
			.focus();

		this.highlightAndMakeVisible(selected.value);
		this.registerDocumentClick();

		visible = this;

		if (evt.type === 'keypress') {
			this
				.$search
				.val(String.fromCharCode(evt.charCode));

			this.filterOptions();
		}
	};

	/**
	 * Hide the drop down menu
	 */
	Seligo.prototype.hideDrop = function hideDrop() {
		visible = null;

		this.lastUserText = null;
		this.$drop.hide();
		this.$search.blur();
		this.clearDocumentClick();
	};

	/**
	 * Make the specified option visible in the scrolling list
	 *
	 * @param {Object} option The DOM element to make visible
	 */
	Seligo.prototype.makeOptionVisible = function makeOptionVisible(option) {
		this.ignoreMouseEnter = true;

		if (!option) {
			return;
		}

		var position = $(option).position();
		var height = $(option).outerHeight();
		var scrollerHeight = this.$options.innerHeight();

		if (position.top < 0 ) {
			this.elOptions.scrollTop += position.top;
		}
		else if (position.top > scrollerHeight) {
			this.elOptions.scrollTop = position.top;
		}
		else if (position.top + height > scrollerHeight) {
			this.elOptions.scrollTop += position.top + height - scrollerHeight;
		}
	};

	/**
	 * Handle keydown event on the .seligo-drop element
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.dropKeyDown = function dropKeyDown(evt) {
		var el;
		var handled = false;

		switch (evt.keyCode) {
			case 9: // tab
				handled = true;
				this.hideDrop();
				this.focusCover();
				break;

			case 13: // enter
				handled = true;
				if (this.$highlighted) {
					this.$highlighted.mouseup();
				}
				break;

			case 27: // esc
				handled = true;
				this.hideDrop();
				this.focusCover();
				break;

			case 38: // up arrow
				handled = true;
				if (this.$highlighted) {
					el = this.$highlighted.get(0);
					if (el && el.previousElementSibling) {
						this.optionHighlight(el.previousElementSibling);
						this.makeOptionVisible(el.previousElementSibling);
					}
				}
				break;

			case 40: // down arrow
				handled = true;
				if (this.$highlighted) {
					el = this.$highlighted.get(0);
					if (el && el.nextElementSibling) {
						this.optionHighlight(el.nextElementSibling);
						this.makeOptionVisible(el.nextElementSibling);
					}
				}
				break;
		}

		if (handled) {
			evt.preventDefault();
			evt.stopPropagation();
		}
	};

	/**
	 * Handle clicks on the X icon in XHR mode
	 * Clears the current selected item
	 */
	Seligo.prototype.removeClicked = function removeClicked() {
		var proceed = true;

		if (typeof this.config.onBeforeChange === 'function') {
			proceed = this.config.onBeforeChange.call(this, '');
		}

		if (proceed) {
			this.$select.val('');
			this.$select.change();
			this.currentClicked();
		}
	};

	/**
	 * Handle clicks on the current selected item
	 */
	Seligo.prototype.currentClicked = function currentClicked() {
		this.hideDrop();
		this.focusCover();
	};

	/**
	 * Done handler for XHR search request
	 *
	 * @param {Object} doc The XML document returned form the XHR
	 */
	Seligo.prototype.xhrSearchDone = function xhrSearchDone(doc) {
		var html = '';
		this.$drop.attr('data-loading', '0');

		if (doc && doc.documentElement) {
			$(doc).find('option').each(function () {
				html += '<div data-value="' + $(this).attr('value') + '">' + $(this).text() + '</div>';
			});
		}

		this.$options.html(html);
		this.elOptions.scrollTop = 0;
		this.optionHighlight(this.$options.children(':first-child').get(0));
	};

	/**
	 * Process the XHR url, adding on the query parameter
	 *
	 * @returns {string}
	 */
	Seligo.prototype.getXhrUrl = function getXhrUrl() {
		if (!this.xhrUrl) {
			Seligo.aTag.href = this.config.xhrUrl;
			Seligo.aTag.search += (Seligo.aTag.search === '' ? '' : '&') + this.config.xhrQueryParam + '=';
			this.xhrUrl = Seligo.aTag.href;
		}

		return this.xhrUrl;
	};

	/**
	 * Handle user clicks on the XHR search icon
	 */
	Seligo.prototype.xhrSearchClicked = function xhrSearchClicked() {
		var that = this;
		var userText = that.$search.val();

		// Don't perform a new search if the user text is the same
		if (userText === that.lastUserText) {
			return;
		}

		that.lastUserText = userText;

		if (userText.trim() === '') {
			that.xhrSearchDone();
			return
		}

		var isLoading = that.$drop.attr('data-loading') === '1';
		var url = that.getXhrUrl() + encodeURIComponent(userText);

		if (isLoading && that.xhr) {
			that.xhr.abort();
			that.xhr = null;
		}

		that.$drop.attr('data-loading', '1');

		that.xhr = $.ajax({
			url: url,
			seligo: true
		}).done(function (doc) {
			that.xhrSearchDone(doc);
		});

		return false;
	};

	/**
	 * Highlight the specified option
	 *
	 * @param {Object} option
	 */
	Seligo.prototype.optionHighlight = function optionHighlight(option) {
		if (option) {
			if (this.$highlighted) {
				this.$highlighted.removeClass(seligo.CLASS_SELECTED);
			}

			this.$highlighted = $(option).addClass(seligo.CLASS_SELECTED);
		}
	};

	/**
	 * Handle clicks on the list of options
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.optionsClicked = function optionsClicked(evt) {
		/*jshint validthis: true*/
		var value = $(evt.target).attr('data-value');
		var proceed = true;

		if (typeof this.config.onBeforeChange === 'function') {
			proceed = this.config.onBeforeChange.call(this, value);
		}

		if (proceed) {
			if (this.$select.children('[value="' + value + '"]').length === 0) {
				this.$select.append('<option value="' + value + '">' + $(evt.target).text() + '</option>');
			}

			this.$select.val(value);
			this.$select.change();
			this.hideDrop();
			this.focusCover();
		}
	};

	/**
	 * Handle mouseenter events on the list of options
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.optionsMouseEnter = function optionsMouseEnter(evt) {
		/*jshint validthis: true*/
		if (this.ignoreMouseEnter) {
			this.ignoreMouseEnter = false;
			return;
		}

		this.optionHighlight(evt.target);
	};

	/**
	 * Filter the options displayed in the .seligo-options list
	 */
	Seligo.prototype.filterOptions = function filterOptions() {
		var html = '';
		var selectValue = null;
		var text = this.$search.val().trim().replace(/([.?*+^$[\]\\(){}|-])/g, '\\$1');

		if (text === '') {
			html = this.allOptions;
			selectValue = this.currentSelected.value;
		}
		else {
			var match;
			var re = new RegExp(this.config.regExp.replace('%text%', text), 'i');

			for (var i = 0; i < this.select.options.length; i++) {
				var opt = this.select.options[i];
				var args = {
					userText: text,
					optionIndex: i,
					optionValue: opt.value,
					optionText: opt.text,
					regExp: re
				};

				if ((match = this.config.filterFunction(args)) !== false) {
					html += '<div data-value="' + opt.value + '">' + opt.text + '</div>';

					if (selectValue === null || opt.value === this.currentSelected.value) {
						selectValue = opt.value;
					}
				}
			}
		}

		this.$options.html(html);

		if (selectValue === this.currentSelected.value) {
			this.highlightAndMakeVisible(selectValue);
		}
		else {
			this.elOptions.scrollTop = 0;
			this.optionHighlight(
				this.$options.find('[data-value="' + selectValue + '"]').get(0)
			);
		}
	};

	/**
	 * Handle keydown events on the .seligo-search field
	 *
	 * @param {Object} evt
	 */
	Seligo.prototype.searchKeyDown = function searchKeyDown(evt) {
		var that = this;
		var func = null;
		var delay = null;

		switch (evt.keyCode) {
			case 9:
			case 13:
			case 27:
			case 38:
			case 40:
				return;
		}

		switch (that.mode) {
			case seligo.MODE_INLINE:
				delay = 100;
				func = that.filterOptions.bind(that);
				break;

			case seligo.MODE_XHR:
				delay = 200;
				func = that.xhrSearchClicked.bind(that);
				break;
		}

		clearTimeout(that.keyUpTimeout);
		that.keyUpTimeout = setTimeout(func, delay);
	};

	/**
	 * Set the mode on the seligo object and it's DOM elements
	 *
	 * @param {string} mode
	 */
	Seligo.prototype.setMode = function setMode(mode) {
		this.mode = mode;
		this.$seligo.attr('data-mode', mode);
		this.$drop.attr('data-mode', mode);
		this.$search.val('').focus();
	};

	/**
	 * Set the mode to "inline"
	 *
	 */
	Seligo.prototype.setModeInline = function setModeInline() {
		this.setMode(seligo.MODE_INLINE);
		this.filterOptions();
		this.$search.attr('placeholder', this.config.filterPlaceholder);
	};

	/**
	 * Set the mode to "xhr"
	 */
	Seligo.prototype.setModeXhr = function setModeXhr() {
		this.setMode(seligo.MODE_XHR);
		this.$options.html('');
		this.$search.attr('placeholder', this.config.searchPlaceholder);
	};

	/**
	 * Update the seligo configuration options
	 *
	 * @param {Object} config The new configuration options
	 */
	Seligo.prototype.updateConfig = function updateConfig(config) {
		this.config = $.extend(
			{},
			this.config,
			config
		);

		this.xhrUrl = null;
		this.getXhrUrl();
	};

	// Initialize on document ready
	$(function () {
		var resizeTimeout;

		$(window).resize(function windowResize() {
			if (visible !== null) {
				visible.hideDrop();
			}

			clearTimeout(resizeTimeout);
			resizeTimeout = setTimeout(
				function () {
					for (var i = 0; i < converted.length; i++) {
						var seligo = converted[i];
						seligo.maskSelect();
					}
				},
				300
			);
		});

		$(seligo.SELECTOR_SELIGO).seligo();
	});

	/**
	 * jQuery seligo plugin
	 *
	 * @param {string|Object} [command]
	 * @param {Object} [config]
	 * @returns {Array}
	 */
	$.fn.seligo = function seligoPlugin(command, config) {
		if ($.isPlainObject(command)) {
			config = command;
			command = seligo.CMD_DEFAULT;
		}

		switch (command) {
			case seligo.CMD_MODE_INLINE:
				return this.each(function modeInlineEachDomElement() {
					if (this.seligo) {
						this.seligo.setModeInline();
					}
				});

			case seligo.CMD_MODE_XHR:
				return this.each(function modeXhrEachDomElement() {
					if (this.seligo) {
						this.seligo.setModeXhr();
					}
				});

			case seligo.CMD_CONFIG:
				return this.each(function configEachDomElement() {
					if (this.seligo) {
						this.seligo.updateConfig(config);
					}
				});

			default:
				config = $.extend(
					{},
					Seligo.defaultConfig,
					config
				);

				return this.each(function initEachDomElement() {
					if (this.seligo) {
						return;
					}

					this.seligo = new Seligo(this, config);
					this.seligo.init();
				});
		}
	};

	/**
	 * Check if any one of the seligo drop down menus is visisble
	 *
	 * @returns {boolean}
	 */
	seligo.isVisible = function isVisible() {
		return visible !== null;
	};

	/**
	 * Hide the currently visible seligo drop down menu, if any
	 */
	seligo.hideVisible = function hideVisible() {
		if (visible !== null) {
			visible.hideDrop();
		}
	};

	seligo.Seligo = Seligo;

	return seligo;
})(jQuery);
/*global lfjs*/

lfjs.stache = (function lfjsStacheIIFE() {
	'use strict';

	var stache = {
		CHAR_DOT: '.',
		CHAR_END_OF_LINE: '\n',
		CHAR_ESCAPE: '\\',
		CHAR_START: '{',
		CHAR_NO_TRIM: '+',
		CHAR_LEFT_BRACKET: '[',
		CHAR_RIGHT_BRACKET: ']',
		CHARS_INTEGER: '0123456789',
		CHARS_OPERATOR: '!<>=.%*+-/&^|~',
		CHARS_SPECIAL: '()[]{}%*-+/#,:|.<>=!&',
		CHARS_WHITESPACE: ' \r\t\n',
		BLOCK_START: '{%',
		BLOCK_END: '%}',
		BLOCK_START_NO_TRIM: '{%+',
		BLOCK_END_NO_TRIM: '+%}',
		VARIABLE_START: '{{',
		VARIABLE_END: '}}',
		COMMENT_START: '{#',
		COMMENT_END: '#}',
		TOKEN_STRING: 'string',
		TOKEN_WHITESPACE: 'whitespace',
		TOKEN_DATA: 'data',
		TOKEN_BLOCK_START: 'block-start',
		TOKEN_BLOCK_END: 'block-end',
		TOKEN_VARIABLE_START: 'variable-start',
		TOKEN_VARIABLE_END: 'variable-end',
		TOKEN_COMMENT: 'comment',
		TOKEN_LEFT_PAREN: 'left-paren',
		TOKEN_RIGHT_PAREN: 'right-paren',
		TOKEN_LEFT_BRACKET: 'left-bracket',
		TOKEN_RIGHT_BRACKET: 'right-bracket',
		TOKEN_LEFT_CURLY: 'left-curly',
		TOKEN_RIGHT_CURLY: 'right-curly',
		TOKEN_OPERATOR: 'operator',
		TOKEN_COMMA: 'comma',
		TOKEN_DOT: 'dot',
		TOKEN_COLON: 'colon',
		TOKEN_PIPE: 'pipe',
		TOKEN_INTEGER: 'integer',
		TOKEN_FLOAT: 'float',
		TOKEN_BOOLEAN: 'boolean',
		TOKEN_SYMBOL: 'symbol',
		TOKEN_SPECIAL: 'special',
		TOKEN_REGEX: 'regex',
		TOKEN_NULL: 'null',
		KEYWORD_IF: 'if',
		KEYWORD_IN: 'in',
		KEYWORD_ELIF: 'elif',
		KEYWORD_ELSE: 'else',
		KEYWORD_ENDIF: 'endif',
		KEYWORD_FOR: 'for',
		KEYWORD_ENDFOR: 'endfor',
		KEYWORD_TYPEOF: 'typeof',
		KEYWORD_INSTANCEOF: 'instanceof',
		FILTER_RANGE: 'range',
		FILTER_RAW: 'raw',
		FILTER_SAFE: 'safe',
		FILTER_ESCHTML: 'eschtml',
		FILTER_ESCATTR: 'escattr',
		FILTER_ESCXML: 'escxml',
		FILTER_ESCURL: 'escurl',
		FILTER_ESCCSS: 'esccss',
		FILTER_PERCENT: 'percent',
		FILTER_DEFAULT: 'default',
		GLOBAL_PREFIX: '_g',
		OUT_VAR: '_out',
		REGEX_INTEGER: /^[-+]?[0-9]+$/
	};
	var self = stache;

	/**
	 * Object representing a token
	 *
	 * @param {number} line The line on which the token appears
	 * @param {number} column The column on which the token appears
	 * @constructor
	 */
	var Token = function Token(line, column) {
		this.type = null;
		this.value = null;
		this.line = line;
		this.column = column;
	};

	/**
	 * Set the token type and value
	 *
	 * @param {string} type
	 * @param {string} value
	 * @returns {Token}
	 */
	Token.prototype.set = function set(type, value) {
		this.type = type;
		this.value = value;
		return this;
	};

	/**
	 * Object representing a collection of tokens
	 *
	 * @param {Token[]} tokens
	 * @constructor
	 */
	var TokenCollection = function TokenCollection(tokens) {
		this.index = 0;
		this.lastIndex = tokens.length - 1;
		this.length = tokens.length;
		this.tokens = tokens;
	};

	/**
	 * See if we are at the end of the token collection
	 * @returns {boolean}
	 */
	TokenCollection.prototype.isFinished = function isFinished() {
		return this.index > this.lastIndex;
	};

	/**
	 * Get the current token in the collection
	 *
	 * @returns {Token|null}
	 */
	TokenCollection.prototype.current = function current() {
		if (this.isFinished()) {
			return null;
		}

		return this.tokens[this.index];
	};

	/**
	 * Get the next token in the collection
	 *
	 * @returns {Token|null}
	 */
	TokenCollection.prototype.next = function next() {
		if (this.index < this.lastIndex) {
			return this.tokens[this.index + 1];
		}

		return null;
	};

	/**
	 * Get the previous token in the collection
	 *
	 * @returns {Token|null}
	 */
	TokenCollection.prototype.previous = function previous() {
		if (this.index > 0) {
			return this.tokens[this.index - 1];
		}

		return null;
	};

	/**
	 * Move forward in the collection
	 */
	TokenCollection.prototype.forward = function forward() {
		this.index++;
	};

	/**
	 * Move back in the collection
	 */
	TokenCollection.prototype.back = function back() {
		this.index = Math.max(this.index - 1, 0);
	};


	/**
	 * Object representing a tokenizer
	 *
	 * @param {string} str The string to tokenize
	 * @constructor
	 */
	var Tokenizer = function Tokenizer(str) {
		this.str = str;
		this.index = 0;
		this.length = str.length;
		this.line = 1;
		this.column = 0;
		this.inCode = false;
		this.inVariable = false;
	};

	/**
	 * Get the next token from the input string
	 *
	 * @returns {Token}
	 */
	Tokenizer.prototype.nextToken = function nextToken() {
		// Nothing left to process
		if (this.isFinished()) {
			return null;
		}

		var cur = this.current();
		var token = new Token(this.line, this.column);
		var slice;

		// We are in template code
		if (this.inCode) {
			// A string
			if (cur === '"' || cur === '\'') {
				return token.set(self.TOKEN_STRING, this._extractString(cur));
			}

			// Whitespace
			else if ((slice = this._extractChars(self.CHARS_WHITESPACE)) !== null) {
				return token.set(self.TOKEN_WHITESPACE, slice);
			}

			// Block end
			else if ((slice = this._extract(self.BLOCK_END)) !== null) {
				this.inCode = false;
				return token.set(self.TOKEN_BLOCK_END, slice);
			}

			// Block end (trimmed)
			else if ((slice = this._extract(self.BLOCK_END_NO_TRIM)) !== null) {
				this.inCode = false;
				return token.set(self.TOKEN_BLOCK_END, slice);
			}

			// Variable end
			else if ((slice = this._extract(self.VARIABLE_END)) !== null) {
				this.inCode = false;
				this.inVariable = false;
				return token.set(self.TOKEN_VARIABLE_END, slice);
			}

			// Special character
			else if(this._isSpecial(cur)) {
				var type = null;

				switch(cur) {
					case '(': type = self.TOKEN_LEFT_PAREN; break;
					case ')': type = self.TOKEN_RIGHT_PAREN; break;
					case '[': type = self.TOKEN_LEFT_BRACKET; break;
					case ']': type = self.TOKEN_RIGHT_BRACKET; break;
					case '{': type = self.TOKEN_LEFT_CURLY; break;
					case '}': type = self.TOKEN_RIGHT_CURLY; break;
					case ',': type = self.TOKEN_COMMA; break;
					case ':': type = self.TOKEN_COLON; break;
					case '.': type = self.TOKEN_DOT; break;
					case '|': type = this.inVariable ? self.TOKEN_PIPE : self.TOKEN_OPERATOR; break;
					default: type = self.TOKEN_OPERATOR;
				}

				if (type === self.TOKEN_OPERATOR) {
					cur = this._extractChars(self.CHARS_OPERATOR);
				}
				else {
					this.forward();
				}

				return token.set(type, cur);
			}

			// Everything else
			else {
				slice = this._extractNotChars(self.CHARS_WHITESPACE + self.CHARS_SPECIAL);

				switch (slice) {
					case 'true':
					case 'false':
						return token.set(self.TOKEN_BOOLEAN, slice);

					case 'null':
						return token.set(self.TOKEN_NULL, slice);
				}

				if (self.REGEX_INTEGER.exec(slice) !== null) {
					if (this.current() === self.CHAR_DOT) {
						this.forward();
						slice += self.CHAR_DOT + this._extractChars(self.CHARS_INTEGER);
						return token.set(self.TOKEN_FLOAT, slice);
					}
					return token.set(self.TOKEN_INTEGER, slice);
				}

				return token.set(self.TOKEN_SYMBOL, slice);
			}
		}

		// Not in code
		else {
			// Block start (trimmed)
			if ((slice = this._extract(self.BLOCK_START_NO_TRIM)) !== null) {
				this.inCode = true;
				return token.set(self.TOKEN_BLOCK_START, slice);
			}

			// Block start
			else if ((slice = this._extract(self.BLOCK_START)) !== null) {
				this.inCode = true;
				return token.set(self.TOKEN_BLOCK_START, slice);
			}

			// Variable start
			else if ((slice = this._extract(self.VARIABLE_START)) !== null) {
				this.inCode = true;
				this.inVariable = true;
				return token.set(self.TOKEN_VARIABLE_START, slice);
			}

			// Comment start
			else if ((slice = this._extract(self.COMMENT_START)) !== null) {
				var comment = this._extractUntil(self.COMMENT_END);
				this._extract(self.COMMENT_END);
				return token.set(self.TOKEN_COMMENT, self.COMMENT_START + comment + self.COMMENT_END);
			}
			// Data
			else {
				var data = '';
				var dataPiece = '';

				while ((dataPiece = this._extractNotChars(self.CHAR_START)) !== null) {
					data += dataPiece;

					var isStartToken = this.matches(self.BLOCK_START) ||
						this.matches(self.VARIABLE_START) ||
						this.matches(self.COMMENT_START);

					if (isStartToken) {
						break;
					}
					else {
						data += this.current();
						this.forward();
					}
				}

				return token.set(self.TOKEN_DATA, data);
			}
		}
	};

	/**
	 * Check if the current index matches the provided string
	 *
	 * @param {string} str
	 * @returns {boolean}
	 */
	Tokenizer.prototype.matches = function matches(str) {
		if (this.index + str.length > this.length) {
			return false;
		}

		var slice = this.str.slice(this.index, this.index + str.length);
		return slice === str;
	};

	/**
	 * Check if a character is a special character
	 *
	 * @param {string} char
	 * @returns {boolean}
	 */
	Tokenizer.prototype._isSpecial = function _isSpecial(char) {
		switch (char) {
			case '(':
			case ')':
			case '[':
			case ']':
			case '{':
			case '}':
			case '%':
			case '*':
			case '-':
			case '+':
			case '/':
			case '#':
			case ',':
			case ':':
			case '|':
			case '.':
			case '<':
			case '>':
			case '=':
			case '!':
			case '&':
				return true;
		}

		return false;
	};

	/**
	 * Extract part of the input string from the current index
	 *
	 * @param {string} str
	 * @returns {string|null}
	 */
	Tokenizer.prototype._extract = function _extract(str) {
		var slice = this.str.slice(this.index, this.index + str.length);
		if (slice === str) {
			this.index += str.length;
			this.column += str.length;
			return str;
		}
		return null;
	};

	/**
	 * Extract part of the input string until it is not one of the characters
	 * in the chars parameter
	 *
	 * @param {string} chars
	 * @returns {string|null}
	 */
	Tokenizer.prototype._extractChars = function _extractChars(chars) {
		var extracted = null;

		while (chars.indexOf(this.current()) !== -1) {
			if (extracted === null) {
				extracted = '';
			}
			extracted += this.current();
			this.forward();
		}

		return extracted;
	};

	/**
	 * Extract part of the input string until it is one of the characters
	 * in the chars parameter
	 *
	 * @param {string} chars
	 * @returns {string|null}
	 */
	Tokenizer.prototype._extractNotChars = function _extractNotChars(chars) {
		var extracted = null;

		while (chars.indexOf(this.current()) === -1) {
			if (extracted === null) {
				extracted = '';
			}
			extracted += this.current();
			this.forward();
		}

		return extracted;
	};

	/**
	 * Extract part of the input string until it matches the provided string
	 *
	 * @param {string} str The string which will cause extraction to stop
	 * @returns {string}
	 */
	Tokenizer.prototype._extractUntil = function _extractUntil(str) {
		var extracted = '';

		while (!this.matches(str)) {
			extracted += this.current();
			this.forward();

			if (this.isFinished()) {
				throw new Error('Unexpected end of input');
			}
		}

		return extracted;
	};

	/**
	 * Extract a string token
	 *
	 * @param {string} delimiter The string enclosure character
	 * @returns {string}
	 */
	Tokenizer.prototype._extractString = function _extractString(delimiter) {
		this.forward();

		var str = '';
		var cur = null;

		while ((cur = this.current()) !== delimiter) {
			str += cur;
			if (cur === self.CHAR_ESCAPE) {
				this.forward();
				str += this.current();
			}

			this.forward();

			if (this.isFinished()) {
				throw new Error('Unexpected end of input');
			}
		}

		this.forward();
		return delimiter + str + delimiter;
	};

	/**
	 * See if we are at the end of the input
	 *
	 * @returns {boolean}
	 */
	Tokenizer.prototype.isFinished = function isFinished() {
		return this.index >= this.length;
	};

	/**
	 * Move forward to the next character
	 *
	 * @param {number} [n=1] The number of characters to move
	 */
	Tokenizer.prototype.forward = function forward(n) {
		if (n) {
			for (var i = 0; i < n; i++) {
				this.forward();
			}
		}
		else {
			this.index++;

			if(this.previous() === self.CHAR_END_OF_LINE) {
				this.line++;
				this.column = 0;
			}
			else {
				this.column++;
			}
		}
	};

	/**
	 * Get the current character
	 *
	 * @returns {string}
	 */
	Tokenizer.prototype.current = function current() {
		return this.str.charAt(this.index);
	};

	/**
	 * Get the previous character
	 *
	 * @returns {string}
	 */
	Tokenizer.prototype.previous = function previous() {
		return this.str.charAt(this.index - 1);
	};

	/**
	 * Compiler object
	 *
	 * @param {TokenCollection} tokens
	 * @param {Object} [args]
	 * @param {Object} [args.escape]
	 * @constructor
	 */
	var Compiler = function Compiler(tokens, args) {
		/** @type {TokenCollection} */
		this.tokens = tokens;
		this.blockStack = [];
		this.blockStackTop = -1;
		this.loopCounter = 0;
		this.declared = {};
		this.scope = [];
		this.currentScope = null;
		this.inScope = {};

		args = args || {};
		this.escape = args.escape !== false;
	};

	/**
	 *
	 * @param {string} message
	 * @param {Token} token
	 */
	Compiler.prototype.fail = function fail(message, token) {
		throw new Error(
			message + ': line ' + token.line + ' column ' + token.column
		);
	};

	/**
	 * Get the next token
	 *
	 * @returns {Token|null}
	 */
	Compiler.prototype.nextToken = function nextToken() {
		this.tokens.forward();
		return this.tokens.current();
	};

	/**
	 * Get the next "real" token
	 * Real tokens are everything except whitespace
	 *
	 * @returns {Token|null}
	 */
	Compiler.prototype.nextRealToken = function nextRealToken() {
		var token;

		do {
			this.tokens.forward();
			token = this.tokens.current();
		} while (token && token.type === self.TOKEN_WHITESPACE);

		return token;
	};

	/**
	 * Check if whitespace should be trimmed from the left side of the current data token
	 *
	 * @returns {boolean}
	 */
	Compiler.prototype.shouldTrimLeft = function shouldTrimLeft() {
		var prev = this.tokens.previous();
		return prev !== null &&
			prev.type === self.TOKEN_BLOCK_END &&
			prev.value.charAt(0) !== self.CHAR_NO_TRIM;
	};

	/**
	 * Check if whitespace should be trimmed from the right side of the current data token
	 *
	 * @returns {boolean}
	 */
	Compiler.prototype.shouldTrimRight = function shouldTrimRight() {
		var next = this.tokens.next();
		return next !== null &&
			next.type === self.TOKEN_BLOCK_START &&
			next.value.charAt(next.value.length - 1) !== self.CHAR_NO_TRIM;
	};

	/**
	 * Enter a scope in the template
	 */
	Compiler.prototype.enterScope = function enterScope() {
		this.currentScope = [];
		this.scope.push(this.currentScope);
	};

	/**
	 * Add a variable name to the current scope
	 *
	 * @param {string} variable
	 * @param {string} safeName
	 */
	Compiler.prototype.addScopeVar = function addScopeVar(variable, safeName) {
		safeName = safeName || true;
		this.currentScope.push({name: variable, safe: safeName});
		this.inScope[variable] = safeName;
	};

	/**
	 * Exit a scope in the template
	 */
	Compiler.prototype.exitScope = function exitScope() {
		var scopeVars = this.scope.pop();
		for (var i = 0; i < scopeVars.length; i++) {
			var scopeVar = scopeVars[i];
			delete this.inScope[scopeVar.name];
		}

		this.currentScope = this.scope[this.scope.length - 1] || [];
		for (var j = 0; j < this.currentScope.length; j++) {
			var curScopeVar = this.currentScope[j];
			this.inScope[curScopeVar.name] = curScopeVar.safe;
		}
	};

	/**
	 * Indicate that a block has been entered
	 *
	 * @param block
	 */
	Compiler.prototype.enterBlock = function enterBlock(block) {
		this.blockStack.push(block);
		this.blockStackTop = this.blockStack.length - 1;
	};

	/**
	 * Check that we are currently inside a specific block type
	 *
	 * @param block
	 * @param token
	 */
	Compiler.prototype.verifyInBlock = function verifyInBlock(block, token) {
		if (this.blockStack[this.blockStackTop] !== block) {
			this.fail('Not inside ' + block + ' block', token);
		}
	};

	/**
	 * Indicate that a block has been exited
	 *
	 * @param block
	 * @param token
	 */
	Compiler.prototype.exitBlock = function exitBlock(block, token) {
		var popped = this.blockStack.pop();
		if (popped !== block) {
			this.fail('Unexpected ' + token.value, token);
		}
		this.blockStackTop = this.blockStack.length - 1;
	};

	/**
	 * Parse variable filters
	 *
	 * @returns {Array}
	 */
	Compiler.prototype.parseFilters = function parseFilters() {
		function filter() {
			return {
				name: null,
				args: []
			};
		}

		function addArg(f, arg) {
			f.args.push(arg);
			return [];
		}

		var token;
		var inArgs = false;
		var current = filter();
		var filters = [current];
		var argStack = [];

		filters.hasRaw = false;
		filters.hasSafe = false;

		while ((token = this.nextRealToken()) !== null) {
			if (token.type === self.TOKEN_VARIABLE_END) {
				break;
			}

			switch (token.type) {
				case self.TOKEN_SYMBOL:
					if (!inArgs) {
						if (current.name !== null) {
							this.fail('Unexpected symbol: ' + token.value, token);
						}
						current.name = token.value;
						switch (current.name) {
							case self.FILTER_RAW:
								filters.hasRaw = true;
								break;

							case self.FILTER_SAFE:
							case self.FILTER_ESCHTML:
							case self.FILTER_ESCATTR:
							case self.FILTER_ESCXML:
							case self.FILTER_ESCURL:
							case self.FILTER_ESCCSS:
								filters.hasSafe = true;
								break;
						}
					}
					else {
						argStack.push(token.value);
					}
					break;

				case self.TOKEN_DOT:
					if (argStack.length > 0) {
						argStack.push(token.value);
					}
					else {
						this.fail('Unexpected dot', token);
					}
					break;

				case self.TOKEN_LEFT_PAREN:
					inArgs = true;
					break;

				case self.TOKEN_RIGHT_PAREN:
					if (argStack.length > 0) {
						argStack = addArg(current, this.scopeVar(argStack));
					}
					inArgs = false;
					break;

				case self.TOKEN_FLOAT:
				case self.TOKEN_STRING:
				case self.TOKEN_INTEGER:
				case self.TOKEN_BOOLEAN:
				case self.TOKEN_NULL:
					argStack = addArg(current, token.value);
					break;

				case self.TOKEN_COMMA:
					if (argStack.length > 0) {
						argStack = addArg(current, this.scopeVar(argStack));
					}
					break;

				case self.TOKEN_PIPE:
					current = filter();
					filters.push(current);
					break;

				default:
					this.fail('Unexpected token: ' + token.type, token);
			}
		}

		return filters;
	};

	/**
	 * Parse the contents of a variable tag
	 *
	 * @returns {string}
	 */
	Compiler.prototype.parseVariable = function parseVariable() {
		var token;
		var filters = [];
		var varStack = [];

		while ((token = this.nextRealToken()) !== null) {
			if (token.type === self.TOKEN_VARIABLE_END) {
				break;
			}

			if (token.type === self.TOKEN_PIPE) {
				filters = this.parseFilters();
				break;
			}

			switch (token.type) {
				case self.TOKEN_SYMBOL:
				case self.TOKEN_LEFT_BRACKET:
				case self.TOKEN_LEFT_PAREN:
				case self.TOKEN_RIGHT_BRACKET:
				case self.TOKEN_RIGHT_PAREN:
				case self.TOKEN_INTEGER:
				case self.TOKEN_DOT:
					varStack.push(token.value);
					break;

				default:
					this.fail('Unexpected token', token);
			}
		}

		if (this.escape && !filters.hasSafe && !filters.hasRaw) {
			filters.push({name: self.FILTER_SAFE, args: []});
		}

		var scopedVar = this.scopeVar(varStack);

		for (var i = 0; i < filters.length; i++) {
			var filter = filters[i];
			if (filter.name !== self.FILTER_RAW) {
				scopedVar = 'this.filters[\'' + filter.name + '\'](' + scopedVar;
				if (filter.args.length > 0) {
					scopedVar += ', ' + filter.args.join(', ');
				}
				scopedVar += ')';
			}
		}

		return self.OUT_VAR + ' += ' + scopedVar + ';';
	};

	/**
	 * Generate a variable declaration
	 *
	 * @param {string} variable
	 * @returns {*}
	 */
	Compiler.prototype.declare = function declare(variable) {
		var code = variable;

		if (typeof this.declared[variable] === 'undefined') {
			code = 'var ' + code;
			this.declared[variable] = true;
		}

		return code;
	};

	/**
	 * Generate a safe variable name to avoid conflicts with JavaScript reserved words
	 *
	 * @param {string} variable
	 * @returns {Object}
	 */
	Compiler.prototype.safeVar = function safeVar(variable) {
		var safe = variable;
		if (variable.charAt(0) !== '_') {
			safe = '_' + variable;
		}

		return {
			orig: variable,
			safe: safe
		};
	};

	/**
	 * Add scope handling to a variable
	 *
	 * @param varParts
	 * @returns {string}
	 */
	Compiler.prototype.scopeVar = function scopeVar(varParts) {
		var scope = self.GLOBAL_PREFIX;
		var buffer = '';
		var args = [];

		varParts.push(self.CHAR_DOT);
		for (var i = 0; i < varParts.length; i++) {
			var part = varParts[i];

			switch (part) {
				case self.CHAR_DOT:
				case self.CHAR_LEFT_BRACKET:
					args.push(buffer);
					buffer = '';
					break;

				case self.CHAR_RIGHT_BRACKET:
					// Intentional no-op
					break;

				default:
					buffer += part;
					break;
			}
		}

		if (this.inScope[args[0]]) {
			scope = args.shift();
			if (this.inScope[scope] !== true) {
				scope = this.inScope[scope];
			}
		}

		if (args.length === 0) {
			return 'this.lookup(' + scope + ')';
		}

		for (var j = 0; j < args.length; j++) {
			var argInt = parseInt(args[j], 10);
			if (isNaN(argInt)) {
				args[j] = '\'' + args[j] + '\'';
			}
		}

		return 'this.lookup(' + scope + ', ' + args.join(', ') + ')';
	};

	/**
	 * Check if a string is a JavaScript keyword
	 *
	 * @param {string} str
	 * @returns {boolean}
	 */
	Compiler.prototype.isJsKeyword = function isJsKeyword(str) {
		switch (str) {
			case self.KEYWORD_TYPEOF:
			case self.KEYWORD_INSTANCEOF:
				return true;
		}

		return false;
	};

	/**
	 * Parse the contents of an if block
	 */
	Compiler.prototype.parseIf = function parseIf() {
		var token;
		var code = '';
		var piece = '';
		var collecting = false;
		var varStack = [];

		while ((token = this.nextToken()) !== null) {
			piece = '';

			if (token.type === self.TOKEN_BLOCK_END) {
				this.tokens.back();
				break;
			}

			if (token.type === self.TOKEN_SYMBOL) {
				collecting = !this.isJsKeyword(token.value);
			}

			if (collecting) {
				switch (token.type) {
					case self.TOKEN_DOT:
					case self.TOKEN_SYMBOL:
					case self.TOKEN_LEFT_BRACKET:
					case self.TOKEN_RIGHT_BRACKET:
					case self.TOKEN_STRING:
					case self.TOKEN_INTEGER:
						varStack.push(token.value);
						break;

					default:
						collecting = false;
						piece = token.value;
				}
			}
			else {
				piece = token.value;
			}

			if (!collecting && varStack.length > 0) {
				code += this.scopeVar(varStack);
				varStack = [];
			}

			code += piece;
		}

		return code.trim();
	};

	/**
	 * Parse the contents of a for block
	 */
	Compiler.prototype.parseFor = function parseFor() {
		this.loopCounter++;
		var token;
		var iterVar = '_loop' + this.loopCounter;

		// Process up to the "in" token
		var loopVars = [];
		while ((token = this.nextRealToken()) !== null) {
			if (token.value === self.KEYWORD_IN) {
				break;
			}

			switch (token.type) {
				case self.TOKEN_SYMBOL:
					loopVars.push(token.value);
					break;

				case self.TOKEN_COMMA:
					break;

				default:
					this.fail('Unexpected token "' + token.value + '" in for block', token);
			}
		}

		var indexVar = null;
		var valueVar = null;
		switch (loopVars.length) {
			case 1:
				valueVar = this.safeVar(loopVars[0]);
				break;

			case 2:
				indexVar = this.safeVar(loopVars[0]);
				valueVar = this.safeVar(loopVars[1]);
				break;

			default:
				this.fail('Invalid for block', token);
		}

		// Process everything after the "in" token
		var varStack = [];
		var isRange = false;
		var rangeVals = [];
		while ((token = this.nextRealToken()) !== null) {
			if (token.type === self.TOKEN_BLOCK_END) {
				this.tokens.back();
				break;
			}

			switch (token.type) {
				case self.TOKEN_SYMBOL:
					var next = this.tokens.next();
					if (next.type === self.TOKEN_LEFT_PAREN) {
						if (token.value !== self.FILTER_RANGE) {
							this.fail('Unexpected filter ' + token.value, token);
						}
						isRange = true;
					}
					else {
						varStack.push(token.value);
					}
					break;

				case self.TOKEN_COMMA:
					if (!isRange) {
						this.fail('Unexpected comma', token);
					}
					break;

				case self.TOKEN_INTEGER:
					if (isRange) {
						rangeVals.push(token.value);
					}
					else {
						varStack.push(token.value);
					}
					break;

				case self.TOKEN_DOT:
				case self.TOKEN_LEFT_BRACKET:
				case self.TOKEN_RIGHT_BRACKET:
					varStack.push(token.value);
					break;
			}
		}

		if (isRange && rangeVals.length !== 2) {
			this.fail('Expected 2 parameters for range()', token);
		}

		var arrVar = isRange ?
			rangeVals[0] + ', ' + rangeVals[1] :
			this.scopeVar(varStack);

		this.addScopeVar(valueVar.orig, valueVar.safe);
		this.addScopeVar('loop', iterVar);

		var code = [
			this.declare(iterVar) + ' = new this.Iterable(' + arrVar + ');',
			this.declare(valueVar.safe) + ' = null;',
			'while ((' + valueVar.safe + ' = ' + iterVar + '.next()) !== null) {'
		];

		if (indexVar !== null) {
			this.addScopeVar(indexVar.orig, indexVar.safe);
			code.push(this.declare(indexVar.safe) + ' = ' + iterVar + '.index();');
		}

		return code.join('\n');
	};

	/**
	 * Parse contents of a block tag
	 *
	 * @returns {string}
	 */
	Compiler.prototype.parseBlock = function parseBlock() {
		var code = '';
		var token = this.nextRealToken();
		if (token.type !== self.TOKEN_SYMBOL) {
			this.fail('Unexpected token', token);
		}

		switch (token.value) {
			case self.KEYWORD_IF:
				this.enterBlock(self.KEYWORD_IF);
				code = 'if (' + this.parseIf() + ') {';
				break;

			case self.KEYWORD_ELIF:
				this.verifyInBlock(self.KEYWORD_IF, token);
				code = '} else if (' + this.parseIf() + ') {';
				break;

			case self.KEYWORD_ELSE:
				this.verifyInBlock(self.KEYWORD_IF, token);
				code = '} else {';
				break;

			case self.KEYWORD_ENDIF:
				this.exitBlock(self.KEYWORD_IF, token);
				code = '}';
				break;

			case self.KEYWORD_FOR:
				this.enterBlock(self.KEYWORD_FOR);
				this.enterScope();
				code = this.parseFor();
				break;

			case self.KEYWORD_ENDFOR:
				this.exitScope();
				this.exitBlock(self.KEYWORD_FOR, token);
				code = '}';
				break;

			default:
				this.fail('Expected keyword, got ' + token.value, token);
				break;
		}

		token = this.nextRealToken();
		if (token.type !== self.TOKEN_BLOCK_END) {
			this.fail('Expected block end, got ' + token.value, token);
		}

		return code;
	};

	/**
	 * Compile tokens to JavaScript
	 *
	 * @returns {string}
	 */
	Compiler.prototype.compile = function compile() {
		var token;
		var code = [
			'\'use strict\';' +
			'var ' + self.OUT_VAR + ' = \'\';'
		];

		while ((token = this.tokens.current()) !== null) {
			switch (token.type) {
				case self.TOKEN_DATA:
					var value = token.value;

					if (this.shouldTrimLeft()) {
						value = value.replace(/^[\s\t]+/g, '');
					}

					if (this.shouldTrimRight()) {
						value = value.replace(/[\s\uFEFF\xA0]+$/g, '');
					}

					code.push(self.OUT_VAR + ' += ' + JSON.stringify(value) + ';');
					break;

				case self.TOKEN_VARIABLE_START:
					code.push(this.parseVariable());
					break;

				case self.TOKEN_BLOCK_START:
					code.push(this.parseBlock());
					break;

				case self.TOKEN_COMMENT:
					// Do nothing with comments
					break;

				default:
					this.fail('Unexpected token', token);
					break;
			}

			this.tokens.forward();
		}

		code.push('return ' + self.OUT_VAR + ';');

		return code.join('\n');
	};

	/**
	 * The stache runtime
	 */
	stache.runtime = function runtime() {
		var REGEX_BAD_CHARS = /[&<>"'`]/g;
		var REPLACEMENTS = {
			'&': '&amp;',
			'<': '&lt;',
			'>': '&gt;',
			'"': '&quot;',
			'\'': '&#x27;',
			'`': '&#x60;'
		};

		/**
		 * Callback for String.replace()
		 *
		 * @param {string} char
		 * @returns {string}
		 */
		var replaceChar = function replaceChar(char) {
			return REPLACEMENTS[char] || char;
		};

		/**
		 * Variable lookup function
		 *
		 * @returns {string}
		 */
		var lookup = function lookup() {
			var value = arguments[0];

			for (var i = 1; i < arguments.length; i++) {
				if (value && typeof value === 'object') {
					value = value[arguments[i]];
				}
				else {
					value = void 0;
					break;
				}
			}

			return typeof value === 'undefined' ? '' : value;
		};

		/**
		 * Iterable object
		 *
		 * @param {Array|Object} obj
		 * @constructor
		 */
		var Iterable = function Iterable(obj) {
			var idx = 0;

			if (arguments.length === 2) {
				var range = [];
				for (var i = arguments[0]; i <= arguments[1]; i++) {
					range.push(i);
				}
				obj = range;
			}

			if (Array.isArray(obj)) {
				this.length = obj.length;
				this.end = this.length - 1;
				this.next = function next() {
					this.first = idx === 0;
					this.last = idx === this.end;
					if (idx > this.end) {
						return null;
					}
					var val = obj[idx];
					idx++;
					return val;
				};
				this.index = function index() {
					return idx;
				};
			}
			else if (Object.prototype.toString.call(obj) === '[object Object]') {
				this.keys = Object.keys(obj);
				this.length = this.keys.length;
				this.end = this.length - 1;
				this.next = function next() {
					this.first = idx === 0;
					this.last = idx === this.end;
					if (idx > this.end) {
						return null;
					}
					var val = obj[this.keys[idx]];
					idx++;
					return val;
				};
				this.index = function index() {
					return this.keys[idx];
				};
			}
			else {
				this.next = function next() { return null; };
				this.index = function index() { return idx; };
				this.first = false;
				this.last = false;
				this.length = 0;

			}
		};

		var filters = {};

		/**
		 * Default value filter
		 *
		 * @param val
		 * @param def
		 * @returns {*}
		 */
		filters['default'] = function filterDefaultValue(val, def) {
			if (typeof val === 'undefined' || val === '' || val === null) {
				return def;
			}
			return val;
		};

		/**
		 * Percentage filter
		 *
		 * @param part
		 * @param whole
		 * @param precision
		 * @returns {string}
		 */
		filters.percent = function filterPercent(part, whole, precision) {
			precision = parseInt(precision, 10);

			if (isNaN(precision)) {
				precision = 1;
			}

			part = parseFloat(part);
			whole = parseFloat(whole);
			if (isNaN(whole) || isNaN(part) || whole === 0) {
				return '0%';
			}

			var pct = (part / whole) * 100;
			return pct.toFixed(precision).toString() + '%';
		};

		/**
		 * eschtml filter and safe alias
		 *
		 * @param str
		 * @returns {*}
		 */
		filters.safe = filters.eschtml = function filterEscHtml(str) {
			return typeof str === 'string' ? str.replace(REGEX_BAD_CHARS, replaceChar) : str;
		};

		/**
		 * escattr filter
		 *
		 * @param str
		 * @returns {*}
		 */
		filters.escattr = function filterEscAttr(str) {
			return typeof str === 'string' ? str.replace(REGEX_BAD_CHARS, replaceChar) : str;
		};

		/**
		 * escurl filter
		 *
		 * @param str
		 * @returns {*}
		 */
		filters.escurl = function filterEscUrl(str) {
			return str;
		};

		/**
		 * escxml filter
		 *
		 * @param str
		 * @returns {*}
		 */
		filters.escxml = function filterEscXml(str) {
			return typeof str === 'string' ? str.replace(REGEX_BAD_CHARS, replaceChar) : str;
		};

		/**
		 * esccss filter
		 *
		 * @param str
		 * @returns {*}
		 */
		filters.esccss = function filterEscCss(str) {
			return str;
		};

		/**
		 * Create the runtime
		 *
		 * @returns {Object}
		 */
		return (function create() {
			var rt = {
				lookup: lookup,
				Iterable: Iterable,
				filters: {},
				filter: function addFilter(name, func) {
					this.filters[name] = func;
				}
			};

			for (var filter in filters) {
				rt.filters[filter] = filters[filter];
			}

			return rt;
		})();
	};

	/**
	 * Lex a string
	 *
	 * @param {string} str
	 * @returns {TokenCollection}
	 */
	stache.lex = function lex(str) {
		var token;
		var tokens = [];
		var tokenizer = new Tokenizer(str);

		while ((token = tokenizer.nextToken()) !== null) {
			tokens.push(token);
		}

		return new TokenCollection(tokens);
	};

	/**
	 * Compile a stache template
	 *
	 * @param {string} str The string to compile
	 * @param {Object} [args]
	 * @param {Object} [args.escape=true]
	 * @returns {Object}
	 */
	stache.compile = function compile(str, args) {
		var compiler = new Compiler(self.lex(str), args);
		var compiled = compiler.compile();
		var runtime = self.runtime();

		runtime.render = new Function(self.GLOBAL_PREFIX, compiled);

		return runtime;
	};

	return stache;
})();
