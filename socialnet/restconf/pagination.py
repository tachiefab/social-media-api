from rest_framework import pagination


class TMStoreAPIPagination(pagination.PageNumberPagination):
	
   page_size   =  100

