from typing import Union

import discord


class UserCustom:
    """
    Represents a discord User as a UserCustom.
    Uses the users discord ID. And this field is immutable to support
    hashing and equality checks.

    WARNING: Two users with different display names but the same ID are
    considered equal and ALL users with ID "None" are considered equal
    """

    def __init__(self, id_: Union[int, None], display: str, *,
                 is_dummy: bool = False):
        self._id = id_
        self.display = display
        self.is_dummy = is_dummy  # Indicates temp users for passing data

    @property
    def id(self):
        return self._id

    def __eq__(self, other):
        if isinstance(other, UserCustom):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):
        return hash(self.id)

    @property
    def mention(self):
        if self.id is None:
            raise Exception(
                f'Unable to mention user without ID saved. Display: {self}')
        return f'<@{self.id}>'

    def __str__(self):
        return f'{self.display}'

    @staticmethod
    def get_user_custom(user: discord.User):
        # TODO Add a converter to use this function to auto convert to user
        return UserCustom(user.id, user.display_name)
