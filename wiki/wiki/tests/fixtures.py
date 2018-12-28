from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import json
import pytest


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('wiki')
    else:
        settings['applications'] = ['wiki']


testing.configure_with(base_settings_configurator)


class wiki_Requester(ContainerRequesterAsyncContextManager):  # noqa

    async def __aenter__(self):
        await super().__aenter__()
        resp = await self.requester(
            'POST', '/db/guillotina/@addons',
            data=json.dumps({
                'id': 'wiki'
            })
        )
        return self.requester


@pytest.fixture(scope='function')
async def wiki_requester(guillotina):
    return wiki_Requester(guillotina)
