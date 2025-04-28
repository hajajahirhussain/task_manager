from rest_framework.throttling import UserRateThrottle

class AdminRateThrottle(UserRateThrottle):
    scope = 'admin'
    
    # def get_cache_key(self, request, view):
    #     """
    #     Generates a separate cache key for admin users so they don’t share the user throttle.
    #     """
    #     if request.user.is_staff:
    #         self.scope = 'admin'
    #         print(f"Admin user detected. Applying throttle: {self.scope}")  
    #     else:
    #         self.scope = 'user'
    #         print(f"Normal user detected. Applying throttle: {self.scope}")  

    #     cache_key = super().get_cache_key(request, view)
    #     print(f"Generated cache key: {cache_key}")  # Debugging throttle application
    #     return cache_key
    
    # def allow_request(self, request, view):
    #     """Ensure admin users get the correct throttle rate."""
    #     if request.user.is_staff:  # If user is admin
    #         self.scope = 'admin'  # Apply admin rate
    #         print(f"Admin user detected. Applying throttle: {self.scope}")  
    #     else:
    #         self.scope = 'user'  # Apply normal user rate

    #     return super().allow_request(request, view)
    
    # def get_cache_key(self, request, view):
    #     if request.user.is_staff:
    #         self.scope = 'admin'
    #         print(f"Admin user detected. Applying throttle: {self.scope}")  
    #     else:
    #         # self.scope = 'user'
    #         # print(f"Non-admin user detected. Applying throttle: {self.scope}")  
    #         return None  # Disable this throttle for normal users

    #     cache_key = super().get_cache_key(request, view)
    #     print(f"Generated cache key: {cache_key}")  # Debugging throttle application
    #     return cache_key
    # scope = 'admin'  # Default scope for admins

    # def get_cache_key(self, request, view):
    #     if request.user.is_staff:  # Apply admin throttle only if user is admin
    #         self.scope = 'admin'
    #         print(f"Admin throttle applied: {self.scope}")  
    #         return super().get_cache_key(request, view)

    #     print(f"Normal user throttle applied: {self.scope}")  
    #     return None  # Disable this throttle for normal users (prevents conflict)
    