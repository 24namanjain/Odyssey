# Odyssey — root Makefile
# -----------------------
# Odyssey is a monorepo that links to separate repos via git submodules.
# Each submodule has its own commit history; Odyssey only stores a pointer
# to one commit per submodule.
#
# Typical solo workflow:
#   1. Edit code inside a submodule (e.g. languages/go)
#   2. make push-sub MODULE=languages/go MSG="your message"
#   3. Done — submodule and Odyssey pointer are both pushed
#
# After cloning on a new machine:
#   make init

.DEFAULT_GOAL := help
SHELL := /bin/bash

# Submodule paths — keep in sync with .gitmodules
SUBMODULES := languages/go languages/java cloud/aws cloud/goK8sBible DataLabs

.PHONY: help init sync pull status sub-status sub-pull push push-sub go-run java-build

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

help: ## Show available commands
	@echo "Odyssey Makefile"
	@echo ""
	@echo "Submodule workflow:"
	@echo "  make init                              Clone/checkout all submodules"
	@echo "  make sync                              Pull Odyssey + sync submodules"
	@echo "  make status                            Show Odyssey + submodule status"
	@echo "  make sub-pull                          Pull latest main in all submodules"
	@echo "  make push-sub MODULE=<path> MSG=\"...\"  Commit submodule, push, update Odyssey"
	@echo "  make push                              Push submodules (if ahead), then Odyssey"
	@echo ""
	@echo "Quick dev:"
	@echo "  make go-run                            Run languages/go"
	@echo "  make java-build                        Build languages/java with Gradle"
	@echo ""
	@echo "Submodules: $(SUBMODULES)"

# ---------------------------------------------------------------------------
# Submodule setup & sync
# ---------------------------------------------------------------------------

init: ## First-time setup: init and checkout all submodules
	git submodule update --init --recursive

sync: ## Pull Odyssey and sync every submodule to its pinned commit
	git pull --recurse-submodules
	git submodule update --init --recursive

pull: sync ## Alias for sync

sub-pull: ## Pull latest main inside every submodule (does not update Odyssey pointers)
	@for module in $(SUBMODULES); do \
		echo ">>> Pulling $$module"; \
		git -C $$module checkout main && git -C $$module pull; \
	done

# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

status: ## Show Odyssey branch status and each submodule commit
	@echo "=== Odyssey ==="
	@git status -sb
	@echo ""
	@echo "=== Submodules ==="
	@git submodule status
	@echo ""
	@echo "Legend: + = submodule commit differs from Odyssey pointer"

sub-status: status ## Alias for status

# ---------------------------------------------------------------------------
# Push helpers
# ---------------------------------------------------------------------------

push: ## Push submodules that are ahead, update pointers, then push Odyssey
	@for module in $(SUBMODULES); do \
		if [ -n "$$(git -C $$module rev-list --count @{u}..HEAD 2>/dev/null)" ] && \
		   [ "$$(git -C $$module rev-list --count @{u}..HEAD 2>/dev/null)" -gt 0 ]; then \
			echo ">>> Pushing $$module"; \
			git -C $$module push; \
		fi; \
	done
	@git add $(SUBMODULES)
	@if ! git diff --cached --quiet; then \
		git commit -m "Update submodule pointers"; \
	fi
	@git push

# Commit inside a submodule, push it, then update and push Odyssey's pointer.
# Example: make push-sub MODULE=languages/go MSG="Add variables lesson"
push-sub:
ifndef MODULE
	$(error MODULE is required. Example: make push-sub MODULE=languages/go MSG="Add variables lesson")
endif
ifndef MSG
	$(error MSG is required. Example: make push-sub MODULE=languages/go MSG="Add variables lesson")
endif
	@if [ ! -d "$(MODULE)/.git" ] && [ ! -f "$(MODULE)/.git" ]; then \
		echo "Error: $(MODULE) is not a submodule path."; exit 1; \
	fi
	@echo ">>> $(MODULE): commit (if needed) and push"
	@if [ -n "$$(git -C $(MODULE) status --porcelain)" ]; then \
		git -C $(MODULE) add -A && \
		git -C $(MODULE) commit -m "$(MSG)"; \
	else \
		echo "    No local changes to commit in $(MODULE)"; \
	fi
	@git -C $(MODULE) push
	@echo ">>> Odyssey: update submodule pointer and push"
	@git add $(MODULE)
	@if git diff --cached --quiet; then \
		echo "    Odyssey pointer already up to date"; \
	else \
		git commit -m "Update $(MODULE) submodule"; \
	fi
	@git push

# ---------------------------------------------------------------------------
# Quick dev shortcuts
# ---------------------------------------------------------------------------

go-run: ## Run the Go hello-world program
	cd languages/go && go run main.go

java-build: ## Compile the Java project
	cd languages/java && ./gradlew build
