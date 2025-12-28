#============================================================================================================================#
#                                             ⚠️  before you run this code                                                   #
#                                                                                                                            #
# hey!                                                                                                                       #
# before u start, make sure of this:                                                                                         #
#                                                                                                                            #
# - you got connection to SQL db (ich-edit) for accounting users                                                             #
# - you got connection to mongo, needed for logging queries                                                                  #
# - you can reach sakila db (sql for reading movies etc)                                                                     #
# - in file QueryLogger.py line 19, dont forget to change path to last_query.txt (or it wont save last query)                #
#                                                                                                                            #
# ⚠️ WARNINGs:                                                                                                               #
# - if mongo or last_query.txt not setup – program still gonna work                                                          #
# - if sakila not availble – u can still run the program, but film search won't work                                         #
#                                                                                                                            #
# BUT❗                                                                                                                      #
# - if SQL ich-edit is not reachable – program will crash instantly                                                          #
#   since login depends on username & pass from that DB                                                                      #
#                                                                                                                            #
#   P.S. all those settings (DB logins, hosts, etc) are controlled in the .env file – so just check there if smth broken     #
#                                                                                                                            #
#   Good luck :)                                                                                                             #
#============================================================================================================================#


from functions import main

if __name__ == "__main__":
    main()





