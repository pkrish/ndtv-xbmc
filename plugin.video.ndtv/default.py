'''
Created on Jun 24, 2012

@author: praveen
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys

thisPlugin = int(sys.argv[1])

liveTVURL1="http://bglive-a.bitgravity.com/ndtv/247lo/live/native"

liveTVURL2="http://www.yupptv.com/streams/ndtvenglish.aspx"

vodLinkPrefix="http://bitcast-b.bitgravity.com/ndtvod/23372/ndtv/"
#http://bitcast-b.bitgravity.com/ndtvod/23372/ndtv/18062012_n_TopMontek_150782_55918.mp4

def CATEGORIES():
    addLink("Live TV",liveTVURL1,"")
    addDir("Most Popular","http://www.ndtv.com/video",2,"")
    addDir("The Big Fight","http://www.ndtv.com/video/list/shows/Big+Fight",2,"")
    addDir("We The People","http://www.ndtv.com/video/list/shows/We+The+People",2,"")
    addDir("NDTV 24x7","http://www.ndtv.com/video/list/channel/NDTV+24x7",2,"")
    addDir("NDTV Profit","http://www.ndtv.com/video/list/channel/NDTV+Profit",2,"")
    addDir("Buck Stops Here","http://www.ndtv.com/video/list/shows/Buck+Stops+Here",2,"")
    addDir("Battleground","http://www.ndtv.com/video/list/shows/Battleground",2,"")
    addDir("The 9 O'Clock News","http://www.ndtv.com/video/list/shows/The+9+O%27Clock+News",2,"")
    addDir("Left, Right & Center","http://www.ndtv.com/video/list/shows/Left%2C+Right+%26+Centre",2,"")
    addDir("Truth vs Hype","http://www.ndtv.com/video/list/shows/Truth+vs+Hype",2,"")
    addDir("Walk The Talk","http://www.ndtv.com/video/list/shows/Walk+The+Talk",2,"")
    
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('').findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,2,thumbnail)

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        page=response.read()
        response.close()
        videoDivs = page.split('<li class="">')

        for videoDiv in videoDivs[1:len(videoDivs)-1]:
                #print "line: " + str(videoDiv)
                #parse the video page link
                vLinkTemp = re.compile('http.*"').findall(videoDiv)
                vLink = str(str(vLinkTemp[0]).split('"')[0])
                
                #vTitle = vLink
                
                #parse the video title
                #vTitleTemp = re.compile('<a href=".*">.*</a>').findall(videoDiv)
                #vTitle = str(str(str(vTitleTemp[0]).split('">')[1]).split('<')[0])
                vTitleTemp = re.compile('title=".*"').findall(videoDiv)
                vTitle = str(str(vTitleTemp[0]).split('"')[1])

                #parse the video thumbnail 
                vIconTemp = re.compile('original=".*"').findall(videoDiv)
                vIcon = str(str(vIconTemp[0]).split('"')[1])

                #parse the video duration
                vDuration = re.compile('[0-9]{1,2}:[0-9]{2}').findall(videoDiv)

                vTitle = vTitle + " - " + vDuration[0]
                
                #fetch video link for each item
                addDir(vTitle,vLink,3,vIcon)

def VIDEOLINKS2(url,name,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('__filename=.*.mp4').findall(link)
        
        for line in match:
                vLink = str(str(line).split('\'')[1])
                addLink(name,vodLinkPrefix+vLink,iconimage)

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=str(iconimage))
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+iconimage
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=str(iconimage))
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
     
              
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "iconimage: "+str(iconimage)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==3:
        print ""+url
        VIDEOLINKS2(url,name,iconimage)
        

xbmcplugin.endOfDirectory(int(sys.argv[1]))

