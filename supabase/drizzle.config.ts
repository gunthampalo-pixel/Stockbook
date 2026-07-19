import { defineConfig } from "drizzle-kit";

export default defineConfig({
  out: "./supabase/drizzle",
  schema: "./supabase/db/schema.ts",
  dialect: "sqlite",
});
