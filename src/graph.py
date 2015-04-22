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
    self.output_port = Port([], self.run)

  def run(self):
    records = self.input_port.get()
    records = [re.sub(RemoveUrls.URL_REGEX, "URL", record) for record in records]
    self.output_port.update(records)

  def get_ouput_ports(self):
    return [self.output_port]

class NaiveBayes_model:
  def __init__(self, training_set):
    self.training_set = training_set
    self.model = Port([], self.run)

  def run(self):
    self.model.update(nltk.NaiveBayesClassifier.train(training_set.get()))

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
