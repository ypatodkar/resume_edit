/**
 * Database connection and logging utilities for Aurora/RDS (PostgreSQL)
 */
const { Pool } = require('pg');

// Database configuration from environment variables
const dbConfig = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: parseInt(process.env.DB_PORT) || 5432,
  ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : false,
  connectionTimeoutMillis: 30000, // 30 seconds
  idleTimeoutMillis: 30000, // Close idle connections after 30 seconds
  max: 2, // Reduce pool size for Lambda (fewer connections)
  allowExitOnIdle: true // Allow Lambda to exit when idle
};

let pool = null;

/**
 * Initialize database connection pool
 */
function initPool() {
  if (!pool) {
    pool = new Pool(dbConfig);
    
    // Handle pool errors
    pool.on('error', (err) => {
      console.error('❌ Unexpected database pool error:', err);
    });
  }
  return pool;
}

/**
 * Get database connection (creates pool if needed)
 */
function getPool() {
  if (!pool) {
    initPool();
  }
  return pool;
}

/**
 * Log a resume optimization request
 */
async function logRequest(data) {
  const {
    resume_text,
    job_description,
    custom_prompt,
    response_data,
    duration_ms,
    status_code,
    error_message,
    user_ip,
    user_agent
  } = data;

  const pool = getPool();
  
  try {
    console.log('📝 Executing database insert...');
    const query = `
      INSERT INTO optimization_logs (
        resume_text,
        job_description,
        custom_prompt,
        response_data,
        duration_ms,
        status_code,
        error_message,
        user_ip,
        user_agent,
        created_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW())
      RETURNING id
    `;

    const params = [
      resume_text || null,
      job_description || null,
      custom_prompt || null,
      response_data ? JSON.stringify(response_data) : null,
      duration_ms || null,
      status_code || null,
      error_message || null,
      user_ip || null,
      user_agent || null
    ];

    console.log('📝 Insert params:', {
      has_resume_text: !!resume_text,
      has_job_description: !!job_description,
      duration_ms,
      status_code,
      user_ip
    });

    // Execute query with explicit timeout (10 seconds)
    const queryPromise = pool.query(query, params);
    const timeoutPromise = new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Query timeout after 10 seconds')), 10000)
    );
    
    const result = await Promise.race([queryPromise, timeoutPromise]);
    
    const logId = result.rows[0]?.id;
    
    console.log(`✅ Database insert successful, ID: ${logId}`);
    return logId;
  } catch (error) {
    console.error('❌ Database logging error:', error.message);
    console.error('❌ Error details:', {
      code: error.code,
      detail: error.detail,
      hint: error.hint,
      position: error.position
    });
    // Don't throw - logging failure shouldn't break the API
    return null;
  }
}

/**
 * Log prompt edit (when user customizes prompt)
 */
async function logPromptEdit(data) {
  const {
    original_prompt,
    edited_prompt,
    user_ip,
    user_agent
  } = data;

  const pool = getPool();
  
  try {
    const query = `
      INSERT INTO prompt_edits (
        original_prompt,
        edited_prompt,
        user_ip,
        user_agent,
        created_at
      ) VALUES ($1, $2, $3, $4, NOW())
      RETURNING id
    `;

    const result = await pool.query(query, [
      original_prompt || null,
      edited_prompt || null,
      user_ip || null,
      user_agent || null
    ]);

    return result.rows[0]?.id;
  } catch (error) {
    console.error('❌ Database logging error:', error.message);
    return null;
  }
}

/**
 * Test database connection
 */
async function testConnection() {
  try {
    const pool = getPool();
    const result = await pool.query('SELECT 1 as test');
    return result.rows[0].test === 1;
  } catch (error) {
    console.error('❌ Database connection test failed:', error.message);
    return false;
  }
}

module.exports = {
  initPool,
  getPool,
  logRequest,
  logPromptEdit,
  testConnection
};

