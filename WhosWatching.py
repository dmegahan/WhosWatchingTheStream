import requests

#trackedUsers are the people you're looking for
trackedUsers = ['Totalbiscuit', 'LIRIK', 'summit1g', 'kinetick42', 'AmazHS', 'Voket']
#stream is the stream chat to search in
stream = 'trumpsc'

def findUsersInChatters(chatters, users):
    for chatter in chatters:
        for user in users:
            if chatter.lower() == user.lower():
                #found the user, no need to keep searching
                print "Found: " + user
                continue

def main():
    CHATTERS_REQUEST = "http://tmi.twitch.tv/group/user/" + stream + "/chatters"

    #request chatters info
    try:
        responseChatters = requests.get(CHATTERS_REQUEST)
    except(requests.exceptions.ConnectionError):
        print "request failure: " + CHATTERS_REQUEST

    #get list of people currently in chat
    try:
        chattersObj = responseChatters.json()
        allModerators = chattersObj['chatters']['moderators']
        allStaff = chattersObj['chatters']['staff']
        allAdmins = chattersObj['chatters']['admins']
        allGlobalMods = chattersObj['chatters']['global_mods']
        allViewers = chattersObj['chatters']['viewers']
    except (TypeError, ValueError, KeyError):
        allViewers = []

    allChatters = allModerators + allStaff + allAdmins + allGlobalMods + allViewers

    findUsersInChatters(allChatters, trackedUsers)

main()



