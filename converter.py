import cloudconvert

class CloudConvert:
	def __init__(self):
		self.api = cloudconvert.Api('Insert Cloud Convert API Token Here')
	def convert(self, inputfile, outputfile):
		process = self.api.convert({
		    'inputformat': 'mp4',
		    'outputformat': 'wav',
		    'input': 'upload',
		    'file': open(inputfile+'.mp4', 'rb')
		})
		process.wait() # wait until conversion finished
		process.download(outputfile+".wav") # download output file

if __name__ == '__main__':
    cc = CloudConvert()
    cc.convert('test','testy')