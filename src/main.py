import wx
import wx.adv
from ui import root
import tempfile


class App(wx.App):

	downloadUrl = 'TODO'
	installPath = '%userprofile%/appdata/Local/Programs'
	root: root
	updating: bool = False
	# window properties
	title: str = 'Bridge. {ver} installer'
	height: int = 178
	width: int = 440

	def OnInit(self):
		self.root = root(self)
		self.root.Show(True)
		self.root.Raise()
		return True

	def OnExit(self):
		return True


if __name__ == '__main__':
	app = App()
	app.MainLoop()
