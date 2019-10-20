
<footer>
	<div style="clear:both"></div>
	<p>Contact <a href="mailto:{{mail}}">{{name}}</a>. Powered by <a href="https://github.com/riotbib/ilil">ilil</a>. 
% if loggedIn:
	<a href="/add">Add</a>. <a href="/logout">Log out</a>.
% else:
	<a href="/login">Login</a>.
% end
	</p>
</footer>
</body>
</html>
