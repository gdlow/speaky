import os
import time
import requests
from requests_toolbelt import MultipartEncoder
import json
from flask import Flask, request

#import converter class
from converter import CloudConvert

#import downloadsequence class
from downloadsequence import DownloadSequence

#import texttospeech class
from waveCat import TextToSpeech
tts = TextToSpeech()



# FB messenger credentials
ACCESS_TOKEN = "Insert FB Access Token Here"

application = Flask(__name__)

@application.route('/', methods=['GET'])
def verify():
    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello from Flask!", 200

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

def replyattachments(user_id, file):
    data = {
        "recipient": json.dumps({"id": user_id}),
        "message": json.dumps({"attachment":{"type":"audio", "payload":{}}}),
        "filedata": (file, open(file, "rb"), 'audio/wav') #wav file formatting works
        }
    # multipart encode the entire payload
    multipart_data = MultipartEncoder(data)

    # multipart header from multipart_data
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, headers=multipart_header, data=multipart_data)
    print(resp.content)

@application.route('/', methods=['POST'])
def handle_incoming_messages():

    data = request.json
    #log the entry sent
    print(data)
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    try:
        if data['entry'][0]['messaging'][0]['message']['attachments'][0]['type'] == 'audio': #if message sent was an audio file
            #downloads the audio file given and returns it back
            ds = DownloadSequence() #instantiate DownloadSequence class
            download_url = data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url']
            # timenow = str(int(time.time()))
            # sampleaudio = 'sendervoice/'+timenow
            ds.download_file(url=download_url,outputname='sendervoice/placeholder') #placeholder mp4 
            reply(sender,'Your snippet has been recorded successfully.')
            #convert file to output.wav
            cc = CloudConvert()
            wavfiles = []
            wavdict = {}
            sendervoicelist = os.listdir("sendervoice")
            for item in sendervoicelist:
                if item.endswith('wav'): 
                    wavfiles.append(item)
            for i,item in enumerate(sorted(os.listdir("damon"))):
                wavdict[i] = item[:-4] #just take the name without .wav
            cc.convert('sendervoice/placeholder','sendervoice/'+wavdict[len(wavfiles)]) #converts to the appropriate naming convention
            reply(sender,'Your snippet "{}" has been coverted successfully.'.format(wavdict[len(wavfiles)]))
    except KeyError:
        pass
    try:
        if data['entry'][0]['messaging'][0]['message']['text']: #if message sent was a text
            message = data['entry'][0]['messaging'][0]['message']['text']
            if 'begin' in [word.lower() for word in message.strip().split()]:
                #begin onboarding instructions
                onboarding_instructions_1 = 'Greetings! Welcome to Speaky. To onboard your voice onto the platform, please follow the instructions carefully. \
                \nSpeaky works based on ARPABETS. To begin, record voice snippets of the 39 ARPABET sounds below (in order) and send each one separately.\
                \n1. Say "aa"\
                \n2. Say "ae"\
                \n3. Say "ah"\
                \n4. Say "ao"\
                \n5. Say "aw"\
                \n6. Say "ay"\
                \n7. Say "b"\
                \n8. Say "ch"\
                \n9. Say "d"\
                \n10. Say "dh"\
                \n11. Say "eh"\
                \n12. Say "er"\
                \n13. Say "ey"\
                \n14. Say "f"\
                \n15. Say "g"\
                \n16. Say "hh"\
                \n17. Say "ih"\
                \n18. Say "iy"\
                \n19. Say "jh"\
                \n20. Say "k"\
                \n21. Say "l"\
                \n22. Say "m"\
                \n23. Say "n"\
                \n24. Say "ng"\
                \n25. Say "ow"\
                \n26. Say "oy"\
                \n27. Say "p"\
                \n28. Say "r"\
                \n29. Say "s"\
                \n30. Say "sh"\
                \n31. Say "t"\
                \n32. Say "th"\
                \n33. Say "uh"\
                \n34. Say "uw"\
                \n35. Say "v"\
                \n36. Say "w"\
                \n37. Say "y"\
                \n38. Say "z"\
                \n39. Say "zh"'
                onboarding_instructions_2 = 'Once you are done, say "it is done" '
                reply(sender,onboarding_instructions_1)
                reply(sender,onboarding_instructions_2)
            elif message.lower() == "it is done":
                #Begin sorting procedure and rename wav files to actual sounds
                if len(os.listdir("sendervoice")) != 40:
                    reply(sender,"Count = {}. You have not completed the list".format(str(len(os.listdir("sendervoice"))-2)))
                else:
                    # sendervoicelist = os.listdir("sendervoice")
                    # voicelist = []
                    # voicelistdict = {}
                    # for item in sendervoicelist:
                    #     if item.startswith('1'):
                    #         voicelist.append(item)
                    # voicelist = sorted(voicelist)
                    # for i,item in enumerate(os.listdir("damon")):
                    #     voicelistdict[voicelist[i]] = item
                    # for key, value in voicelistdict.items():
                    #     os.rename("sendervoice/"+key,"sendervoice/"+value)
                    reply(sender,"Onboarding process completed.")
            elif message.lower() == "thank you":
                #Send Lyrebird message
                reply(sender,'That was our project on text to speech synthesis of your own voice. We hope you enjoyed it. Thank you for your attention.')
                replyattachments(sender,"thankyoumessage.wav")
            elif message.lower() == "hey speaky":
                #Send Lyrebird message
                reply(sender,'Hey guys, I sound like you.')
                tts.get_pronunciation('hey guys, I sound like you.','clippedAudio/ashley/')
                replyattachments(sender,"messages/datastream.wav")
            else:
                #Normal conversation with cleverbot AI
                #cleverbot response
                r = requests.get("https://www.cleverbot.com/getreply?key=CC6zvN57mAqJ-qUnUu-z_mDzt8w&input=" + message)
                resp = r.json()
                if "output" in resp:
                    response = resp["output"]
                    if 'zh.wav' in os.listdir("sendervoice"): #if user is onboarded (for testing, just check till b.wav)
                        tts.get_pronunciation(response,'clippedAudio/ashley/') #saves the response as messages/datastream.wav
                        reply(sender,response)
                        replyattachments(sender,"messages/datastream.wav")
                    else: #otherwise revert to default voice
                        tts.get_pronunciation(response,'clippedAudio/ashley/') #saves the response as messages/datastream.wav
                        reply(sender,response)
                        replyattachments(sender,"messages/datastream.wav")
    except KeyError:
        pass

        # retvallist = os.listdir("sendervoice") #queries and returns a list of all files in sendervoice
        # try:
        #     replyattachments(sender,'sendervoice/'+retvallist[-1]) #returns the first entry voice snippet stored
        # except:
        #     replyattachments(sender,'sendervoice/'+retvallist[0]) #or the last entry if the first is .ignore
        #print(data['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['url']) #works
    # try:
    #     sender = data['entry'][0]['messaging'][0]['sender']['id']
    #     message = data['entry'][0]['messaging'][0]['message']['text']

    #     #cleverbot response
    #     r = requests.get("https://www.cleverbot.com/getreply?key=CC6zvN57mAqJ-qUnUu-z_mDzt8w&input=" + message)
    #     resp = r.json()
    #     if "output" in resp:
    #         response = resp["output"]
    #         tts.get_pronunciation(response) #saves the response as messages/datastream.wav
    #         reply(sender,response)
    #         replyattachments(sender,"messages/datastream.wav")
    # except:
    #     pass
    return "ok"

if __name__ == '__main__':
    application.run(debug=True)

