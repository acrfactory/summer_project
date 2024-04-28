from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List, Union

from bot.common.user_custom import UserCustom


@dataclass
class UserList:
    """
    Stores a list of users. Does not allow duplicates. Users stored in
    order added.
    """
    users: List[UserCustom] = field(default_factory=list)
    _str_disp: Union[str, None] = None

    def add(self, user: UserCustom):
        """
        Adds the user if there were not already there otherwise does nothing
        :param user: The user to be added
        """
        if user not in self.users:
            self.users.append(user)
            self._invalidate_calculated()

    def remove(self, user: UserCustom):
        """
        Removes the user passed (or does nothing if user does not exist)
        :param user: user to be removed
        """
        if user in self.users:
            self.users.remove(user)
            self._invalidate_calculated()

    def has_users(self):
        return len(self.users) > 0

    def _invalidate_calculated(self):
        self._str_disp = None

    def __str__(self):
        if self._str_disp is None:
            self._str_disp = self.get_str_rep()
        return self._str_disp

    def users_as_str(self, separator: str = ", "):
        result = ""
        for user in self.users:
            result += f'{user}{separator}'
        if result != "":
            # Crop of trailing separator
            result = result[:-len(separator)]

        return result

    def __len__(self):
        return len(self.users)

    @abstractmethod
    def get_str_rep(self):
        return f'{self.users_as_str()}'
