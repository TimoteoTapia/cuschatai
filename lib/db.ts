import { Pool } from 'pg';
import fs from 'fs';
import path from 'path';

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL
});

export async function getCompanyContext() {
    try {
        const result = await pool.query(
            'SELECT company_name, initial_context FROM company_settings LIMIT 1'
        );
        return result.rows[0];
    } catch (error) {
        console.error('Database connection error:', error);
        // Fallback to reading from the JSON file
        try {
            const initialContextPath = path.join(process.cwd(), 'initial-context.json');
            const data = fs.readFileSync(initialContextPath, 'utf8');
            return JSON.parse(data);
        } catch (fileError) {
            console.error('Error reading fallback file:', fileError);
            return {
              company_name: "Default Company",
              initial_context:
                "You are a customer service representative for Dunder Mifflin Paper Company...",
            };
        }
    }
}
