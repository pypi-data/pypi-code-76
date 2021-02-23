L_EMPH  = "\033[1m"
L_RESET = "\033[0m"
C_INFO 	= "\x1b[1;32m"
C_DEBUG = "\x1b[1;34m"
C_ERROR	= "\x1b[1;31m"
C_WARN	= "\x1b[1;33m"
C_TRACE	= "\x1b[37m"
C_TODO	= "\x1b[1;96m"

print("{}##############################################################################{}".format(C_ERROR, L_RESET))
print("")
print("{}  Dear user,{}".format(C_TRACE, L_RESET))
print("")
print("{}  you tried to install NEC SOL from a public repository! Please check that{}".format(C_TRACE, L_RESET))
print("{}  you have correctly set your --extra-index-url! If this error persists,{}".format(C_TRACE, L_RESET))
print("{}  please contact the SOL helpdesk for assistance.{}".format(C_TRACE, L_RESET))
print("")
print("{}##############################################################################{}".format(C_ERROR, L_RESET))

exit(1)