# ################################################
# 			Global Variables
PREFIX 	 = "/video/tekthing"
NAME 	 = "TekThing Podcast"
ART      = 'art-default.jpg'
ICON     = 'icon-default.png'
RSSFEED  = 'http://feeds.feedburner.com/tekthing'
YT_START = 'embed/'
YT_END = '?wmode'
# ################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
	# Setup the default breadcrumb title for the plugin
	ObjectContainer.title1 = NAME
	HTTP.CacheTime = CACHE_1HOUR
	
# Setup main landing page
@handler(PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer()
	xml = XML.ElementFromURL(RSSFEED)

	for item in xml.xpath('//item'):
		try :
			title = item.xpath('./title/text()')[0]
		except :
			pass
		thumb = Resource.ContentsOfURLWithFallback(url=GetThumbUrl(item), fallback=R(ICON))
		url = GetVideoUrl(item)
		
		if url:
			url = item.xpath('./link/text()')[0]	# Use page url, need tp pass to service to get summary on video page.

			oc.add(VideoClipObject(
				url = url, 
				title = title, 
				thumb = thumb
				)
			)
		
	# Display empty ObjectContainer and write to log.
	if len(oc) < 1:
		Log.Debug('No items found in Feed')
		return ObjectContainer(header="Empty", message="No Videos found for this Show right now.")     
	return oc

# Unfortunately the episode summary is unreliable at best. Maybe after a few more
# episodes they will finalize their rss feed.
def GetEpisodeSummary(item):
	itunesSummary = item.xpath('./*[local-name()="summary"]/text()')
	if len(itunesSummary) > 0:
		return itunesSummary[0]
	description = item.xpath('./description/text()')
	if len(description) > 0 and 'iframe' not in description[0]:
		Log.Debug('description: ' + description[0])
		return description[0]
	return 'No Summary Available'

# See if we can pull the thumbnail from the RSS feed via the youtube url.
def GetThumbUrl(item):
	content = item.xpath('./*[local-name()="encoded"]/text()')
	if len(content) > 0:
		youtubeurl = FindYoutubeUrl(content[0])
		if youtubeurl:
			Log.Debug('youtube url 1: ' + youtubeurl)
			return youtubeurl
	content = item.xpath('./description/text()')
	if len(content) > 0:
		youtubeurl = FindYoutubeUrl(content[0])
		if youtubeurl:
			Log.Debug('youtube url 2: ' + youtubeurl)
			return youtubeurl
	Log.Debug('no content found')
	return R(ICON)

def GetVideoUrl(item):
	# Need to research how to do this without service.
	enclosure = item.xpath('./enclosure')
	if len(enclosure) > 0:
		return enclosure[0].get('url')
	return ''

def FindYoutubeUrl(content):
	startIndex = content.find(YT_START) + len(YT_START)
	endIndex = content.find(YT_END)
	return 'http://img.youtube.com/vi/' + content[startIndex:endIndex] + '/0.jpg'
