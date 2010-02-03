from django.conf import settings
from django.template import TemplateSyntaxError, VariableDoesNotExist, Node
from django.template import Library, Variable, loader, Context

register = Library()

class FlowPlayerNode(Node):
    "Renderer class for the flowplayer template tag."
    
    def __init__(self, video_url, player_url):
        """
        Constructor.

        Parameters:

            file_url
                Video url.
            player_url
                Flowplayer url.
        """
        self.player_url = player_url
        self.video_url = Variable(video_url)    

   
    def render(self, context):
    
        try:           
            video_url = self.video_url.resolve(context) 
        except VariableDoesNotExist:
            video_url = self.video_url       
              
        t = loader.get_template('videoplayer/flowplayer.html')
        code_context = Context(
                            {"player_url": self.player_url,
                             "video_url": video_url,
                            }, autoescape=context.autoescape)
        return t.render(code_context)

def do_flowplayer(parser, token):
    """
    This will insert an flash-based flv videoplayer (flowplayer) in form of an <object>
    code block.

    Usage::

        {% flowplayer video_url %}

    Example::
    
        {% flowplayer video.flv %}        
    
    By default, 'flowplayer' tag will use FlowPlayerLight.swf found at  
    ``{{ MEDIA_URL }}flowplayer/FlowPlayerLight.swf``.
    
    To change this, pass the flowplayer url as the keyword argument    
    
    Example::
        
        {% flowplayer video.flv /media/flowplayer/FlowPlayerDark.swf %}
    
    """    
   
   
    args = token.split_contents()
    
    if len(args) < 2:
        raise TemplateSyntaxError, "'flowplayer' tag requires at least one argument."            
    
    video_url = args[1]
    
    if len(args) == 3:
        player_url = args[2]
    else:
        player_url = "%sflowplayer/FlowPlayerLight.swf" % (settings.MEDIA_URL)
        
    return FlowPlayerNode(video_url, player_url)


# register the tag 
register.tag('flowplayer', do_flowplayer)

