
def extractComponent(domSubtree, selector, attribute=None):
    try:
        if attribute:
            return domSubtree.select(selektor).pop(0)[attribute].strip()
        if attribute is None:
            return domSubtree.select(selektor).pop(0).get_text().strip()
        return [item.get_text().strip() for item in domSubtree.select(selektor)]
    except IndexError:
        return None