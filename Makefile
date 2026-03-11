# ========== INIT SERVICE ==========
up:
	bentoml serve src.service:MyBentoML --port 3000

up-dev:
	bentoml serve src.service:MyBentoML --port 3000 --reload

# ========== LOGIN ==========
api-login-admin:
	curl -X 'POST' \
		'http://localhost:3000/login' \
		-H 'accept: application/json' \
		-H 'Content-Type: application/x-www-form-urlencoded' \
		-d 'username=admin&password=secret123'

api-login-user:
	curl -X 'POST' \
		'http://localhost:3000/login' \
		-H 'accept: application/json' \
		-H 'Content-Type: application/x-www-form-urlencoded' \
		-d 'username=user&password=passwd123'

# ========== TEST API ==========
api-predict:
	curl -X POST "http://localhost:3000/predict" \
		-H "Authorization: Bearer ${ACCESS_TOKEN}" \
		-d "gre_score=327&toefl_score=113&university_rating=4&sop=4.5&lor=4.5&cgpa=9.04&research=0"

test-api:
	uv run --group dev python3 -m pytest -svv tests/

# ==== TRAIN MODEL ====
train-model:
	uv run python3 src/train_model.py

# ==== DOCKER ====
docker-up:
	docker run --rm -p 3000:3000 my_bentoml:gnpqwrq5jwlvmfo4

docker-load-image:
	docker load -i docker/bentoml_stojcheski
