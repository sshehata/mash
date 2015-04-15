import re

class RemoveUrls:
  """
  Type: Node
  Function: Replace urls from raw text.
  Input port requirements: RAW_TEXT
  Output port promises: no changes
  """

  URL_REGEX = r"(http(s)?://.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

  def __init__(self, input_port, output_port):
    self.input_port = input_port
    self.output_port = output_port

  def run(self):
    data = self.input_port.get()
    records = data.records
    recorde = [re.sub(RemoveUrls.URL_REGEX, "URL", record) for record in records]
    self.output_port.update(data)

class Port:
  # TODO Update the active set of flags

  def __init__(self, required_flags):
    # To check compatibility between ports Ex:
    self.required_flags = required_flags
    #POS_TAGGED, TOKENIZED

  def get(self):
    if not self.data:
      raise Exception, "Port contains no data"
    return self.data

  def update(self, data):
    self.data = data
