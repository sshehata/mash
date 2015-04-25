import re, nltk, csv
from decorators import run_once

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
    self.output_port = Port([], self.run)

  def run(self):
    records = self.input_port.get()
    records = [re.sub(RemoveUrls.URL_REGEX, "URL", record) for record in records]
    self.output_port.update(records)

  def get_output_ports(self):
    return [self.output_port]

class NaiveBayes_model:
  def __init__(self, training_set, labels):
    self.training_set = training_set
    self.labels = labels
    self.model = Port([], self.run)

  def run(self):
    training_set = self.training_set.get()
    labels = self.labels.get()
    self.model.update(nltk.NaiveBayesClassifier.train( zip(training_set,
        labels)))

  def get_output_ports(self):
    return [self.model]

class NaiveBayes_classifier:
  def __init__(self, model, data):
    self.model = model
    self.data = data
    self.labels = Port([], self.run)

    def run(self):
      model = self.model.get()
      records = self.data.get()
      self.labels.update([model.classify(record) for record in records])

    def get_output_ports(self):
      return [self.labels]

class Summarizer:
  """
  Type: Node
  Function: Summarizes tokenized records into most useful.
  Input port requirements: TOKENIZED
  Output port promises: no changes
  """

  def __init__(self, records_port, labels_port, unigram_count=150):
    self.records_port = records_port
    self.labels_port = labels_port
    self.tokens_port = Port([], self.run)
    self.unigram_count = unigram_count

  @run_once
  def run(self):
    records = self.records_port.get()
    labels = self.labels_port.get()
    dist = nltk.FreqDist(token for record in records for token in record if \
        token not in nltk.corpus.stopwords.words(english) and token.isalpha())
    self.tokens_port.update([word for word, count in \
        dist.most_common(self.unigram_count)])

  def get_output_ports(self):
    return [self.tokens_port]

class evaluater:
  def __init__(self, labels, golden):
    self.labels = labels
    self.golden = golden
    self.acc = Port([], self.run)

  @run_once
  def run(self):
    labels = self.labels
    golden = self.golden
    correct = [ l == g for (l, g) in zip(labels, golden) ]
    if correct:
      self.acc.update(float(sum(correct))/len(correct))
    else:
      self.acc.update(0)

  def get_output_ports(self):
    return [self.acc]

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

class Reader:

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.sents = Port([], self.read)
        self.labels = Port([], self.read)

    def read(self):
        sents = []
        labels = []
        csv_file = open(self.input_file_path, 'rb')
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            sents += [row[0]]
            labels += [row[1]]
        self.sents.update(sents)
        self.labels.update(labels)

    def get_output_ports(self):
        return [self.sents, self.labels]


