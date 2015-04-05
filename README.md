# mash
Sentiment Analysis framework written in python!

- split dataset
- tokenizer
- remove mentions
- process hashtags
- remove urls
- POS tagging
- unigram counter
- remove stop words
- summarizier
- naiver bayes classifier
- accuracy evaluater

Design Decision:
- Port carries one data object
- if u need more than one dataobject, use multiple ports
- shoof rabid miner 

Design questions:
- should the same dataobject be modified between the input and the output ports
  and thus needing a cloner node
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


