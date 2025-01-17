from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.cache import cache_control

# Here view_func is a any general view. Any request by the user is 1st passed thru this middleware before going to the respective view.
# This middleware uses cache_control decorator of django which prevents browser to cache the html pages and prevents unauthorized and unathuenticated access.
# The parameters no_store,no_cache,must_revalidate values are used in order to do so.
class CacheControlMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func,args,kwargs):
        return cache_control(no_store=True,no_cache=True,must_revalidate=True)(view_func)(request,*args,**kwargs)