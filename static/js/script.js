'use strict';
window.addEventListener('load', function() {
		document.getElementById('sign-out').onclick = function() {
		// ask firebase to sign out the user
		firebase.auth().signOut();
	}

	var uiConfig = {
		signInSuccessUrl: '/home',
		signInOptions: [firebase.auth.GoogleAuthProvider.PROVIDER_ID]
	}; // uiConfig

	firebase.auth().onAuthStateChanged(function(user) {
		if(user) { // If user is logged in...

			// hide the sign-out button and login-info
			document.getElementById('sign-out').hidden = false;
			// document.getElementById('login-info').hidden = false;

			// Print to the Console Logs
			// console.log('Signed in as ${user.displayName} (${user.email})');

			// Set the cookie as the token
			user.getIdToken().then(function(token) {
				document.cookie = "token=" + token;
			});
		}
		else
		{	// If user is not logged in...

			// reinitialise the firebase login authentication
			var ui = new firebaseui.auth.AuthUI(firebase.auth());
			ui.start('#firebase-auth-container', uiConfig);

			// Show the sign-out button and login-info
			document.getElementById('sign-out').hidden = true;
			document.getElementById('login-info').hidden = true;

			// Reset the cookie as the token to blank
			document.cookie = "token=";
		}
	}, function(error) {
		console.log(error);
		alert('Unable to log in: ' + error);
	});

}); // addEventListener