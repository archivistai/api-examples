/**
 * Archivist API Quickstart — list campaigns, characters, and sessions.
 *
 * Run: npx tsx quickstart.ts
 */

const BASE_URL = "https://api.myarchivist.ai";
const API_KEY = process.env.ARCHIVIST_API_KEY!;

if (!API_KEY) {
  console.error("Set ARCHIVIST_API_KEY environment variable");
  process.exit(1);
}

const headers = { "x-api-key": API_KEY };

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

interface Campaign {
  id: string;
  title: string;
  description?: string;
  system: string;
  summary?: string;
  language: string;
  image?: string;
  public: boolean;
  mature: boolean;
  owner_id: string;
  created_at: string;
  updated_at?: string;
}

interface Character {
  id: string;
  campaign_id: string;
  character_name: string;
  character_alias?: string;
  character_aliases: string[];
  player_name?: string;
  description?: string;
  backstory?: string;
  type: string;
  image?: string;
  tcg_image?: string;
  merge: boolean;
  created_at: string;
  updated_at?: string;
}

interface GameSession {
  id: string;
  campaign_id: string;
  title: string;
  type: string;
  summary?: string;
  notes?: string;
  session_date: string;
  image?: string;
  index?: number;
  public: boolean;
  created_at: string;
  updated_at?: string;
}

async function listCampaigns(): Promise<Campaign[]> {
  const resp = await fetch(`${BASE_URL}/v1/campaigns?size=5`, { headers });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${await resp.text()}`);

  const data: PaginatedResponse<Campaign> = await resp.json();
  console.log(`Found ${data.total} campaign(s):\n`);
  for (const c of data.data) {
    console.log(`  [${c.id}] ${c.title} (system: ${c.system})`);
  }
  return data.data;
}

async function listCharacters(campaignId: string): Promise<void> {
  const params = new URLSearchParams({ campaign_id: campaignId, size: "10" });
  const resp = await fetch(`${BASE_URL}/v1/characters?${params}`, { headers });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${await resp.text()}`);

  const data: PaginatedResponse<Character> = await resp.json();
  console.log(`\nCharacters (${data.total} total):\n`);
  for (const char of data.data) {
    const aliases = char.character_aliases.length
      ? ` (aliases: ${char.character_aliases.join(", ")})`
      : "";
    console.log(`  [${char.type}] ${char.character_name}${aliases}`);
  }
}

async function listSessions(campaignId: string): Promise<void> {
  const params = new URLSearchParams({ campaign_id: campaignId, size: "5" });
  const resp = await fetch(`${BASE_URL}/v1/sessions?${params}`, { headers });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${await resp.text()}`);

  const data: PaginatedResponse<GameSession> = await resp.json();
  console.log(`\nSessions (${data.total} total):\n`);
  for (const s of data.data) {
    console.log(`  [${s.type}] ${s.title} — ${s.session_date}`);
  }
}

async function main() {
  const campaigns = await listCampaigns();
  if (campaigns.length > 0) {
    await listCharacters(campaigns[0].id);
    await listSessions(campaigns[0].id);
  }
}

main().catch(console.error);
