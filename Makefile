target: 
	make -j 2 b f

z:
	make -j 2 b-pip f

b:
	cd backend && flask run --debug

b-pip:
	cd backend && pipenv shell & flask run --debug

f:
	cd frontend && npm run dev