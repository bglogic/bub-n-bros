#
#  A series of compact levels.
#

import boarddef
from boarddef import LNasty, LMonky, LGhosty, LFlappy
from boarddef import LSpringy, LOrcy, LGramy, LBlitzy
from boarddef import RNasty, RMonky, RGhosty, RFlappy
from boarddef import RSpringy, ROrcy, RGramy, RBlitzy


class level01(boarddef.Level):
    a = LNasty
    b = RNasty
    
    walls = """
#############################
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##         a     b         ##
####   ###############   ####
##                         ##
##                         ##
##                         ##
##         a     b         ##
####   ###############   ####
##                         ##
##                         ##
##                         ##
##         a     b         ##
####   ###############   ####
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""


class level02(boarddef.Level):
    a = LNasty
    b = RNasty
    g = RGhosty
    
    walls = """
#############################
##            #            ##
##            #            ##
##            #            ##
##            #   g        ##
##  g         #            ##
##            #            ##
##            #            ##
####   ###############   ####
##     #             #     ##
##     #             #     ##
##     #             #     ##
##     #   a     b   #     ##
####   ###############   ####
##                         ##
##                         ##
##                         ##
##                         ##
####                     ####
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""


class level03(boarddef.Level):
    a = LNasty
    b = RNasty

    letter = 1
    
    walls = """
#########    ###    #########
##      #           #      ##
##      #           #      ##
##      #           #      ##
##      #           #      ##
##b  #  #           #  # a ##
######  #####   #####  ######
##                         ##
##                         ##
##                         ##
##  #b  #   #   #   # a #  ##
##  #####   #####   #####  ##
##    #               #    ##
##    #               #    ##
##    #               #    ##
##b   #               #  a ##
#######    # b   #    #######
##         #######         ##
##            #            ##
##            #            ##
##            #            ##
##            #            ##
##            #            ##
#########    ###    #########
"""   #|#    #|#    #|#   """


class level04(boarddef.Level):
    a = LNasty
    b = RNasty
    g = LOrcy

    fire = 1
    
    walls = """
#########    ###    #########
##      #           #      ##
##      #           #      ##
##      #           #      ##
##      #           #      ##
##b  #  #           #  # a ##
######  #####   #####  ######
##                         ##
##                         ##
##                         ##
##  #b  #   #gg #   # a #  ##
##  #####   #####   #####  ##
##    #               #    ##
##    #               #    ##
##    #               #    ##
##b   #               #  a ##
#######    # b   #    #######
##         #######         ##
##            #            ##
##            #            ##
##            #            ##
##            #            ##
##            #            ##
#########    ###    #########
"""   #|#    #|#    #|#   """

class level05(boarddef.Level):
    a = LNasty
    b = RNasty
    g = LOrcy
    f = RFlappy

    water = top = letter = 1
    
    walls = """
##      #           #      ##
##      #           #      ##
##      #           #      ##
##      #           #      ##
##      #           #      ##
##b  #  #           #  # a ##
#### #  #####   #####  # ####
##                         ##
##                         ##
##                         ##
##  #b  #   #gg #   # a #  ##
##  # ###   ## ##   ### #  ##
##    #               #    ##
##    #               #    ##
##    #       f       #    ##
##b   #               #  a ##
#######    # b   #    #######
##         # ### #         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
#########           #########
"""   #|#    #|#    #|#   """

    winds = """
>>                         <<
>>xxxxxxxxxxxxxxxxxxxxxxxxx<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
"""

class level06(boarddef.Level):
    a = LNasty, RNasty, LMonky

    letter = fire = 1
    
    walls = """
#############################
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##        ###              ##
##          #           ## ##
##      ##  #       ##  #  ##
##       #  #   ##  #   #  ##
##   ##  #  #   #   #   #  ##
##    #  ####   #   #   #a ##
## a  ####      #############
## ####                    ##
####                       ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level07(boarddef.Level):
    g = LGhosty, LGhosty, LGhosty, LGhosty
    h = RGhosty, RGhosty, RGhosty, RGhosty

    letter = lightning = 1
    
    walls = """
