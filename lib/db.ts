import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL
});

export async function getCompanyContext() {
  const result = await pool.query(
    'SELECT company_name, initial_context FROM company_settings LIMIT 1'
  );
  return result.rows[0];
}
