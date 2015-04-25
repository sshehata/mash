from data import DataObject
from graph import RemoveUrls, Port, Reader, Tokenizer
from unigram_counter import UnigramCounter

tweets = ["www.google.com", "facebook.com that controls my life www.grooveshark.com which I love."]
ip1 = Port([], None)
ip1.update(tweets)
node = RemoveUrls(ip1)
#ip2 = op1
#op2 = Port([])
#node_unigram = UnigramCounter(ip2, op2)
#node_unigram.run()
node_reader = Reader('tweets.csv')
node_reader.read()
tweets = node_reader.get_output_ports()[0].get()
#print node_reader.get_output_ports()[0].get()
#print node_reader.get_output_ports()[1].get()
#print tweets
#print node.get_output_ports()[0].get()
node_tok = Tokenizer(tweets)
node_tok.run()
out = node_tok.get_port("tokenized_records")
for o1 in out.get():
    for o2 in o1:
        print(o2 + "\n")
