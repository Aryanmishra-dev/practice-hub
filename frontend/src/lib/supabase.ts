// Legacy re-export for backward compatibility
// Use @/lib/supabase/client or @/lib/supabase/server for new code

import { createBrowserClient } from "@supabase/ssr";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

// For backward compatibility - creates browser client
export const supabase = createBrowserClient(supabaseUrl, supabaseAnonKey);

export type SupabaseClient = typeof supabase;

// Re-export the new client functions
export { createClient } from "./supabase/client";
