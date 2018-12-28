from guillotina import configure


app_settings = {
    # provide custom application settings here...
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('wiki.api')
    configure.scan('wiki.install')
    configure.scan('wiki.content')
