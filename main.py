from urllib.parse import parse_qs

def generate_cat(message, custom_message_provided=False):
    message_lines = message.split("\n")
    max_len = max(len(line) for line in message_lines)

    bubble_width = max_len + 4
    top_border = " " + "_" * bubble_width
    bottom_border = " " + "-" * bubble_width

    bubble_content_lines = []
    for line in message_lines:
        bubble_content_lines.append(f"< {line.ljust(max_len + 2)} >")

    bubble = "\n".join([top_border] + [bubble_content_lines] + [bottom_border])

    if custom_message_provided:
        cat_art = r"""
        /\_/\   /
       ( o.o ) <
        > ^ <  \
       /     \  \
      ( ( ( ) ) )
       \_)-(_/
        """
        pointer_line = "      \\"
    else: 
        cat_art = r"""
           __..--''``---....___   _..._    __
 /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
///_.-' _..--.'_    \                    `( ) ) // //
/ (_..-' // (< _     ;_..__               ; `' / ///
 / // // //  `-._,_)' // / ``--...____..-' /// / //
        """


        pointer_line = "                                     \\" 
    

    cleaned_cat_lines = []
    for line in cat_art.splitlines():
        if line.strip():
            first_char_idx = len(line) - len(line.lstrip())
            cleaned_cat_lines.append(line[first_char_idx])
        else:
            cleaned_cat_lines.append("")
    

    final_cat_art = "\n".join(cleaned_cat_lines)

    full_output = f"{bubble}\n{pointer_line}\n{final_cat_art}"

    return full_output
async def app(scope, receive, send):
    if scope['type'] == 'http':
        message_to_display = ""
        custom_message_provided = False

        if scope["method"] == "POST":
            body_bytes = b''
            async for message_part in receive:
                if message_part['type'] =='http.request':
                    body_bytes += message_part.get('body', b'')
                    if not message_part.get('more_body', False):
                        break

        if body_bytes:
            message_to_display = body_bytes.decode('utf-8')
            custom_message_provided = True
        else:
            message_to_display = "Meow!! Wagahai wa neko de aru!"
    
        reponse_body = generate_cat(message_to_display, custom_message_provided)

        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "header": [
                    [b"content-type", b"text/plain"],
                    [b"content-length", str(len(reponse_body)).encode("utf-8")],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": reponse_body.encode("utf-8"),
            }
        )
    else:
        pass
