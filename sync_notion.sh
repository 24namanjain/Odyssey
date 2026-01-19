#!/bin/bash

# Notion Sync Script
# One-step script to sync markdown files from docs/ to Notion

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
cd "$PROJECT_ROOT"

echo -e "${GREEN}=== Notion Sync Script ===${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import notion_client" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r notion_sync/requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please create a .env file with:${NC}"
    echo "  NOTION_TOKEN=your_notion_token"
    echo "  NOTION_ROOT_PAGE_ID=your_root_page_id"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check required environment variables
if [ -z "$NOTION_TOKEN" ]; then
    echo -e "${RED}Error: NOTION_TOKEN not set in .env file${NC}"
    exit 1
fi

if [ -z "$NOTION_ROOT_PAGE_ID" ]; then
    echo -e "${YELLOW}Warning: NOTION_ROOT_PAGE_ID not set in .env file${NC}"
    echo -e "${YELLOW}You may need to provide it via --root-page-id argument${NC}"
fi

# Parse command line arguments
SYNC_DIR="${1:-docs}"
PULL_MODE=false
DRY_RUN=false
VERBOSE=false
ROOT_PAGE_ID=""

shift || true

# Parse additional arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --pull)
            PULL_MODE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --root-page-id)
            ROOT_PAGE_ID="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [DIRECTORY] [OPTIONS]"
            echo ""
            echo "Arguments:"
            echo "  DIRECTORY          Directory to sync (default: docs)"
            echo ""
            echo "Options:"
            echo "  --pull             Sync FROM Notion TO local files"
            echo "  --dry-run          Perform dry run without writing to Notion"
            echo "  --verbose          Enable verbose logging"
            echo "  --root-page-id ID  Override NOTION_ROOT_PAGE_ID from .env"
            echo "  --help, -h         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                          # Sync docs/ directory"
            echo "  $0 docs --dry-run           # Dry run sync"
            echo "  $0 docs --pull              # Pull from Notion to local"
            echo "  $0 docs --verbose           # Verbose output"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if sync directory exists
if [ ! -d "$SYNC_DIR" ]; then
    echo -e "${RED}Error: Directory '$SYNC_DIR' not found!${NC}"
    exit 1
fi

# Build command
CMD="python notion_sync/sync.py \"$SYNC_DIR\""

if [ "$PULL_MODE" = true ]; then
    CMD="$CMD --pull"
fi

if [ "$DRY_RUN" = true ]; then
    CMD="$CMD --dry-run"
fi

if [ "$VERBOSE" = true ]; then
    CMD="$CMD --verbose"
fi

if [ -n "$ROOT_PAGE_ID" ]; then
    CMD="$CMD --root-page-id \"$ROOT_PAGE_ID\""
fi

# Run sync
echo -e "${GREEN}Running sync for directory: $SYNC_DIR${NC}"
if [ "$PULL_MODE" = true ]; then
    echo -e "${YELLOW}Mode: PULL (Notion → Local)${NC}"
elif [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Mode: DRY RUN${NC}"
else
    echo -e "${YELLOW}Mode: PUSH (Local → Notion)${NC}"
fi
echo ""

eval $CMD

# Check exit status
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Sync completed successfully!${NC}"
else
    echo ""
    echo -e "${RED}✗ Sync failed with exit code: $EXIT_CODE${NC}"
    exit $EXIT_CODE
fi
