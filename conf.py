import logging
from datetime import timezone
from string import Template


class MasterPermissions:
    class PRIV:
        REGISTRATION = {'summer-proj'}
        SETTINGS = REGISTRATION  # Set to equal for now nothing more needed
        ALERT = SETTINGS
        TOP = SETTINGS

    class Channels:
        REGISTRATION = {'software'}
        ALERT = REGISTRATION
        TOP_ONLY = REGISTRATION
        TOP = TOP_ONLY.union(REGISTRATION).union(REGISTRATION)
        SETTINGS = TOP


class DBKeys:  # Database key values
    REGISTRATION = 'registration'
    ALERT = 'alert'


class Conf:
    BOT_DESCRIPTION = "LSat BOT"
    VERSION = '1.3.1'
    LOG_LEVEL = logging.INFO
    COMMAND_PREFIX = 'cb'  # CubeBot
    SAVE_CACHE_DELAY = 30  # Minimum number of seconds between saves
    EXPORT_FILE_NAME = 'export.yaml'
    EXPORT_DELAY = 15
    URL = 'https://summerproject.lassat.repl.co/'
    EMBED_COLOR = 0x373977

    class ENV:  # Environment variable names
        TOKEN = 'TOKEN_LASSAT'

    class TopLevel:
        class Permissions:
            ALLOWED_DM_COMMANDS = {  # Hard coded to allow for debugging
                'version',
                'ping',
            }
            ALLOWED_CHANNELS = MasterPermissions.Channels.TOP
            PRIV_ROLES = MasterPermissions.PRIV.TOP

        class Command:
            DM = {
                'name': 'dm',
                'help': 'Sends a DM to the user'}
            PING = {
                'name': 'ping',
                'help': 'Tests if the bot is alive. If alive bot responds '
                        'pong'}
            VERSION = {
                'name': 'version',
                'hidden': True}
            SAVE = {
                'name': 'save',
                'hidden': True}
            EXPORT = {
                'name': 'export',
                'hidden': True}

    class Settings:
        class Permissions:
            PRIV_ROLES = MasterPermissions.PRIV.SETTINGS
            ALLOWED_CHANNELS = MasterPermissions.Channels.SETTINGS

    class Registration:
        BASE_GROUP = {'name': 'r',
                      'help': 'Grouping for Registration List Commands',
                      'invoke_without_command': True}

        class Command:
            REGISTER = {
                'name': 'reg',
                'help': 'Registers you for the category specified (If only '
                        'one exists specification is not required)'}

            REGISTER_OTHER = {
                'name': 'reg_other',
                'help': 'Registers another user see help for self '
                        'registration for details on parameter'}

            UNREGISTER = {
                'name': 'unreg',
                'help': 'Unregisters user from category passed or "all" if '
                        'passed as parameter'}

            UNREGISTER_OTHER = {
                'name': 'unreg_other',
                'help': 'Unregisters another user from category passed or '
                        '"all" if passed as parameter'}

            CAT_NEW = {
                'name': 'cat_new',
                'help': 'Creates a new category'}

            CAT_REMOVE = {
                'name': 'cat_rem',
                'help': 'Removes a category'}

            CAT_RENAME = {
                'name': 'cat_rn',
                'help': 'Changes the description of a category'}

            DISPLAY = {
                'name': 'disp',
                'help': 'Shows the registered users'}

            RESET = {
                'name': 'reset',
                'help': 'Clears all data.'}

            SET_MESSAGE = {
                'name': 'msg',
                'help': 'Sets a general message that is displayed at the top.'}

        class Permissions:
            PRIV_ROLES = MasterPermissions.PRIV.REGISTRATION
            ALLOWED_CHANNELS = MasterPermissions.Channels.REGISTRATION

    class Alert:
        DEF_TZ = timezone.utc
        ALERT_MSG = Template(
            '<@&747938666667835393> "$event_name" starts at $next_time.\n'
            'This event is in $time_delta from now\n'
            '$final_notice')
        ALERT_CHANNEL_ID = 747915319149854890
        ALERT_POLL_INTERVAL = 60
        BASE_GROUP = {'name': 'a',
                      'help': 'Grouping for Alert Commands',
                      'invoke_without_command': True}

        class Command:
            CREATE = {
                'name': 'create',
                'help': 'Creates a new event'}

            REMOVE = {
                'name': 'rem',
                'help': 'Remove an event'}
            DISPLAY = {
                'name': 'disp',
                'help': 'Display currently configured events'}
            SET_LEAD = {
                'name': 'set_lead',
                'help': 'Sets the number of minutes before an event that the '
                        'notification is sent'}
            SET_TZ = {
                'name': 'set_tz',
                'help': 'Sets default timezone to be used by the bot if a '
                        'timezone for an event is not provided'}

        class Permissions:
            PRIV_ROLES = MasterPermissions.PRIV.ALERT
            ALLOWED_CHANNELS = MasterPermissions.Channels.ALERT
