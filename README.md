### Overview
___
* project from Data Engineering course on dataquest.io 
* basically word count example
* Hacker News posts json data used (not included)
* used to familiarize with concepts of:
  - functional programming
  - closures 
  - decorators
  - directed acyclic graph scheduler
  - pipelines
### TO DO
___
* Rewrite the Pipeline class' output to save a file of the output for each task. This will allow "checkpoint" tasks so they don't have to be run twice.
* Use the nltk package for more advanced natural language processing tasks.
* Convert to a CSV before filtering, so we can keep all the stories from 2014 in a raw file.
* Fetch the data from Hacker News directly from a JSON API. Instead of reading from the file provided, 
* Perform additional data processing using newer data