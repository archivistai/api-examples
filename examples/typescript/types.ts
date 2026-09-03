/**
 * Archivist API Response Types
 *
 * Importable TypeScript definitions for all public API response shapes.
 * These match the API as of 2026-09-02.
 */

export type ID = string;
export type ISODate = string;

// ---------------------------------------------------------------------------
// Pagination
// ---------------------------------------------------------------------------

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// ---------------------------------------------------------------------------
// Campaign
// ---------------------------------------------------------------------------

export interface Campaign {
  id: ID;
  title: string;
  description?: string;
  system: string;
  summary?: string;
  language: string;
  image?: string;
  public: boolean;
  mature: boolean;
  owner_id: ID;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface CampaignStats {
  campaign_id: ID;
  title: string;
  characters: number;
  sessions: number;
  moments: number;
  public: boolean;
  created_at: ISODate;
}

// ---------------------------------------------------------------------------
// Character
// ---------------------------------------------------------------------------

export interface CharacterPlayer {
  id: ID;
  name?: string;
  handle?: string;
  roles: string[];
  campaign_id: ID;
  created_at: ISODate;
}

export interface Character {
  id: ID;
  campaign_id: ID;
  character_name: string;
  character_alias?: string;
  character_aliases: string[];
  player_handle?: string;
  player_name?: string;
  player?: CharacterPlayer;
  description?: string;
  backstory?: string;
  type: string;
  image?: string;
  tcg_image?: string;
  merge: boolean;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface CharacterCard {
  id: ID;
  character_name: string;
  type: string;
  image?: string;
}

// ---------------------------------------------------------------------------
// Game Session
// ---------------------------------------------------------------------------

export type GameSessionType =
  | "audioUpload"
  | "playByPost"
  | "discordVoice"
  | "txtUpload"
  | "rawNotes"
  | "other";

export interface GameSession {
  id: ID;
  campaign_id: ID;
  title: string;
  type: GameSessionType;
  summary?: string;
  /**
   * User-supplied session notes. This is `null` for all session types except
   * `rawNotes`. Raw-notes sessions contain notes but have no transcript content.
   */
  notes?: string;
  session_date: ISODate;
  image?: string;
  index?: number;
  public: boolean;
  pbp_start_msg_url?: string;
  pbp_end_msg_url?: string;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface GameSessionDetail extends GameSession {
  beats?: Beat[];
  moments?: Moment[];
}

// ---------------------------------------------------------------------------
// Beat
// ---------------------------------------------------------------------------

export type BeatType = "major" | "minor" | "step";

export interface Beat {
  id: ID;
  campaign_id: ID;
  label: string;
  description?: string;
  type: BeatType;
  index: number;
  parent_id?: ID;
  metadata?: Record<string, unknown>;
  game_session_ids: ID[];
  game_session_id?: ID;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface BeatLinkedEntities {
  characters: ID[];
  factions: ID[];
  locations: ID[];
  items: ID[];
}

export interface BeatHierarchyRead extends Beat {
  children: BeatHierarchyRead[];
  linkedEntities: BeatLinkedEntities;
}

// ---------------------------------------------------------------------------
// Moment
// ---------------------------------------------------------------------------

export interface Moment {
  id: ID;
  campaign_id: ID;
  session_id: ID;
  label?: string;
  content?: string;
  image?: string;
  index?: number;
  categories?: string[];
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface MomentCard {
  id: ID;
  label?: string;
  image?: string;
  session_id: ID;
  created_at: ISODate;
  categories: string[];
}

// ---------------------------------------------------------------------------
// Compendium Entities
// ---------------------------------------------------------------------------

export interface Faction {
  id: ID;
  campaign_id: ID;
  name: string;
  aliases: string[];
  type?: string;
  description?: string;
  image?: string;
  tcg_image?: string;
  merge: boolean;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface Location {
  id: ID;
  campaign_id: ID;
  name: string;
  aliases: string[];
  type?: string;
  description?: string;
  image?: string;
  tcg_image?: string;
  parent_id?: ID;
  merge: boolean;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface Item {
  id: ID;
  campaign_id: ID;
  name: string;
  aliases: string[];
  type?: string;
  description?: string;
  image?: string;
  tcg_image?: string;
  merge: boolean;
  created_at: ISODate;
  updated_at?: ISODate;
}

// ---------------------------------------------------------------------------
// Quest
// ---------------------------------------------------------------------------

export type QuestCategory = "main" | "side" | "faction" | "personal" | "n/a";
export type QuestStatus = "planned" | "in-progress" | "blocked" | "failed" | "done" | "n/a";
export type ObjectiveStatus = "pending" | "in-progress" | "completed" | "failed" | "blocked";

export interface QuestObjective {
  id: ID;
  text: string;
  status: ObjectiveStatus;
  order: number;
}

export interface QuestProgressEntry {
  id: ID;
  text: string;
  order: number;
  session_id?: ID;
  session_number?: number;
  session_title?: string;
  session_date?: ISODate;
}

export interface QuestRelatedEntityRef {
  id: ID;
  entity_type: "character" | "faction" | "location" | "item";
  entity_id?: ID;
  entity_name_snapshot?: string;
  label?: string;
  order: number;
}

export interface QuestSessionRef {
  id: ID;
  number?: number;
  title?: string;
  session_date?: ISODate;
}

export interface Quest {
  id: ID;
  campaign_id: ID;
  order_index: number;
  quest_name: string;
  quest_giver?: string;
  quest_giver_id?: ID;
  quest_category: QuestCategory;
  status: QuestStatus;
  success_definition?: string;
  failure_conditions?: string;
  next_action?: string;
  resolution?: string;
  objective_count: number;
  completed_objective_count: number;
  progress_entry_count: number;
  objectives: QuestObjective[];
  progress_log: string[];
  progress_log_entries: QuestProgressEntry[];
  related_characters: string[];
  related_factions: string[];
  related_locations: string[];
  related_items: string[];
  related_entity_refs: QuestRelatedEntityRef[];
  first_session?: QuestSessionRef;
  last_session?: QuestSessionRef;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface QuestSummary {
  id: ID;
  campaign_id: ID;
  order_index: number;
  quest_name: string;
  quest_giver?: string;
  quest_giver_id?: ID;
  quest_category: QuestCategory;
  status: QuestStatus;
  next_action?: string;
  resolution?: string;
  objective_count: number;
  completed_objective_count: number;
  progress_entry_count: number;
  related_entity_count: number;
  first_session?: QuestSessionRef;
  last_session?: QuestSessionRef;
  created_at: ISODate;
  updated_at?: ISODate;
}

// ---------------------------------------------------------------------------
// Journal
// ---------------------------------------------------------------------------

export type JournalStatus = "draft" | "published" | "archived";

export interface JournalEntry {
  id: ID;
  campaign_id: ID;
  title: string;
  summary?: string;
  content?: string;
  content_rich?: Record<string, unknown>;
  content_metadata?: Record<string, unknown>;
  tags: string[];
  token_count: number;
  cover_image?: string;
  is_pinned: boolean;
  is_public: boolean;
  status?: JournalStatus;
  published_at?: ISODate;
  archived_at?: ISODate;
  folder_id?: ID;
  author_id?: ID;
  last_edited_by_id?: ID;
  permission_level?: string;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface JournalCard {
  id: ID;
  title: string;
  summary?: string;
  updated_at?: ISODate;
  folder_id?: ID;
}

export interface JournalFolder {
  id: ID;
  campaign_id: ID;
  parent_id?: ID;
  name: string;
  path: string;
  description?: string;
  position: number;
  metadata?: Record<string, unknown>;
  created_at: ISODate;
  updated_at?: ISODate;
}

// ---------------------------------------------------------------------------
// Unified Entity Picker
// ---------------------------------------------------------------------------

export interface EntityCard {
  id: ID;
  name: string;
  type?: string;
  image?: string;
}

export interface EntitiesListResponse {
  results: EntityCard[];
  hasMore: boolean;
  page: number;
  pages: number;
  total: number;
}

// ---------------------------------------------------------------------------
// Link
// ---------------------------------------------------------------------------

export interface EntityLink {
  id: ID;
  campaign_id: ID;
  from_id: ID;
  from_type: string;
  to_id: ID;
  to_type: string;
  alias: string;
  created_at: ISODate;
}

// ---------------------------------------------------------------------------
// Session Sub-Resources
// ---------------------------------------------------------------------------

export interface CastAnalysis {
  id: ID;
  session_id: ID;
  analysis: Record<string, unknown>;
  /** Set when a rendered PDF has been persisted; null until then. */
  pdfPageCount?: number | null;
  pdfSavedAt?: ISODate | null;
  created_at: ISODate;
  updated_at?: ISODate;
}

export interface SessionHandout {
  summary: string;
  sessionOutline: string | Array<{ title: string }>;
  encounters: Array<{ title: string; bullets: string[] }>;
  characterSpotlight: Array<{ name: string; description: string; bullets: string[] }>;
  otherEntitySpotlight: Array<{ name: string; description: string }>;
  items: Array<{ name: string; description: string }>;
  valuableInformation: Array<{ info: string }>;
  partyStatusAndNextSteps: {
    partyStatus: { summary: string; bullets: string[] };
    nextSteps: { summary: string };
  };
  moments: Array<{ label: string; content: string }>;
  pdfPageCount?: number | null;
  pdfSavedAt?: ISODate | null;
}

export interface TranscriptUtterance {
  speaker_label: string;
  transcript: string;
  start: number;
  end: number;
  said_at?: string;
}

export interface TranscriptStats {
  char_count: number;
  tokens: number;
  utterance_count: number;
}

export interface TranscriptMetadata {
  session_id: ID;
  session_type?: string;
  campaign_id?: ID;
  world_title?: string;
  world_language?: string;
  session_date?: ISODate;
  speakers?: string[];
  speaker_count?: number;
  source_type?: string;
  created_at?: ISODate;
}

/**
 * JSON response shape for `GET /v1/sessions/{id}/transcript`.
 * Use `?format=markdown` to receive a plain-text markdown document instead
 * (returned with `Content-Type: text/markdown`).
 */
export interface Transcript {
  version: number;
  created_at: ISODate;
  metadata: TranscriptMetadata;
  utterances: TranscriptUtterance[];
  text: string;
  stats: TranscriptStats;
}

// ---------------------------------------------------------------------------
// Ask (RAG)
// ---------------------------------------------------------------------------

export interface AskRequest {
  campaign_id: ID;
  messages: Array<{ role: "user" | "assistant"; content: string }>;
  stream?: boolean;
}

export interface AskCitation {
  citation_id: string;
  source_type: string;
  source_id?: ID;
  title?: string;
  session_number?: number;
  excerpt?: string;
}

/** Ask quota and non-streaming Ask responses use camelCase keys. */
export interface AskQuota {
  monthlyTokensRemaining: number;
  hourlyTokensRemaining: number;
  launchPromoActive: boolean;
}

export interface AskResponse {
  answer: string;
  citations: AskCitation[];
  monthlyTokensRemaining: number;
  hourlyTokensRemaining: number;
}

export interface CampaignSearchHit {
  id: ID;
  image?: string | null;
}

export interface CampaignSearchResponse {
  characters: Array<CampaignSearchHit & { characterName: string; type?: string }>;
  factions: Array<CampaignSearchHit & { name: string; type?: string }>;
  locations: Array<CampaignSearchHit & { name: string; type?: string }>;
  items: Array<CampaignSearchHit & { name: string; type?: string }>;
  sessions: Array<CampaignSearchHit & { title: string; session_number?: number }>;
  recaps: Array<CampaignSearchHit & { title: string; session_number?: number; summary?: string }>;
  quests: Array<{ id: ID; questName: string; status?: string | null }>;
  journals: Array<CampaignSearchHit & { title: string }>;
}