##                         ##
##                         ##
##   #                 #   ##
##   #                 #   ##
##   #                 #   ##
##  ###               ###  ##
##h # #       #       # #g ##
## # # #      #      # # # ##
##### ####    #    #### #####
## # # #     ###     # # # ##
##  # #      # #      # #  ##
##  ###     # # #     ###  ##
##   #    #### ####    #   ##
##   #      # # #      #   ##
##   #       # #       #   ##
##           ###           ##
##            #            ##
##      #     #     #      ##
##      #     #     #      ##
##      #           #      ##
##     ###         ###     ##
##     # #         # #     ##
##    # # #       # # #    ##
##  #### ####   #### ####  ##
"""   #|#    #|#    #|#   """

class level08(boarddef.Level):
    s = LSpringy
    r = RSpringy
    f = LFlappy
    g = RFlappy
    
    walls = """
#############################
##                         ##
## g                    f  ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##            #            ##
##                         ##
##           ###           ##
##                         ##
##          #####          ##
##                         ##
##         #######         ##
##                         ##
##        #########        ##
##         sssrrr          ##
##       ###########       ##
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level09(boarddef.Level):
    m = (LMonky, RMonky,)*5
    g = LGhosty
    
    walls = """
#######  ####   ####  #######
#######  ####   ####  #######
##         ##   ##         ##
##         ##   ##         ##
##   g     ##   ##     g   ##
##         ##   ##         ##
##         ##   ##         ##
####    #####   #####    ####
####    #####   #####    ####
##                         ##
##   ##  ####   ####  ##   ##
##   ##  ####   ####  ##   ##
##       ##       ##       ##
####     ##       ##     ####
####     ##   m   ##     ####
##       ##  ###  ##       ##
##   ##  ##  ###  ##  ##   ##
##   ##  ##  ###  ##  ##   ##
##       ##  ###  ##       ##
####     ##       ##     ####
####     ##       ##     ####
##       ##       ##       ##
##   ##  ####   ####  ##   ##
#######  ####   ####  #######
"""   #|#    #|#    #|#   """

class level10(boarddef.Level):
    n = LNasty

    fire = top = 1
    
    walls = """
##            #####   ##   ##
##               ##nn ##   ##
##               #######   ##
##                         ##
##                         ##
##  ##   #####             ##
##  ##nn ##                ##
##  #######     #####   ## ##
##                 ##nn ## ##
##                 ####### ##
##                         ##
##                         ##
## ##   #####              ##
## ##nn ##                 ##
## #######                 ##
##                         ##
##           #####   ##    ##
##              ##nn ##    ##
##              #######    ##
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

    winds = """
>>                         <<
>>>           >>v  xxx    <<<
>>^                       ^<<
>>^                   v<<<^<<
>>^                       ^<<
>>^                       ^<<
>>^   xxx  v<<            ^<<
>>^                       ^<<
>>^>>>v         >>v  xxx  ^<<
>>^                       ^<<
>>^               >v      ^<<
>>^                       ^<<
>>^                       ^<<
>>^  xxx  v<<             ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^               xxx     ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
"""

class level11(boarddef.Level):
    o = LOrcy
    p = ROrcy

    letter = fire = water = lightning = top = 1
    
    walls = """
##                         ##
##                         ##
###                       ###
##  #                   #  ##
##    #               #    ##
##      #           #      ##
##        # #   # #        ##
##            #            ##
## o  p  o #  #  #p  o  p  ##
####### ####  #  #### #######
##            #            ##
##            #            ##
##            #            ##
##     #      #      #     ##
##     #      #      #     ##
##     #      #      #     ##
##     #      #      #     ##
##     #      #      #     ##
##     #      #      #     ##
##     #      #      #     ##
##     #      #      #     ##
##     #  # #   # #  #     ##
##     #             #     ##
###### ######   ###### ######
"""   #|#    #|#    #|#   """

