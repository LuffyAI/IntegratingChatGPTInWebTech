var lfjs = lfjs || {};
var lf = lf || {};
var isSpidercode = false;
var tcfdata = tcfdata || {};
if (typeof print_doc === "function" &&
		typeof print_debug === "function" &&
		typeof addwarning === "function") {
	isSpidercode = true;	
}

function error(msg) {
// Report error, on client or server side.
	if (isSpidercode)
		addwarning(msg);
	else
		alert(msg);
}

function warn(msg) {
// Report minor warning, on client or server side.
	msg = "WARNING: " + msg;
	if (isSpidercode)
		print_debug(msg + '\n');
	else if (window.console)
		window.console.log(msg);
}

function info(msg) {
// Report verbose log message using warn(), but only if tcfdata.verbose (or
// on browser, lf.verbose) is set.
	if (isSpidercode) {
		if (!tcfdata.verbose || !tcfdata.verbose[0])
			return;
	}
	else if (!lf.verbose)
		return;
	msg = "INFO: " + msg;
	if (isSpidercode)
		print_debug(msg + '\n');
	else if (window.console)
		window.console.log(msg);
}

if (! isSpidercode) {
	var escxml = function (url) {
		if (!url || typeof url !== "string")
			return '';
		url = url.replace("&", "&amp;")
			.replace("<", "&lt;")
			.replace(">", "&gt;")
			.replace('"', "&quot;");
		return url;
	};

	var escurl = function (url) {
		url = escxml(url);
		if (!url || typeof url !== "string")
			return '';
		return url.replace(/^.*(javascript|data):/, '');
	};

	var escattr = function (str) {
		return escxml(str).replace(/'/g, '&#39;');
	}

	/*
	// TODO: a real one; this is just a placeholder in case we need it
	var escjsvar = function (str) {
		return str.replace(/["']/g, '');
	};
	*/
}

lfjs.neatpath = function(path) {
	if (!path)
		return '';
	else
		return path.replace(/\/(index|default)\.[^\/]+$/, "/");
}

lfjs.repeat = function(str, count, delim) {
	if (!delim)
		delim = '';
	var ret_arr = [];
	for (var i=0; i < count; i++)
		ret_arr.push(str);
	return ret_arr.join(delim);
}


//
// Begin utils copied directly out of lfjs.js.
// If we can get this file included in <script> tags everywhere, they should be
// deleted from lfjs.js and maintained here.
//

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

