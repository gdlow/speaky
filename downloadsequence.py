import requests
import time

class DownloadSequence:
	def __init__(self):
		pass
	def download_file(self,url,outputname):
	    outputfile = outputname+".mp4"
	    # NOTE the stream=True parameter
	    r = requests.get(url, stream=True)
	    with open(outputfile, 'wb') as f:
	        for chunk in r.iter_content(chunk_size=1024): 
	            if chunk: # filter out keep-alive new chunks
	                f.write(chunk)
	                #f.flush() commented by recommendation from J.F.Sebastian
	    return outputfile


if __name__ == '__main__':
	ds = DownloadSequence()
	myurl='https://cdn.fbsbx.com/v/t59.3654-21/27420221_10155525017327909_3743011788841549824_n.mp4/audioclip-1517584828000-1344.mp4?oh=d10ab3d37e8aeda88ddb01ee90c22aa9&oe=5A7682D8'
	ds.download_file(myurl,'sendervoice/sabbie')
	print(str(int(time.time())))

