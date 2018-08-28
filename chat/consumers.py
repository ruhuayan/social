from channels import Group
from channels.sessions import channel_session
from social.membership.models import SocialGroup
#import logging
import json
from collections import OrderedDict

#log = logging.getLogger(__name__)
class DefaultListOrderedDict(OrderedDict):
    def __missing__(self,k):
        self[k] = []
        return self[k]

dict = DefaultListOrderedDict()

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Work out room name from path (ignore slashes)
    #prefix, label = message['path'].decode('ascii').strip('/').split('/')

    room = message.content['path'].strip("/").split("/")[1]
    user = message.content['path'].strip("/").split("/")[2]
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)
    if user not in dict[room]:
        dict[room].append(user)
    print " in - %s" % dict[room]
    Group("chat-%s" % room).send({"text": json.dumps({'members_on': dict[room]})})

# Connected to websocket.receive
@channel_session
def ws_message(message):
    #log.info(message['text'])
    label = message.channel_session['room']
    sgroup = SocialGroup.objects.get(name=label)
    data = json.loads(message['text'])

    if data['message'] and data['message'] !='':
        m = sgroup.chats.create(handle=data['handle'], message=data['message'])
        Group("chat-%s" % label).send({
            "text": json.dumps(m.as_dict())
        })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    user = message.content['path'].strip("/").split("/")[2]
    dict[label].remove(user)
    Group("chat-%s" % label).send({"text": json.dumps({'members_on': dict[label]})})
    Group("chat-%s" % label).discard(message.reply_channel)
    print "left - %s" % dict[label]