SRC:=app tests
PROJECT_NAME:=metrik

.PHONY:
	copy-config
	install-pre-commit
	run
	lint-flake8
	lint-pylint
	lint-black
	lint
	format-autoflake
	format-isort
	format-black
	format
	test
	check-no-test
	check
	clean-logs
	clean-cov
	clean
	link-edgedb-dc
	edgedb-repl
	create-migration
	apply-migration
	generate-scripts
	dc-server
	dc-edgedb
	dc-monitoring

copy-config:
	@echo "🔧 Coping configs from example.env ..."
	@cat ./config/example.env >> ./config/debug.env
	@cat ./config/example.env >> ./config/docker.env
	@cat ./config/example.env >> ./config/test.env

install-pre-commit:
	@echo "🔧 Installing pre-commit hooks ..."
	@pre-commit install

run:
	@echo "🚨 Running service ..."
	@poetry run python -m uvicorn app.asgi:create \
    	--factory \
    	--port 8080 \
    	--host 0.0.0.0 $(ARGS)

lint-flake8:
	@echo "🐍 Linting python source code with flake8 ..."
	@flake8 \
		--jobs 4 \
		--statistics \
		--show-source \
		$(SRC)

lint-pylint:
	@echo "🐍 Linting python source code with pylint ..."
	@pylint \
		--verbose \
		--jobs 4 \
		--rcfile=setup.cfg \
		$(SRC)

lint-black:
	@echo "🐍 Linting python source code with black ..."
	@black \
		--verbose \
		--target-version py310 \
		--skip-string-normalization \
		--check \
		$(SRC)

lint: lint-flake8 lint-pylint lint-flake8

format-isort:
	@echo "🐍 Formatting python source code with isort ..."
	@isort \
		--verbose \
		$(SRC)

format-autoflake:
	@echo "🐍 Formatting python source code with autoflake ..."
	@autoflake \
		--verbose \
		--recursive \
		--in-place \
		--remove-all-unused-imports \
		$(SRC)

format-black:
	@echo "🐍 Formatting python source code with black ..."
	@black \
		--verbose \
		--target-version py310 \
		--skip-string-normalization \
		$(SRC)

format: format-autoflake format-isort format-black

test:
	@echo "🧪 Running tests..."
	@python -m pytest \
		--verbosity=1 \
		--showlocals \
		--show-capture=no \
		--strict $(ARGS) \
		-k "$(k)" \
		--cov

check-no-test: format lint

check: format lint test

clean-logs:
	@echo "🧹 Cleaning /logs ..."
	@rm -f ./logs/*.log

clean-cov:
	@echo "🧹 Cleaning coverage ..."
	@rm .coverage

clean: clean-logs clean-cov

link-edgedb-dc:
	@echo "💿 Linking remote Docker instance of EdgeDB to current project ..."
	@edgedb instance link $(PROJECT_NAME) \
		--non-interactive \
		--trust-tls-cert \
		--dsn edgedb://localhost:5656

edgedb-repl:
	@echo "💿 Opening EdgeDB REPL..."
	@edgedb -I $(PROJECT_NAME)

create-migration:
	@echo "💿 Creating migration in database ..."
	@edgedb migration create -I $(PROJECT_NAME)

apply-migration:
	@echo "💿 Applying migration in database ..."
	@edgedb migration apply -I $(PROJECT_NAME)

generate-scripts:
	@echo "💿 Generating Python functions from EdgeQL query scripts..."
	@edgedb-py \
		-I $(PROJECT_NAME) \
		--target async \
		--file $(PWD)/scripts/__init__.py

dc-edgedb:
	@echo "🐳 Running EdgeDB in Docker ..."
	@docker-compose up edgedb $(ARGS) -d

dc-monitoring:
	@echo "🐳 Running monitoring tools in Docker ..."
	@docker-compose up \
		prometheus \
		grafana \
		$(ARGS) -d

dc-server:
	@echo "🐳 Running service in Docker ..."
	@docker-compose up server $(ARGS) -d
