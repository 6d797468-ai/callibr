PYTHONPATH := apps/api/src:packages/kernel/src:packages/contracts/src:packages/persistence/src:packages/shared/src:packages/telemetry/src:packages/seed/src:platform/identity/src:engines/crm/src:engines/conversation/src:engines/evaluation/src:engines/persona/src:engines/procedure/src:engines/rule/src:engines/scenario/src:engines/simulation/src

.PHONY: api-dev frontend-dev test test-api lint build-frontend doctor verify repair score plan trend gate capabilities

api-dev:
	PYTHONPATH=$(PYTHONPATH) python3 -m uvicorn callibr_api.main:create_app --factory --reload --app-dir apps/api/src

frontend-dev:
	cd apps/frontend && npm run dev

test:
	python3 -m pytest

test-api:
	python3 -m pytest apps/api/tests

lint:
	python3 -m ruff check apps packages platform engines tests

build-frontend:
	cd apps/frontend && npm run build

doctor:
	python3 -m engineering doctor

verify:
	python3 -m engineering verify

repair:
	python3 -m engineering repair

score:
	python3 -m engineering score

plan:
	python3 -m engineering plan

trend:
	python3 -m engineering trend

gate:
	python3 -m engineering gate

capabilities:
	python3 -m engineering capabilities
