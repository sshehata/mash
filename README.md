# mash
Sentiment Analysis framework written in python!

  - read raw text (array of records)
  - split dataset
  - tokenizer (array of records, each array of tokens)
  - remove mentions
  - process hashtags
  - remove urls
  - POS tagging
  - unigram counter
  - remove stop words
  - summarizier
  - naiver bayes classifier
  - accuracy evaluater
  - duplicator

  Design Decision:
  - Port carries one data object
  - if u need more than one dataobject, use multiple ports
  - Node creates its own output port explicitly
  - Output port calls method that is attached to it on creation
  - node is only evaluated once, caches in the node
  - ports pass normal python object
  - pull method
  - ports carry promises, evaluated by the node on port creation from
    input port promises
  - shoof rabid miner


  Design questions:
  - should the same dataobject be modified between the input and the output ports and thus needing a cloner node
  or
  create a new dataobject and kill it when the output port is no longer needed

  Future work:
  - introduce phases
  EX:
  remove url in phase 0
  pos tagging in phase 1
  classifier phase 2
  why: we can automate ordering of nodes to prevent editing duplicate text, tokens
  and meta.


