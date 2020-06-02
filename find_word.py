import requests

def find_word(input_word):

	clientId = "FREE_TRIAL_ACCOUNT"
	clientSecret = "PUBLIC_SECRET"

	# TODO: Specify your translation requirements here:
	fromLang = "es"
	toLang = "en"
	text = input_word

	jsonBody = {
	    'fromLang': fromLang,
	    'toLang': toLang,
	    'text': text
	}

	headers = {
	    'X-WM-CLIENT-ID': clientId, 
	    'X-WM-CLIENT-SECRET': clientSecret
	}

	r = requests.post('http://api.whatsmate.net/v1/translation/translate', 
	    headers=headers,
	    json=jsonBody)

	english_word = str(r.content.decode("utf-8"))
	print("palabra en inglés: " + english_word)
	#.decode("utf-8")

	words = ['bottle', 'book', 'keyboard', 'laptop', 'mobile phone', 'mouse', 'pen' ]

	is_valid = False

	for word in words:
		if word == english_word:
			#print("Entendido, voy a traer un " + input_word + "\n") 
			is_valid = True

	#if not is_valid:
	#	print("Lo lamento, no sabemos qué es un " + input_word + "\n") 

	return is_valid, english_word
			

