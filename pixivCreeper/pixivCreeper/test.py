from django.http import HttpResponse
def test(request):
	return HttpResponse(
'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Test</title>
</head>
<body>
<FORM name=form method=get>
	<input type="input-field" placeholder="something here..." name="sh">
	<input type="submit" value=" 提交 " name="submnt"/>
</FORM>
</body>
</html>
''')