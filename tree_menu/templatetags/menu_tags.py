from django import template
from django.urls import reverse, resolve, Resolver404
from django.utils.safestring import mark_safe
from ..models import Menu

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    except Menu.DoesNotExist:
        return ''

    request = context['request']
    current_url = request.path_info

    items = list(menu.items.all())

    menu_tree = build_menu_tree(items)

    active_item = None
    for item in items:
        if item.get_url() == current_url:
            active_item = item
            break

    expanded_items = set()

    if active_item:
        parent = active_item.parent
        while parent:
            expanded_items.add(parent.id)
            parent = parent.parent

        for child in items:
            if child.parent == active_item:
                expanded_items.add(child.id)

    rendered_menu = render_menu(menu_tree, expanded_items, active_item)

    return mark_safe(rendered_menu)

def build_menu_tree(items, parent=None):
    tree = []
    for item in items:
        if item.parent == parent:
            children = build_menu_tree(items, item)
            tree.append({
                'item': item,
                'children': children
            })
    return tree

def render_menu(tree, expanded_items, active_item, level=0):
    if not tree:
        return ''

    html = '<ul>'
    for node in tree:
        item = node['item']
        children = node['children']
        is_active = active_item and (item == active_item)
        has_children = len(children) > 0
        is_expanded = item.id in expanded_items or is_active

        html += '<li>'
        html += f'<a href="{item.get_url()}" class="{"active" if is_active else ""}">'
        html += item.title
        html += '</a>'

        if has_children and (level == 0 or is_expanded or (active_item and item == active_item.parent)):
            html += render_menu(children, expanded_items, active_item, level + 1)

        html += '</li>'

    html += '</ul>'
    return html