class level12(boarddef.Level):
    o = LGramy
    
    walls = """
##            ####         ##
##            #  #         ##
##            ####         ##
##            #  #         ##
##          #            o ##
##          #################
##                   #  #  ##
##                   ####  ##
##       o #         #  #  ##
## #########         ####  ##
## #  #              #  #  ##
## ####          #       o ##
## #  #          ############
## ####          #  #      ##
## #  #          ####      ##
##       o #     #  #      ##
############     ####      ##
##    #  #       #  #      ##
##    ####           o #   ##
##    #  #      ########   ##
##    ####                 ##
##    #  #                 ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level13(boarddef.Level):
    n = LNasty
    m = LMonky
    g = LGhosty
    f = LFlappy
    s = LSpringy
    o = LOrcy
    r = LGramy
    b = LBlitzy
    
    walls = """
##         # ####          ##
##  f      ##  ##   ####   ##
##          ####   ##  ##  ##
##                 #### #  ##
##   ####   f      ######  ##
##  ##  ##     f   ######  ##
##  # ####   ####   ####   ##
##  ######  ######         ##
##  ######  ######         ##
##   ####   #### #         ##
##          ##  ##     f   ##
##           ####          ##
##  f                      ##
##                ####     ##
##               ######    ##
##     ####      ######    ##
##    ##  ##     # ####    ##
##    # ####  f  ##  ##    ##
##    ######      ####     ##
##    ######               ##
##     ####                ##
##                         ##
##          ####           ##
######     ######       #####
"""   #|#    #|#    #|#   """

class level14(boarddef.Level):
    o = LOrcy
    r = LGramy
    
    walls = """
#############################
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##    ###           ###    ##
##     ##           ##     ##
##      #           #      ##
##    ###           ###    ##
##     ##           ##     ##
##      #           #      ##
##      ##         ##      ##
##     ##           ##     ##
##    ###           ###    ##
##    ##             ##    ##
##    ##             ##    ##
##    ##or        or ##    ##
#############################
"""   #|#    #|#    #|#   """

class level15(boarddef.Level):
    s = LSpringy
    g = LGhosty
    
    walls = """
#############################
##                         ##
##                         ##
##                         ##
##       s       s         ##
##       s       s         ##
##       s       s         ##
##    ###s  #####s  ###    ##
##   #  ## ####### ##  #   ##
##   #    ###   ###    #   ##
##   ##  ###     ###  ##   ##
##     # ###  g  ### #     ##
##    #  ###     ###  #    ##
##   #    ###   ###    #   ##
##   #  ## ####### ##  #   ##
##    ###   #####   ###    ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level16(boarddef.Level):
    l = LBlitzy, LGramy
    r = RBlitzy, RGramy

    letter = 1
    
    walls = """
#############################
##           l r           ##
##           ####       ## ##
## ####   ## ####       ## ##
## ####   ##       #### ## ##
##    l   ##    ## #### ## ##
##  ####  ##    ##      l  ##
##  ####     ## ##    #### ##
##       ##  ## ##    #### ##
## ####  ##  ##            ##
## ####  ##  ## #### ##    ##
##       ##     #### ##    ##
##  ##      ####     ##    ##
##  ## #### ####  l  ## ## ##
##  ## ####       ##    ## ##
##  ##            ##    ## ##
##        ##      ## r  ## ##
##   #### ##      ## ##    ##
##   #### ## ####    ## ## ##
##        ## ####    ## ## ##
##   ####            ## ## ##
##   ####               ## ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level17(boarddef.Level):
    m = LMonky
    j = RMonky
    g = LGhosty
    h = RGhosty
    b = LBlitzy
    
    walls = """
############               ##
##         #               ##
##   g     #               ##
##  #####  #  ###########  ##
##  #   #  #  #         #  ##
##  #  ##  #  #   g     #  ##
##  #  #j  #  #  #####  #  ##
##  #  #####  #  #   #  #  ##
##  #         #  #  ##  #  ##
##  #b        #  #  #j  #  ##
##  ###########  #  #####  ##
##               #         ##
##               #         ##
##  ###########  #    h    ##
##  #         #  #  #####  ##
##  #    h    #  #  #   #  ##
##  #  #####  #  #  ##  #  ##
##  #  #   #  #  # m #  #  ##
##  #  ##  #  #  #####  #  ##
##  # m #  #  #         #  ##
##  #####  #  #       b #  ##
##         #  ###########  ##
##       b #               ##
############               ##
"""   #|#    #|#    #|#   """

