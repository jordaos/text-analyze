from enum import Enum

class RefactoringsEnum(Enum):
  ExtractMethod = 1
  InlineMethod = 2
  MoveMethod = 3
  MoveAttribute = 3
  PullUpMethod = 4
  PullUpAttribute = 4
  PushDownMethod = 5
  PushDownAttribute = 5
  ExtractSuperclass = 6
  ExtractInterface = 6
  MoveClass = 7
  RenameClass = 8
  RenameMethod = 9
  ExtractAndMoveMethod = 10
  ChangePackage = 11