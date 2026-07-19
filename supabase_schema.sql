-- Supabase schema for the Stock Research Dashboard.
-- Run in the SQL editor for the target Supabase project.

create table if not exists public.stocks (
  ticker text primary key,
  name text not null,
  logo_url text,
  "group" text,
  style text,
  market text default 'US',
  target_price text,
  what_it_does text,
  how_it_makes_money text,
  deals text,
  moat text,
  risks text,
  financials jsonb default '[]'::jsonb,
  image_url text,
  why_interest text,
  financials_snapshot text,
  summary text,
  created_at timestamptz default timezone('utc'::text, now()) not null,
  updated_at timestamptz default timezone('utc'::text, now()) not null
);

create table if not exists public.portfolio_notes (
  ticker text primary key references public.stocks(ticker) on delete cascade,
  notes text,
  updated_at timestamptz default timezone('utc'::text, now()) not null
);

create table if not exists public.stock_research_knowledge_documents (
  path text primary key,
  title text not null,
  category text not null,
  content text not null,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default timezone('utc'::text, now()) not null,
  updated_at timestamptz default timezone('utc'::text, now()) not null
);

create or replace function public.update_modified_column()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  new.updated_at = timezone('utc'::text, now());
  return new;
end;
$$;

drop trigger if exists update_stocks_modtime on public.stocks;
create trigger update_stocks_modtime
before update on public.stocks
for each row execute function public.update_modified_column();

drop trigger if exists update_portfolio_notes_modtime on public.portfolio_notes;
create trigger update_portfolio_notes_modtime
before update on public.portfolio_notes
for each row execute function public.update_modified_column();

drop trigger if exists update_stock_research_knowledge_documents_modtime on public.stock_research_knowledge_documents;
create trigger update_stock_research_knowledge_documents_modtime
before update on public.stock_research_knowledge_documents
for each row execute function public.update_modified_column();

alter table public.stocks enable row level security;
alter table public.portfolio_notes enable row level security;
alter table public.stock_research_knowledge_documents enable row level security;

drop policy if exists "stock research public read stocks" on public.stocks;
drop policy if exists "stock research public insert stocks" on public.stocks;
drop policy if exists "stock research public update stocks" on public.stocks;
drop policy if exists "stock research public delete stocks" on public.stocks;

create policy "stock research public read stocks"
on public.stocks for select to anon, authenticated using (true);

create policy "stock research public insert stocks"
on public.stocks for insert to anon, authenticated with check (true);

create policy "stock research public update stocks"
on public.stocks for update to anon, authenticated using (true) with check (true);

create policy "stock research public delete stocks"
on public.stocks for delete to anon, authenticated using (true);

drop policy if exists "stock research public read portfolio notes" on public.portfolio_notes;
drop policy if exists "stock research public insert portfolio notes" on public.portfolio_notes;
drop policy if exists "stock research public update portfolio notes" on public.portfolio_notes;
drop policy if exists "stock research public delete portfolio notes" on public.portfolio_notes;

create policy "stock research public read portfolio notes"
on public.portfolio_notes for select to anon, authenticated using (true);

create policy "stock research public insert portfolio notes"
on public.portfolio_notes for insert to anon, authenticated with check (true);

create policy "stock research public update portfolio notes"
on public.portfolio_notes for update to anon, authenticated using (true) with check (true);

create policy "stock research public delete portfolio notes"
on public.portfolio_notes for delete to anon, authenticated using (true);

drop policy if exists "stock research public read knowledge docs" on public.stock_research_knowledge_documents;
drop policy if exists "stock research public insert knowledge docs" on public.stock_research_knowledge_documents;
drop policy if exists "stock research public update knowledge docs" on public.stock_research_knowledge_documents;
drop policy if exists "stock research public delete knowledge docs" on public.stock_research_knowledge_documents;

create policy "stock research public read knowledge docs"
on public.stock_research_knowledge_documents for select to anon, authenticated using (true);

create policy "stock research public insert knowledge docs"
on public.stock_research_knowledge_documents for insert to anon, authenticated with check (true);

create policy "stock research public update knowledge docs"
on public.stock_research_knowledge_documents for update to anon, authenticated using (true) with check (true);

create policy "stock research public delete knowledge docs"
on public.stock_research_knowledge_documents for delete to anon, authenticated using (true);

grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on public.stocks to anon, authenticated;
grant select, insert, update, delete on public.portfolio_notes to anon, authenticated;
grant select, insert, update, delete on public.stock_research_knowledge_documents to anon, authenticated;
