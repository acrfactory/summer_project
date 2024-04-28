from typing import List, Union

from discord.ext import commands

from bot.common.user_custom import UserCustom
from bot.registration.category import Category


class Registration:
    def __init__(self, are_mutually_exclusive_events: bool = False):
        self.message = ""
        self.categories = {1: Category(number=1)}
        self.max_cat_num = 1
        self.are_mutually_exclusive_events = are_mutually_exclusive_events
        self.user_cat_dict = {}

    def category_new(self, name: str, number: int):
        if number < 0:
            number = self.max_cat_num + 1
            self.max_cat_num = number

        self.confirm_cat_exists(number, False)

        self.categories[number] = Category(number=number, name=name)

    def category_remove(self, number: int):
        self.confirm_cat_exists(number, True)
        if len(self.categories) == 1:
            raise commands.errors.UserInputError(
                'Unable to remove only one category left')
        if self.are_mutually_exclusive_events:
            # Clear out users from dict
            for user in self.categories[number]:
                self.user_cat_dict.pop(user)
        self.categories.pop(number)
        if number == self.max_cat_num:
            # Max removed find new max
            self.max_cat_num = max(self.categories.keys())

    def category_rename(self, number: int, new_name: str):
        self.confirm_cat_exists(number, True)
        self.categories[number].name = new_name

    def resolve_cat_number(self,
                           cat_number:
                           Union[int, str]) -> Union[int, List[int]]:
        """
        Resolves an input into a valid category number or list of category 
        numbers.
        - None: Only available category or an error
        - "all": If events are not mutually exclusive returns all category 
                numbers
        - single int: Returns the input
        :param cat_number: The value to be resolved
        :return: A valid category number or list of category numbers
        """
        if cat_number is None:
            if len(self.categories) == 1:
                assert self.max_cat_num in self.categories
                return self.max_cat_num
            else:
                raise commands.errors.UserInputError(
                    'Category number required when there is more than one '
                    'category')
        else:
            if isinstance(cat_number, str):
                if cat_number == 'all':
                    if self.are_mutually_exclusive_events:
                        raise commands.errors.UserInputError(
                            f'"all" only allowed if events are not mutually '
                            f'exclusive')
                    else:
                        return [x for x in self.categories.keys()]
                else:
                    raise commands.errors.UserInputError(
                        f'Expected a category NUMBER or "all" but got '
                        f'{cat_number}')
            else:
                # Only other expected type is an int
                assert isinstance(cat_number, int)
                return cat_number

    def register(self, user: UserCustom, cat_number: Union[int, str, None]):
        cat_number = self.resolve_cat_number(cat_number)
        if isinstance(cat_number, List):
            for x in cat_number:
                self.register(user, x)
            return  # Do nothing more already called
        self.confirm_cat_exists(cat_number, True)
        if self.are_mutually_exclusive_events:
            # Check if user is already registered
            if user in self.user_cat_dict:
                self.unregister(user, self.user_cat_dict[user])
            self.user_cat_dict[user] = cat_number
        self.categories[cat_number].add(user)

    def unregister(self, user: UserCustom, cat_number: Union[int, str, None]):
        cat_number = self.resolve_cat_number(cat_number)
        if isinstance(cat_number, List):
            for x in cat_number:
                self.unregister(user, x)
            return  # Do nothing more already called

        self.confirm_cat_exists(cat_number, True)
        self.categories[cat_number].remove(user)
        self.user_cat_dict.pop(user, "No Exception If Not Present")

    def set_msg(self, msg: str):
        self.message = msg

    def __str__(self):

        total_users = 0
        result = f'REGISTRATION (' \
                 f'{"" if self.are_mutually_exclusive_events else "NOT "}' \
                 f'MUTUALLY EXCLUSIVE)\n{self.message}\n\n'
        for key in self.categories.keys():
            total_users += len(self.categories[key])
            result += f'{self.categories[key]}\n'

        result += f'Total Number of Users: {total_users}'
        return result

    def confirm_cat_exists(self, number: int, should_exist: bool):
        """
        Checks if a category exists or not based on the number and raises a
        exception if the expectation is not met with a suitable error message
        :param number: The number of the category to find
        :param should_exist: if true category must exist or exception is
        raised else exception is raised if the category does not exist
        """
        if (number in self.categories) != should_exist:
            raise commands.errors.UserInputError(
                f'Category {number} '
                f'{"does not" if should_exist else "already"} exists')
