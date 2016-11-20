import tweepy

class MyStreamListener(tweepy.StreamListener) :

 def on_connect(self):
  print("\nEntrou\n")
			
	
 def on_data(self, data):
  print("NOVO TWEET", data)
  with open('stream_trumpwins.txt','a') as tb:
      tb.write(data) 
  
 def on_status(self, status): 
  print("[on_status]",status)
  
 #status.text
 
 def keep_alive(self): 
  print("[keep_alive]") 
 
 
 def on_exception(self, exception): 
  print("[on_exception] Called when an unhandled exception occurs.", exception)  
 
 def on_delete(self, status_id, user_id): 
  print("[on_delete] Called when a delete notice arrives for a status status_id=%d, user_id=%d" % status_id, user_id) 
 
 
 def on_event(self, status): 
  print("[on_event] Called when a new event arrives", status) 
 
 
 def on_direct_message(self, status): 
  print("[on_direct_message] Called when a new direct message arrives", status) 
 
 
 def on_friends(self, friends): 
  print("[on_friends] Called when a friends list arrives.", friends) 
 
 def on_limit(self, track): 
  print("[on_limit] Called when a limitation notice arrives", track) 
 
 
 def on_timeout(self): 
  print("[on_timeout] Called when stream connection times out") 
 
 
 def on_disconnect(self, notice): 
  print("[on_disconnect] Called when twitter sends a disconnect notice", notice) 
 
 
 def on_warning(self, notice): 
  print("[on_warning] Called when a disconnection warning message arrives", notice) 
 
 
 def on_error(self, status_code): 
  print("[on_error] Called when a non-200 status code is returned", status_code) 

  if status_code == 420: 
    #returning False in on_data disconnects the stream 
   print ("\n[on_error] Limite atingido\n") 
   return False 
 
			

consumer_key="EJfQxNO4MO6QXocu51jf0FivZ"
consumer_secret="g7RdCeTkJSxVKxfKWqGXcPS3gWCChRcT4ZEGaE05Ngmzkw9dw0"
access_token="3107743679-i8GoA7zxexWOEaFxPvjdRfRgGEQdVpWkp0Eo6vI"
access_token_secret="ZslrTwPbWldSLZwmZwYZYhPdhofNz388A0x8b3dQGHsIf"
 
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api=tweepy.API(auth)

# criterio = ["lula", "#lula"]

	# hashtag dia 09/05
  #democracia - #todospelademocracia #naovaitergolpe #emdefesadademocracia #foradilma 
  # hashtag dia 26 de agosto as 15h28- lula

#stream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())

#stream.filter(track=criterio, async=True)

while True:

	try:
		myStreamListener = MyStreamListener()
		myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
		myStream.filter(track=["#trumpwins"])
		# diretas jah dia 4 setembro manif sao paulo 

	except:
		continue


