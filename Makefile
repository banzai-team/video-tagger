build:
	docker compose build

up:
	docker compose up

restart:
	docker compose up -d

down:
	docker compose down

extract-texts:
	PYTHONPATH=ml python ml/scripts/extract_text_from_video.py --input_path=./notebooks/videos/ --texts_output_path=./notebooks/texts --max_minutes=1