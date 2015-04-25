class SplitNode:
  # TODO Naming convention

  """
  Type: Node
  Function: Splits the dataset into 2 sets
  Input port requirements: DATASET, PERCENTAGES
  Output port promises: a tuple that contains the 2 new sets
  """

  def __init__(self, input_port, output_port1, output_port2):
    self.input_port = input_port
    self.output_port1 = output_port1
    self.output_port2 = output_port2

  def run(self):
    # TODO Define the function to get the percentages from the port
    # TODO Define the function to set the output port splitsets
    # TODO Agree on the output ports features
    dataset = self.input_port.get()
    out1_percentage, out2_percentage = input_port.get_percentages()
    out1_end = int(out1_percentage * len(dataset))
    out1 = dataset[:out1_end]
    out2 = dataset[out1_end:]
    self.output_port1.data = out1
    self.output_port2.data = out2
