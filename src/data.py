class DataObject:
    """
    Function: Holds a list of objects representing the data and
              an active set of flags.
    """
    def __init__(self, records):
        self.records = records
        self.flags = set()

    def add_flag(flag):
        self.flags.add(flag)

    def check_flag(flag):
        return flag in self.flags
