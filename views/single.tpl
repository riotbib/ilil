% import toml
% timeStamp = filename.rsplit('.',1)[0]
% imageDescription = parsedData['data'][timeStamp]
% if imageDescription:
	<a href="/id/{{timeStamp}}" style="background-image: url('/thumbs/{{filename}}')"><span>{{imageDescription}}</span></a>
% else:
	<a href="/id/{{timeStamp}}" style="background-image: url('/thumbs/{{filename}}')"></a>
