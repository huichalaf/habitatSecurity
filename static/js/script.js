function aResidente(user, password){
	console.log("redireccionando a Residente");
	console.log(window.location.origin);
	window.location.assign(window.location.origin+"/residente/")
}
function aAdmin(user, password){
	console.log("redireccionando a Admin")
	console.log(window.location.origin);
	window.location.assign(window.location.origin+"/administrador/")
}

async function hashCadena(string) {
	const utf8 = new TextEncoder().encode(string);
	const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
	const hashArray = Array.from(new Uint8Array(hashBuffer));
	const hashHex = hashArray
		.map((bytes) => bytes.toString(16).padStart(2, '0'))
		.join('');
	console.log("hash: "+hashHex);
	return hashHex;
}

$(document).ready(function(){
	$("#nextButton").click(function(){
		var dataPreCrypted = document.getElementById("userPasswordForm");
		hashCadena(dataPreCrypted.password.value).then((hex) => dataPreCrypted.password.value = hex);
		//dataPreCrypted.password.value = hex; 
		console.log("enviando");
		setTimeout(() => {
			console.log(dataPreCrypted.password.value)
			var serializedData = $("#userPasswordForm").serialize();
			for (index = 0; index < serializedData.length; ++index) {
			    if (serializedData[index].name == "password") {
			        serializedData[index].value = dataPreCrypted.password.value;
			        break;
			    }
			}
			console.log(serializedData);
			$.ajax({
			url: $("userPasswordForm").data('url'),
			data: serializedData,
			dataType: 'json',
			type: 'post',
			success: function(data){
				console.log(data.user);
				console.log(data.token);
				console.log(data.result);
				if(data.result==2){
					aResidente(data.user, data.token);
				}
				if(data.result==1){
					aAdmin(data.user, data.token);
				}
				if(data.result==0){
					alert("Usuario no registrado");
				}
			}
		});}, 1000);
	});
});
