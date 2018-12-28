from guillotina import configure, schema, interfaces, content


class IWikiEntry(interfaces.IItem):
    Title = schema.Text()
    Body = schema.Text()


@configure.contenttype(
    type_name="WikiEntry",
    schema=IWikiEntry)
class WikiEntry(content.Item):
    pass
