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
            self.admin_list = config.config_field(key = 'admin_list', layer = 'bot', default = [])
            self.while_time = config.config_field(key = 'while_true', layer = 'bot', default = 1200)
    class Text:
        def __init__(self, config: CreatingConfig) -> None:
            self.welcome = config.config_field(key = 'welcome', layer = 'text', default = ' ')
            self.add_domen = config.config_field(key='add_domen', layer='text', default=' ')
            self.remove_domen = config.config_field(key='remove_domen', layer='text', default=' ')
            self.errorconection = config.config_field(key = 'errorconection', layer = 'text', default = ' ')
            self.admin_menu = config.config_field(key='admin_menu', layer='text', default=' ')
    class Buttons:
        def __init__(self, config: CreatingConfig) -> None:
            self.add_admin = config.config_field(key = 'add_admin', layer = 'buttons', default = ' ')
            self.remove_admin = config.config_field(key='remove_admin', layer='buttons', default=' ')
            self.change_time = config.config_field(key='change_time', layer='buttons', default=' ')
            self.list_domens = config.config_field(key='list_domens', layer='buttons', default=' ')
            self.add_domen = config.config_field(key='add_domen', layer='buttons', default=' ')
            self.remove_domen = config.config_field(key='remove_domen', layer='buttons', default=' ')
            self.exit = config.config_field(key='exit', layer='buttons', default=' ')
