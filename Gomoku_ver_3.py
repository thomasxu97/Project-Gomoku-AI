# -*- coding: utf-8 -*-

START = "START"
PLACE = "PLACE"
DONE = "DONE"
TURN = "TURN"
BEGIN = "BEGIN"
END = "END"

BOARD_SIZE = 15
EMPTY = 0
ME = 1
OTHER = 2

THRESHOLD = 10
DEPTH = 6

FREE = 3
NFREE = 4

SML = -float("Inf")
TWO = 10            # two   = 5 
THR = 100           # three = 100
FOU = 1000          # four  = 1000
FIV = 10000         # five  = 10000
ITW = 5             # ill shape two: O_O O__O = 1
ITH = 90            # ill shape three O_OO OO_O = 90
DTH = 10            # dead three = 10
DFO = 80            # dead four  = 80
DEX = 90            # dead four with extra hand = 100

NUM_STEPS = 0
NUM_STEPS_THRESHOLD = 2400

quick_check_table = {
    # store shape score if ME play at EMPTY
    # 
    (FREE,  EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY,  FREE): [[0,      0,      0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  EMPTY,  EMPTY,  ME,     FREE): [[0,      ITW,    ITW,    TWO,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  EMPTY,  ME,     EMPTY,  FREE): [[ITW,    ITW,    TWO,    SML,    TWO],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  EMPTY,  ME,     ME,     FREE): [[DTH,    ITH,    THR,    SML,    SML],  [0,  1,  1,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     EMPTY,  EMPTY,  FREE): [[ITW,    TWO,    SML,    TWO,    ITW],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     EMPTY,  ME,     FREE): [[DTH,    ITH,    SML,    THR,    SML],  [0,  1,  0,  1,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     ME,     EMPTY,  FREE): [[ITH,    THR,    SML,    SML,    THR],  [1,  1,  0,  0,  1], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     ME,     ME,     FREE): [[DEX,    FOU,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [1,  1,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  EMPTY,  EMPTY,  FREE): [[TWO,    SML,    TWO,    ITW,    ITW],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  EMPTY,  ME,     FREE): [[DTH,    SML,    ITH,    ITH,    SML],  [0,  0,  1,  1,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  ME,     EMPTY,  FREE): [[ITH,    SML,    THR,    SML,    ITH],  [1,  0,  1,  0,  1], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  ME,     ME,     FREE): [[DFO,    SML,    FOU,    SML,    SML],  [0,  0,  0,  0,  0], [1,  0,  1,  0,  0]],
    (FREE,  EMPTY,  ME,     ME,     EMPTY,  EMPTY,  FREE): [[THR,    SML,    SML,    THR,    ITH],  [1,  0,  0,  1,  1], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     ME,     EMPTY,  ME,     FREE): [[DEX,    SML,    SML,    FOU,    SML],  [0,  0,  0,  0,  0], [1,  0,  0,  1,  0]],
    (FREE,  EMPTY,  ME,     ME,     ME,     EMPTY,  FREE): [[FOU,    SML,    SML,    SML,    FOU],  [0,  0,  0,  0,  0], [1,  0,  0,  0,  1]],
    (FREE,  EMPTY,  ME,     ME,     ME,     ME,     FREE): [[FIV,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  EMPTY,  EMPTY,  FREE): [[SML,    TWO,    ITW,    ITW,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  EMPTY,  ME,     FREE): [[SML,    DTH,    DTH,    DTH,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  ME,     EMPTY,  FREE): [[SML,    ITH,    ITH,    SML,    DTH],  [0,  1,  1,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  ME,     ME,     FREE): [[SML,    DFO,    DEX,    SML,    SML],  [0,  0,  0,  0,  0], [0,  1,  1,  0,  0]],
    (FREE,  ME,     EMPTY,  ME,     EMPTY,  EMPTY,  FREE): [[SML,    THR,    SML,    ITH,    DTH],  [0,  1,  1,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  ME,     EMPTY,  ME,     FREE): [[SML,    DEX,    SML,    DEX,    SML],  [0,  0,  0,  0,  0], [0,  1,  0,  1,  0]],
    (FREE,  ME,     EMPTY,  ME,     ME,     EMPTY,  FREE): [[SML,    FOU,    SML,    SML,    DEX],  [0,  0,  0,  0,  0], [0,  1,  0,  0,  1]],
    (FREE,  ME,     EMPTY,  ME,     ME,     ME,     FREE): [[SML,    FIV,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     EMPTY,  EMPTY,  EMPTY,  FREE): [[SML,    SML,    THR,    ITH,    DTH],  [0,  0,  1,  1,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     EMPTY,  EMPTY,  ME,     FREE): [[SML,    SML,    DEX,    DFO,    SML],  [0,  0,  0,  0,  0], [0,  0,  1,  1,  0]],
    (FREE,  ME,     ME,     EMPTY,  ME,     EMPTY,  FREE): [[SML,    SML,    FOU,    SML,    DFO],  [0,  0,  0,  0,  0], [0,  0,  1,  0,  1]],
    (FREE,  ME,     ME,     EMPTY,  ME,     ME,     FREE): [[SML,    SML,    FIV,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     ME,     EMPTY,  EMPTY,  FREE): [[SML,    SML,    SML,    FOU,    DEX],  [0,  0,  0,  0,  0], [0,  0,  0,  1,  1]],
    (FREE,  ME,     ME,     ME,     EMPTY,  ME,     FREE): [[SML,    SML,    SML,    FIV,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     ME,     ME,     EMPTY,  FREE): [[SML,    SML,    SML,    SML,    FIV],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     ME,     ME,     ME,     FREE): [[SML,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],

    (NFREE, EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY,  FREE): [[0,      0,      0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],  
    (NFREE, EMPTY,  EMPTY,  EMPTY,  EMPTY,  ME,     FREE): [[0,      ITW,    ITW,    TWO,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  EMPTY,  ME,     EMPTY,  FREE): [[0,      ITW,    TWO,    SML,    TWO],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  EMPTY,  ME,     ME,     FREE): [[DTH,    ITH,    THR,    SML,    SML],  [0,  1,  1,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     EMPTY,  EMPTY,  FREE): [[0,      ITW,    SML,    TWO,    ITW],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     EMPTY,  ME,     FREE): [[DTH,    ITH,    SML,    THR,    SML],  [0,  1,  0,  1,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     ME,     EMPTY,  FREE): [[DTH,    ITH,    SML,    SML,    THR],  [0,  1,  0,  0,  1], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     ME,     ME,     FREE): [[DEX,    FOU,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [1,  1,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  EMPTY,  EMPTY,  FREE): [[0,      SML,    ITW,    ITW,    ITW],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  EMPTY,  ME,     FREE): [[DTH,    SML,    ITH,    ITH,    SML],  [0,  0,  1,  1,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  ME,     EMPTY,  FREE): [[DTH,    SML,    ITH,    SML,    ITH],  [0,  0,  1,  0,  1], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  ME,     ME,     FREE): [[DFO,    SML,    FOU,    SML,    SML],  [0,  0,  0,  0,  0], [1,  0,  1,  0,  0]],
    (NFREE, EMPTY,  ME,     ME,     EMPTY,  EMPTY,  FREE): [[DTH,    SML,    SML,    ITH,    ITH],  [0,  0,  0,  1,  1], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     ME,     EMPTY,  ME,     FREE): [[DFO,    SML,    SML,    FOU,    SML],  [0,  0,  0,  0,  0], [1,  0,  0,  1,  0]],
    (NFREE, EMPTY,  ME,     ME,     ME,     EMPTY,  FREE): [[DFO,    SML,    SML,    SML,    FOU],  [0,  0,  0,  0,  0], [1,  0,  0,  0,  1]],
    (NFREE, EMPTY,  ME,     ME,     ME,     ME,     FREE): [[FIV,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  EMPTY,  EMPTY,  FREE): [[SML,    0,      0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  EMPTY,  ME,     FREE): [[SML,    DTH,    DTH,    DTH,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  ME,     EMPTY,  FREE): [[SML,    DTH,    DTH,    SML,    DTH],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  ME,     ME,     FREE): [[SML,    DFO,    DEX,    SML,    SML],  [0,  0,  0,  0,  0], [0,  1,  1,  0,  0]],
    (NFREE, ME,     EMPTY,  ME,     EMPTY,  EMPTY,  FREE): [[SML,    DTH,    SML,    DTH,    DTH],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  ME,     EMPTY,  ME,     FREE): [[SML,    DFO,    SML,    DEX,    SML],  [0,  0,  0,  0,  0], [0,  1,  0,  1,  0]],
    (NFREE, ME,     EMPTY,  ME,     ME,     EMPTY,  FREE): [[SML,    DFO,    SML,    SML,    DEX],  [0,  0,  0,  0,  0], [0,  1,  0,  0,  1]],
    (NFREE, ME,     EMPTY,  ME,     ME,     ME,     FREE): [[SML,    FIV,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     EMPTY,  EMPTY,  EMPTY,  FREE): [[SML,    SML,    DTH,    DTH,    DTH],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     EMPTY,  EMPTY,  ME,     FREE): [[SML,    SML,    DFO,    DFO,    SML],  [0,  0,  0,  0,  0], [0,  0,  1,  1,  0]],
    (NFREE, ME,     ME,     EMPTY,  ME,     EMPTY,  FREE): [[SML,    SML,    DFO,    SML,    DFO],  [0,  0,  0,  0,  0], [0,  0,  1,  0,  1]],
    (NFREE, ME,     ME,     EMPTY,  ME,     ME,     FREE): [[SML,    SML,    FIV,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     ME,     EMPTY,  EMPTY,  FREE): [[SML,    SML,    SML,    DFO,    DFO],  [0,  0,  0,  0,  0], [0,  0,  0,  1,  1]],
    (NFREE, ME,     ME,     ME,     EMPTY,  ME,     FREE): [[SML,    SML,    SML,    FIV,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     ME,     ME,     EMPTY,  FREE): [[SML,    SML,    SML,    SML,    FIV],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     ME,     ME,     ME,     FREE): [[SML,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],

    (FREE,  EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY, NFREE): [[0,      0,      0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  EMPTY,  EMPTY,  ME,    NFREE): [[0,      0,      0,      0,      SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  EMPTY,  ME,     EMPTY, NFREE): [[ITW,    ITW,    ITW,    SML,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  EMPTY,  ME,     ME,    NFREE): [[DTH,    DTH,    DTH,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     EMPTY,  EMPTY, NFREE): [[ITW,    TWO,    SML,    ITW,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     EMPTY,  ME,    NFREE): [[DTH,    DTH,    SML,    DTH,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     ME,     EMPTY, NFREE): [[ITH,    ITH,    SML,    SML,    DTH],  [1,  1,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  EMPTY,  ME,     ME,     ME,    NFREE): [[DFO,    DFO,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [1,  1,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  EMPTY,  EMPTY, NFREE): [[TWO,    SML,    TWO,    ITW,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  EMPTY,  ME,    NFREE): [[DTH,    SML,    DTH,    DTH,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  ME,     EMPTY, NFREE): [[ITH,    SML,    ITH,    SML,    DTH],  [1,  0,  1,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     EMPTY,  ME,     ME,    NFREE): [[DFO,    SML,    DFO,    SML,    SML],  [0,  0,  0,  0,  0], [1,  0,  1,  0,  0]],
    (FREE,  EMPTY,  ME,     ME,     EMPTY,  EMPTY, NFREE): [[THR,    SML,    SML,    ITH,    DTH],  [1,  0,  0,  1,  0], [0,  0,  0,  0,  0]],
    (FREE,  EMPTY,  ME,     ME,     EMPTY,  ME,    NFREE): [[DEX,    SML,    SML,    DFO,    SML],  [0,  0,  0,  0,  0], [1,  0,  0,  1,  0]],
    (FREE,  EMPTY,  ME,     ME,     ME,     EMPTY, NFREE): [[FOU,    SML,    SML,    SML,    DFO],  [0,  0,  0,  0,  0], [1,  0,  0,  0,  1]],
    (FREE,  EMPTY,  ME,     ME,     ME,     ME,    NFREE): [[FIV,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  EMPTY,  EMPTY, NFREE): [[SML,    TWO,    ITW,    ITW,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  EMPTY,  ME,    NFREE): [[SML,    DTH,    DTH,    DTH,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  ME,     EMPTY, NFREE): [[SML,    ITH,    ITH,    SML,    DTH],  [0,  1,  1,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  EMPTY,  ME,     ME,    NFREE): [[SML,    DFO,    DFO,    SML,    SML],  [0,  0,  0,  0,  0], [0,  1,  1,  0,  0]],
    (FREE,  ME,     EMPTY,  ME,     EMPTY,  EMPTY, NFREE): [[SML,    THR,    SML,    ITH,    DTH],  [0,  1,  0,  1,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     EMPTY,  ME,     EMPTY,  ME,    NFREE): [[SML,    DEX,    SML,    DFO,    SML],  [0,  0,  0,  0,  0], [0,  1,  0,  1,  0]],
    (FREE,  ME,     EMPTY,  ME,     ME,     EMPTY, NFREE): [[SML,    FOU,    SML,    SML,    DFO],  [0,  0,  0,  0,  0], [0,  1,  0,  0,  1]],
    (FREE,  ME,     EMPTY,  ME,     ME,     ME,    NFREE): [[SML,    FIV,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     EMPTY,  EMPTY,  EMPTY, NFREE): [[SML,    SML,    THR,    ITH,    DTH],  [0,  0,  1,  1,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     EMPTY,  EMPTY,  ME,    NFREE): [[SML,    SML,    DEX,    DFO,    SML],  [0,  0,  0,  0,  0], [0,  0,  1,  1,  0]],
    (FREE,  ME,     ME,     EMPTY,  ME,     EMPTY, NFREE): [[SML,    SML,    FOU,    SML,    DFO],  [0,  0,  0,  0,  0], [0,  0,  1,  0,  1]],
    (FREE,  ME,     ME,     EMPTY,  ME,     ME,    NFREE): [[SML,    SML,    FIV,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     ME,     EMPTY,  EMPTY, NFREE): [[SML,    SML,    SML,    FOU,    DEX],  [0,  0,  0,  0,  0], [0,  0,  0,  1,  1]],
    (FREE,  ME,     ME,     ME,     EMPTY,  ME,    NFREE): [[SML,    SML,    SML,    FIV,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     ME,     ME,     EMPTY, NFREE): [[SML,    SML,    SML,    SML,    FIV],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (FREE,  ME,     ME,     ME,     ME,     ME,    NFREE): [[SML,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],

    (NFREE, EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY, NFREE): [[0,      0,      0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  EMPTY,  EMPTY,  ME,    NFREE): [[0,      0,      0,      0,      SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  EMPTY,  ME,     EMPTY, NFREE): [[0,      0,      0,      SML,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  EMPTY,  ME,     ME,    NFREE): [[0,      0,      0,      SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     EMPTY,  EMPTY, NFREE): [[0,      0,      SML,    0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     EMPTY,  ME,    NFREE): [[0,      0,      SML,    0,      SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     ME,     EMPTY, NFREE): [[0,      0,      SML,    SML,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  EMPTY,  ME,     ME,     ME,    NFREE): [[DFO,    DFO,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [1,  1,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  EMPTY,  EMPTY, NFREE): [[0,      SML,    0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  EMPTY,  ME,    NFREE): [[0,      SML,    0,      0,      SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  ME,     EMPTY, NFREE): [[0,      SML,    0,      SML,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     EMPTY,  ME,     ME,    NFREE): [[DFO,    SML,    DFO,    SML,    SML],  [0,  0,  0,  0,  0], [1,  0,  1,  0,  0]],
    (NFREE, EMPTY,  ME,     ME,     EMPTY,  EMPTY, NFREE): [[0,      SML,    SML,    0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, EMPTY,  ME,     ME,     EMPTY,  ME,    NFREE): [[DFO,    SML,    SML,    DFO,    SML],  [0,  0,  0,  0,  0], [1,  0,  0,  1,  0]],
    (NFREE, EMPTY,  ME,     ME,     ME,     EMPTY, NFREE): [[DFO,    SML,    SML,    SML,    DFO],  [0,  0,  0,  0,  0], [1,  0,  0,  0,  1]],
    (NFREE, EMPTY,  ME,     ME,     ME,     ME,    NFREE): [[FIV,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  EMPTY,  EMPTY, NFREE): [[SML,    0,      0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  EMPTY,  ME,    NFREE): [[SML,    0,      0,      0,      SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  ME,     EMPTY, NFREE): [[SML,    0,      0,      SML,    0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  EMPTY,  ME,     ME,    NFREE): [[SML,    DFO,    DFO,    SML,    SML],  [0,  0,  0,  0,  0], [0,  1,  1,  0,  0]],
    (NFREE, ME,     EMPTY,  ME,     EMPTY,  EMPTY, NFREE): [[SML,    0,      SML,    0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     EMPTY,  ME,     EMPTY,  ME,    NFREE): [[SML,    DFO,    SML,    DFO,    SML],  [0,  0,  0,  0,  0], [0,  1,  0,  1,  0]],
    (NFREE, ME,     EMPTY,  ME,     ME,     EMPTY, NFREE): [[SML,    DFO,    SML,    SML,    DFO],  [0,  0,  0,  0,  0], [0,  1,  0,  0,  1]],
    (NFREE, ME,     EMPTY,  ME,     ME,     ME,    NFREE): [[SML,    FIV,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     EMPTY,  EMPTY,  EMPTY, NFREE): [[SML,    SML,    0,      0,      0],    [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     EMPTY,  EMPTY,  ME,    NFREE): [[SML,    SML,    DFO,    DFO,    SML],  [0,  0,  0,  0,  0], [0,  0,  1,  1,  0]],
    (NFREE, ME,     ME,     EMPTY,  ME,     EMPTY, NFREE): [[SML,    SML,    DFO,    SML,    DFO],  [0,  0,  0,  0,  0], [0,  0,  1,  0,  1]],
    (NFREE, ME,     ME,     EMPTY,  ME,     ME,    NFREE): [[SML,    SML,    FIV,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     ME,     EMPTY,  EMPTY, NFREE): [[SML,    SML,    SML,    DFO,    DFO],  [0,  0,  0,  0,  0], [0,  0,  0,  1,  1]],
    (NFREE, ME,     ME,     ME,     EMPTY,  ME,    NFREE): [[SML,    SML,    SML,    FIV,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     ME,     ME,     EMPTY, NFREE): [[SML,    SML,    SML,    SML,    FIV],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
    (NFREE, ME,     ME,     ME,     ME,     ME,    NFREE): [[SML,    SML,    SML,    SML,    SML],  [0,  0,  0,  0,  0], [0,  0,  0,  0,  0]],
}

def dynamicThreshold(depth):
    return max(THRESHOLD - depth, 1)


class BoardScore:
    def __init__(self):
        self.ban = None
        self.board = [[EMPTY for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        # 0: score on - 
        # 1: score on \ 
        # 2: score on |
        # 3: score on /
        self.myBoardScore = [[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)] for k in range(4)]
        self.opponentBoardScore = [[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)] for k in range(4)]
        # 
        self.myThree = [[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)] for k in range(4)]
        self.myFour = [[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)] for k in range(4)]
        self.opponentThree = [[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)] for k in range(4)]
        self.opponentFour = [[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)] for k in range(4)]
        # total 
        self.myBoardScoreTotal = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.opponentBoardScoreTotal = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.history = []

    def debugPrintAll(self):
        print("Board:")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                print("%-5d"%self.board[i][j], end = "")
            print("")
        print("MyScore")
        for k in range(4):
            print("direction: " + str(k))
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.myBoardScore[k][i][j] == -float("Inf"):
                        print("-Inf ", end = "")
                    else:
                        print("%-5d"%self.myBoardScore[k][i][j], end = "")
                print("")
        print("OpponentScore")
        for k in range(4):
            print("direction: " + str(k))
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.opponentBoardScore[k][i][j] == -float("Inf"):
                        print("-Inf ", end = "")
                    else:
                        print("%-5d"%self.opponentBoardScore[k][i][j], end = "")
                print("")
        print("MyThree")
        for k in range(4):
            print("direction: " + str(k))
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.myThree[k][i][j] == -float("Inf"):
                        print("-Inf ", end = "")
                    else:
                        print("%-5d"%self.myThree[k][i][j], end = "")
                print("")
        print("MyFour")
        for k in range(4):
            print("direction: " + str(k))
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.myFour[k][i][j] == -float("Inf"):
                        print("-Inf ", end = "")
                    else:
                        print("%-5d"%self.myFour[k][i][j], end = "")
                print("")
        print("OpponentThree")
        for k in range(4):
            print("direction: " + str(k))
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.opponentThree[k][i][j] == -float("Inf"):
                        print("-Inf ", end = "")
                    else:
                        print("%-5d"%self.opponentThree[k][i][j], end = "")
                print("")
        for k in range(4):
            print("direction: " + str(k))
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.opponentFour[k][i][j] == -float("Inf"):
                        print("-Inf ", end = "")
                    else:
                        print("%-5d"%self.opponentFour[k][i][j], end = "")
                print("")
        print("MyTotal")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.myBoardScoreTotal[i][j] == -float("Inf"):
                    print("-Inf ", end = "")
                else:
                    print("%-5d"%self.myBoardScoreTotal[i][j], end = "")
            print("")
        print("OpponentTotal")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.opponentBoardScoreTotal[i][j] == -float("Inf"):
                    print("-Inf ", end = "")
                else:
                    print("%-5d"%self.opponentBoardScoreTotal[i][j], end = "")
            print("")


    def boardScoreInitialization(self, outsideBoard, ban):
        # a function only called once at the beginning where an initial board is given
        # ban = player who plays first
        self.ban = ban
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if outsideBoard[i][j] != EMPTY:
                    self.boardScoreUpdate(outsideBoard[i][j], [i, j])
        #self.debugPrintAll()

    def withinBoardRange(self, position):
        # a help function used to determine whether point is inside board range
        [x, y] = position
        if (x<0 or y<0 or x>=BOARD_SIZE or y>=BOARD_SIZE):
            return False
        else:
            return True

    def next(self, position, direction, distance):
        [x, y] = position
        if direction == 0:
            pos = [x, y-distance]
        elif direction == 1:
            pos = [x-distance, y-distance]
        elif direction == 2:
            pos = [x-distance, y]
        elif direction == 3:
            pos = [x-distance, y+distance]
        else:
            return None
        return pos

    def allocateUpdate(self, pos, direction):
        [x, y] = pos
        player = self.board[x][y]
        if player == ME:
            opponent = OTHER
        else:
            opponent = ME
        if direction == 0:
            line = [EMPTY] * BOARD_SIZE
            for i in range(BOARD_SIZE):
                line[i] = self.board[x][i]
            place = y
        elif direction == 1:
            if (x > y):
                line = [EMPTY] * (BOARD_SIZE-x+y)
                for i in range(BOARD_SIZE-x+y):
                    line[i] = self.board[i+x-y][i]
                place = y
            else:
                line = [EMPTY] * (BOARD_SIZE-y+x)
                for i in range(BOARD_SIZE-y+x):
                    line[i] = self.board[i][i+y-x]
                place = x
        elif direction == 2:
            line = [EMPTY] * BOARD_SIZE
            for i in range(BOARD_SIZE):
                line[i] = self.board[i][y]
            place = x
        else:
            if (x + y < BOARD_SIZE):
                line = [EMPTY] * (x+y+1)
                for i in range(x+y+1):
                    line[i] = self.board[i][x+y-i]
                place = x
            else:
                line = [EMPTY] * (BOARD_SIZE*2-x-y-1)
                for i in range(BOARD_SIZE*2-x-y-1):
                    line[i] = self.board[x+y+i+1-BOARD_SIZE][BOARD_SIZE-i-1]
                place = BOARD_SIZE-1-y
        place3 = place4 = place
        length = len(line)
        while (place3 >= 0 and line[place3] != opponent):
            place3 = place3 - 1
        while (place4 < length and line[place4] != opponent):
            place4 = place4 + 1
        place1 = place3
        place2 = place3 + 1
        place5 = place4 - 1
        place6 = place4
        while (place1 >= 0 and line[place1] != player):
            place1 = place1 - 1
        while (line[place2] != player):
            place2 = place2 + 1
        while (place6 < length and line[place6] != player):
            place6 = place6 + 1
        while (line[place5] != player):
            place5 = place5 - 1
        return line[place1+1:place2], line[place3+1:place4], line[place5+1:place6],\
            self.next(pos, direction, place-place1-1), \
            self.next(pos, direction, place-place3-1), \
            self.next(pos, direction, place-place5-1)

    def clearScore(self, length, direction, startPos):
        for i in range(length):
            updatePos = self.next(startPos, direction, -i)
            if self.board[updatePos[0]][updatePos[1]] == EMPTY:
                if (updatePos[0], updatePos[1]) not in self.history[-1]:
                    self.history[-1][(updatePos[0], updatePos[1])] = \
                        [self.myBoardScore[i][updatePos[0]][updatePos[1]] for i in range(4)] + \
                        [self.opponentBoardScore[i][updatePos[0]][updatePos[1]] for i in range(4)] + \
                        [self.myThree[i][updatePos[0]][updatePos[1]] for i in range(4)] + \
                        [self.myFour[i][updatePos[0]][updatePos[1]] for i in range(4)] + \
                        [self.opponentThree[i][updatePos[0]][updatePos[1]] for i in range(4)] + \
                        [self.opponentFour[i][updatePos[0]][updatePos[1]] for i in range(4)] + \
                        [self.myBoardScoreTotal[updatePos[0]][updatePos[1]]] + \
                        [self.opponentBoardScoreTotal[updatePos[0]][updatePos[1]]]
                self.myBoardScore[direction][updatePos[0]][updatePos[1]] = 0
                self.opponentBoardScore[direction][updatePos[0]][updatePos[1]] = 0
                self.myBoardScoreTotal[updatePos[0]][updatePos[1]] = None
                self.opponentBoardScoreTotal[updatePos[0]][updatePos[1]] = None
            else:
                self.myBoardScore[direction][updatePos[0]][updatePos[1]] = SML
                self.opponentBoardScore[direction][updatePos[0]][updatePos[1]] = SML
            self.myThree[direction][updatePos[0]][updatePos[1]] = 0
            self.myFour[direction][updatePos[0]][updatePos[1]] = 0
            self.opponentThree[direction][updatePos[0]][updatePos[1]] = 0
            self.opponentFour[direction][updatePos[0]][updatePos[1]] = 0

    def shapeScoreUpdate(self, shape, direction, player, startPos):
        len_shape = len(shape)
        if (len_shape < 5):
            return
        record = [-float("Inf")] * len_shape
        recordThree = [0] * len_shape
        recordFour = [0] * len_shape
        if player != ME:
            for i in range(len_shape):
                if shape[i] == OTHER:
                    shape[i] = ME
                elif shape[i] == ME:
                    shape[i] = OTHER
        for i in range(len_shape-4):
            tup = tuple(shape[i:i+5])
            if i == 0:
                tup = (NFREE,) + tup
            else:
                tup = (FREE,) + tup
            if i == len_shape - 5:
                tup = tup + (NFREE,)
            else:
                tup = tup + (FREE,)
            result = quick_check_table[tup]
            for j in range(5):
                if (record[i+j] < result[0][j]):
                    record[i+j] = result[0][j]
                if (result[1][j] == 1 and recordFour[i+j] == 0):
                    recordThree[i+j] = 1
                if (result[2][j] == 1):
                    recordThree[i+j] = 0
                    recordFour[i+j] = 1
        for i in range(len_shape):
            updatePos = self.next(startPos, direction, -i)
            if player == ME:
                self.myBoardScore[direction][updatePos[0]][updatePos[1]] += record[i]
                self.myThree[direction][updatePos[0]][updatePos[1]] += recordThree[i]
                self.myFour[direction][updatePos[0]][updatePos[1]] += recordFour[i]
                if record[i] != SML:
                    self.opponentBoardScore[direction][updatePos[0]][updatePos[1]] += int(record[i]/10)
            else:
                self.opponentBoardScore[direction][updatePos[0]][updatePos[1]] += record[i]
                self.opponentThree[direction][updatePos[0]][updatePos[1]] += recordThree[i]
                self.opponentFour[direction][updatePos[0]][updatePos[1]] += recordFour[i]
                if record[i] != SML:
                    self.myBoardScore[direction][updatePos[0]][updatePos[1]] += int(record[i]/10)

    def boardScoreUpdate(self, player, pos):
        # player play at pos
        # update all score after this move
        self.history.append({})
        [x, y] = pos
        self.board[x][y] = player
        if player == ME:
            opponent = OTHER
        else:
            opponent = ME
        self.history[-1][(x, y)] = [self.myBoardScore[i][x][y] for i in range(4)]\
            +[self.opponentBoardScore[i][x][y] for i in range(4)]\
            +[self.myThree[i][x][y] for i in range(4)]+[self.myFour[i][x][y] for i in range(4)]\
            +[self.opponentThree[i][x][y] for i in range(4)]+[self.opponentFour[i][x][y] for i in range(4)]\
            +[self.myBoardScoreTotal[x][y]]+[self.opponentBoardScoreTotal[x][y]]
        self.myBoardScoreTotal[x][y] = -float("Inf")
        self.opponentBoardScoreTotal[x][y] = -float("Inf")
        for direction in range(4):
            left, mid, right, pos1, pos2, pos3 = self.allocateUpdate(pos, direction)
            self.clearScore(len(left), direction, pos1)
            self.clearScore(len(mid), direction, pos2)
            self.clearScore(len(right), direction, pos3)
            self.shapeScoreUpdate(left, direction, opponent, pos1)
            self.shapeScoreUpdate(mid, direction, player, pos2)
            self.shapeScoreUpdate(right, direction, opponent, pos3)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.myBoardScoreTotal[i][j] == None:
                    self.myBoardScoreTotal[i][j] = self.myBoardScore[0][i][j] + self.myBoardScore[1][i][j] + self.myBoardScore[2][i][j] + self.myBoardScore[3][i][j]
                    self.opponentBoardScoreTotal[i][j] = self.opponentBoardScore[0][i][j] + self.opponentBoardScore[1][i][j] + self.opponentBoardScore[2][i][j] + self.opponentBoardScore[3][i][j]
                    myThree = self.myThree[0][i][j] + self.myThree[1][i][j] + self.myThree[2][i][j] + self.myThree[3][i][j]
                    myFour = self.myFour[0][i][j] + self.myFour[1][i][j] + self.myFour[2][i][j] + self.myFour[3][i][j]
                    opponentThree = self.opponentThree[0][i][j] + self.opponentThree[1][i][j] + self.opponentThree[2][i][j] + self.opponentThree[3][i][j]
                    opponentFour = self.opponentFour[0][i][j] + self.opponentFour[1][i][j] + self.opponentFour[2][i][j] + self.opponentFour[3][i][j]
                    if (myThree + myFour > 1 or opponentThree + opponentFour > 1):
                        self.myBoardScoreTotal[i][j] += 1000
                        self.opponentBoardScoreTotal[i][j] += 1000
                    if (self.ban == ME):
                        if (myThree > 1 or myFour > 1):
                            self.myBoardScoreTotal[i][j] = -10000
                            self.opponentBoardScoreTotal[i][j] -= 1000
                    else:
                        if (opponentThree > 1 or opponentFour > 1):
                            self.opponentBoardScoreTotal[i][j] = -10000
                            self.myBoardScoreTotal[i][j] -= 1000


    def getPossiblePosition(self, player, depth):
        possible = []
        if player == ME:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.myBoardScoreTotal[i][j] > 0:
                        possible.append([[i, j], self.myBoardScoreTotal[i][j]])
        else:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.opponentBoardScoreTotal[i][j] > 0:
                        possible.append([[i, j], self.opponentBoardScoreTotal[i][j]])
        if len(possible) == 0:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == EMPTY:
                        if player == ME:
                            possible.append([[i, j], self.myBoardScoreTotal[i][j]])
                        else:
                            possible.append([[i, j], self.opponentBoardScoreTotal[i][j]])
        # sorting makes alpha-beta cutting more efficient
        possible.sort(key = lambda s:s[1], reverse = True)
        for i in range(len(possible)):
            if possible[i][1] < possible[0][1]/10:
                possible = possible[0:i]
                break
        return possible[0: dynamicThreshold(depth)]

    def backspace(self):
        global NUM_STEPS
        NUM_STEPS += 1
        if self.history == []:
            return
        dic = self.history.pop()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i, j) in dic:
                    past = dic[(i,j)]
                    for k in range(4):
                        self.myBoardScore[k][i][j] = past[k]
                        self.opponentBoardScore[k][i][j] = past[4+k]
                        self.myThree[k][i][j] = past[8+k]
                        self.myFour[k][i][j] = past[12+k]
                        self.opponentThree[k][i][j] = past[16+k]
                        self.opponentFour[k][i][j] = past[20+k]
                    self.myBoardScoreTotal[i][j] = past[24]
                    self.opponentBoardScoreTotal[i][j] = past[25]

class Node:
    # class of search tree node
    def __init__(self, place):
        self.height = None      # distance to root
        self.score = None       # score
        self.place = place      # position at board
        self.parent = None      # parent
        self.child = []         # children
        self.alpha = None       # alpha - beta value

class MinMaxTree:
    # class of search tree
    def __init__(self):
        self.root = Node(None)
        self.root.height = 0
        self.root.alpha = -50000

    def reconstruct(self):
        self.root = Node(None)
        self.root.height = 0
        self.root.alpha = -50000

    def insert(self, node, place, change):
        # insert a new node as child of node
        # change: score change compared with score of node
        newChild = Node(place)
        newChild.parent = node
        newChild.height = node.height + 1
        newChild.score = node.score + change
        if (newChild.height % 2 == 0):
            newChild.alpha = -50000
        else:
            newChild.alpha = 50000
        node.child.append(newChild)

    def deepsearch(self, node, boardScore):
        # deep search code (alpha-beta cutting)
        # reference: https://github.com/lihongxun945/myblog/labels/五子棋AI教程第二版
        place = node.place
        height = node.height
        if height < DEPTH:
            if (height % 2 == 1):
                boardScore.boardScoreUpdate(ME, place)
                possible = boardScore.getPossiblePosition(OTHER, height)
                if height == DEPTH - 1:
                    node.score -= possible[0][1]
                    boardScore.backspace()
                    boardScore.board[place[0]][place[1]] = EMPTY
                    return False
                for position, change in possible:
                    self.insert(node, position, -change)
            else:
                boardScore.boardScoreUpdate(OTHER, place)
                possible = boardScore.getPossiblePosition(ME, height)
                for position, change in possible:
                    self.insert(node, position, change)
            if NUM_STEPS > NUM_STEPS_THRESHOLD:
                boardScore.backspace()
                boardScore.board[place[0]][place[1]] = EMPTY
                return True
            node.score = None
            scorelist = []
            for childnode in node.child:
                alpha = node.parent.alpha
                broken = self.deepsearch(childnode, boardScore)
                if broken:
                    boardScore.backspace()
                    boardScore.board[place[0]][place[1]] = EMPTY
                    return True
                if (node.height%2 == 1):
                    # opponent choose
                    if (childnode.score < alpha):
                        node.score = childnode.score
                        break
                    else:
                        scorelist.append(childnode.score)
                else:
                    # I choose:
                    if (childnode.score > alpha):
                        node.score = childnode.score
                        break
                    else:
                        scorelist.append(childnode.score)
            # set alpha-beta value
            if (node.height%2 == 1):
                if (node.score == None):
                    node.score = min(scorelist)
                if (node.score > alpha):
                    node.parent.alpha = node.score
            else:
                if (node.score == None):
                    node.score = max(scorelist)
                if (node.score < alpha):
                    node.parent.alpha = node.score
            # set board back to origianl status
            boardScore.backspace()
            boardScore.board[place[0]][place[1]] = EMPTY
            return False

    def choice(self):
        # select best child of root and return its position
        self.root.child.sort(key = lambda s:s.score, reverse = True)
        return self.root.child[0].place
        
class AI:
    boardSize = BOARD_SIZE;
    # TODO: add your own attributes here if you need any

    # Constructor
    def __init__(self):
        self.board = []
        for i in range(0,BOARD_SIZE):
            self.board.append([])
            for j in range(0,BOARD_SIZE):
                self.board[i].append(EMPTY)
        # TODO: add your own contructing procedure here if necessary
        self.boardScore = BoardScore()
        self.tree = MinMaxTree()
        self.ban = ME
        self.hand = 0
        self.score = 0

    def init(self):
        # TODO: add your own initilization here if you need any
        self.boardScore = BoardScore()
        self.tree = MinMaxTree()
        self.ban = ME
        self.hand = 0
        self.score = 0

    def begin(self):
        # TODO: write your own opening here
        # NOTE: this method is only called when it's your turn to begin (先手)
        # RETURN: two integer represent the axis of target position
        self.ban = OTHER
        return self.turn()

    def turn(self):
        # TODO: write your in-turn operation here
        # NOTE: this method is called when it's your turn to put chess
        # RETURN: two integer represent the axis of target position
        global NUM_STEPS
        NUM_STEPS = 0
        if self.hand == 0:
            self.boardScore.boardScoreInitialization(self.board, self.ban)
        #self.boardScore.debugPrintAll()
        self.tree.reconstruct()
        self.tree.root.score = self.score
        possible = self.boardScore.getPossiblePosition(ME, 0)
        if self.hand >= 107 or self.hand <= 1:
            self.hand += 1
            self.boardScore.boardScoreUpdate(ME, possible[0][0])
            self.boardScore.history = []
            return possible[0][0]
        for position, change in possible:
            self.tree.insert(self.tree.root, position, change)
        for child in self.tree.root.child:
            broken = self.tree.deepsearch(child, self.boardScore)
            if broken:
                child.score = -float("Inf")
        self.hand += 1
        self.boardScore.boardScoreUpdate(ME, self.tree.choice())
        self.boardScore.history = []
        #print("# of move: " + str(NUM_STEPS))
        return self.tree.choice()

    @classmethod
    # NOTE: don't change this function
    def display(self):
        for i in range(0,BOARD_SIZE):
            print(self.board[i])

def loop(AI):
    # NOTE: don't change this function
    while True:
        buffer = input()
        buffersplitted = buffer.split(' ');
        if len(buffersplitted) == 0:
            continue
        command = buffersplitted[0]
        if command == START:
            AI.init();
        elif command == PLACE:
            x = int(buffersplitted[1])
            y = int(buffersplitted[2])
            v = int(buffersplitted[3])
            AI.board[x][y] = v
        elif command == DONE:
            print("OK")
        elif command == BEGIN:
            x, y = AI.begin()
            AI.board[x][y] = ME
            print(str(x)+" "+str(y))
        elif command == TURN:
            x = int(buffersplitted[1])
            y = int(buffersplitted[2])
            AI.board[x][y] = OTHER
            AI.boardScore.boardScoreUpdate(OTHER, [x, y])
            x, y = AI.turn()
            AI.board[x][y] = ME
            print(str(x)+" "+str(y))
        elif command == "print":
           AI.display()
        elif command == END:
            break

if __name__ == "__main__":
    # NOTE: don't change main function
    ai = AI()
    loop(ai)