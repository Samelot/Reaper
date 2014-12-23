#this script will act on all points in an envelope.
#If there are less than 7 points it will leave the last point 
#so the envelope doesn't go away.

from reaper_python import * 

def main():

	envelopedata = '' #the whole string
	PTdata = '' #Only the line terminating with a newline that contains a point
	PTdatalast = '' #The last point to retain so the envelope doesn't get deleted
	dataheader = '' #Save for later to rebuild the envelopedata
	databody = '' #Built data from a nested if structure that takes 1 out of 8 points
	gotone = 0 # point counter
	gottwo = 0 # nested point counter
	gotthree = 0 # double nested point counter
	
	envelopepointer = RPR_GetSelectedTrackEnvelope(0) 
	envelopestate = RPR_GetSetEnvelopeState(envelopepointer,envelopedata,1048575) #can handle a lot of points
	envpointdata = envelopestate[2] #string of passed parameter in GetSetEnvelopeState
	if envelopestate: # if envelope selected true
		i = 0

		envlength = len(envpointdata) #size of string in int
		#RPR_ShowConsoleMsg(str(envlength))
		for i in range(envlength-1): #iterate through string
			PTdata = PTdata+envpointdata[i] #build a string
			
			if envpointdata[i] == "\n": #if row of data
				if PTdata.startswith("PT"): #if point data string
					PTdatalast = PTdata #retain the last point so the envelope doesn't get deleted
					gotone = gotone+1 #increment point counter
					
					if gotone%2 == 0: #if point is even
						databody = databody+PTdata	#build 50% of point data
								
					PTdata = ''#clean up for next iteration
					
				else: #store the envheader data for later
					dataheader = dataheader+PTdata
					PTdata = '' #clean up for next iteration
			i = i+1 #next character in string
			
		envelopedata = dataheader+databody+PTdatalast+'>' #build the envelope parameters back together
		
		#RPR_ShowConsoleMsg(envelopedata+str(gotone)+"\n"+str(gotthree/2)+"\n") #for debugging
		envelopestate = RPR_GetSetEnvelopeState(envelopepointer,envelopedata,40959) #assign to envelope
	else:
		return #no envelope selected
	
main()