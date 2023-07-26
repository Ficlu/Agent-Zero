$(document).ready(function() {
    $('#signupForm').submit(function(e) {
        e.preventDefault();
        $.post('/sign-up', {
            email: $('#signup-email').val(),
            password: $('#signup-password').val()
        }).done(function(data) {
            if (data.error) {
                // Handle error during sign-up.
                alert("Sign-up failed: " + data.message);
            } else {
                // Handle successful sign-up.
                alert("Sign-up successful. Please check your email to confirm your account.");
            }
        }).fail(function() {
            // Handle failed sign-up.
            alert("An error occurred. Please try again.");
        });
    });

    $('#signinForm').submit(function(e) {
        e.preventDefault();
        $.post('/sign-in', {
            email: $('#signin-email').val(),
            password: $('#signin-password').val()
        }).done(function(data) {
            if (data.error) {
                // Handle error during sign-in.
                alert("Sign-in failed: " + data.message);
            } else {
                // Handle successful sign-in.
                const idToken = data.data.IdToken;
                const payload = JSON.parse(atob(idToken.split('.')[1]));
                const userId = payload['sub'];
                
                // Store the userId in localStorage or some other suitable place
                localStorage.setItem("userId", userId);

                alert("Sign-in successful. Welcome!");
            }
        }).fail(function() {
            // Handle failed sign-in.
            alert("An error occurred. Please try again.");
        });
    });

    $('#signoutButton').click(function() {
        // Handle sign-out.
        localStorage.removeItem("userId");
        alert("You've successfully signed out.");
    });
});
