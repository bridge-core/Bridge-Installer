import wx
import wx.adv
from wx.lib.progressindicator import ProgressIndicator
import tempfile
import threading
import requests
from PIL import Image


def getBitmap():
	png: Image.Image = Image.open('icon.png')
	png = png.resize( (38, 38) )
	width, height = png.size
	return wx.Bitmap.FromBufferRGBA(width, height, png.convert('RGBA').tobytes() )


class root(wx.Frame):

	def __init__(self, app: 'App'):
		super().__init__(
			parent=None,
			title='Bridge. installer',
			size=wx.Size( app.width, app.height ),
			style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX ^ wx.RESIZE_BORDER
		)
		self.SetIcon( wx.Icon('./icon.png') )
		self.CenterOnScreen()
		self.SetBackgroundColour(wx.Colour(240, 240, 240))
		icon = wx.StaticBitmap(
			parent=self,
			bitmap=getBitmap(),
			pos=wx.Point(20, 14)
		)
		text = wx.StaticText(
			parent=self,
			label='Attendere prego. Installazione in corso...',
			pos=wx.Point(70, 18)
		)
		statusText = wx.StaticText(
			parent=self,
			label='Downloading package.7z',
			pos=wx.Point( 20, 64 )
		)
		progBar = wx.Gauge(
			parent=self,
			pos=wx.Point(20, 102),
			size=wx.Size(387, 20)
		)




		self.Bind(wx.EVT_CLOSE, self.OnClose, self)

	def OnClose( self, evt: wx.CloseEvent ):
		self.Destroy()


