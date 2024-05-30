target: b f

b:
	cd backend && flask run --debug

f:
	cd frontend && npm run dev
