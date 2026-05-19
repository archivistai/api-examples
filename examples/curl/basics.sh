#!/usr/bin/env bash
# Archivist API — Common operations as cURL commands
#
# Usage:
#   export ARCHIVIST_API_KEY="your-key-here"
#   bash basics.sh

set -euo pipefail

API="https://api.myarchivist.ai"
KEY="${ARCHIVIST_API_KEY:?Set ARCHIVIST_API_KEY}"

echo "=== Health Check ==="
curl -s "$API/health" | jq .

echo -e "\n=== List Campaigns ==="
curl -s -H "x-api-key: $KEY" "$API/v1/campaigns?size=3" | jq .

echo -e "\n=== Get First Campaign ID ==="
CAMPAIGN_ID=$(curl -s -H "x-api-key: $KEY" "$API/v1/campaigns?size=1" | jq -r '.data[0].id')
echo "Campaign ID: $CAMPAIGN_ID"

echo -e "\n=== Campaign Stats ==="
curl -s -H "x-api-key: $KEY" "$API/v1/campaigns/$CAMPAIGN_ID/stats" | jq .

echo -e "\n=== List Characters ==="
curl -s -H "x-api-key: $KEY" "$API/v1/characters?campaign_id=$CAMPAIGN_ID&size=5" | jq '.data[] | {id, character_name, type}'

echo -e "\n=== List Sessions ==="
curl -s -H "x-api-key: $KEY" "$API/v1/sessions?campaign_id=$CAMPAIGN_ID&size=5" | jq '.data[] | {id, title, type, session_date}'

echo -e "\n=== List Beats ==="
curl -s -H "x-api-key: $KEY" "$API/v1/beats?campaign_id=$CAMPAIGN_ID&size=5" | jq '.data[] | {id, label, type, index}'

echo -e "\n=== List Moments ==="
curl -s -H "x-api-key: $KEY" "$API/v1/moments?campaign_id=$CAMPAIGN_ID&size=5" | jq '.data[] | {id, label, session_id}'

echo -e "\n=== List Quests ==="
curl -s -H "x-api-key: $KEY" "$API/v1/quests?campaign_id=$CAMPAIGN_ID&size=5" | jq '.data[] | {id, quest_name, status, quest_category}'

echo -e "\n=== List Entity Links ==="
curl -s -H "x-api-key: $KEY" "$API/v1/campaigns/$CAMPAIGN_ID/links?size=5" | jq '.data[] | {id, from_type, to_type, alias}'

echo -e "\n=== Ask a Question (non-streaming) ==="
curl -s -H "x-api-key: $KEY" -H "Content-Type: application/json" \
  -d "{\"campaign_id\": \"$CAMPAIGN_ID\", \"messages\": [{\"role\": \"user\", \"content\": \"Who are the main characters?\"}], \"stream\": false}" \
  "$API/v1/ask" | jq .answer
