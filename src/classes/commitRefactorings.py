
class CommitRefactorings():
  def __init__(self, sha):
    self.sha = sha
    self.__ExtractMethod = 0
    self.__InlineMethod = 0
    self.__MoveMethodOrAttribute = 0
    self.__PullUpMethodOrAttribute = 0
    self.__PushDownMethodOrAttribute = 0
    self.__ExtractSuperclassOrInterface = 0
    self.__MoveClass = 0
    self.__RenameClass = 0
    self.__RenameMethod = 0
    self.__ExtractAndMoveMethod = 0
    self.__ChangePackage = 0
    self.__Total = 0
  
  def __eq__(self, other):
    """Override the default Equals behavior"""
    return self.sha == other.sha
  
  def addExtractedMethod(self):
    self.__ExtractMethod += 1
    self.__addTotal()
  def addInlineMethod(self):
    self.__InlineMethod += 1
    self.__addTotal()
  def addMoveMethodOrAttribute(self):
    self.__MoveMethodOrAttribute += 1
    self.__addTotal()
  def addPullUpMethodOrAttribute(self):
    self.__PullUpMethodOrAttribute += 1
    self.__addTotal()
  def addPushDownMethodOrAttribute(self):
    self.__PushDownMethodOrAttribute += 1
    self.__addTotal()
  def addExtractSuperclassOrInterface(self):
    self.__ExtractSuperclassOrInterface += 1
    self.__addTotal()
  def addMoveClass(self):
    self.__MoveClass += 1
    self.__addTotal()
  def addRenameClass(self):
    self.__RenameClass += 1
    self.__addTotal()
  def addRenameMethod(self):
    self.__RenameMethod += 1
    self.__addTotal()
  def addExtractAndMoveMethod(self):
    self.__ExtractAndMoveMethod += 1
    self.__addTotal()
  def addChangePackage(self):
    self.__ChangePackage += 1
    self.__addTotal()
  def __addTotal(self):
    self.__Total += 1
  
  def getTotal(self):
    return self.__Total
  def getExtractedMethod(self):
    return self.__ExtractMethod
  def getInlineMethod(self):
    return self.__InlineMethod
  def getMoveMethodOrAttribute(self):
    return self.__MoveMethodOrAttribute
  def getPullUpMethodOrAttribute(self):
    return self.__PullUpMethodOrAttribute
  def getPushDownMethodOrAttribute(self):
    return self.__PushDownMethodOrAttribute
  def getExtractSuperclassOrInterface(self):
    return self.__ExtractSuperclassOrInterface
  def getMoveClass(self):
    return self.__MoveClass
  def getRenameClass(self):
    return self.__RenameClass
  def getRenameMethod(self):
    return self.__RenameMethod
  def getExtractAndMoveMethod(self):
    return self.__ExtractAndMoveMethod
  def getChangePackage(self):
    return self.__ChangePackage