class level18(boarddef.Level):
    o = (ROrcy,)*10
    
    walls = """
#############   #############
##                         ##
##            #            ##
##                         ##
##          #   #          ##
##                         ##
##                         ##
##       #         #       ##
##                         ##
##     #   #######   #     ##
##     #             #     ##
##     ##           ##     ##
##     #  ###   ###  #     ##
##     ##           ##     ##
##     #             #     ##
##     #   #######   #     ##
##     #             #     ##
##     ##           ##     ##
##     ######   ######     ##
##     ###         ###     ##
##     ##     o     ##     ##
##     ##  #######  ##     ##
##     ##           ##     ##
#############   #############
"""   #|#    #|#    #|#   """

class level19(boarddef.Level):
    n = LNasty
    g = RGhosty
    f = LFlappy
    s = LSpringy
    
    walls = """
##    ###    ###    ###    ##
##   #   #  #   #  #   #   ##
##   #   ####   ####   #   ##
##   #n  #  #n  #  #n  #   ##
##    ###    ###    ###    ##
##     #             #     ##
##     #             #     ##
##    ###      f    ###    ##
##   #   #  g      #   #   ##
##   #   #     f   #   #   ##
##   #n  #  g      #n  #   ##
##    ###           ###    ##
##     #             #     ##
##     #             #     ##
##    ###    ###    ###    ##
##   #   #s #   #s #   #   ##
##   #   ####   ####   #   ##
##   #n  #  #n  #  #n  #   ##
##    ###    ###    ###    ##
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level20(boarddef.Level):
    s = LSpringy, RSpringy

    letter = fire = top = 1
    
    walls = """
###                       ###
###                       ###
##                         ##
##                         ##
##ss  ss   #     #  ss  ss ##
## #   #   #     #   #   # ##
## #   #    #####    #   # ##
## #   #             #   # ##
## #   #             #   # ##
## #                     # ##
## #                     # ##
## #                     # ##
##                         ##
##                         ##
##                         ##
##                         ##
##    #               #    ##
##    #               #    ##
##    #               #    ##
##                         ##
##                         ##
##                         ##
##                         ##
## #########     ######### ##
"""   #|#    #|#    #|#   """

class level21(boarddef.Level):
    n = (RNasty,)*12

    letter = 1
    
    walls = """
#############################
##                         ##
##n                        ##
#########################  ##
##                         ##
##                         ##
##  #########################
##                         ##
##                         ##
#########################  ##
##                         ##
##                         ##
##  #########################
##                         ##
##                         ##
#########################  ##
##                         ##
##                         ##
##  #########################
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level22(boarddef.Level):
    n = LNasty
    m = LMonky
    g = LGhosty
    f = LFlappy
    s = LSpringy
    o = LOrcy
    r = LGramy
    b = LBlitzy
    
    walls = """
