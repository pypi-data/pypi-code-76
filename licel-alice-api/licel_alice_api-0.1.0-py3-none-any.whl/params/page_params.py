class PageParams:
    """
    List pagination parameters
    """

    page_number: int
    page_size: int

    def __init__(self, page_number: int, page_size: int = 10):
        """
        :param page_number: wanted page number starts from 1
        :param page_size: item count per page
        """
        self.page_number = page_number
        self.page_size = page_size

    def __str__(self) -> str:
        return f"{self.page_number},{self.page_size}"
