import wx
import wx.adv


class App(wx.App):

	path = "%userprofile%/appdata/Local/Programs"
	root: root

	def OnPreInit(self):
		wx.Exit()

	def OnInit(self):
		pass

	def OnExit(self):
		pass


if __name__ == '__main__':
	app = App()
	app.MainLoop()
