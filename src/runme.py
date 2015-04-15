from data import DataObject
from graph import RemoveUrls, Port
from unigram_counter import UnigramCounter

tweets = ["www.google.com", "facebook.com that controls my life www.grooveshark.com which I love."]
data = DataObject(tweets)
ip1 = Port([])
op1 = Port([])
ip1.update(data)
node = RemoveUrls(ip1, op1)
node.run()
ip2 = op1
op2 = Port([])
node_unigram = UnigramCounter(ip2, op2)
node_unigram.run()
print tweets
print op2.data.records
