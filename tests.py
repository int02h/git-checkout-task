import os
from pathlib import Path
import shutil
import tempfile
import unittest
import subprocess

class Git:

    repo = Path("./test-repo").resolve()

    def init(self):
        shutil.rmtree(self.repo, ignore_errors=True)
        self.repo.mkdir()
        os.chdir(self.repo)
        os.system("git init")
        os.system("touch file.txt")
        os.system("git add file.txt")
        os.system("git commit -m \"test commit\"")
        return self

    def createBranch(self, name):
        os.system("git branch %s" % name)

    def deleteBranchLocally(self, name):
        os.system("git branch -D %s" % name)

    def checkoutBranch(self, name):
        os.system("git checkout %s" % name)        

    def checkoutTask(self, id):
        result = subprocess.getoutput("git checkout-task %s" % id).strip()
        print("checkoutTask: %s" % result)
        return result

    def setupRemote(self): 
        os.system("git remote add test-origin git@github.com:int02h/git-checkout-task.git")
        os.system("git fetch")
        return self

    def setupUpstream(self, branch):
        os.system("git branch -u test-origin/%s %s" % (branch, branch))

class TestGitCommand(unittest.TestCase):
	
    def test_no_branch(self):
        git = Git().init()
        self.assertEqual(git.checkoutTask("ABC-123"), "No branches found for ABC-123")

    def test_already_on_branch(self):
        git = Git().init()
        git.createBranch("ABC-123/test-branch")
        git.checkoutBranch("ABC-123/test-branch")
        self.assertEqual(git.checkoutTask("ABC-123"), "Already on ABC-123/test-branch")

    def test_more_than_one_branch(self):
        git = Git().init()
        git.createBranch("ABC-123/test-branch-1")
        git.createBranch("ABC-123/test-branch-2")
        self.assertEqual(git.checkoutTask("ABC-123"), "There are clashing branches for ABC-123:\n- ABC-123/test-branch-1\n- ABC-123/test-branch-2")


    def test_checkout_success(self):
        git = Git()
        git.init()
        git.createBranch("ABC-123/test-branch")
        self.assertTrue(git.checkoutTask("ABC-123").startswith("Checking out ABC-123/test-branch"))

        git.init()
        git.createBranch("ABC-123-test-branch")
        self.assertTrue(git.checkoutTask("ABC-123").startswith("Checking out ABC-123-test-branch"))

        git.init()
        git.createBranch("feature/ABC-123-test-branch")
        self.assertTrue(git.checkoutTask("ABC-123").startswith("Checking out feature/ABC-123-test-branch"))

        git.init()
        git.createBranch("bug-fix/ABC-123-test-branch")
        self.assertTrue(git.checkoutTask("ABC-123").startswith("Checking out bug-fix/ABC-123-test-branch"))

    def test_checkout_success_remote_and_local(self):
        git = Git().init().setupRemote()
        git.createBranch("ABC-123-test-branch")
        git.setupUpstream("ABC-123-test-branch")
        self.assertTrue(git.checkoutTask("ABC-123").startswith("Checking out ABC-123-test-branch"))

    def test_checkout_success_remote_only(self):
        git = Git().init().setupRemote()
        git.createBranch("ABC-123-test-branch")
        git.setupUpstream("ABC-123-test-branch")
        git.deleteBranchLocally("ABC-123-test-branch")
        self.assertTrue(git.checkoutTask("ABC-123").startswith("Checking out ABC-123-test-branch"))

if __name__ == '__main__':
    unittest.main()