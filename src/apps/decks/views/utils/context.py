def set_context_headings(context, main_h1):
    context["main_h1"] = main_h1
    context["head_title"] = f"{context["main_h1"]} - FlashMode"


def set_card_context_headings(context, prefix):
    set_context_headings(context, f"{prefix.title()} - Deck '{context["deck"].title}'")


def set_card_edit_context_headings(context, edit_type):
    set_card_context_headings(context, f"{edit_type.title()} Card")
