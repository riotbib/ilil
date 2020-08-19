% import os
% include('header.tpl', title=title, description=description, totalNumberOfPages=totalNumberOfPages)

<section>
% for filename in imagesPerPage:
%	include('single.tpl', filename=filename, parsedData=parsedData)
% end
</section>

% if totalNumberOfPages > 1:
<div style="clear:both"></div>
<nav> 
	<p class="pagination">
% for i in range(totalNumberOfPages):
% i = i + 1
%	if i == 1:
	<a href="/">{{i}}</a>
%	else:
	<a href="/page/{{i}}">{{i}}</a>
%	end
% end
	</p>
</nav>
% end

% include('footer.tpl', name=name, mail=mail, loggedIn=loggedIn)
