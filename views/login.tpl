<!DOCTYPE html>
<html>
<head>
	<title>login &ndash; ilil</title>
	<link rel="stylesheet" href="/static/style.css"/>
	<meta name="viewport" content="width=device-width,initial-scale=1.0">
</head>
<body class="login">
<form action="/login" method="post" class="login">
	<label for="password">Enter password</label>
	<input name="password" type="password" id="password" />
	<input value="Login" type="submit" />
% if loginfailed:
	<p>Login failed</p>
% end
</form>
</body>
</html>
