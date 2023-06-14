import os
from pathlib import Path
import shutil
import tempfile
import unittest
import subprocess

class Git:

    repo = Path("./test-repo")

    def init(self):
        shutil.rmtree(self.repo, ignore_errors=True)
        self.repo.mkdir(parents=True)
        os.chdir(self.repo)
        os.system("git init")
        os.system("touch file.txt")
        os.system("git add file.txt")
        os.system("git commit -m \"test commit\"")
        return self

    def createBranch(self, name):
        os.system("git branch %s" % name)

    def checkoutBranch(self, name):
        os.system("git checkout %s" % name)        

    def checkoutTask(self, id):
        return subprocess.getoutput("git checkout-task %s" % id).strip()

class TestGitCommand(unittest.TestCase):
	
    def test_no_branch(self):
        git = Git().init()
        self.assertEqual(git.checkoutTask("ABC-123"), "No branches found for ABC-123")

    def test_already_on_branch(self):
        git = Git().init()
        git.createBranch("ABC-123/test-branch")
        git.checkoutTask("ABC-123/test-branch")
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
        self.assertEqual(git.checkoutTask("ABC-123"), "Checking out ABC-123/test-branch\nSwitched to branch 'ABC-123/test-branch'")

        git.init()
        git.createBranch("ABC-123-test-branch")
        self.assertEqual(git.checkoutTask("ABC-123"), "Checking out ABC-123-test-branch\nSwitched to branch 'ABC-123-test-branch'")

        # git.init()
        # git.createBranch("feature/ABC-123-test-branch")
        # self.assertEqual(git.checkoutTask("ABC-123"), "Checking out feature/ABC-123-test-branch\nSwitched to branch 'feature/ABC-123-test-branch'")


if __name__ == '__main__':
    unittest.main()