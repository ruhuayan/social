from django.shortcuts import render, redirect
#from django.http import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Message, Invitation, SocialGroup, Membership
from datetime import datetime
from django.db.models import Q
# Create your views here.

@login_required(login_url='/account/login')
def profile(request):
    invites = Invitation.objects.filter(invite = request.user, responsed_at=None)
    messages = Message.objects.filter(toUser = request.user).order_by('-sent_at')
    return render(request, 'profile.html', {'invites': invites, 'msg': messages} )

@login_required(login_url='/account/login')
def group(request):
    sgroup = SocialGroup.objects.filter(creator = request.user).order_by('-created_at')
    memberships = Membership.objects.filter(member=request.user)
    return render(request, 'groups.html', {'sgroup': sgroup, 'memberships': memberships} )

@login_required(login_url='/account/login')
def add_group(request):
    msg = msgType = groupName = None
    if request.method == 'POST':
        groupName = request.POST['name']

        if SocialGroup.objects.filter(name=groupName).exists():
            msg = 'Social Group %s alread exits! '% groupName
            msgType = 0
        elif groupName=='':
            msg = "Group Name can't be null"
            msgType = 0
        elif ' ' in groupName:
            msg = "Group Name can't contain space"
            msgType = 0
        else:
            newgroup = SocialGroup(creator=request.user, name=groupName) #Group.objects.create(name = groupName)
            newgroup.save()                                              #request.user.groups.add(newgroup)
            msg = 'Social Group %s Created ! ' % groupName
            msgType = 1  # msgType - 1 (created successful)

    return render(request, 'add_group.html', {'msg': msg, 'msgType': msgType, 'groupName': groupName})

@login_required(login_url='/account/login')
def add_group_user(request, groupName = None):

    if request.method == 'POST':
        users = request.POST.getlist('user')
        groupName = request.POST['groupName']
        sgroup = get_object_or_404(SocialGroup, name=groupName)
        if request.user != sgroup.creator:
            msg = 'You dont have the permission'
        else:
            msg = ""
            ul=User.objects.filter(username__in = users)
            for u in ul:
                #to make sure user isnot already in and not already sent
                if not Membership.objects.filter(sgroup=sgroup, member= u).count(): # = Invitation.objects.get(sgroup, u).response='accept'
                    if not Invitation.objects.filter(socialgroup=sgroup, invite=u, response='').count() :
                        invite = Invitation(invite=u, socialgroup= sgroup)
                        invite.save()
                        msg = msg + 'Invitation sent to users'
                else:
                    msg  = msg + '%s already in the group or is invited <br />' % u

    else:
        sgroup = get_object_or_404(SocialGroup, name=groupName)
        invitations = Invitation.objects.filter(socialgroup=sgroup).exclude(response="reject")
        invitedList = []
        for invitation in invitations:
            invitedList.append(invitation.invite)
        users = User.objects.exclude(id=request.user.id).exclude(id__in=sgroup.members.all()).exclude(username__in = invitedList)
        # to exclude members already in or already invited

        return render(request, 'add_group_user.html', {'groupName': groupName, 'users': users})
    return render(request, 'add_group_user.html', {'groupName': groupName, 'msg': msg})

@login_required(login_url='/account/login')
def confirm_invite(request, invite_id, accept=None):
    msg='Error occured at accept %d' % int(accept)
    invite = get_object_or_404(Invitation, id=invite_id)
    sgroup = get_object_or_404(SocialGroup, name=invite.socialgroup)
    if int(accept)==1:
        invite.response = "accept"
        invite.responsed_at = datetime.now()
        invite.save()
        Membership.objects.create(sgroup=sgroup, member=invite.invite)
        msg = "Invite accepted msg sent"
    elif int(accept)==0:
        invite.response = "reject"
        invite.responsed_at = datetime.now()
        invite.save()
        msg='Invite rejected msg sent'
    return render(request, 'confirm_group.html', {'msg': msg})

@login_required(login_url='/account/login')
def edit_group(request, groupName = None):
    msg = ''
    sgroup = get_object_or_404(SocialGroup, name=groupName)
    members = sgroup.members.all()
    if not sgroup.creator == request.user:
        msg = " You do not have the permission to edit the group"
    elif request.method == 'POST':
        title = 'Group %s message' %groupName
        message = Message.objects.create(user=request.user, title=title, content=request.POST['content'])
        users = request.POST.getlist('members')
        ul = User.objects.filter(username__in=users)
        message.toUser.add(*ul)
        msg = "message sent"
    return render(request, 'edit_group.html', {'msg': msg, 'members': members, 'groupName': groupName})

@login_required(login_url='/account/login')
def delete_group(request, groupName = None):
    sgroup = get_object_or_404(SocialGroup, name=groupName)

    if not sgroup.creator == request.user:
        msg = " You do not have the permission to edit the group"
        render(request, 'delete_group.html', {'msg': msg})
    else:
        sgroup.delete()
        msg = "Group '%s' deleted" % groupName
        return redirect('/social/group')

@login_required(login_url='/account/login')
def member_group(request, groupName=None):
    sgroup = get_object_or_404(SocialGroup, name=groupName)
    if not Membership.objects.filter(sgroup=sgroup, member=request.user).count():
        msg = 'You dont have permission to view the page'
        return render(request, 'membership_group.html', {'msg': msg})
    return render(request, 'membership_group.html', {'group': sgroup})

@login_required(login_url='/account/login')
def message(request, mid=None):
    if mid:
        msg = Message.objects.get(id=mid)
        users = User.objects.filter(id__in=msg.toUser.all())
    else:
        msgs = Message.objects.filter(Q(toUser=request.user) | Q(user = request.user)).order_by('-sent_at')
        return render(request, 'message.html', {'msgs': msgs})
    return render(request, 'message.html', {'msg': msg, 'users':users})

@login_required(login_url='/account/login')
def group_chat(request, label=None):
    sgroup = get_object_or_404(SocialGroup, name=label)
    if not Membership.objects.filter(sgroup=sgroup, member=request.user).count() and sgroup.creator != request.user:
        msg = 'You dont have permission to view the page'
        return render(request, 'membership_group.html', {'msg': msg})
    chats = reversed(sgroup.chats.order_by('-timestamp')[:50])
    members = User.objects.filter(id__in=sgroup.members.all() )
    return render(request, 'group_chat.html', {'sgroup': sgroup, 'chats': chats, 'creator': sgroup.creator, 'members': members})

