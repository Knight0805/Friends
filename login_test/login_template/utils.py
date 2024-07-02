# filters.py
from rest_framework import filters
from django.db.models import Q, CharField
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import status

class MultiFieldSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        search_fields = getattr(view, 'search_fields', None)
        if search_fields:
            return search_fields
        return super().get_search_fields(view, request)

    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get(self.search_param, '').strip()
        if not search_param:
            return queryset

        search_fields = self.get_search_fields(view, request)
        queries = []

        for field_name in search_fields:
            queries.append(Q(**{f'{field_name}__icontains': search_param}))
            queries.append(Q(**{f'{field_name}__iexact': search_param}))
            queries.append(Q(**{f'{field_name}__istartswith': search_param}))
            queries.append(Q(**{f'{field_name}__iregex': search_param}))

            # Exclude '__search' lookup for SQLite
            if not isinstance(queryset.model._meta.get_field(field_name), CharField):
                queries.append(Q(**{f'{field_name}__search': search_param}))

        combined_query = queries.pop()
        for query in queries:
            combined_query |= query

        return queryset.filter(combined_query)
    


def custom_ratelimiter(request, *args, **kwargs):
    # Define your rate-limiting parameters
    allowed_requests_per_minute = 3
    user_id = request.user.id if request.user.is_authenticated else "anonymous"
    cache_key = f"custom_rate_limit:{user_id}"

    # Get the current count from the cache
    current_count = cache.get(cache_key, 0)

    # Increment the count
    current_count += 1
    
    # Check if the rate limit is exceeded
    if current_count > allowed_requests_per_minute:
        # Rate limit exceeded, reject the request
        print('echj')
        return Response({'detail': "Rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    # Rate limit not exceeded, allow the request
    # Set the cache key with an expiration time (e.g., 60 seconds)
    cache.set(cache_key, current_count, 60)
    return True
