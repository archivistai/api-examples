/**
 * Archivist API Response Types
 *
 * Importable TypeScript definitions for all public API response shapes.
 * These match the API as of 2026-05-19.
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
}

// ---------------------------------------------------------------------------
// Ask (RAG)
// ---------------------------------------------------------------------------

export interface AskRequest {
  campaign_id: ID;
  messages: Array<{ role: "user" | "assistant"; content: string }>;
  stream?: boolean;
}

export interface AskResponse {
  answer: string;
  monthly_tokens_remaining?: number;
  hourly_tokens_remaining?: number;
}
