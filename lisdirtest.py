import os
import time
# print(os.listdir("damon"))
# filelist = os.listdir("damon")
# print(filelist[-1])


#Create random text files in time-incrasing order
for i in range(39):
	timenow = str(int(time.time()+i))
	timenowwav = timenow+'.wav'
	outputfile = 'sendervoice/'+timenowwav
	with open(outputfile, 'wb') as f:
		f.write(b'random text here.')
		print(outputfile)
	    # for chunk in r.iter_content(chunk_size=1024): 
	    #     if chunk: # filter out keep-alive new chunks
	    #         f.write(chunk)
	    #         #f.flush() commented by recommendation from J.F.Sebastian
print(len(os.listdir("sendervoice")))
# sendervoicelist = os.listdir("sendervoice")
# voicelist = []
# voicelistdict = {}
# for item in sendervoicelist:
# 	if item.startswith('1'):
# 		voicelist.append(item)
# voicelist = sorted(voicelist)
# print(voicelist)
# print(len(voicelist))
# for i,item in enumerate(os.listdir("damon")):
# 	voicelistdict[voicelist[i]] = item

# print(voicelistdict)
# for key, value in voicelistdict.items():
# 	os.rename("sendervoice/"+key,"sendervoice/"+value)
# # for i,item in enumerate(os.listdir("damon")):
# # 	print(i,item)