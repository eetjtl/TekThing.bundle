####################################################################################################

PREFIX = "/video/tekthing"
NAME = "TekThing Podcast"

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():

# Setup the default breadcrumb title for the plugin
ObjectContainer.title1 = NAME

# This main function will setup the displayed items.
# Initialize the plugin
@handler(PREFIX, NAME)  #, thumb="icon-default.png", art="art-default.jpg")
def MainMenu():
oc = ObjectContainer()

return oc