Working Environment: 

Framework: Python Django 1.9
OS: Ubuntu 16.04  ( Linux )
Database: MySql

1 Configuration (settings.py): 

There are a few things that I added in the settings.py file for the project to work: 

 INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Channels',               # for the chatting application to work and below I also added layers
    'Bootstrap3',              # 
    'Social.membership',    # application membership
    'Social.chat',                 # application chat
)
BOOTSTRAP3 = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',
}

redis_host = os.environ.get('REDIS_HOST', 'localhost')             # redis host
# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel$
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        "ROUTING": "social.chat.routing.channel_routing",
    },
}
# databases settings
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
	    'NAME': 'social',
	    'USER':'myproject',
	    'PASSWORD':'p@ssword',
	    'HOST':'localhost',
	    'PORT': '',
    }
}




2 Grouping Application
Requirements: 
Anyone can create a group and become the group owner;
      2)  Group owner can set the group name and description;
      3) Group owner should be able to choose “on my approval” for invitations send by the     members [invitations must be approved by owner before sending out];
     4) Anyone can invite others to the group by sending an invitation, and the invitation must be    approved by the owner if “on my approval” is chosen;
      5) An invited member must acknowledge the invitation to join the group

2.1 Django Registration: 
I used predefined package Django-Registration 2.2 to achieve the functionalities of user registration, login, logout, password reset, etc. For the installation of django-registration 2.2, refer to the web page https://django-registration.readthedocs.io/en/2.2/install.html

Please note that django-registration 2.2 does not work in Django 1.11

3. Chat Application
Requirements: 
1) Anyone can chat within a group
2) Can @mention someone

3.1 Django Channels
I used Django channels module to achieve real time messaging, passing SocialGroup name to window.location.path (client side javascript), and to retrieve SocialGroup name when websocket.connect, then create a chat room for the SocialGroup (in server side consumers.py).  

For the installation of Django channels, refer to web page http://channels.readthedocs.io/en/stable/index.html
