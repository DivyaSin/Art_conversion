import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import httplib, urllib, base64, json
from urllib2 import Request, urlopen
import matplotlib.image as mpimg

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '5216b6516c044672ac78e87efe525abf',
}

params = urllib.urlencode({
    # Request parameters
    'maxCandidates': '1',
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1.0/describe?%s" % params, "{'url':'http://i68.tinypic.com/2d82rli.jpg'}", headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    features = data["description"]["captions"][0]["text"]
    search_text_components = str(features).strip().split(" ")
    search_text = '+'.join(search_text_components[0:])
    url = "http://api.giphy.com/v1/gifs/search?q=%s&limit=10&api_key=dc6zaTOxFJmzC" % search_text
    print url
    request = Request(url)
    random_image = json.loads(urlopen(request).read())
    length = len(random_image['data'])
    from random import randint
    url = random_image['data'][randint(0,length - 1)]['url']
    print url
    testfile = urllib.URLopener()
    conn.close()
except Exception as e:
    print ("[Errno {0}] {1}".format(e.errno, e.strerror))

data = urllib.urlencode({"text": features})
print data
u = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
the_page = json.loads(u.read())
sentiment = str(the_page["label"])
print "----"
print sentiment

# New figure with white background
fig = plt.figure(figsize=(6,6),facecolor='white')
size = fig.get_size_inches()*fig.dpi # size in pixels

# New axis over the whole figure, no frame and a 1:1 aspect ratio
ax = fig.add_axes([0,0,1,1], frameon=False, aspect=1)

# Number of ring
n = 100
size_min = 50
size_max = 500

# Ring position
P = np.random.uniform(0,1,(n,2))

# Ring colors
C = np.ones((n,4)) * (1,0,0,1)

# Alpha color channel goes from 0 (transparent) to 1 (opaque)
C[:,3] = np.linspace(0,1,n)

# Ring sizes
S = np.linspace(size_min, size_max, n)

# Scatter plot
if (sentiment == 'neutral'):
    img=mpimg.imread('deepskyblue.png')
    imgplot = plt.figimage(img)
    scat = ax.scatter(P[:,0], P[:,1], s=S, lw = 0.5,
                  edgecolors = C, facecolors='skyblue')

elif(sentiment == 'pos'):
    img=mpimg.imread('pink_blue#A429F6.jpg')
    imgplot = plt.figimage(img)
    scat = ax.scatter(P[:,0], P[:,1], s=S, lw = 0.5,
                  edgecolors = C, facecolors='#A429F6')

elif(sentiment == 'neg'):
    img=mpimg.imread('dark_image.jpg')
    imgplot = plt.figimage(img)
    scat = ax.scatter(P[:,0], P[:,1], s=S, lw = 0.5,
                  edgecolors = C, facecolors='grey')


# Ensure limits are [0,1] and remove ticks
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])

def update(frame):
    global P, C, S

    # Every ring is made more transparent
    C[:,3] = np.maximum(0, C[:,3] - 1.0/n)

    # Each ring is made larger
    S += (size_max - size_min) / n

    # Reset ring specific ring (relative to frame number)
    i = frame % 100
    P[i] = np.random.uniform(0,1,2)
    S[i] = size_min
    C[i,3] = 1

    # Update scatter object
    scat.set_edgecolors(C)
    scat.set_sizes(S)
    scat.set_offsets(P)

    # Return the modified object
    return scat,

animation = FuncAnimation(fig, update, interval=5, blit=True, frames=200)
#animation.save('sentiment.gif', writer='imagemagick', fps=30, dpi=40)
plt.show()
