# Section and key are used to define a sort of "place" where your variable will be saved
# If using persist option (so it`s saved throught sessions) you will be able to find it in
# reaper_extstate.ini
# Section will be called [babaG] and it will contain all the keys you saved under that section
# In this example it would look something like this:
# 
# [babaG]
# test = 42
#
section = "babaG"
key = "test"



# In this example saved variable does not persist between reaper restarts
# If you want for a variable to be saved between reaper restarts you need to set persist
# parameter in RPR_SetExtState to true (ie 1)
# When deleting the variable with RPR_DeleteExtState it is the opposite. You need to set
# persist parameter to true for a key to remain truly deleted from reaper_extstate.ini
# if it was written there in the first place


# Check if variable has been saved

#If saved variable has not been found ask user to input it
if not RPR_HasExtState(section, key):	
	user = RPR_GetUserInputs("No saved variable found", 1, "Save variable" , 0, 1024)
	RPR_SetExtState(section, key, user[4], 0)


# Else inform user it has been found, it`s value and if it should be changed
else:									
	message = "Saved variable has been found: " + RPR_GetExtState(section, key) + "\nDo you want to change it?"
	user = RPR_ShowMessageBox(message, "Variable found", 4)
	
	# User wants to change the saved variable
	if user == 6:
		user = RPR_GetUserInputs("Please input a variable to be saved", 1, "Save variable" , 0, 1024)
		RPR_SetExtState(section, key, user[4], 0)

	# User does not want to change it, ask if variable can be deleted
	if user == 7:
		user = RPR_ShowMessageBox("Do you want to delete saved variable?", "Delete variable", 4)
		if user == 6:
			RPR_DeleteExtState(section, key, 0)