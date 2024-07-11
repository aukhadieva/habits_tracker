from rest_framework import pagination


class HabitPaginator(pagination.PageNumberPagination):
    """
    Пагинатор для вывода списка привычек текущего пользователя.
    """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100
