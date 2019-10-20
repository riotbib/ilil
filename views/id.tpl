% import os, toml
% include('header.tpl', title=title, description=description)

% parsedData = toml.load("data.toml")
% parsedConfig = toml.load("config.toml")
% imageDescription = parsedData['data'][timeStamp]
% fileName = "{timeStamp}.jpg".format(timeStamp=timeStamp)
% if imageDescription:
	<p class="description"><span>{{imageDescription}}</span> {{timeStamp}}</p>
	<img src="/pictures/{{fileName}}" />
% else:
	<p class="description">{{timeStamp}}</p>
	<img src="/pictures/{{fileName}}" />
% end
	<br />	
% if parsedConfig['server']['enableDownload']:
	<p><a href="/originals/{{fileName}}" class="original">download</a></p>
% end

% include('footer.tpl', name=name, mail=mail, loggedIn=loggedIn)
