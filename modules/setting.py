from modules.config_creater import CreatingConfig


class Config(CreatingConfig):
    def __init__(self) -> None:
        super().__init__(path = 'configs/config.json')
        self.bot = self.Bot(config = self)
        self.text = self.Text(config = self)
    class Bot:
        def __init__(self, config : CreatingConfig) -> None:
            self.token = config.config_field(key = 'token', layer = 'bot', default = 'Здесь ваш токен бота')
            self.admin = config.config_field(key = 'admin', layer = 'bot', default = None)
            self.while_time = config.config_field(key = 'while_true', layer = 'bot', default = 1200)
    class Text:
        def __init__(self, config: CreatingConfig) -> None:
            self.welcome = config.config_field(key = 'welcome', layer = 'text', default = ' ')
            self.add_domen = config.config_field(key='add_domen', layer='text', default=' ')
            self.errorconection = config.config_field(key = 'errorconection', layer = 'text', default = ' ')
