from graph import *

tweets = ["www.google.com", "facebook.com that controls my life www.grooveshark.com which I love."]

tweeets = [["I", "am", "a", "bad", "coder"]]

reader = Reader("tweets.csv")
tokenizer = Tokenizer(reader.get_port("records"))
summarizer = Summarizer(tokenizer.get_port("tokenized_records"))
unigramer = UnigramCounter(tokenizer.get_port("tokenized_records"),
    summarizer.get_port("bag-of-words"))
unigram_splitter = SplitNode(unigramer.get_port("unigrams"))
label_splitter = SplitNode(reader.get_port("labels"))
trainer = NaiveBayes_model(unigram_splitter.get_port("first-set"),
    label_splitter.get_port("first-set"))
classifier = NaiveBayes_classifier(trainer.get_port("model"),
    unigram_splitter.get_port("second-set"))

evaluater = Evaluater(classifier.get_port("labels"),
    label_splitter.get_port("second-set"))

print("The accuracy of the pipeline is", evaluater.get_port("accuracy").get())
