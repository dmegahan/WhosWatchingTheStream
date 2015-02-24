import requests

#trackedUsers are the people you're looking for
trackedUsers = ['Totalbiscuit', 'LIRIK', 'summit1g', 'kinetick42', 'AmazHS', 'Voket']
#stream is the stream chat to search in
stream = 'summit1g'

#will read the twitch users followed streamers and track them instead
def trackFollowed(twitchUsername):

    #API only shows the first 25 followed streams by default
    #defaults: offset = 0, limit = 25
    #https://github.com/justintv/Twitch-API/blob/master/v3_resources/follows.md#get-usersuserfollowschannels
    offset = "0"
    limit = "100"

    FOLLOWING_REQUEST = "https://api.twitch.tv/kraken/users/" + twitchUsername + "/follows/channels?&limit=" + limit + "&offset=" + offset
    try:
       responseFollowing = requests.get(FOLLOWING_REQUEST)
    except(requests.exceptions.ConnectionError):
        print "request failure: " + FOLLOWING_REQUEST

    try:
        followingObj = responseFollowing.json()
        followedStreams = followingObj['follows']
    except (TypeError, ValueError, KeyError):
        print "Error occured."
        followedStreams = []

    trackedUsers = []
    for stream in followedStreams:
        trackedUsers = trackedUsers + [stream['channel']['name']]

    return trackedUsers

def findUsersInChatters(chatters, users):
    for chatter in chatters:
        for user in users:
            if chatter.lower() == user.lower():
                #found the user, no need to keep searching
                print "Found: " + user
                continue

def main():
    #comment out if you want to track a manually input list of users
    trackedUsers = trackFollowed('kinetick42')
    CHATTERS_REQUEST = "http://tmi.twitch.tv/group/user/" + stream + "/chatters"

    #request chatters info
    try:
        responseChatters = requests.get(CHATTERS_REQUEST)
    except(requests.exceptions.ConnectionError):
        print "request failure: " + CHATTERS_REQUEST

    #get list of people currently in chat
    try:
        chattersObj = responseChatters.json()
        moderators = chattersObj['chatters']['moderators']
        staff = chattersObj['chatters']['staff']
        admins = chattersObj['chatters']['admins']
        globalMods = chattersObj['chatters']['global_mods']
        viewers = chattersObj['chatters']['viewers']
    except (TypeError, ValueError, KeyError):
        viewers = []

    allChatters = moderators + staff + admins + globalMods + viewers

    findUsersInChatters(allChatters, trackedUsers)

main()



