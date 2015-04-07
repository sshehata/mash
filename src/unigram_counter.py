'''
Created on Apr 8, 2015

@author: maged
'''

from data import DataObject

class UnigramCounter(object):
    '''
    classdocs
    '''


    def __init__(self, input_port, output_port):
        '''
        Constructor
        '''
        self.input_port = input_port
        self.output_port = output_port
        
    def run(self):
        data = self.input_port.get()
        records = data.records
        u = DataObject([])
        unigrams = u.records
        for i in range(len(records)):
            unigrams.append(dict())
            for word in records[i].split(" "):
                if not unigrams[i].has_key(word):
                    unigrams[i][word] = 1
                else:    
                    unigrams[i][word]+=1
                #print word + ' ' + str(unigrams[i][word])
        self.output_port.update(u)