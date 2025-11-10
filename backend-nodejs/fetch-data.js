/**
 * Script to fetch data from the database
 * Usage:
 *   node fetch-data.js logs [limit]    - Fetch logs (default: 10)
 *   node fetch-data.js stats           - Fetch statistics
 *   node fetch-data.js prompt-edits     - Fetch prompt edits
 */

const { Pool } = require('pg');

// Database configuration from environment variables
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: parseInt(process.env.DB_PORT) || 5432,
  ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : false
});

async function fetchLogs(limit = 10) {
  try {
    console.log(`\n📊 Fetching last ${limit} optimization logs...\n`);
    
    const result = await pool.query(
      `SELECT 
        id,
        created_at,
        status_code,
        duration_ms,
        user_ip,
        CASE WHEN custom_prompt IS NOT NULL THEN 'Yes' ELSE 'No' END as has_custom_prompt,
        error_message
      FROM optimization_logs 
      ORDER BY created_at DESC 
      LIMIT $1`,
      [limit]
    );
    
    if (result.rows.length === 0) {
      console.log('No logs found.');
      return;
    }
    
    console.log(`Found ${result.rows.length} logs:\n`);
    result.rows.forEach((log, index) => {
      console.log(`${index + 1}. ID: ${log.id}`);
      console.log(`   Created: ${log.created_at}`);
      console.log(`   Status: ${log.status_code}`);
      console.log(`   Duration: ${log.duration_ms}ms`);
      console.log(`   IP: ${log.user_ip || 'N/A'}`);
      console.log(`   Custom Prompt: ${log.has_custom_prompt}`);
      if (log.error_message) {
        console.log(`   Error: ${log.error_message.substring(0, 100)}...`);
      }
      console.log('');
    });
  } catch (error) {
    console.error('❌ Error fetching logs:', error.message);
  }
}

async function fetchStats() {
  try {
    console.log('\n📈 Fetching statistics...\n');
    
    const stats = await pool.query(`
      SELECT 
        COUNT(*) as total_requests,
        SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful,
        SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) as failed,
        AVG(duration_ms)::INTEGER as avg_duration_ms,
        MIN(duration_ms) as min_duration_ms,
        MAX(duration_ms) as max_duration_ms,
        COUNT(DISTINCT user_ip) as unique_users,
        COUNT(CASE WHEN custom_prompt IS NOT NULL THEN 1 END) as requests_with_custom_prompt
      FROM optimization_logs
    `);
    
    const dailyStats = await pool.query(`
      SELECT 
        DATE(created_at) as date,
        COUNT(*) as requests,
        AVG(duration_ms)::INTEGER as avg_duration_ms
      FROM optimization_logs
      WHERE created_at >= NOW() - INTERVAL '7 days'
      GROUP BY DATE(created_at)
      ORDER BY date DESC
    `);
    
    console.log('Overall Statistics:');
    console.log('─────────────────');
    const s = stats.rows[0];
    console.log(`Total Requests:     ${s.total_requests}`);
    console.log(`Successful:         ${s.successful}`);
    console.log(`Failed:             ${s.failed}`);
    console.log(`Avg Duration:       ${s.avg_duration_ms}ms`);
    console.log(`Min Duration:       ${s.min_duration_ms}ms`);
    console.log(`Max Duration:       ${s.max_duration_ms}ms`);
    console.log(`Unique Users:       ${s.unique_users}`);
    console.log(`Custom Prompts:     ${s.requests_with_custom_prompt}`);
    
    if (dailyStats.rows.length > 0) {
      console.log('\nLast 7 Days:');
      console.log('────────────');
      dailyStats.rows.forEach(day => {
        console.log(`${day.date.toISOString().split('T')[0]}: ${day.requests} requests (avg: ${day.avg_duration_ms}ms)`);
      });
    }
    
    console.log('');
  } catch (error) {
    console.error('❌ Error fetching stats:', error.message);
  }
}

async function fetchPromptEdits(limit = 10) {
  try {
    console.log(`\n📝 Fetching last ${limit} prompt edits...\n`);
    
    const result = await pool.query(
      `SELECT 
        id,
        created_at,
        user_ip,
        LENGTH(original_prompt) as original_length,
        LENGTH(edited_prompt) as edited_length
      FROM prompt_edits 
      ORDER BY created_at DESC 
      LIMIT $1`,
      [limit]
    );
    
    if (result.rows.length === 0) {
      console.log('No prompt edits found.');
      return;
    }
    
    console.log(`Found ${result.rows.length} prompt edits:\n`);
    result.rows.forEach((edit, index) => {
      console.log(`${index + 1}. ID: ${edit.id}`);
      console.log(`   Created: ${edit.created_at}`);
      console.log(`   IP: ${edit.user_ip || 'N/A'}`);
      console.log(`   Original length: ${edit.original_length} chars`);
      console.log(`   Edited length: ${edit.edited_length} chars`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Error fetching prompt edits:', error.message);
  }
}

async function main() {
  const command = process.argv[2];
  const limit = parseInt(process.argv[3]) || 10;
  
  if (!process.env.DB_HOST) {
    console.error('❌ Database environment variables not set!');
    console.error('Set DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT');
    process.exit(1);
  }
  
  try {
    switch (command) {
      case 'stats':
        await fetchStats();
        break;
      case 'prompt-edits':
        await fetchPromptEdits(limit);
        break;
      case 'logs':
      default:
        await fetchLogs(limit);
        break;
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await pool.end();
  }
}

main();



