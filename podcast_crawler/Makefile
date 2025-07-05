.PHONY: help install test lint format sort-imports clean run

help:
	@echo "Comandos disponibles:"
	@echo "  install       - Instalar dependencias y paquete en modo desarrollo"
	@echo "  test          - Ejecutar tests con pytest"
	@echo "  lint          - Ejecutar linting con ruff"
	@echo "  format        - Formatear código con ruff"
	@echo "  sort-imports  - Ordenar imports con ruff"
	@echo "  clean         - Limpiar archivos temporales"
	@echo "  run           - Ejecutar el crawler"
	@echo "  help          - Mostrar esta ayuda"

install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Instalación completada"

test:
	@echo "Ejecutando tests..."
	pytest tests/ -v
	@echo "✅ Tests completados"

lint:
	@echo "Ejecutando linting..."
	ruff check .
	@echo "✅ Linting completado"

format:
	@echo "Formateando código..."
	ruff format .
	@echo "✅ Formateo completado"

sort-imports:
	@echo "Ordenando imports..."
	ruff check --select I --fix .
	@echo "✅ Imports ordenados"

clean:
	@echo "Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpieza completada"

run:
	@echo "Ejecutando podcast crawler..."
	python -m app.crawler