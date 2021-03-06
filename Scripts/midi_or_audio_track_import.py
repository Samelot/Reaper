import os
import shutil
import tempfile

function getItemType() (

	itemId = GetSelectedMediaItem(0, 0);
	active_take = GetActiveTake(itemId);	// get active take
	PCM_source = GetMediaItemTake_Source(active_take);	// get PCM source from active take
	
	GetMediaSourceType(PCM_source, #buffer);  // get source type from source -> store type to #buffer
		/* GetMediaSourceType(PCM_source* source, #typebuf)  
		   copies the media source type ("WAV", "MIDI", etc) to typebuf 
		*/
		
	// stricmp(str, str2) -- compares str to str2, ignoring case, returns -1, 0, or 1
	// NOTE: returns 0 if #buf == "MIDI"
 	stricmp(#buffer, "MIDI") == 0 ? (	
		ShowMessageBox("Midi Item", "ITEM TYPE", 0);
	) : (
		ShowMessageBox("Audio Item", "ITEM TYPE", 0);
	);
);

getItemType();