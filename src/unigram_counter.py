"""
Created on Apr 8, 2015

@author: maged
"""

from data import DataObject
import re

class UnigramCounter(object):

  """
  Type: Node
  Function: Counts unigrams in text.
  Input port requirements: RAW_TEXT
  Output port promises: UNIGRAMS
  """

  def __init__(self, input_port, output_port):
    """
    Constructor
    """
    self.input_port = input_port
    self.output_port = output_port

  def run(self):
    data = self.input_port.get()
    records = data.records
    u = DataObject([])
    unigrams = u.records
    delimiters = " ", ".", ","
    regex_pattern = '|'.join(map(re.escape, delimiters))
    for i in range(len(records)):
      unigrams.append(dict())
      # print re.split(regex_pattern,records[i])
      for word in re.split(regex_pattern, records[i]):
        if word == "":
          continue
        if word not in unigrams[i]:
          unigrams[i][word] = 1
        else:
          unigrams[i][word] += 1
        # print word + ' ' + str(unigrams[i][word])
    self.output_port.update(u)