##    ###    ###    ###    ##
##   #   #  #   #  #   #   ##
##   #   ####   ####   #   ##
##   #o  #  #b  #  #r  #   ##
##    ###    ###    ###    ##
##     #             #     ##
##     #             #     ##
##    ###           ###    ##
##   #   #         #   #   ##
##   #   #         #   #   ##
##   #g  #         #f  #   ##
##    ###           ###    ##
##     #             #     ##
##     #             #     ##
##    ###    ###    ###    ##
##   #   #  #   #  #   #   ##
##   #   ####   ####   #   ##
##   #m  #  #s  #  #n  #   ##
##    ###    ###    ###    ##
##                         ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level23(boarddef.Level):
    m = LMonky

    water = top = 1
    
    walls = """
######    #       #    ######
######    #       #    ######
##        #  m    #        ##
## ######## ##### ######## ##
## ######## ##### ######## ##
## ######## #####   m   ## ##
## ######## ########### ## ##
##      m      ######## ## ##
## ########### ######## ## ##
## ###########      m   ## ##
## ################ ###### ##
## ################ ###### ##
## ########     m          ##
## ######## ############## ##
## ######## ############## ##
## ########m   ########### ##
##  m    ##### #####   m   ##
######## ##### ##### ########
######## m       m   ########
############## ##############
#############################
##                         ##
##                         ##
######    #########    ######
"""   #|#    #|#    #|#   """

class level24(boarddef.Level):
    g = RGhosty
    f = RFlappy
    s = LSpringy
    t = RSpringy
    
    walls = """
#############################
##                         ##
##                         ##
## s                    t  ##
## s                    t  ##
## s                    t  ##
######                 ######
##                         ##
##   #####  #####  #####   ##
##   #      #      #       ##
##   #g     #      #g      ##
##   #      #f     #       ##
##   #      #      #       ##
##                         ##
##                         ##
##   #####  #####  #####   ##
##   #      #      #       ##
##   #      #g     #       ##
##   #f     #      #f      ##
##   #      #      #       ##
##                         ##
##                         ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level25(boarddef.Level):
    s = LSpringy
    t = RSpringy

    letter = lightning = 1
    
    walls = """
#############   #############
##                         ##
##            #            ##
##            #            ##
##  s                  t   ##
##   #    #       #    #   ##
##   #    #       #    #   ##
##                         ##
##            #            ##
##            #            ##
##  t                  s   ##
##   #    #       #    #   ##
##   #    #       #    #   ##
##                         ##
##            #            ##
##            #            ##
##  s                  t   ##
##   #    #       #    #   ##
##   #    #       #    #   ##
##                         ##
##            #            ##
##            #            ##
##                         ##
#############   #############
"""   #|#    #|#    #|#   """

class level26(boarddef.Level):
    s = LSpringy

    fire = 1
    
    walls = """
#######               #######
##                         ##
##                         ##
##s                      s ##
##s   #######   #######  s ##
##s                      s ##
####                     ####
##                         ##
##    ##             ##    ##
##                         ##
##        ##     ##        ##
##                         ##
##           ###           ##
##                         ##
##s                      s ##
####   ##           ##   ####
##                         ##
##                         ##
##                         ##
##                         ##
##         s    s          ##
##       ##       ##       ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level27(boarddef.Level):
    s = LSpringy

    fire = 1
    
    walls = """
##                         ##
##                         ##
##        #  s    #        ##
##s  #     # s   #     # s ##
##  #       #s  #       #  ##
## #         # #         # ##
###           #           ###
##           ###           ##
###           #           ###
##   #     #  #  #     #   ##
##    #s  #   #   #s  #    ##
##     # #         # #     ##
##      #           #      ##
##     ###         ###     ##
##      #           #      ##
##      #           #      ##
##   s      #s  #     s    ##
##   #   #   # #   #   #   ##
##    # #     #     # #    ##
##     #     ###     #     ##
##    ###     #     ###    ##
##     #             #     ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level28(boarddef.Level):
    f = LFlappy
    
    walls = """
#############################
#########         ###########
##     ##   f     ####     ##
##f    ##   ff    ####   f ##
##f  f ##   ###   ####f f  ##
##   f ##   ###   #### f   ##
#####  ##   ###    ######  ##
#####  ##   ###    ######  ##
#####  ##   ####   ######  ##
#####  ##   ####   ######  ##
##          ####           ##
##                         ##
##                         ##
##   ##   ########   ###   ##
##   ##   ########   ###   ##
##   ##   ########   ###   ##
##   ##      ###     ###   ##
##   ##      ###     ###   ##
##   ##      ###     ###   ##
##   #####   ###   #####   ##
##   #####   ###   #####   ##
##           ###           ##
##           ###           ##
#############################
"""   #|#    #|#    #|#   """

