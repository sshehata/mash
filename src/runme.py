from data import DataObject
from graph import RemoveUrls, Port

tweets = ["www.google.com", "facebook.com that controls my life www.grooveshark.com which I love."]
data = DataObject(tweets)
ip = Port([])
op = Port([])
ip.update(data)
node = RemoveUrls(ip, op)
node.run()
print tweets
