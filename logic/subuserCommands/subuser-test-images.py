#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

try:
  import pathConfig
except ImportError:
  pass
#external imports
import sys
import optparse
#internal imports
from subuserlib.classes.user import User
import subuserlib.commandLineArguments
import subuserlib.testImages
from subuserlib.classes.permissionsAccepters.acceptPermissionsAtCLI import AcceptPermissionsAtCLI

def parseCliArgs(realArgs):
  usage = "usage: subuser test-images <repo-name> <image-source-names>"
  description = """ Test image sources by building and running them.

  Usage:

  1. Add a temporary local repository to build your images from:

     subuser repository add test-repo /home/timothy/current/subuser-default-repository

     Note: by specifying the path as a local directory, you do not need to commit your changes to git before testing them.

  2. Test the image sources.

     subuser test-images test-repo iceweasel vim

  3. Remove the left over images.

     subuser remove-old-images --repo=test-repo

   """
  parser=optparse.OptionParser(usage=usage,description=description,formatter=subuserlib.commandLineArguments.HelpFormatterThatDoesntReformatDescription())
  parser.add_option("--accept",dest="accept",action="store_true",default=False,help="Accept permissions without asking.")
  return parser.parse_args(args=realArgs)

def testImages(realArgs):
  """
  Test the given images.
  """
  options,args = parseCliArgs(realArgs)
  user = User()
  permissionsAccepter = AcceptPermissionsAtCLI(user,alwaysAccept = options.accept)
  with user.getRegistry().getLock() as lockFileHandler:
    subuserlib.testImages.testImages(user=user,sourceRepoId=args[0],imageSourceNames=args[1:],permissionsAccepter=permissionsAccepter)

#################################################################################################

if __name__ == "__main__":
  testImages(sys.argv[1:])
