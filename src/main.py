from pathlib import Path
import tempfile

import wx
import wx.adv
from semver import VersionInfo

from ui import root


class App(wx.App):

	# changeable properties
	version: str = 'v1.17.11'
	repoApiUrl: str = 'https://api.github.com/repos/Bridge-Core/Bridge./releases'
	installPath: Path = Path( '%userprofile%/appdata/Local/Programs/Bridge' ).resolve()
	# window properties
	title: str = f'Bridge. {version} installer'
	height: int = 178
	width: int = 440
	# do not change
	root: root
	updating: bool = installPath.exists()
	instanceChecker = wx.SingleInstanceChecker()

	def OnInit(self):
		if self.instanceChecker.IsAnotherRunning():
			return False
		if not self.installPath.exists():
			self.installPath.mkdir(exist_ok=True, parents=True)
		self.SetAppName('BridgeInstaller')
		self.root = root(self)
		self.root.Show(True)
		self.SetTopWindow(self.root)
		self.root.Raise()
		return True

	def OnExit(self):
		return True


if __name__ == '__main__':
	app = App()
	app.MainLoop()
