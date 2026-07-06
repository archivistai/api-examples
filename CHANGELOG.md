# Changelog

All notable changes to the Archivist public API are documented here.

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions.

---

## [2026-07-05] — Entity images API and MCP v2 write tools

### Added

- **`GET /v1/images/usage?campaign_id={id}`** — Returns the account's image quota for a campaign (`used`, `limit`, `can_access`, `tier`, billing cycle window). Requires campaign read access.
- **`POST /v1/images/generate`** — Server-side AI image generation for `character`, `faction`, `location`, `item`, or `world`. Returns a public URL; does not auto-attach to the entity. Consumes quota and requires campaign manage access.
- **`POST /v1/campaigns/{campaign_id}/images/init`** — Step 1 of direct upload: reserve an object key and receive a presigned PUT URL for the client to upload image bytes.
- **`POST /v1/campaigns/{campaign_id}/images/complete`** — Step 2 of direct upload: validate the uploaded object, run moderation, and optionally attach the image to an entity.
- **`DELETE /v1/campaigns/{campaign_id}/images`** — Detach and delete an entity image, or delete a managed object by URL.
- **MCP v2 write tools** — The Archivist MCP server now exposes create/update/delete tools for campaigns, beats, moments, compendium entities, quests, journals, journal folders, and entity links, plus session metadata updates (`patch_session`, `update_session` — not create/delete), and five image tools (`get_image_usage`, `generate_image`, `init_image_upload`, `complete_image_upload`, `delete_entity_image`). OAuth clients require the `agent_write` scope for mutating tools. See the [MCP tool reference](https://github.com/Archivist-AI/agent-examples/blob/main/docs/mcp-tool-reference.md) and [server README](https://github.com/Astrotomic/mcp.myarchivist.ai).

### Changed

- **Read tools with `with_links`** — MCP get/list tools for characters, factions, locations, items, beats, moments, sessions, and journals accept an optional `with_links` parameter. Pass `true` before editing text fields that contain `[[wikilink]]` markup.
- **Session create/delete restricted to product API** — `POST` and `DELETE /v1/sessions` now require a registered product OAuth client with `product_write`. Developer API keys and agent OAuth clients receive `403`. Developer and MCP clients may still read sessions and patch/update metadata (`PATCH`/`PUT /v1/sessions/{id}`).
- **MCP: removed `create_session`** — Session creation is not exposed as an MCP tool; use first-party product clients to create sessions.
- **Updated examples**: Added `images.py` demonstrating quota check, AI generation, and the two-step upload flow.

### Notes

- Image routes are available on the developer API surface (API keys and agent OAuth). Supported entity types for upload/attach: campaign, character, faction, location, item, moment, and session.
- Direct upload requires a client-side HTTP PUT to the presigned URL between `init` and `complete`; MCP agents that cannot make arbitrary PUTs should prefer `generate_image` or delegate the upload step.
- Additional read routes reserved for first-party product OAuth clients are not part of the developer API contract and are intentionally omitted from this changelog.

---

## [2026-06-09] — Remove legacy `/v1/worlds` routes

### Removed

- **`/v1/worlds`** — All legacy world routes were removed. Campaigns are the sole public API surface for the `World` table. Use **`POST /v1/campaigns`** to create campaigns and **`/v1/campaigns/{campaign_id}`** for all other campaign operations.

### Notes

- Request bodies may still accept `worldId` as an alias for `campaign_id` on some endpoints for backward compatibility.
- OAuth scope `worlds_read` is unchanged; it grants read access to campaigns, not a separate `/v1/worlds` route.

---

## [2026-06-09] — Session beat list modes and developer session writes

### Added

- **`GET /v1/beats?session_id={id}`** — Returns a paginated flat list of beats linked to the session (standard `{ data, total, page, size, pages }` envelope). Use `include_hierarchy=true` for the nested tree response instead.

### Fixed

- **Developer session writes** — `POST`, `PATCH`, `PUT`, and `DELETE /v1/sessions` remain available to campaign owners using API keys (developer view). Session create/update/delete were briefly gated to product OAuth only during staging; that restriction was removed. *(Superseded 2026-07-05: `POST` and `DELETE /v1/sessions` are product-only again; developer and MCP clients retain read plus `PATCH`/`PUT`.)*

### Changed

- **Updated examples**: `beats.py` and `basics.sh` now demonstrate both flat session beat lists and hierarchy mode.

---

## [2026-06-09] — Full-text search for compendium and journal lookups

### Changed

- **Compendium `search` parameters** (`GET /v1/characters`, `/factions`, `/locations`, `/items`, and `GET /v1/entities`) now use Postgres `searchVector` full-text search (aliases, player names, tags, and related indexed fields) with ILIKE fallback when FTS returns no matches.
- **`GET /v1/campaigns/{id}/search`** — Characters, factions, locations, items, and journals now use the same FTS strategy. Sessions and quests remain substring-based.

---

## [2026-06-08] — Beat hierarchy, unified entities list, moment filters, and card fieldsets

### Added

- **`GET /v1/beats?session_id={id}&include_hierarchy=true`** — Returns the session's beat tree as a nested JSON array. Each node includes a `children` array (not paginated). Use with `with_links=true` to preserve `[[wikilinks]]` in descriptions.
- **`GET /v1/entities`** — Unified compendium picker endpoint. Required query params: `campaign_id`, `type` (`characters`, `factions`, `locations`, or `items`). Optional: `search`, `page`, `limit` (max 100). Response envelope: `{ results, hasMore, page, pages, total }` where each result includes `id`, `name`, `type`, and `image`.
- **Entity and session filters on `GET /v1/moments`** — Filter by linked entities using comma-separated `character_ids`, `location_ids`, `faction_ids`, `item_ids`, and/or `session_ids` (in addition to existing `search`). Available in both developer and product API views.
- **`fields=card` on list endpoints** — Pass `fields=card` on `GET /v1/characters`, `GET /v1/moments`, and `GET /v1/journals` for lightweight list items suited to pickers and feeds.
- **Updated examples**: Added `beats.py`, `entities.py`, and `moments.py`; extended `journals.py`, `pagination.py`, `basics.sh`, and `types.ts`.

### Changed

- **`GET /v1/journals`** — List responses now use the standard paginated envelope `{ data, total, page, size, pages }` with explicit `page` and `size` query parameters (defaults: page 1, size 20).

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
