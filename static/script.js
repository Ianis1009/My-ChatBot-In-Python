const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chat = document.getElementById("chat");
const sendButton = document.getElementById("send-button");


function addMessage(text, type) {

    const message = document.createElement("div");
    message.classList.add(

        "message",

        type + "-message"

    );

    const avatar = document.createElement("div");
    avatar.classList.add(

        "message-avatar"

    );

    if (type === "user") {

        avatar.textContent = "👤";

    }

    else {

        avatar.textContent = "🤖";

    }

    const content = document.createElement("div");

    content.classList.add(

        "message-content"

    );

    const header = document.createElement("div");
    header.classList.add(

        "message-header"

    );

    if (type === "user") {

        header.textContent = "You";

    } else {

        header.textContent = "Voice Assistant";

    }

    const messageText = document.createElement("div");

    messageText.classList.add(

        "message-text"

    );
    messageText.textContent = text;
    content.appendChild(header);


    content.appendChild(messageText);


    if (type === "user") {

        message.appendChild(content);

        message.appendChild(avatar);

    }

    else {

        message.appendChild(avatar);

        message.appendChild(content);

    }


    chat.appendChild(message);


    chat.scrollTop = chat.scrollHeight;


}


function showTyping() {


    const typing = document.createElement("div");


    typing.id = "typing";


    typing.classList.add(

        "message",

        "bot-message",

        "typing"

    );


    typing.textContent =

        "🤖 Assistant is thinking...";


    chat.appendChild(typing);


    chat.scrollTop = chat.scrollHeight;


}


function removeTyping() {


    const typing =

        document.getElementById("typing");


    if (typing) {

        typing.remove();

    }


}


form.addEventListener(

    "submit",

    async function(event) {


        event.preventDefault();


        const message =

            input.value.trim();


        if (message === "") {

            return;

        }


        addMessage(

            message,

            "user"

        );


        input.value = "";


        input.disabled = true;


        sendButton.disabled = true;


        showTyping();


        try {


            const response =

                await fetch(

                    "/chat",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":

                                "application/json"

                        },

                        body:

                            JSON.stringify({

                                message: message

                            })

                    }

                );


            const data = await response.json();
            removeTyping();
            addMessage(data.response,"bot");
            updateVoiceButton(data.voice_enabled); //switch icon mute/unmute

        }

        catch (error) {


            removeTyping();


            addMessage(

                "[ERROR]: Could not connect to the server.",

                "bot"

            );


        }

        finally {


            input.disabled = false;


            sendButton.disabled = false;


            input.focus();


        }


    }

);

/*DARK / LIGHT MODE*/

const themeToggle =

    document.getElementById(
        "theme-toggle"
    );


const themeIcon =

    document.getElementById(
        "theme-toggle-icon"
    );


const themeText =

    document.getElementById(
        "theme-toggle-text"
    );


function setTheme(theme) {


    if (theme === "light") {


        document.body.classList.add(

            "light-mode"

        );


        themeIcon.textContent =

            "🌙";


        themeText.textContent =

            "Dark";


        themeToggle.title =

            "Switch to dark mode";


        themeToggle.setAttribute(

            "aria-label",

            "Switch to dark mode"

        );


        themeToggle.setAttribute(

            "aria-pressed",

            "true"

        );


    }

    else {


        document.body.classList.remove(

            "light-mode"

        );


        themeIcon.textContent =

            "☀️";


        themeText.textContent =

            "Light";


        themeToggle.title =

            "Switch to light mode";


        themeToggle.setAttribute(

            "aria-label",

            "Switch to light mode"

        );


        themeToggle.setAttribute(

            "aria-pressed",

            "false"

        );


    }


    localStorage.setItem(

        "voice-assistant-theme",

        theme

    );


}

const savedTheme =

    localStorage.getItem(

        "voice-assistant-theme"

    );

if (savedTheme === "light") {


    setTheme("light");


}
themeToggle.addEventListener(

    "click",

    function() {


        const isLight =

            document.body.classList.contains(

                "light-mode"

            );


        if (isLight) {


            setTheme("dark");


        }

        else {


            setTheme("light");


        }


    }

);

const voiceToggle =

    document.getElementById(
        "voice-toggle"
    );


const voiceIcon =

    document.getElementById(
        "voice-toggle-icon"
    );


const voiceText =

    document.getElementById(
        "voice-toggle-text"
    );


//swap interfaces

function updateVoiceButton (enabled) {

    if (enabled) {
        voiceToggle.classList.remove("muted");
        voiceIcon.textContent = "🔊";
        voiceText.textContent = "Voice";
        voiceToggle.title = "Mute voice";
        voiceToggle.setAttribute("aria-label", "Mute voice");
        voiceToggle.setAttribute("aria-pressed", "false");
    }   else {

        voiceToggle.classList.add("muted");
        voiceIcon.textContent = "🔇";
        voiceText.textContent = "Muted";
        voiceToggle.title = "Enable voice";
        voiceToggle.setAttribute("aria-label", "Enable voice");
        voiceToggle.setAttribute("aria-passed", "true");
    }
}

async function loadVoiceState() {
    
    try {

        const response = await fetch("/api/voice");
        const data = await response.json();
        updateVoiceButton(data.voice_enabled);

    } catch(error) {

        console.error("Could not load voice state -->", error);
    }
}

loadVoiceState();

voiceToggle.addEventListener(

    "click",

    async function() {


        const isMuted =

            voiceToggle.classList.contains(

                "muted"

            );


        const newState =

            isMuted;


        try {


            const response = await fetch(

                "/api/voice",

                {

                    method:

                        "POST",


                    headers:

                        {

                            "Content-Type":

                            "application/json"

                        },


                    body:

                        JSON.stringify(

                            {

                                enabled:

                                newState

                            }

                        )

                }

            );


            const data =

                await response.json();


            updateVoiceButton(

                data.voice_enabled

            );


        }

        catch (error) {


            console.error(

                "Could not change voice:",

                error

            );


        }


    }

);