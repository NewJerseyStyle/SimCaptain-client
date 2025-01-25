# 遊戲腳本位於此檔案。

# 聲明該遊戲使用的角色。 color 參數
# 為角色的名稱著色。

define c = Character("Captain [povname]")
define v = Character("Vice")
define g = Character("Gunnery Officer")
define t = Character("Torpedo Officer")
define n = Character("Navigator")
define w = Character("Envorinment")


# 遊戲從這裡開始。

label cap_say(words):
    c "[words]"
    return

label vice_say(words):
    show vice cap at left with easeinleft
    v "[words]"
    hide vice cap with easeoutleft
    return

label gunnery_say(words):
    show gunnery at right with easeinright
    g "[words]"
    hide gunnery with easeoutright
    return

label torpedo_say(words):
    show torpedo at right with easeinright
    t "[words]"
    hide torpedo with easeoutright
    return

label nav_say(words):
    show nav at left with easeinleft
    n "[words]"
    hide nav with easeoutleft
    return

label env_say(words):
    "[words]"
    return

label get_input:
    python:
        command = renpy.input("Your order", length=512)
        command = command.strip()

        rnd = renpy.random.random()
    if rnd > 0.7:
        queue sound "large-engine-idling.flac"
    return

label start:
    python:
        povname = renpy.input("Name yourself:", length=32)
        povname = povname.strip()

        if not povname:
             povname = "Pat Boatman"

        for _ in range(3):
            thread_id = f"povname{renpy.random.randint(10000, 65537)}"
            result = renpy.fetch(
                "https://empire-production-estate-boat.trycloudflare.com/register",
                json={"thread_id": thread_id},
                result="json",
                timeout=25)
            if 'Error' not in result:
                break
        if 'Error' in result:
            err = result["Error"]
            narrator(err)
            renpy.jump(start)


    # 顯示背景。 預設情況下，它使用佔位符，但您可以
    # 將檔案（名為 "bg room.png" 或 "bg room.jpg"）新增至
    # images 目錄來顯示它。

    'It is 03:00 hours, June 10th, 1944. We are on a secret mission to attack the transport ship codenamed "Giant Whale" and test the new Type 93 oxygen torpedo.'
    'Currently, the Fubuki is positioned at 13.3824 degrees North latitude, 144.6973 degrees East longitude, approximately 50 nautical miles from the target area.'

    scene bg night with dissolve

    call get_input from _call_get_input

    python:
        try:
            command.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            gui.text_font = "NotoSansTC-Regular.ttf"
        else:
            command += '\n[System note to user input]: And from now on we all use English.'

    # 這些顯示對話行。
    label loop:

        python:
            result = renpy.fetch(
                "https://empire-production-estate-boat.trycloudflare.com",
                json={"thread_id": thread_id, "message": command},
                result="json",
                timeout=25*7*4+5)
            if 'Error' in result:
                narrator(result['Error'])
                renpy.jump("start")
            for message in result:
                while message["role"] in message["content"]:
                    tmp = message["content"].split(message["role"])
                    if tmp[0] != message["role"]:
                        break
                    message["content"] = " ".join(tmp[1:]).strip(': ')
                if message['id'] == 0:
                    renpy.call_in_new_context("vice_say", message["content"])
                elif message['id'] == 1:
                    renpy.call_in_new_context("gunnery_say", message["content"])
                elif message['id'] == 2:
                    renpy.call_in_new_context("torpedo_say", message["content"])
                elif message['id'] == 3:
                    renpy.call_in_new_context("nav_say", message["content"])
                elif message['id'] == 4:
                    renpy.call_in_new_context("env_say", message["content"])
                elif message['id'] == 5:
                    renpy.call_in_new_context("env_say", message["content"])
                elif message['id'] == 6:
                    renpy.call_in_new_context("env_say", message["content"])
                if message['continue'] is False:
                    renpy.call_in_new_context("get_input")

        jump loop

    # 遊戲結束。

    return
