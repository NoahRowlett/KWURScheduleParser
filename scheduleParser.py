import collections
import sys, os, re
import HTMLParser
 
if len(sys.argv) < 2:
	sys.exit("Usage: %s filename. No command line argument found that specifies a file to use." % sys.argv[0])

DAYS = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

#thanks to http://stackoverflow.com/questions/4126348/how-do-i-rewrite-this-function-to-implement-ordereddict/4127426#4127426
class OrderedDefaultdict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        if not args:
            self.default_factory = None
        else:
            if not (args[0] is None or callable(args[0])):
                raise TypeError('first argument must be callable or None')
            self.default_factory = args[0]
            args = args[1:]
        super(OrderedDefaultdict, self).__init__(*args, **kwargs)

    def __missing__ (self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = default = self.default_factory()
        return default

    def __reduce__(self):  # optional, for pickle support
        args = (self.default_factory,) if self.default_factory else tuple()
        return self.__class__, args, None, None, self.iteritems()

filename = sys.argv[1]
schedule = OrderedDefaultdict(list)
 
if not os.path.exists(filename):
	sys.exit("Error: File '%s' not found" % sys.argv[1])

def timeifyHelper(timeFragment):
	timeString = ""
	if(timeFragment=="00"):
		timeString="12am"
	elif(timeFragment[0]=="0"):
		timeString=timeFragment[1] + "am"
	else:
		numTime = int(timeFragment)
		if(numTime < 12):
			timeString=timeFragment + "am"
		elif(numTime == 12):
			timeString=timeFragment + "pm"
		else:
			timeString=str(numTime-12) + "pm"
	return timeString

def timeify(time):
	startTime = timeifyHelper(time[1])
	endTime = timeifyHelper(time[2])
	
	timeString = startTime + "-" + endTime
	dayString = DAYS[int(time[0])]
	return dayString, timeString

class Show:
	# constructor:
	def __init__(self, time, name, genre, tagline, description):
		self.time = timeify(time)
		self.name = name.rstrip()
		self.genre = genre.rstrip()
		self.tagline = tagline.rstrip()
		self.description = description.rstrip()

	def get_time(self):
		return self.time 

	def get_name(self):
		return self.name

	def get_genre(self):
		return self.genre

	def get_tagline(self):
		return self.tagline

	def get_description(self):
		return self.description

	def set_time(self, time):
		self.time = time.rstrip()

	def set_name(self, name):
		self.name = name.rstrip()

	def set_genre(self, genre):
		self.genre = genre.rstrip()

	def set_tagline(self, tagline):
		self.tagline = tagline.rstrip()

	def set_description(self, description):
		self.description = description.rstrip()

	def format_output(self):
		return  self.get_time()[1] + " - " + self.get_name() + " - " + self.get_genre() + " - " + self.get_tagline()

	def format_html_output(self):
		string = "<tr height=\"16\">\n"
		string += "\t<td height=\"16\" style=\"height:21px;\">" + self.get_time()[1] + "</td>\n"
		string += "\t<td>" + self.get_name() + "</td>\n"
		string += "\t<td>" + self.get_genre() + "</td>\n"
		string += "\t<td>" + self.get_tagline() + "</td>\n"
		string += "</tr>\n"
		return string


def parseString(string):
	match = re.findall(r"<tr valign=\"top\" bgcolor=\"(.*)\"><td nowrap=\"1\">(.*)</td>(.*)\">(.*)</A></td><td>(.*)</td><td>(.*)</td><td>(.*)</td></tr>", string)
	if match is not None:
		return match

def infoOrg(infoContainer):
	if isinstance(infoContainer,list):
		if len(infoContainer) > 0:
			info = infoContainer[0]
			time = re.findall(r"(.*)](.*):00-(.*):00", info[1])
			show = Show(time[0], info[3], info[4], info[5], info[6])
			schedule[show.time[0]].append(show)

def printNumberedList(sDict):
	if isinstance(sDict,OrderedDefaultdict):
		counter = 0
		for day in sDict.values():
			for show in day:
				counter += 1
				print str(counter) + ". " + show.format_output()

def printHTMLTable(sDict):
	if isinstance(sDict,OrderedDefaultdict):
		for day,shows in sDict.items():
			print "<p>&nbsp;</p>\n"
			print "<p><span style=\"font-family:times new roman,times,serif;\"><strong>" + day + "</strong></span></p>\n"
			print "<p>&nbsp;</p>\n"
			print "<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" dir=\"ltr\" style=\"width:754px;\" width=\"754\">\n<colgroup>\n<col /><col /><col /><col /></colgroup>\n<tbody>\n<tr>\n<td height=\"16\" style=\"height:21px;width:75px; padding-left:2px; padding-right:2px;\"><strong>Time</strong></td>\n<td style=\"width:225px;\"><strong>Show Name</strong></td>\n<td style=\"width:225px;\"><strong>Genre</strong></td>\n<td style=\"width:225px;\"><strong>Tagline</strong></td>\n</tr>\"\n"
			for show in shows:
				print show.format_html_output()
			print "</tbody>\n</table>"
			print "<p>&nbsp;</p>\n"



#Main
f = open(filename)
for line in f:
	lineAsString = line.rstrip()
	lineAsString = HTMLParser.HTMLParser().unescape( lineAsString ) 
	if parseString(lineAsString) is not None:
		infoOrg(parseString(lineAsString))
#printNumberedList(schedule)
printHTMLTable(schedule)
f.close()
