from decorators import run_once
import csv
import nltk
import re


class RemoveUrls:

  """
  Type: Node
  Function: Replace urls from raw text.
  Input port requirements: RAW_TEXT
  Output port promises: no changes
  """

  URL_REGEX = r"(http(s)?://.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

  def __init__(self, input_port):
    self.input_port = input_port
    self.training_set = Port([], self.run)
    self.output_ports = {'training_set': self.training_set}

  def run(self):
    records = self.input_port.get()
    records = [re.sub(RemoveUrls.URL_REGEX, "URL", record)
               for record in records]
    self.training_set.update(records)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class SVM_model:

  def __init__(self, training_set_port, labels_port):
    self.training_set_port = training_set_port
    self.labels_port = labels_port
    self.model_port = Port([], self.run)
    self.output_ports = {'model': self.model_port }

  @run_once
  def run(self):
    training_set = self.training_set_port.get()
    labels = self.labels_port.get()
    classif = nltk.classify.scikitlearn.SklearnClassifier(
        sklearn.svm.LinearSVC())
    self.model_port.update(classif.train(zip(training_set, labels)))

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class SVM_classifier:

  def __init__(self, model_port, data_port):
    self.model_port = model_port
    self.data_port = data_port
    self.labels = Port([], self.run)
    self.output_ports = {'labels': self.labels}

  @run_once
  def run(self):
    model = self.model_port.get()
    records = self.data_port.get()
    self.labels.update([model.classify(record) for record in records])

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]

class NaiveBayes_model:

  def __init__(self, training_set, labels):
    self.training_set = training_set
    self.labels = labels
    self.model_port = Port([], self.run)
    self.output_ports = {'model': self.model_port}

  def run(self):
    training_set = self.training_set.get()
    labels = self.labels.get()
    self.model_port.update(nltk.NaiveBayesClassifier.train(zip(training_set,
                                                          labels)))

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class NaiveBayes_classifier:

  def __init__(self, model, data):
    self.model = model
    self.data = data
    self.labels = Port([], self.run)
    self.output_ports = {'labels': self.labels}

  def run(self):
    model = self.model.get()
    records = self.data.get()
    self.labels.update([model.classify(record) for record in records])

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class Summarizer:

  """
  Type: Node
  Function: Summarizes tokenized records into most useful.
  Input port requirements: TOKENIZED
  Output port promises: no changes
  """

  def __init__(self, records_port, unigram_count=150):
    self.records_port = records_port
    self.unigram_count = unigram_count
    self.tokens_port = Port([], self.run)
    self.output_ports = {'bag-of-words': self.tokens_port}

  @run_once
  def run(self):
    records = self.records_port.get()
    dist = nltk.FreqDist(token for record in records for token in record if
                         token not in nltk.corpus.stopwords.words("english") and token.isalpha())
    self.tokens_port.update([word for word, count in
                             dist.most_common(self.unigram_count)])

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class Evaluater:

  def __init__(self, labels_port, golden_port):
    self.labels_port = labels_port
    self.golden_port = golden_port
    self.acc_port = Port([], self.run)
    self.output_ports = {'accuracy': self.acc_port}

  @run_once
  def run(self):
    labels = self.labels_port.get()
    golden = self.golden_port.get()
    correct = [l == g for (l, g) in zip(labels, golden)]
    if correct:
      self.acc_port.update(float(sum(correct)) / len(correct))
    else:
      self.acc_port.update(0)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class UnigramCounter(object):

  """
  Type: Node
  Function: Counts unigrams in text.
  Input port requirements: RAW_TEXT
  Output port promises: UNIGRAMS
  """

  def __init__(self, data_port, tokens_port):
    self.data_port = data_port
    self.tokens_port = tokens_port
    self.unigrams_port = Port([], self.run)
    self.output_ports = {'unigrams': self.unigrams_port}

  @run_once
  def run(self):
    data = self.data_port.get()
    most_frequent_tokens = self.tokens_port.get()
    unigrams = [
        [record.count(token) for token in most_frequent_tokens] for record in data]
    self.unigrams_port.update(unigrams)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class SplitNode:

  """
  Type: Node
  Function: Splits the dataset into 2 sets
  Input port requirements: DATASET, PERCENTAGES
  Output port promises: a tuple that contains the 2 new sets
  """

  def __init__(self, input_port, ratio=0.8):
    self.input_port = input_port
    self.ratio = ratio
    self.output_port1 = Port([], self.run)
    self.output_port2 = Port([], self.run)
    self.output_ports = {'first-set': self.output_port1, 'second-set':
        self.output_port2}

  def run(self):
    # TODO Define the function to get the percentages from the port
    # TODO Define the function to set the output port splitsets
    # TODO Agree on the output ports features
    dataset = self.input_port.get()
    out1_end = int(self.ratio * len(dataset))
    out1 = dataset[:out1_end]
    out2 = dataset[out1_end:]
    self.output_port1.update(out1)
    self.output_port2.update(out2)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class Reader:

  def __init__(self, input_file_path):
    self.input_file_path = input_file_path
    self.sents = Port([], self.read)
    self.labels = Port([], self.read)
    self.output_ports = {'records': self.sents, 'labels': self.labels}

  @run_once
  def read(self):
    sents = []
    labels = []
    csv_file = open(self.input_file_path, 'r')
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      sents += [row[0]]
      labels += [row[1]]
    self.sents.update(sents)
    self.labels.update(labels)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class Tokenizer:

  def __init__(self, records_port):
    self.records_port = records_port
    self.tokenized_records_port = Port([], self.run)
    self.output_ports = {"tokenized_records" : self.tokenized_records_port}

  def run(self):
    tokenized_recs = []
    for tweet in self.records_port.get():
      tokenized_recs = tokenized_recs + [nltk.word_tokenize(tweet)]
    self.tokenized_records_port.update(tokenized_recs)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]

class POSTagger:
  def __init__(self, data_port):
    self.data_port = data_port
    self.tagged_data_port = Port([], self.run)
    self.output_ports = {'POS-tagged': self.tagged_data_port}

  @run_once
  def run(self):
    data = self.data_port.get()
    tags = [[tag for (word, tag) in nltk.pos_tag(record)] for record in data]
    self.tagged_data_port.update(tags)

  def get_output_ports(self):
    return self.output_ports.keys()

  def get_port(self, port):
    return self.output_ports[port]


class Port:
  # TODO Update the active set of flags

  def __init__(self, required_flags, ex_func):
    # To check compatibility between ports Ex:
    self.required_flags = required_flags
    self.ex_func = ex_func
    self.data = None
    #POS_TAGGED, TOKENIZED

  def get(self):
    if not self.data:
      self.ex_func()
    return self.data

  def update(self, data):
    self.data = data
