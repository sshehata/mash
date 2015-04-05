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
        for i in range(len(records)):
            records[i] = re.sub(RemoveUrls.URL_REGEX, "URL", records[i])
        self.output_port.update(data)

class Port:
#TODO Update the active set of flags
    def __init__(self, required_flags):
        self.required_flags = required_flags    #To check compatibility between ports Ex:
                              #POS_TAGGED, TOKENIZED

    def get(self):
        return self.data

    def update(self, data):
        self.data = data

    
