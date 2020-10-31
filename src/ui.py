import tempfile
import threading
import io
import shutil

import wx
from requests import get
from PIL import Image
import py7zr


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
			size=wx.Size(387, 20),
			style=wx.GA_PROGRESS
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
	app.root: root

	def run( self ):
		self.thread = threading.Thread(target=self.install)
		self.thread.run()

	def install( self ):
		downloadUrl: str = None
		for tag in get(self.app.repoApiUrl).json():
			if tag['name'] == self.app.version:
				for asset in tag['assets']:
					if '.exe' in asset['name']:
						downloadUrl = asset['browser_download_url']
						break
				break
		if not downloadUrl:
			wx.GenericMessageDialog(
				parent=self.app.root,
				message="Can't find the version specified",
				caption='Error',
				style=None,
			).ShowModal()
			wx.CallAfter( self.app.root.Destroy )
			return
		request = get( downloadUrl, stream=True )  # download BEE
		# working variables
		zipdata = io.BytesIO()
		dl = 0
		total_length = int( request.headers.get( 'content-length' ) )
		total_length_mb: int( total_length / 1024 / 1024 )
		wx.CallAfter( self.app.root.progBar.SetRange, total_length )
		# download!
		for data in request.iter_content( chunk_size=1024 ):
			dl += len( data )
			zipdata.write( data )
			done = int( 100 * dl / total_length )
			print( f'total: {total_length}, dl: {dl}, done: {done}' )
			wx.CallAfter( self.app.root.progBar.SetValue, done )
			wx.CallAfter( self.app.root.megaText.SetLabel, f'Done: {done / 1024 / 1024 }/{total_length_mb}MB')
			wx.CallAfter( self.app.root.speedText.SetLabel, f'Speed: {len(data)}mbs')
		wx.CallAfter( self.app.root.progBar.Pulse )
		# read the data as bytes and then create the zipfile object from it
		if py7zr.is_7zfile(zipdata):
			wx.GenericMessageDialog(
				parent=self.app.root,
				message="The downloaded file wasn't a 7z file.",
				caption='Error',
				style=None,
			).ShowModal()
			wx.CallAfter( self.app.root.Destroy )
			return
		tempdir = tempfile.mkdtemp(prefix='bridge-inst')
		py7zr.unpack_7zarchive( zipdata, tempdir )
		shutil.move(tempdir, self.app.installPath)
