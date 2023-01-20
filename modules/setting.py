from modules.config_creater import CreatingConfig


class Config(CreatingConfig):
    def __init__(self) -> None:
        super().__init__(path = 'configs/config.json')
        self.bot = self.Bot(config = self)
        self.text = self.Text(config = self)
        self.buttons = self.Buttons(config = self)
    class Bot:
        def __init__(self, config : CreatingConfig) -> None:
            self.token = config.config_field(key = 'token', layer = 'bot', default = 'Здесь ваш токен бота')
            self.admin_list = config.config_field(key = 'admin_list', layer = 'bot', default = [{"user_id": 5689929885, "nickname": "Michail"}])
            self.while_time = config.config_field(key = 'while_true', layer = 'bot', default = [1200])
    class Text:
        def __init__(self, config: CreatingConfig) -> None:
            self.welcome = config.config_field(key = 'welcome', layer = 'text', default = ' ')
            self.add_domen = config.config_field(key='add_domen', layer='text', default=' ')
            self.remove_domen = config.config_field(key='remove_domen', layer='text', default=' ')
            self.errorconection = config.config_field(key = 'errorconection', layer = 'text', default = ' ')
            self.admin_menu = config.config_field(key='admin_menu', layer='text', default=' ')
            self.error_int = config.config_field(key='error_int', layer='text', default=' ')
            self.succesfully =  config.config_field(key='succesfully', layer='text', default=' ')
            self.error_sqlite = config.config_field(key = 'error_sqlite', layer = 'text', default = ' ')
            self.time_get = config.config_field(key = 'time_get', layer = 'text', default = ' ')
            self.time_count =  config.config_field(key = 'time_count', layer = 'text', default = ' ')
            self.add_admin =  config.config_field(key = 'add_admin', layer = 'text', default = ' ')
            self.error_admin = config.config_field(key='error_admin', layer='text', default=' ')
            self.remove_admin = config.config_field(key='remove_admin', layer='text', default=' ')
            self.not_finden = config.config_field(key='not_finden', layer='text', default=' ')
    class Buttons:
        def __init__(self, config: CreatingConfig) -> None:
            self.add_admin = config.config_field(key = 'add_admin', layer = 'buttons', default = ' ')
            self.remove_admin = config.config_field(key='remove_admin', layer='buttons', default=' ')
            self.change_time = config.config_field(key='change_time', layer='buttons', default=' ')
            self.list_domens = config.config_field(key='list_domens', layer='buttons', default=' ')
            self.add_domen = config.config_field(key='add_domen', layer='buttons', default=' ')
            self.remove_domen = config.config_field(key='remove_domen', layer='buttons', default=' ')
            self.exit = config.config_field(key='exit', layer='buttons', default=' ')
            self.return_back = config.config_field(key='return_back', layer='buttons', default=' ')
