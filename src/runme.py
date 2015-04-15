from data import DataObject
from graph import RemoveUrls, Port
from unigram_counter import UnigramCounter

tweets = ["www.google.com", "facebook.com that controls my life www.grooveshark.com which I love."]
ip1 = Port([], None)
ip1.update(tweets)
node = RemoveUrls(ip1)
#ip2 = op1
#op2 = Port([])
#node_unigram = UnigramCounter(ip2, op2)
#node_unigram.run()
print tweets
print node.get_ouput_ports()[0].get()
