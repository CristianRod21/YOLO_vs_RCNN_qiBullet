from googletrans import Translator

def find_word(input_word):

	translator = Translator()
	english_word = translator.translate(input_word, dest='en').text.lower()

	print("palabra en inglés: " + english_word)
	#.decode("utf-8")

	words = ['person','bicycle','car','motorbike','aeroplane','bus','train','truck','boat','traffic light','fire hydrant','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','sofa','potted plant','bed','dining table','toilet','tvmonitor','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear','hair drier','toothbrush']

	is_valid = False

	for word in words:
		if word == english_word:
			#print("Entendido, voy a traer un " + input_word + "\n") 
			is_valid = True

	#if not is_valid:
	#	print("Lo lamento, no sabemos qué es un " + input_word + "\n") 

	return is_valid, english_word
			

