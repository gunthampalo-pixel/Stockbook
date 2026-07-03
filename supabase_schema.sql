-- Supabase Database Schema for Stock Research Dashboard
-- Copy and paste this script into the SQL Editor in your Supabase project (https://supabase.com)

-- 1. Create the 'stocks' table to store general stock profiles
CREATE TABLE IF NOT EXISTS public.stocks (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    logo_url TEXT,
    "group" TEXT,
    style TEXT,
    market TEXT DEFAULT 'US',
    target_price TEXT,
    what_it_does TEXT,
    how_it_makes_money TEXT,
    deals TEXT,
    moat TEXT,
    risks TEXT,
    financials JSONB DEFAULT '[]'::jsonb,
    image_url TEXT,
    why_interest TEXT,
    financials_snapshot TEXT,
    summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Create the 'portfolio_notes' table to store user-written notes for each stock
CREATE TABLE IF NOT EXISTS public.portfolio_notes (
    ticker TEXT PRIMARY KEY REFERENCES public.stocks(ticker) ON DELETE CASCADE,
    notes TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Enable Row Level Security (RLS) on both tables
ALTER TABLE public.stocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.portfolio_notes ENABLE ROW LEVEL SECURITY;

-- 4. Create Policies for Public Access (using Anon Key)
-- Since this dashboard is run locally (or hosted statically) and shared with iPad,
-- we allow full read/write access via the anon key for simplicity.

-- Policies for 'stocks'
CREATE POLICY "Allow public read for stocks" 
    ON public.stocks FOR SELECT USING (true);

CREATE POLICY "Allow public insert for stocks" 
    ON public.stocks FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public update for stocks" 
    ON public.stocks FOR UPDATE USING (true);

CREATE POLICY "Allow public delete for stocks" 
    ON public.stocks FOR DELETE USING (true);

-- Policies for 'portfolio_notes'
CREATE POLICY "Allow public read for portfolio_notes" 
    ON public.portfolio_notes FOR SELECT USING (true);

CREATE POLICY "Allow public insert for portfolio_notes" 
    ON public.portfolio_notes FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public update for portfolio_notes" 
    ON public.portfolio_notes FOR UPDATE USING (true);

CREATE POLICY "Allow public delete for portfolio_notes" 
    ON public.portfolio_notes FOR DELETE USING (true);

-- 5. Create a function and trigger to automatically update the 'updated_at' column
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_stocks_modtime
    BEFORE UPDATE ON public.stocks
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_portfolio_notes_modtime
    BEFORE UPDATE ON public.portfolio_notes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