class level29(boarddef.Level):
    f = LFlappy, RFlappy

    top = water = 1
    
    walls = """
##  #####################  ##
##                         ##
##    f              f     ##
##  #####################  ##
##  #####################  ##
##                         ##
##     f            f      ##
##  #####################  ##
##  #####################  ##
##                         ##
##      f          f       ##
##  #####################  ##
##  #####################  ##
##                         ##
##       f        f        ##
##  #####################  ##
##  #####################  ##
##                         ##
##        f      f         ##
##  #####################  ##
##  #####################  ##
##                         ##
##         f    f          ##
##  #####################  ##
"""   #|#    #|#    #|#   """

class level30(boarddef.Level):
    g = RGhosty
    h = RGhosty
    i = LGhosty
    j = LGhosty
    
    walls = """
#############################
##                         ##
##                         ##
##                         ##
##         ####g #         ##
##          ######         ##
##        j ######         ##
##         #######         ##
##         ######          ##
##         ######h         ##
##         #  ####         ##
##          i              ##
##                         ##
##                         ##
##   ####g #     ####g #   ##
##    ######      ######   ##
##  j ######    j ######   ##
##   #######     #######   ##
##   ######      ######    ##
##   ######h     ######h   ##
##   #  ####     #  ####   ##
##    i           i        ##
##                         ##
#############################
"""   #|#    #|#    #|#   """

class level31(boarddef.Level):
    o = LGramy, RGramy
    r = LOrcy
    s = ROrcy

    top = letter = lightning = fire = 1
    
    walls = """
##   ########   ########   ##
##                         ##
##                         ##
##    r              s     ##
##   ########   ########   ##
##o                      o ##
######                 ######
##                         ##
##o       s #   #r       o ##
#############   #############
##                         ##
##                         ##
##  #####################  ##
##                         ##
##                         ##
##    #######   #######    ##
##                         ##
##o                      o ##
##########  #   #  ##########
##          #   #          ##
##         ##   ##         ##
##                         ##
##                         ##
#############   #############
"""   #|#    #|#    #|#   """

class level32(boarddef.Level):
    n = LNasty, RNasty
    f = (LFlappy, RFlappy) * 2
    
    walls = """
#############   #############
##         ##   ##         ##
##       f ##   ##f        ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##n        ##   ##       n ##
#############################
#############################
##                         ##
##              f          ##
##n                      n ##
#############################
#############################
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
##         ##   ##         ##
#############   #############
"""   #|#    #|#    #|#   """

    winds = """
>>            ^            <<
>>>>>>>>>>>>> ^ <<<<<<<<<<<<<
>>^           ^           ^<<
>>^           ^           ^<<
>>^           ^           ^<<
>>^           ^           ^<<
>>^           ^           ^<<
>>^           ^           ^<<
>>^           ^           ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^          xxx          ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
>>^                       ^<<
"""

class levelFinal(boarddef.Level):
    
    walls = """
#############   #############
##                         ##
##                         ##
##                         ##
##                         ##
##                         ##
####  #################  ####
##        ###   ###        ##
##         ##   ##         ##
#######     #####     #######
##                         ##
##                         ##
##                         ##
##                         ##
#########           #########
##                         ##
##                         ##
##                         ##
##########         ##########
##                         ##
##                         ##
##                         ##
##                         ##
#############   #############
"""   #|#    #|#    #|#   """
