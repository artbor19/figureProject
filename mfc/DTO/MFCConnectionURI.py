from dataclasses import dataclass


@dataclass
class MFCConnectionURI:
    baseURI: str = "https://myfigurecollection.net/?"
    tab: str = "calendar"
    rootId: str = "0"
    status: str = "-1"
    categoryId: str = "-1"  # Pre-painted = 1, Action/Dolls = 2
    domainId: str = "-1"
    noReleaseDate: str = "0"
    releaseTypeId: str = "0"
    ratingId: str = "0"
    isCastoff: str = "0"
    hasBootleg: str = "0"
    tagId: str = "0"
    noBarcode: str = "0"
    clubId: str = "0"
    isDraft: str = "0"
    year: str = "2024"
    month: str = "1"
    acc: str = "0"
    separator: str = "0"
    sort: str = "insert"
    output: str = "2"
    current: str = "categoryId"
    order: str = "desc"
    page: str = "1"
    _tb: str = "item"

    # region Getter methods
    def get_baseURI(self):
        return self.baseURI

    def get_tab(self):
        return self.tab

    def get_rootId(self):
        return self.rootId

    def get_status(self):
        return self.status

    def get_categoryId(self):
        return self.categoryId

    def get_domainId(self):
        return self.domainId

    def get_noReleaseDate(self):
        return self.noReleaseDate

    def get_releaseTypeId(self):
        return self.releaseTypeId

    def get_ratingId(self):
        return self.ratingId

    def get_isCastoff(self):
        return self.isCastoff

    def get_hasBootleg(self):
        return self.hasBootleg

    def get_tagId(self):
        return self.tagId

    def get_noBarcode(self):
        return self.noBarcode

    def get_clubId(self):
        return self.clubId

    def get_isDraft(self):
        return self.isDraft

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def get_acc(self):
        return self.acc

    def get_separator(self):
        return self.separator

    def get_sort(self):
        return self.sort

    def get_output(self):
        return self.output

    def get_current(self):
        return self.current

    def get_order(self):
        return self.order

    def get_page(self):
        return self.page

    def get_tb(self):
        return self._tb

    # endregion Getter methods

    # region Setter methods
    def set_baseURI(self, value):
        self.baseURI = value

    def set_tab(self, value):
        self.tab = value

    def set_rootId(self, value):
        self.rootId = value

    def set_status(self, value):
        self.status = value

    def set_categoryId(self, value):
        self.categoryId = value

    def set_domainId(self, value):
        self.domainId = value

    def set_noReleaseDate(self, value):
        self.noReleaseDate = value

    def set_releaseTypeId(self, value):
        self.releaseTypeId = value

    def set_ratingId(self, value):
        self.ratingId = value

    def set_isCastoff(self, value):
        self.isCastoff = value

    def set_hasBootleg(self, value):
        self.hasBootleg = value

    def set_tagId(self, value):
        self.tagId = value

    def set_noBarcode(self, value):
        self.noBarcode = value

    def set_clubId(self, value):
        self.clubId = value

    def set_isDraft(self, value):
        self.isDraft = value

    def set_year(self, value):
        self.year = value

    def set_month(self, value):
        self.month = value

    def set_acc(self, value):
        self.acc = value

    def set_separator(self, value):
        self.separator = value

    def set_sort(self, value):
        self.sort = value

    def set_output(self, value):
        self.output = value

    def set_current(self, value):
        self.current = value

    def set_order(self, value):
        self.order = value

    def set_page(self, value):
        self.page = value

    def set_tb(self, value):
        self._tb = value

    # endregion Setter methods

    def get_connection_url(self):
        return (
            f"{self.baseURI}"
            f"tab={self.tab}"
            f"&rootId={self.rootId}"
            f"&status={self.status}"
            f"&categoryId={self.categoryId}"
            f"&domainId={self.domainId}"
            f"&noReleaseDate={self.noReleaseDate}"
            f"&releaseTypeId={self.releaseTypeId}"
            f"&ratingId={self.ratingId}"
            f"&isCastoff={self.isCastoff}"
            f"&hasBootleg={self.hasBootleg}"
            f"&tagId={self.tagId}"
            f"&noBarcode={self.noBarcode}"
            f"&clubId={self.clubId}"
            f"&isDraft={self.isDraft}"
            f"&year={self.year}"
            f"&month={self.month}"
            f"&acc={self.acc}"
            f"&separator={self.separator}"
            f"&sort={self.sort}"
            f"&output={self.output}"
            f"&current={self.current}"
            f"&order={self.order}"
            f"&page={self.page}"
            f"&_tb={self._tb}"
        )
