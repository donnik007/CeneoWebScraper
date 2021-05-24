
def extractComponent(domSubtree, selector, attribute=None):
    try:
        if attribute:
            return domSubtree.select(selector).pop(0)[attribute].strip()
        if attribute is None:
            return domSubtree.select(selector).pop(0).get_text().strip()
        return [item.get_text().strip() for item in domSubtree.select(selector)]
    except IndexError:
        return None