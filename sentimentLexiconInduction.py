"""
SENTIMENT ANALYSIS USING LEXICON PHRASES

SUBMITTED BY:
    PALASH PARMAR
    626008848
"""

import sys
import os
import math
import re





class SentimentLexiconInduction:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """FSentiment Lexicon Induction Initilizations"""
    self.numFolds = 10
    self.phrase_near_great = {}
    self.phrase_near_poor = {}
    self.pos_hit = 0
    self.neg_hit = 0
    self.phrase_polarity = {}
    
    
    """parameter initilizations"""
    self.polarity_threshold = 4
    self.search_radius = 10
    self.pos_word = 'great'
    self.neg_word = 'poor'
    
    


  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    polarity = 0
    l = len(words)
    for i in range(len(words)-2):
        match = []
        line = (words[i]+' '+words[i+1]+' '+words[i+2])
        match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(NN|NNS)_(.+) (.+)_(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(JJ)_(.+) (.+)_(?!NN|NNS)(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(JJ)_(.+) (.+)_(?!NN|NNS)(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(NN|NNS)_(.+) (.+)_(JJ)_(.+) (.+)_(?!NN|NNS)(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(VB|VBD|VBN|VBG)_(.+) (.+)_(.+)_(.+)', line))
        
        
        
        bool_values = [m!=None for m in match]
        
        
        
   
        if(any(bool_values)):
            word1 = (match[bool_values.index(True)].group(1)).lower()
            word2 = (match[bool_values.index(True)].group(4)).lower()
            polarity += self.phrase_polarity.get((word1,word2),0)
                
    
    match = []
    line = (words[l-2]+' '+words[l-1])
    match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(NN|NNS)_(.+)', line))
    match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(JJ)_(.+)', line))
    match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(JJ)_(.+)', line))
    match.append(re.match(r'(.+)_(NN|NNS)_(.+) (.+)_(JJ)_(.+)', line))
    match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(VB|VBD|VBN|VBG)_(.+)', line))
    
    
    
    bool_values = [m!=None for m in match]
    
    if(any(bool_values)):
        word1 = (match[bool_values.index(True)].group(1)).lower()
        word2 = (match[bool_values.index(True)].group(4)).lower()
        polarity += self.phrase_polarity.get((word1,word2),0)
        
    if(polarity > 0):
        return 'pos'
    else:
        return 'neg'
    
  
  def calculate_phase_polarity(self):
      for phrase in self.phrase_near_great.keys():
          if self.phrase_near_great[phrase] < self.polarity_threshold and self.phrase_near_poor[phrase] < self.polarity_threshold:
              continue
          self.phrase_polarity[phrase] = math.log(self.phrase_near_great[phrase]*self.neg_hit,2)-math.log(self.phrase_near_poor[phrase]*self.pos_hit,2)
  
  def near_hits(self, words, i, near):
      count = 0.01
      for j in range(0,self.search_radius + 1):
          if(i-j<0):
              break
          else:
              match = re.match(r'(.+)_(.+)_(.+)', words[i-j])
              if (match.group(1)).lower() == near:
                  count += 1
      for j in range(1,self.search_radius + 2):
          if(i+j>=len(words)):
              break
          else:
              
              match = re.match(r'(.+)_(.+)_(.+)', words[i+j])
              if (match.group(1)).lower() == near:
                  count += 1
              
      return(count)
        

  def addExample(self, klass, words):
    
    l = len(words)
    
    
    for i in range(len(words)-2):
        match = []
        line = (words[i]+' '+words[i+1]+' '+words[i+2])
        match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(NN|NNS)_(.+) (.+)_(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(JJ)_(.+) (.+)_(?!NN|NNS)(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(JJ)_(.+) (.+)_(?!NN|NNS)(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(NN|NNS)_(.+) (.+)_(JJ)_(.+) (.+)_(?!NN|NNS)(.+)_(.+)', line))
        match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(VB|VBD|VBN|VBG)_(.+) (.+)_(.+)_(.+)', line))
        
        
        
        bool_values = [m!=None for m in match]
        
        current_word = ((re.match(r'(.+)_(.+)_(.+)', words[i])).group(1)).lower()
        
        if(current_word == self.pos_word):
            self.pos_hit += 1
        if(current_word == self.neg_word):
            self.neg_hit += 1
        
   
        if(any(bool_values)):
            word1 = (match[bool_values.index(True)].group(1)).lower()
            word2 = (match[bool_values.index(True)].group(4)).lower()
            
            
            self.phrase_near_great[word1, word2] = self.phrase_near_great.get((word1, word2), 0.0) + self.near_hits(words, i, self.pos_word)
            self.phrase_near_poor[word1, word2] = self.phrase_near_poor.get((word1, word2), 0.0) + self.near_hits(words, i, self.neg_word)
        
    
    match = []
    line = (words[l-2]+' '+words[l-1])
    match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(NN|NNS)_(.+)', line))
    match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(JJ)_(.+)', line))
    match.append(re.match(r'(.+)_(JJ)_(.+) (.+)_(JJ)_(.+)', line))
    match.append(re.match(r'(.+)_(NN|NNS)_(.+) (.+)_(JJ)_(.+)', line))
    match.append(re.match(r'(.+)_(RB|RBR|RBS)_(.+) (.+)_(VB|VBD|VBN|VBG)_(.+)', line))
    
    bool_values = [m!=None for m in match]
    if(any(bool_values)):
        word1 = (match[bool_values.index(True)].group(1)).lower()
        word2 = (match[bool_values.index(True)].group(4)).lower()
        
        self.phrase_near_great[word1, word2] = self.phrase_near_great.get((word1, word2), 0.0) + self.near_hits(words, l-2, self.pos_word)
        self.phrase_near_poor[word1, word2] = self.phrase_near_poor.get((word1, word2), 0.0) + self.near_hits(words, l-2, self.neg_word)
    
    for i in range(2):
        word = ((re.match(r'(.+)_(.+)_(.+)', words[l-2+i])).group(1)).lower()
        if word == self.pos_word:
            self.pos_hit += 1
        if word == self.neg_word:
            self.neg_hit += 1
    
        
    
  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      
      self.addExample(example.klass, words)


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args):
  nb = SentimentLexiconInduction()
  splits = nb.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = SentimentLexiconInduction()

    accuracy = 0.0
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words)
      
    classifier.calculate_phase_polarity()
    
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0
    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy
    
    
def classifyDir(trainDir, testDir):
  classifier = SentimentLexiconInduction()

  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
  testSplit = classifier.trainSplit(testDir)
  accuracy = 0.0
  classifier.calculate_phase_polarity()
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy


def main():
    
    args = sys.argv[1:]
    
    if len(args) == 2:
        classifyDir(args[0], args[1])
    elif len(args) == 1:
        test10Fold(args)


if __name__ == "__main__":
    main()
