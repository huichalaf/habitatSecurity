function sendData(){
	user = document.getElementById('user');
	key = document.getElementsByID('key');
	.ajax({
		url: '',
		type='POST',
		data = {'user': user, 'key': key}
		dataType = 'json'
	}).done({
		alert("correcto");
	})
}