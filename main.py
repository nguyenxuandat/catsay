
# app.py
from urllib.parse import parse_qs

def generate_expressive_catsay(message, custom_message_provided=False):
    """
    Generates catsay ASCII art with an expressive cat (now featuring a grand default cat).
    """
    message_lines = message.split('\n')
    max_len = max(len(line) for line in message_lines)
    
    # Calculate bubble width based on message length
    bubble_width = max_len + 4 # +2 for '< >', +2 for extra space
    top_border = "  " + "_" * bubble_width
    bottom_border = "  " + "-" * bubble_width
    
    bubble_content_lines = []
    for line in message_lines:
        bubble_content_lines.append(f"< {line.ljust(max_len + 2)} >")

    bubble = "\n".join([top_border] + bubble_content_lines + [bottom_border])
    
    if custom_message_provided:
        # Attentive, standing cat for custom messages
        cat_art = r"""
        /\_/\   /
       ( o.o ) <
        > ^ <  \
       /     \  \
      ( ( ( ) ) )
       \_)-(_/
        """
        # Pointer for the attentive cat
        pointer_line = "      \\"
    else:
        # The new, grand default cat!
        cat_art = r"""
           __..--''``---....___   _..._    __
 /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
///_.-' _..--.'_    \                    `( ) ) // //
/ (_..-' // (< _     ;_..__               ; `' / ///
 / // // //  `-._,_)' // / ``--...____..-' /// / //
        """
        # Pointer for the grand cat - adjusted for its shape and position
        # This will require some visual fine-tuning. Let's aim for the head area.
        pointer_line = "                                     \\" # A long pointer to reach the head
    
    # Clean up leading spaces from the cat_art, preserving internal structure
    cleaned_cat_lines = []
    for line in cat_art.splitlines():
        if line.strip(): # Avoid adding empty lines from source string
            # Find the first non-whitespace character's index for consistent stripping
            first_char_idx = len(line) - len(line.lstrip())
            cleaned_cat_lines.append(line[first_char_idx:])
        else: # Preserve truly empty lines for vertical spacing in the art itself
            cleaned_cat_lines.append("")


    final_cat_art = "\n".join(cleaned_cat_lines)
    
    # Combine bubble, pointer, and cat art
    full_output = f"{bubble}\n{pointer_line}\n{final_cat_art}"

    return full_output

async def app(scope, receive, send):
    if scope["type"] == "http":
        message_to_display = ""
        custom_message_provided = False
        if scope["method"] == "POST":
            body_bytes = b''
            while True:
                message_part = await receive()
                if message_part['type'] == 'http.request':
                    body_bytes += message_part.get('body', b'')
                    if not message_part.get('more_body', False):
                        break
            if body_bytes:
                message_to_display = body_bytes.decode('utf-8')
                custom_message_provided = True
            else:
                message_to_display = "Meow!! Wagahai wa neko de aru! You just sent a POST request but it's blank!!"
        else:
            query_string = scope.get('query_string', b'').decode('utf-8')
            query_params = parse_qs(query_string)
            if 'message' in query_params:
                message_to_display = query_params.get('message', [""])[0]
                custom_message_provided = True
            else:
                message_to_display = "Meow!! Wagahai wa neko de aru! You just sent a GET request!?"
        response_body = generate_expressive_catsay(message_to_display, custom_message_provided)
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"text/plain"],
                    [b"content-length", str(len(response_body)).encode("utf-8")],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": response_body.encode("utf-8"),
            }
        )