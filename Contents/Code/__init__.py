# ################################################
# 			Global Variables
PREFIX 	 = "/video/tekthing"
NAME 	 = "TekThing Podcast"
ART      = 'art-default.jpg'
ICON     = 'icon-default.png'
RSSFEED  = 'http://feeds.feedburner.com/tekthing'
# ################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
	# Setup the default breadcrumb title for the plugin
	ObjectContainer.title1 = NAME

# Setup main landing page
@handler(PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer()
	xml = RSS.FeedFromURL(RSSFEED)				# Info on RSS API: https://dev.plexapp.com/docs/api/parsekit.html#module-RSS
	for item in xml.entries:					# Use FeedParser to get the "items", in this case episodes (/rss/channel/item): https://pythonhosted.org/feedparser/reference-entry.html
	
		# Pull the data that is available in the form of link, title, date and description. Use get to check if element exists: https://pythonhosted.org/feedparser/basic-existence.html
		title = item.get('title', NAME)												# Get the video title
		date = Datetime.ParseDate(item.get('pubDate', ''))							# Get the date the video is released
		url = item.get('link', '')													# Get the link to the video page
		desc = item.get('description', '')											# Get the episode summary
		
		oc.add(VideoClipObject(
			url = url, 
			title = title, 
			summary = desc, 
			thumb = R(ICON),						# Use generic thumb for time being, Feed doesn't give a thumb and site pages don't have suitable image.
			originally_available_at = date
			)
		)
		
	# Display empty ObjectContainer and write to log.
	if len(oc) < 1:
		Log ('No items found in Feed')
		return ObjectContainer(header="Empty", message="No Videos found for this Show right now.")     
	return oc