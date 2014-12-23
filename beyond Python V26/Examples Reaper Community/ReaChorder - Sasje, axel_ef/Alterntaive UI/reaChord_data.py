# from reaper_python import *
from contextlib import contextmanager


################
                #
debug = False    #-
                #
################


    
class RC:
    """
    ReaChorder data class.
    """
    
    #this is static data, access it without creating an instance of RC by doing RC.circleFifthsInnerTxt(i) etc
    
    REACHORD="ReaChord1"
    
    
    Moods = ('Formula...',)  #create tuple with one entry
    
    # InKey = ('In key:','A','B','C','D','E','F','G','A#','C#','D#','F#','G#')
    InKey = ('C','D','E','F','G','A#','C#','D#','F#','G#','A','B')
    
    # Scales = ('Select scale...','Major','Minor')
    Scales = ('Major','Minor')
    
    ChordAttack = ('','None (default)','Fast','Slow')
    
    Highlight = ('Highlight...','None (default)','Melody','Chords')
        
    entriesStructures = ('Select structure...',)
    
    MelodyType = ('Random','Markov chain')
    
    allowedChars = "VC"      #"IVPCBMDSQLXE"
    pStructureChars = 1 #2nd pos
    pStructureName = 0 
    Structures = [
        ['Verse',             'V'         ],
        ['Verse-Chorus',      'VC'        ],
        ['Verse-Verse-Chorus','VVC'       ],    #### we can now add/remove structures here
        ['VV CC',             'VVCC'      ],         
        ['VC VC',             'VCVC'      ],    #### and it will automagically update
        ['VV CV',             'VVCV'      ],
        ['VV CC VV',          'VVCCVV'    ],
        ['VV CV CV',          'VVCVCV'    ],
        ['VC VC VV C',        'VCVCVVC'   ],
        ['VC VC V CC',        'VCVCVCC'   ]
    ]
    
    circleFifthsInnerTxt = [
        #      Am               Bm             Cm               Dm               Em              Fm               Gm
        ['F', 'C', 'G' ],['G', 'D','A'],['G#','D#','A#'],['A#','F','C' ],['C', 'G', 'D' ],['C#','G#','D#'],['D#','A#','F']
    ]
    
    circleFifthsOuterTxt = [
        #       A                   B                   C                   D                   E                   F                   G
        ['Bm', 'F#m','C#m'],['C#m','G#m','D#m'],['Dm', 'Am', 'Em' ],['Em', 'Bm', 'F#m'],['F#m','C#m','G#m'],['Gm', 'Dm', 'Am' ],['Am', 'Em', 'Bm' ]
    ]
    
    # Melody 
    ChainPitch = [60,61,62,63,64,65,66,67,68,69,70,71]
    # popular melody progressions.
    # C C# D D# E F F# G G# A A# B
    #---------------------------------
    MarkovChain = [
    [1,11,2,9,3,7,10,5,12,6,8,4], #0  C
    [3,4,1,5,2,6,7,8,9,10,11,12], #1  C#
    [1,9,3,8,2,5,11,4,12,7,10,6], #2  D
    [4,12,1,3,11,2,10,5,9,8,7,6], #3  D#
    [5,10,1,12,2,4,7,3,11,6,9,8], #4  E
    [7,12,4,8,1,3,11,2,10,5,9,6], #5  F
    [7,12,5,11,4,6,2,1,10,3,9,8], #6  F#
    [4,12,6,10,3,2,8,1,11,5,9,7], #7  G
    [12,11,10,9,8,2,7,1,6,3,5,4], #8  G#
    [5,12,6,11,7,4,9,1,10,2,8,3], #9  A
    [4,12,6,10,5,7,11,2,9,3,1,8], #10 A#
    [1,12,3,11,7,6,9,5,10,2,8,4]  #11 B
    ]

    # This is how we map the drumkit. 
    # The value is the midi pitch. 
    # The index is the translation from the canvas indices.
    # If the canvas order of indices change, we need to reorder each item here, from top to bottom.
    # To change mapping, only edit the value, !not the indice order!
    
    generalMIDIMap = [
        [41], 	# Floor Tom 2
        [43], 	# Floor Tom 1  
        [55],	# Splash cymbal 
        [51], 	# Ride Cymbal
        [42], 	# Hi-Hat Closed  
        [46], 	# Hi-Hat Open	
        [38],	# Snare Drum 		
        [36] 	# Kick Drum 	
    ]
    
    patternList = ('Select pattern...', 'Basic 1', 'Basic 2', 'Basic 3', 'Basic 4') # change when you add a new drum pattern below, because it needs a name...
            
    DrumPatterns  = [
        [ #Basic 1
        [], # Floor Tom 2
        [], # Floor Tom 1 
        [], # Splash cymbal
        [], # Ride Cymbal
        [], # Hi-Hat Closed 
        ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30'],  # Hi-Hat Open
        ['10', '14', '18', '2', '22', '26', '30', '6'], # Snare Drum 
        ['0', '12', '16', '20', '24', '28', '4', '8'] # Kick Drum
        ],

        [ #Basic 2
        [], # Floor Tom 2
        [], # Floor Tom 1 
        [], # Splash cymbal
        [], # Ride Cymbal
        ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', ], # Hi-Hat Closed 
        ['30'],  # Hi-Hat Open
        ['10', '14', '18', '2', '22', '26', '30', '6'], # Snare Drum 
        ['0', '12', '16', '20', '24', '28', '4', '8'], # Kick Drum
        ],

        [ #Basic 3
        [], # Floor Tom 2
        [], # Floor Tom 1 
        [], # Splash cymbal
        [], # Ride Cymbal
        ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', ], # Hi-Hat Closed 
        ['30'],  # Hi-Hat Open
        ['10', '14', '18', '2', '22', '26', '30', '6'], # Snare Drum 
        ['0', '6', '12', '16', '20', '24', '28', '4', '8'], # Kick Drum
        ],

        [ #Basic 4
        [], # Floor Tom 2
        [], # Floor Tom 1 
        [], # Splash cymbal
        [], # Ride Cymbal
        ['0', '4', '8', '12', '16', '20', '24', '28', ], # Hi-Hat Closed 
        ['30'],  # Hi-Hat Open
        ['10', '14', '18', '2', '22', '26', '30', '6'], # Snare Drum 
        ['0', '10', '12', '16','18', '20', '24', '28', '4', '8'], # Kick Drum
        ],
    ]

    pProgName = 4  #5th position
    progressions = [
        [6, 4, 1, 5, 'Alternative' ],           ### now we can add progressions to this too
        [4, 4, 1, 5, 'Catchy'      ],  
        [1, 1, 1, 1, 'Didgeridoo'  ],
        [1, 6, 4, 5, 'Dreadful'    ], 
        [1, 6, 2, 5, 'Dreadful II' ], 
        [1, 6, 2, 4, 'Endless'     ], 
        [1, 3, 4, 6, 'Energetic'   ],
        [1, 5, 1, 4, 'Folk'        ],
        [1, 6, 1, 4, 'Folk II'     ],
        [6, 5, 4, 3, 'Flamenco'    ], 
        [6, 5, 6, 5, 'Flamenco II' ],        
        [1, 4, 3, 6, 'Grunge'      ],
        [2, 5, 1, 6, 'Jazz'        ],
        [1, 4, 5, 4, 'Love'        ],        
        [1, 4, 1, 5, 'Memories'    ],
        [1, 5, 6, 4, 'Pop'         ], 
        [1, 6, 3, 7, 'Pop II'      ],        
        [4, 1, 4, 5, 'Rebellious'  ],          
        [1, 4, 5, 5, 'Sad'         ],
        [1, 5, 4, 4, 'Sad II'      ],
        [1, 4, 5, 4, 'Sad III'     ],
        [5, 4, 1, 1, 'Sweet'       ],       
        [1, 4, 1, 4, 'Simple'      ], 
        [1, 5, 5, 1, 'Simple II'   ],
        [1, 4, 1, 4, 'Wild side'   ],
        [1, 1, 4, 6, 'Wistful'     ],  
        [2, 1, 5, 7, 'Weep'        ], 
        [2, 1, 7, 6, 'Weep II'     ]
    ]    
    
    
    KeyChartMajor = [
        [0, 9,23,13, 2, 4,18,32], #0 A
        [0,11,13,15, 4, 6,20,34], #1 B
        [0, 0,14,16, 5, 7,21,35], #2 C
        [0, 2,16,18, 7, 9,23,25], #3 D
        [0, 4,18,20, 9,11,13,27], #4 E
        [0, 5,19,21,10, 0,16,28], #5 F
        [0, 7,21,23, 0, 2,16,30], #6 G
        [0,10,12,14, 3, 5,19,33], #7 A# Cm Dm D# F Gm Adim
        [0, 1,15,17, 6, 8,22,24], #8 C# D#m Fm F# G# A#m Cdim
        [0, 3,17,19, 8,10,12,26], #9 D# Fm Gm G# A# Cm Ddim
        [0, 6,20,22,11, 1,15,29], #10 F# G#m A#m B C# D#m Fdim
        [0, 8,22,12, 1, 3,17,31]  #11 G# A#m Cm C# D# Fm Gdim
    ]
    
    circleFifthsInner = [
        [[0, 5,19,21,10, 0,16,28],[0, 0,14,16, 5, 7,21,35],[0, 7,21,23, 0, 2,16,30]], # Am
        [[0, 7,21,23, 0, 2,16,30],[0, 2,16,18, 7, 9,23,25],[0, 9,23,13, 2, 4,18,32]], # Bm
        [[0, 8,22,12, 1, 3,17,31],[0, 3,17,19, 8,10,12,26],[0,10,12,14, 3, 5,19,33]], # Cm
        [[0,10,12,14, 3, 5,19,33],[0, 5,19,21,10, 0,16,28],[0, 0,14,16, 5, 7,21,35]], # Dm
        [[0, 0,14,16, 5, 7,21,35],[0, 7,21,23, 0, 2,16,30],[0, 2,16,18, 7, 9,23,25]], # Em
        [[0, 1,15,17, 6, 8,22,24],[0, 8,22,12, 1, 3,17,31],[0, 3,17,19, 8,10,12,26]], # Fm
        [[0, 3,17,19, 8,10,12,26],[0,10,12,14, 3, 5,19,33],[0, 5,19,21,10, 0,16,28]], # Gm
        [[0, 5,19,21,10, 0,16,28],[0, 0,14,16, 5, 7,21,35],[0, 7,21,23, 0, 2,16,30]], # Am
        [[0, 8,22,12, 1, 3,17,31],[0, 3,17,19, 8,10,12,26],[0,10,12,14, 3, 5,19,33]], # Cm
        [[0,10,12,14, 3, 5,19,33],[0, 5,19,21,10, 0,16,28],[0, 0,14,16, 5, 7,21,35]], # Dm
        [[0, 1,15,17, 6, 8,22,24],[0, 8,22,12, 1, 3,17,31],[0, 3,17,19, 8,10,12,26]], # Fm
        [[0, 3,17,19, 8,10,12,26],[0,10,12,14, 3, 5,19,33],[0, 5,19,21,10, 0,16,28]], # Gm
    ]
    
    KeyChartMinor = [
        [0,21,35, 0,14,16, 5, 7  ], #0 Am
        [0,23,25, 2,16,18, 7, 9  ], #1 Bm
        [0,12,26, 3,17,19, 8,10  ], #2 Cm
        [0,14,28, 5,19,21,23,10,0], #3 Dm
        [0,16,30, 7,21,23, 0, 2  ], #4 Em
        [0,17,31, 8,22,12, 1, 3  ], #5 Fm
        [0,19,33,10,12,14, 3, 5  ], #6 Gm
        [0,22,24, 1,15,17, 6, 8  ], #7 A#m Cdim C# D#m Fm F# G#
        [0,13,27, 4,18,20, 9,11  ], #8 C#m D#dim E F#m G#m A B
        [0,15,29, 6,20,22,11, 1  ], #9 D#m Fdim F# G#m A#m B C#
        [0,18,32, 9,23,13, 2, 4  ], #10 F#m G#dim A Bm C#m D E
        [0,20,34,11,13,15, 4, 6  ]  #11 G#m A#dim B C#m D#m E F# 
    ]
    
    circleFifthsOuter = [
        [[0,23,25, 2,16,18, 7, 9  ],[0,18,32, 9,23,13, 2, 4  ],[0,13,27, 4,18,20, 9,11]], # A
        [[0,13,27, 4,18,20, 9,11  ],[0,20,34,11,13,15, 4, 6  ],[0,15,29, 6,20,22,11, 1]], # B
        [[0,14,28, 5,19,21,23,10,0],[0,21,35, 0,14,16, 5, 7  ],[0,16,30, 7,21,23, 0, 2]], # C
        [[0,16,30, 7,21,23, 0, 2  ],[0,23,25, 2,16,18, 7, 9  ],[0,18,32, 9,23,13, 2, 4]], # D
        [[0,18,32, 9,23,13, 2, 4  ],[0,13,27, 4,18,20, 9,11  ],[0,20,34,11,13,15, 4, 6]], # E
        [[0,19,33,10,12,14, 3, 5  ],[0,14,28, 5,19,21,23,10,0],[0,21,35, 0,14,16, 5, 7]], # F
        [[0,21,35, 0,14,16, 5, 7  ],[0,16,30, 7,21,23, 0, 2  ],[0,23,25, 2,16,18, 7, 9]], # G
        [[0,23,25, 2,16,18, 7, 9  ],[0,18,32, 9,23,13, 2, 4  ],[0,13,27, 4,18,20, 9,11]], # A
        [[0,14,28, 5,19,21,23,10,0],[0,21,35, 0,14,16, 5, 7  ],[0,16,30, 7,21,23, 0, 2]], # C
        [[0,16,30, 7,21,23, 0, 2  ],[0,23,25, 2,16,18, 7, 9  ],[0,18,32, 9,23,13, 2, 4]], # D
        [[0,19,33,10,12,14, 3, 5  ],[0,14,28, 5,19,21,23,10,0],[0,21,35, 0,14,16, 5, 7]], # F
        [[0,21,35, 0,14,16, 5, 7  ],[0,16,30, 7,21,23, 0, 2  ],[0,23,25, 2,16,18, 7, 9]]  # G
    ]
    
    pChordName = 3 #4th position for name (0,1,2,3)
    Chords = [
        [60,64,67, 'C'    ], #0 C
        [61,65,68, 'C#'   ], #1 C#
        [62,66,69, 'D'    ], #2 D
        [63,67,70, 'D#'   ], #3 D#
        [64,68,71, 'E'    ], #4 E
        [65,69,72, 'F'    ], #5 F
        [66,70,73, 'F#'   ], #6 F#
        [67,71,74, 'G'    ], #7 G
        [68,72,75, 'G#'   ], #8 G#
        [69,73,76, 'A'    ], #9 A
        [70,74,77, 'A#'   ], #10 A#
        [71,75,78, 'B'    ], #11 B
        [60,63,67, 'Cm'   ], #12 Cmin
        [61,64,68, 'C#m'  ], #13 C#min
        [62,65,69, 'Dm'   ], #14 Dmin
        [63,66,70, 'D#m'  ], #15 D#min
        [64,67,71, 'Em'   ], #16 Emin
        [65,68,72, 'Fm'   ], #17 Fmin
        [66,69,73, 'F#m'  ], #18 F#min
        [67,70,74, 'Gm'   ], #19 Gmin
        [68,71,75, 'G#m'  ], #20 G#min
        [69,72,76, 'Am'   ], #21 Amin
        [70,73,77, 'A#m'  ], #22 A#min
        [71,74,78, 'Bm'   ], #23 Bmin
        [60,63,66, 'Cdim' ], #24 Cdim
        [61,64,67, 'C#dim'], #25 C#dim
        [62,65,68, 'Ddim' ], #26 Ddim
        [63,66,69, 'D#dim'], #27 D#dim
        [64,68,70, 'Edim' ], #28 Edim
        [65,68,71, 'Fdim' ], #29 Fdim
        [66,69,72, 'F#dim'], #30 F#dim
        [67,70,73, 'Gdim' ], #31 Gdim
        [68,71,74, 'G#dim'], #32 G#dim
        [69,72,75, 'Adim' ], #33 Adim
        [70,73,76, 'A#dim'], #34 A#dim
        [71,74,77, 'Bdim' ]  #35 Bdim
    ]
    
    
    ChordDict = {
        "C"    :[60,64,67],
        "C#"   :[61,65,68],
        "D"    :[62,66,69],    
        "D#"   :[63,67,70], 
        "E"    :[64,68,71], 
        "F"    :[65,69,72], 
        "F#"   :[66,70,73], 
        "G"    :[67,71,74],  
        "G#"   :[68,72,75], 
        "A"    :[69,73,76], 
        "A#"   :[70,74,77], 
        "B"    :[71,75,78], 
        "Cm"   :[60,63,67], 
        "C#m"  :[61,64,68], 
        "Dm"   :[62,65,69], 
        "D#m"  :[63,66,70], 
        "Em"   :[64,67,71], 
        "Fm"   :[65,68,72], 
        "F#m"  :[66,69,73], 
        "Gm"   :[67,70,74], 
        "G#m"  :[68,71,75], 
        "Am"   :[69,72,76], 
        "A#m"  :[70,73,77], 
        "Bm"   :[71,74,78], 
        "Cdim" :[60,63,66], 
        "C#dim":[61,64,67], 
        "Ddim" :[62,65,68], 
        "D#dim":[63,66,69], 
        "Edim" :[64,68,70], 
        "Fdim" :[65,68,71], 
        "F#dim":[66,69,72], 
        "Gdim" :[67,70,73], 
        "G#dim":[68,71,74], 
        "Adim" :[69,72,75], 
        "A#dim":[70,73,76], 
        "Bdim" :[71,74,77]
    }
    
    ############### end of static data ##################
    
    def __init__(self):
        
        self.quartNoteLength = 960 #quarter note length in ticks
        p, bpm, bpi = Reaper.GetProjectTimeSignature2(0, 0, 0)
        bps = 60/bpm
        self.barLength = bps * bpi
        self.barsPerSection = 4  #TODO doesn't work unless 4 at the mo
        
        for val in RC.progressions:
            RC.Moods+=(val[RC.pProgName],)                      ### this section populates the tuple accessed by 
                                                                ### the combo box creation code with names from new combined lists
        for val in RC.Structures:                 
            RC.entriesStructures+=(val[RC.pStructureName],)
            

        
    
    def msg(self,m):
        global msg
        msg(m)
 
        
def msg(m):
    if (debug):
        Reaper.ShowConsoleMsg(str(m)+'\n')
    
    