import structlog
from mwcleric import WikiggClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.page_modifier import PageModifierBase

LOG = structlog.get_logger()


class DataModifier(PageModifierBase):
    def update_plaintext(self, text: str) -> str:
        if self.current_page.name in self.data:
            LOG.info("Updating module data", page=self.current_page.name)
            return self.data[self.current_page.name]
        else:
            LOG.error(
                "No content for page",
                page=self.current_page.name,
                pages=self.data.keys(),
            )
            return text


def get_client() -> WikiggClient:
    # "user_file" is also used for env vars, confusingly
    credentials = AuthCredentials(user_file="BOT")
    site = WikiggClient(
        "bleakfaith", credentials=credentials, user_agent="BleakFaithBot/1.0"
    )
    return site


def get_modifier(data: dict[str, str]) -> DataModifier:
    site = get_client()
    return DataModifier(
        site, title_list=data.keys(), limit=len(data), summary="Data update", **data
    )
