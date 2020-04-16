from tethys_sdk.base import TethysAppBase, url_map_maker


class Vacationeer(TethysAppBase):
    """
    Tethys app class for Vacationeer.
    """

    name = 'Vacationeer'
    index = 'vacationeer:home'
    icon = 'vacationeer/images/icon.gif'
    package = 'vacationeer'
    root_url = 'vacationeer'
    color = '#2980b9'
    description = 'The purpose of this app is to help find the right vacation spots in Costa Rica that match your interests. The app will grow as the community adds new places to it.'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='vacationeer',
                controller='vacationeer.controllers.home'
            ),
            UrlMap(
                name='add_place',
                url='vacationeer/places/add',
                controller='vacationeer.controllers.add_place'
            ),
            UrlMap(
                name='places',
                url='vacationeer/places',
                controller='vacationeer.controllers.list_places'
            ),
        )

        return url_maps

    def custom_settings(self):
        """
        Example custom_settings method.
        """
        custom_settings = (
            CustomSetting(
                name='max_places',
                type=CustomSetting.TYPE_INTEGER,
                description='Maximum number of places that can be created in the app.',
                required=False
            ),
        )
        return custom_settings
