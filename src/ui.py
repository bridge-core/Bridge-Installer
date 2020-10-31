import tempfile
import threading
import io

import wx
from requests import get
from PIL import Image


def getBitmap():
	png: Image.Image = Image.open('icon.png')
	png = png.resize( (38, 38) )
	width, height = png.size
	return wx.Bitmap.FromBufferRGBA(width, height, png.convert('RGBA').tobytes() )


class root(wx.Frame):

	progBar: wx.Gauge
	text: wx.StaticText
	actionText: wx.StaticText
	megaText: wx.StaticText
	speedText: wx.StaticText

	def __init__(self, app: 'App'):
		super().__init__(
			parent=None,
			title=app.title,
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
		self.text = wx.StaticText(
			parent=self,
			label='Attendere prego. Installazione in corso...',
			pos=wx.Point(70, 18)
		)
		self.actionText = wx.StaticText(
			parent=self,
			label='Downloading package.7z',
			pos=wx.Point( 20, 64 )
		)
		self.progBar = wx.Gauge(
			parent=self,
			pos=wx.Point(20, 90),
			size=wx.Size(387, 20)
		)
		self.megaText = wx.StaticText(
			parent=self,
			label='Done: 0/0MB',
			pos=wx.Point( 140, 110 )
		)
		self.speedText = wx.StaticText(
			parent=self,
			label='Speed: 0mbs',
			pos=wx.Point( 20, 110 )
		)
		self.Bind(wx.EVT_CLOSE, self.OnClose, self)
		self.installer = Installer()
		self.installer.app = app
		self.installer.run()

	def OnClose( self, evt: wx.CloseEvent ):
		self.Destroy()


class Installer:

	thread: threading.Thread
	app: 'App'

	def run( self ):
		self.thread = threading.Thread(target=self.install)
		self.thread.run()

	def install( self ):
		downloadUrl: str
		for tag in get(self.app.repoApiUrl).json():
			if tag['name'] == self.app.version:
				for asset in tag['assets']:
					if '.exe' in asset['name']:
						downloadUrl = asset['browser_download_url']
						break
				break
		request = get( downloadUrl, stream=True )  # download BEE
		# working variables
		zipdata = io.BytesIO()
		dialog.Update( 0 )
		dl = 0
		total_length = int( request.headers.get( 'content-length' ) )
		# download!
		for data in request.iter_content( chunk_size=1024 ):
			dl += len( data )
			zipdata.write( data )
			done = int( 100 * dl / total_length )
			print( f'total: {total_length}, dl: {dl}, done: {done}' )
			dialog.Update( done )
		logger.info( 'extracting...' )
		dialog.Pulse( 'Extracting..' )
		# read the data as bytes and then create the zipfile object from it
		ZipFile( zipdata ).extractall( config.load( 'beePath' ) )  # extract BEE
		logger.info( 'BEE2.4 application installed!' )