from channels.routing import ProtocolTypeRouter, URLRouter
import proteindata.routing
from channels.auth import AuthMiddlewareStack

# declaration of new version of application
application = ProtocolTypeRouter({ 
    # Requests sent to the proteindata application   
    'websocket': AuthMiddlewareStack(
        URLRouter(
            proteindata.routing.websocket_urlpatterns
        )
    ),
})