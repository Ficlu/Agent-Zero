$(document).ready(function(){
    var synth = window.speechSynthesis;
    var voices = [];
    var audio = new Audio('static/speech.mp3');

    // Fetch the list of available voices
    window.speechSynthesis.onvoiceschanged = function() {
        voices = window.speechSynthesis.getVoices();
    };
    loadAgentChatIndexes();  // Call the function when the document is ready.

    function loadAgentChatIndexes() {
        $.ajax({
            url: '/load_vars',
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                // Clear previous options
                $('#agent_id').empty();
                $('#chat_id').empty();
                console.log("what up");
                // Populate the agent dropdown
                for (let agent_id of data) {
                    console.log(agent_id);
                    $('#agent_id').append($('<option></option>').val(agent_id).html(agent_id));
                }
    
                // Set default agent and chat ID
                let defaultAgentId = $('#agent_id option:first').val();
                localStorage.setItem('agent_id', defaultAgentId);
                $('#agent_id').val(defaultAgentId);
    
                // Add event listener to agent dropdown
                $('#agent_id').on('change', function() {
                    let selectedAgentId = $(this).val();
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("Error: ", errorThrown);
            }
        });
    }
    
    var agent_name = ''
    var agent_id = localStorage.getItem('agent_id') || 'default_agent_id';
    var chat_id = localStorage.getItem('chat_id') || 'default_chat_id';

    // set form fields
    $('#agent_id').val(agent_id);
    $('#chat_id').val(chat_id);

    $('#configForm').on('submit', function(e) {
        e.preventDefault();
        agent_id = $('#agent_id').val();
        chat_id = $('#chat_id').val();
        localStorage.setItem('agent_id', agent_id);
        localStorage.setItem('chat_id', chat_id);
    });

    
    // Submit message from input
    $("#inputForm").on("submit", function(e){
        e.preventDefault();
        let userMessage = $("#userInput").val();
        processUserMessage(userMessage);
    });

    // Replay Audio button functionality
    $("#replayButton").on("click", function() {
        if (!$(this).hasClass("playing")) {
            $(this).addClass("playing");
            audio.play();
            audio.onended = () => $(this).removeClass("playing");
        } else {
            $(this).removeClass("playing");
            audio.pause();
            audio.currentTime = 0;
        }
    });
    
    // Prevent form submit when pressing 'Enter' unless 'Shift' is also pressed
    $("#userInput").on('keypress', function(e) {
        if(e.keyCode == 13 && !e.shiftKey) {
            e.preventDefault();
            $("#inputForm").submit();
        }
    });

    // Record button functionality
    let mediaRecorder;
    let recordedAudio;

    $("#recordButton").on("click", function() {
        if (!$(this).hasClass("recording")) {
            $(this).addClass("recording");
            startRecording();
        } else {
            $(this).removeClass("recording");
            stopRecording();
        }
    });

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        recordedAudio = [];

        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                recordedAudio.push(event.data);
            }
        };

        mediaRecorder.start();
    }

    async function stopRecording() {
        mediaRecorder.stop();

        const audioChunks = await new Promise((resolve) => {
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(recordedAudio, { type: 'audio/webm; codecs=opus' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                const play = () => audio.play();
                resolve({ audioBlob, audioUrl, play });
            };
        });

        // Log audioChunks for debugging
        console.log(audioChunks);

        // Send recorded audio to server to transcribe
        const formData = new FormData();
        formData.append('audio', audioChunks.audioBlob, "recorded_audio.webm");
        const response = await fetch('/speech-to-text', { method: 'POST', body: formData });
        const data = await response.json();

        // Log response and data for debugging
        console.log(response, data);

        // Check the transcription
        console.log(data.transcription);

        processUserMessage(data.transcription);
    }

    function processUserMessage(userMessage) {
        if (userMessage.trim() != '') {
            $("#chatbox").append("<p class='user-message'>You: " + userMessage + "</p>");
            $("#userInput").val("");

            let typingIndicator = $('<div id="typing" style="display: flex;"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>');
            
            // Wrap the code that appends the typing indicator in a setTimeout function
            setTimeout(() => {
                $("#chatbox").append(typingIndicator); // append a new typing indicator after the user's message
            }, 1800); // Set the delay time in milliseconds (0.6s = 600ms)
            
            $.ajax({
                url: "/process",
                method: "POST",
                data: {
                    message: userMessage,
                    agent_id: agent_id,
                    chat_id: chat_id,
                },
                success: function(data) {
                    console.log("data: " + data); // Add this line
                    typingIndicator.remove(); // remove the typing indicator here, when the response is received
                    if (data.images) {
                        data.images.forEach(function(image_url) {
                            $("#chatbox").append("<p class='mona-message'><img src='" + image_url + "' alt='Generated image' style='max-width: 100%;'></p>");
                        });
                    }
                    if (data.aname) {
                        agent_name = data.aname
                    }
                    // Add this check to handle the message and the speech file
                    if (data.message) {

                
                        var chatBubble = $("<p class='mona-message'>" + agent_name + ": " + data.message + "</p>");
                        $("#chatbox").append(chatBubble);
                
                        audio.src = data.speech_file + "?time=" + new Date().getTime();
                
                
                        audio.play();
                    }
                },
                
                dataType: "json"
            });
        }
    }

    $('#new_agent').on('click', function() {
        newAgentForm();
    });

    function newAgentForm() {
        // Clear the left panel
        $("#leftPanel").empty();

        // New Agent form
        var form = $('<form id="newAgentForm"></form>');
        form.append('<label for="agent_name">Agent Name:</label><br>');
        form.append('<input type="text" id="agent_name" name="agent_name" required><br>');
        form.append('<label for="agent_type">Agent Type:</label><br>');
        form.append('<select id="agent_type" name="agent_type" required><option value="Gf">Partner</option><option value="type2">Mentor</option></select><br>');
        form.append('<label for="agent_gender">Agent Gender:</label><br>');
        form.append('<input type="text" id="agent_gender" name="agent_gender" required><br>');
        form.append('<label for="agent_ethnicity">Agent Ethnicity:</label><br>');
        form.append('<input type="text" id="agent_ethnicity" name="agent_ethnicity" required><br>');
        form.append('<label for="agent_dob">Agent DOB:</label><br>');
        form.append('<input type="date" id="agent_dob" name="agent_dob" required><br>');
        form.append('<label for="agent_physical_characteristic">Agent Physical Characteristic:</label><br>');
        form.append('<input type="text" id="agent_physical_characteristic" name="agent_physical_characteristic" required><br>');
        form.append('<label for="agent_relationship">Agent Relationship:</label><br>');
        form.append('<input type="text" id="agent_relationship" name="agent_relationship" required><br>');
        form.append('<label for="agent_personality">Agent Personality (Myers-Briggs):</label><br>');
        form.append('<select id="personality_type" name="personality_type" required><option value="ISTJ">ISTJ</option><option value="ISFJ">ISFJ</option><option value="INFJ">INFJ</option><option value="INTJ">INTJ</option><option value="ISTP">ISTP</option><option value="ISFP">ISFP</option><option value="INFP">INFP</option><option value="INTP">INTP</option><option value="ESTP">ESTP</option><option value="ESFP">ESFP</option><option value="ENFP">ENFP</option><option value="ENTP">ENTP</option><option value="ESTJ">ESTJ</option><option value="ESFJ">ESFJ</option><option value="ENFJ">ENFJ</option><option value="ENTJ">ENTJ</option></select><br>');
        form.append('<label for="agent_IQ">Intelligence (IQ):</label><br>');
        form.append('<input type="text" id="agent_IQ" name="agent_IQ" required><br>');
        form.append('<label for="agent_EQ">Agent EQ:</label><br>');
        form.append('<input type="text" id="agent_EQ" name="agent_EQ" required><br>');
        form.append('<label for="agent_voice">Agent Voice:</label><br>');
        form.append('<select id="agent_voice" name="agent_voice" required><option value="Hala">Arabic, Gulf - Hala</option><option value="Hiujin">Cantonese - Hiujin</option><option value="Arlet">Catalan - Arlet</option><option value="Zhiyu">Chinese, Mandarin - Zhiyu</option><option value="Sofie">Danish - Sofie</option><option value="Laura">Dutch - Laura</option><option value="Lisa">Dutch, Belgian - Lisa</option><option value="Olivia">English, Australian - Olivia</option><option value="Emma">English, British - Emma</option><option value="Amy">English, British - Amy</option><option value="Kajal">English, Indian - Kajal</option><option value="Niamh">English, Irish - Niamh</option><option value="Aria">English, New Zealand - Aria</option><option value="Ayanda">English, South African - Ayanda</option><option value="Salli">English, US - Salli</option><option value="Kimberly">English, US - Kimberly</option><option value="Kendra">English, US - Kendra</option><option value="Joanna">English, US - Joanna</option><option value="Ivy">English, US - Ivy</option><option value="Ruth">English, US - Ruth</option><option value="Suvi">Finnish - Suvi</option><option value="Lea">French - Lea</option><option value="Gabrielle">French, Canadian - Gabrielle</option><option value="Vicki">German - Vicki</option><option value="Hannah">German, Austrian - Hannah</option><option value="Kajal">Hindi - Kajal</option><option value="Bianca">Italian - Bianca</option><option value="Kazuha">Japanese - Kazuha</option><option value="Tomoko">Japanese - Tomoko</option><option value="Seoyeon">Korean - Seoyeon</option><option value="Ida">Norwegian - Ida</option><option value="Ola">Polish - Ola</option><option value="Ines">Portuguese - Ines</option><option value="Vitoria">Portuguese, Brazilian - Vitoria</option><option value="Lucia">Spanish, Catalan - Lucia</option><option value="Mia">Spanish, Mexican - Mia</option><option value="Lupe">Spanish, US - Lupe</option><option value="Elin">Swedish - Elin</option></select><br>');
        
        form.append('<input type="submit" value="Create Agent"><br>');


        // Add the form to the left panel
        $("#leftPanel").append(form);

        // When the form is submitted
        $("#newAgentForm").on("submit", function(e){
            e.preventDefault();
            var newAgentData = getNewAgentFormInput();
            console.log(newAgentData);
        
            $.ajax({
                url: '/create_agent',
                method: 'POST',
                data: JSON.stringify(newAgentData),
                contentType: 'application/json',
                success: function(data) {
                    if (data.status === 'success') {
                     
                        alert('New agent created successfully.');
                        // save the new agent_id and chat_id to localStorage
              
                        localStorage.setItem('agent_id', data.agent_id);
                        localStorage.setItem('chat_id', 0);
                        // update agent_id and chat_id
                        agent_id = data.agent_id;
                        console.log("agent_id:", agent_id)
                        chat_id = 0;
                        $('#leftPanel').html(`
                            <form id="configForm">
                                <label for="agent_id">Agent ID: </label><br>
                                <select id="agent_id" name="agent_id" required>
                                    <!-- Options can be populated dynamically -->
                                </select><br>
                                <label for="chat_id">Chat ID: </label><br>
                                <input type="text" id="chat_id" name="chat_id" required><br>

                                <input type="submit" value="Load"><br>
                                <input type="button" value="New Agent" id="new_agent"><br>
                                <input type="button" value="New Chat" id="new_chat">
                            </form>
                        `);

                        loadAgentChatIndexes();  // Load the existing agent chat indexes.
                    } else {
                        console.log('Error: unexpected response status');
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("Error: ", errorThrown);
                }
            });
        });
        
    }

    function getNewAgentFormInput() {
        return {
            agent_name: $('#agent_name').val(),
            agent_type: $('#agent_type').val(),
            agent_gender: $('#agent_gender').val(),
            agent_ethnicity: $('#agent_ethnicity').val(),
            agent_dob: $('#agent_dob').val(),
            agent_physical_characteristic: $('#agent_physical_characteristic').val(),
            agent_relationship: $('#agent_relationship').val(),
            agent_personality: $('#personality_type').val(),
            agent_IQ: $('#agent_IQ').val(),
            agent_EQ: $('#agent_EQ').val(),
            agent_voice: $('#agent_voice').val()
        };
    }
    
    function getSignUpFormInput() {
        return {
            username: $('#username').val(),
            password: $('#password').val(),
            email: $('#email').val(),
            given_name: $('#given_name').val(),
            birthdate: $('#birthdate').val(),
        };
    }
    
    function getConfirmFormInput() {
        return {
            username: $('#username').val(),
            confirmCode: $('#confirmCode').val()
        };
    }
        function getSignInFormInput() {
        return {
            username: $('#username').val(),
            password: $('#password').val(),
        };
    }

    $("#signinForm").on("submit", async function(e){
        e.preventDefault();
        let signInData = getSignInFormInput();

        const response = await fetch('/sign-in', { 
            method: 'POST', 
            body: JSON.stringify(signInData),
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            window.location.href = "/index"; // redirect to index page
        } else {
            const error = await response.json();
            alert(error.message); // display the error message
        }
    });

    $("#signupForm").on("submit", async function(e){
        e.preventDefault();
        let signUpData = getSignUpFormInput();
    
        const response = await fetch('/sign-up', { 
            method: 'POST', 
            body: JSON.stringify(signUpData),
            headers: { 'Content-Type': 'application/json' }
        });
    
        if (response.ok) {
            alert("Sign up successful. Please enter the confirmation code sent to your email.");
        } else {
            const error = await response.json();
            alert(error.message); // display the error message
        }
    });
    
    $("#confirmForm").on("submit", async function(e){
        e.preventDefault();
        let confirmData = getConfirmFormInput();
    
        const response = await fetch('/confirm-sign-up', { 
            method: 'POST', 
            body: JSON.stringify(confirmData),
            headers: { 'Content-Type': 'application/json' }
        });
    
        if (response.ok) {
            window.location.href = "/index"; // redirect to index page
        } else {
            const error = await response.json();
            alert(error.message); // display the error message
        }
    });
    
    $(document).ready(function(){
        var isMenuOpen = false;
        $(".hamburger").click(function(){
            if (isMenuOpen) {
                $("h1").show();
                $("#menuContent a").remove();
                $("#menuContent").parent().parent().css({
                    "padding-bottom": "60px"
                })
            } else {
                $("h1").hide();
                var menuHtml = '<a href="#" id="profile">User Profile</a>' +
                               '<a href="#" id="logout">Logout</a>';
                $("#menuContent").append(menuHtml);
                $("#menuContent").parent().parent().css({
                    "padding-bottom": "34px"
                })
    
                // Add click event to the logout button
                $("#logout").click(logout);
    
                // Add click event to the profile button
                // Add click event to the profile button
                $("#profile").click(function(e) {
                    e.preventDefault();  // prevent the default action
                    window.location.href = "/profile"; // request the profile page from the server
                });

            }
            isMenuOpen = !isMenuOpen;
        });
    });
    
    function logout() {
        $.ajax({
            url: '/logout',
            method: 'GET',
            success: function() {
                window.location.href = "/"; // redirect to landing page after successful logout
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("Error: ", errorThrown);
            }
        });
    }
    
    
    
});