# Changelog

All notable changes to the Archivist public API are documented here.

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions.

---

## [2026-05-29] — Session detail wikilink parity for nested beats and moments

### Fixed

- **`with_links` on `GET /v1/sessions/{session_id}`** now strips wikilinks from nested beat `description` and moment `content` fields when `include_beats=true` or `include_moments=true`, matching the dedicated beats and moments endpoints. Previously only the session `summary` respected `with_links`; nested collections always returned raw `[[wikilinks]]` from the database.

---

## [2026-05-25] — Citations in non-streaming ask responses

### Added

- **`citations` array on `POST /v1/ask` non-streaming responses**: The response now includes a `citations` array containing references to the campaign data used to generate the answer. Each citation includes `citation_id`, `source_type`, `source_id`, `title`, `session_number`, and `excerpt`.
- **Updated `ask.py` example**: Non-streaming example now prints citations when present.

---

## [2026-05-22] — Transcript markdown format and session notes documentation

### Added

- **`format` query parameter on `GET /v1/sessions/{session_id}/transcript`**: Accepts `json` (default) or `markdown`. When `format=markdown`, the endpoint returns a plain-text markdown document (`Content-Type: text/markdown`) with metadata, statistics, and speaker-labeled utterances. This format is optimised for LLM agent consumption.

### Clarified

- **`notes` on game session responses**: The `notes` field is `null` for all session types except `rawNotes`. Raw-notes sessions (`type: "rawNotes"`) are a special case where users supply session notes directly instead of uploading audio or text. These sessions contain notes but do not have any transcript content.
- **Enum values in documentation**: All enum parameters now list exact accepted values instead of abbreviated examples. `session_type` accepts `discordVoice`, `rawNotes`, `txtUpload`, or `playByPost`. `character_type` accepts `PC` or `NPC`. Link `from_type` and `to_type` parameters list all valid entity types.

---

## [2026-05-20] — Beat and moment list/detail parity

### Changed

- **`GET /v1/beats` and `GET /v1/beats/{id}`** now return the same beat fields. List responses include `description`, `metadata`, `created_at`, `updated_at`, and `game_session_ids` (not only the previous summary subset).
- **`GET /v1/moments` and `GET /v1/moments/{id}`** now return the same moment fields. List responses include `categories` (and match detail for `image`, timestamps, etc.).
- **`with_links`** on beat and moment list endpoints now strips wikilinks from descriptions/content the same way as detail endpoints.

---

## [2026-05-20] — Compendium search and quest counts

### Fixed

- **`search` on compendium list endpoints** now filters results server-side for `GET /v1/locations`, `GET /v1/factions`, and `GET /v1/items` (the query parameter was documented in OpenAPI but previously ignored). Use `search` to find entities by name without paging through the full campaign.
- **`GET /v1/quests/{quest_id}`** now includes `objective_count` and `completed_objective_count`, matching quest list summaries and MCP client expectations.

### Added

- **`search` on `GET /v1/moments`** — filter moments by label when scoped by `campaign_id` or `session_id`.

---

## [2026-05-19] — API Reconciliation

A comprehensive cleanup of the public API surface to remove internal artifacts, standardize naming conventions, and fully hydrate summary endpoints.

### Breaking Changes

- **Removed fields from all entity responses**: `approved`, `discovered`, `pending`, `shadow_aliases`, `new_description`, `old_description`, `combined_description`, `context`, `match_info`, `speaker_id`, `dg_request_id`
- **Removed fields from campaign responses**: `can_manage`, `new`, `archived`, `archived_at`, `bot_active`, `flagged`, `indexed`, `players`, `keywords`, `kill_list`, `chat_tone`, `ai_image_gen`
- **Renamed `world_id` to `campaign_id`** in journal entry responses, journal folder responses, campaign stats responses, and transcript metadata
- **Campaign stats response**: `campaignId` (camelCase) renamed to `campaign_id` (snake_case); removed `admins` and `players` count fields
- **Archived campaigns** are now silently excluded from list endpoints and return 404 on detail

### Added

- `merge` field added to all compendium entity responses (characters, factions, locations, items)
- `aliases` field added to faction, location, and item summary responses
- `tcg_image` field added to all compendium entity summary responses
- `image` field added to moment and session summary responses
- `index`, `notes`, `pbp_start_msg_url`, `pbp_end_msg_url` added to session summary responses
- `backstory`, `character_aliases` added to character summary responses
- `created_at` and `updated_at` timestamps added to all summary responses (previously detail-only)
- `owner_id` field on campaign responses (replaces internal-only `ownerId`)
- Structured `SessionHandout` response schema for `GET /v1/sessions/{id}/handout` (previously untyped JSON)

### Changed

- Summary and detail endpoints now return the same fields for all entity properties (summaries are fully hydrated)
- The only distinction between list and detail for complex entities (quests, sessions) is nested sub-collections (objectives, moments, beats)
- `GET /v1/sessions/{id}/handout` now validates response through a Pydantic schema

### Naming Convention (standardized)

All foreign key references to campaigns now consistently use `campaign_id` in snake_case across:
- Compendium entities (characters, factions, locations, items, moments, beats)
- Game sessions
- Quests
- Journal entries (previously `world_id`)
- Journal folders (previously `world_id`)
- Campaign stats (previously `campaignId` camelCase)
- Transcript metadata (previously `world_id`)
- Entity links

Input schemas continue to accept both `campaign_id` and `world_id` for backward compatibility on request bodies.
