/**
 * Local testing script for Lambda function
 * Usage: node test-local.js
 */

const { handler } = require('./index');

// Test event for /optimize/text endpoint
const testEvent = {
  httpMethod: 'POST',
  path: '/optimize/text',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    resume_text: `Software Engineer with 5+ years of experience in full-stack development.
    
TECHNICAL SKILLS
- Languages: JavaScript, Python, Java
- Frameworks: React, Node.js, Express
- Databases: PostgreSQL, MongoDB
- Cloud: AWS, Docker

WORK EXPERIENCE
Software Engineer at Tech Corp (2020-Present)
- Developed scalable web applications
- Led team of 3 developers
- Improved system performance by 40%

PROJECTS
1. E-Commerce Platform
   - Built full-stack e-commerce solution
   - Technologies: React, Node.js, MongoDB
   - Increased sales by 25%

2. Task Management App
   - Created task tracking application
   - Technologies: React, Express, PostgreSQL
   - Used by 1000+ users`,
    job_description: `We are looking for a Senior Full-Stack Developer with experience in:
- React and Node.js
- Cloud platforms (AWS preferred)
- Database design and optimization
- Team leadership
- Microservices architecture
- Docker and containerization`
  })
};

// Test health endpoint
const healthEvent = {
  httpMethod: 'GET',
  path: '/health',
  headers: {},
  body: null
};

async function runTest() {
  console.log('🧪 Testing Lambda Function Locally\n');
  console.log('='.repeat(50));
  
  // Test 1: Health Check
  console.log('\n📋 Test 1: Health Check');
  console.log('-'.repeat(50));
  try {
    const healthResult = await handler(healthEvent, {});
    console.log('✅ Status Code:', healthResult.statusCode);
    console.log('📦 Response:', JSON.parse(healthResult.body));
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
  
  // Test 2: Optimize Endpoint
  console.log('\n📋 Test 2: Optimize Resume');
  console.log('-'.repeat(50));
  console.log('⏳ Calling Gemini API (this may take 10-30 seconds)...\n');
  
  const startTime = Date.now();
  try {
    const result = await handler(testEvent, {});
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    
    console.log('✅ Status Code:', result.statusCode);
    console.log('⏱️  Duration:', duration, 'seconds');
    
    if (result.statusCode === 200) {
      const response = JSON.parse(result.body);
      console.log('\n📄 Response Summary:');
      console.log('  - Summary:', response.summary?.substring(0, 100) + '...');
      console.log('  - Technical Skills:', response.technical_skills?.substring(0, 100) + '...');
      console.log('  - Work Experience:', response.work_experience_section?.new_line);
      console.log('  - Projects:', response.projects?.length || 0, 'projects');
      
      // Save full response
      const fs = require('fs');
      fs.writeFileSync('test-response.json', JSON.stringify(response, null, 2));
      console.log('\n💾 Full response saved to: test-response.json');
    } else {
      console.log('❌ Error Response:', result.body);
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error('Stack:', error.stack);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ Testing Complete!\n');
}

// Check for API key
if (!process.env.GEMINI_API_KEY) {
  console.error('❌ Error: GEMINI_API_KEY environment variable not set!');
  console.log('\n💡 Set it with:');
  console.log('   export GEMINI_API_KEY=your-api-key');
  console.log('   node test-local.js\n');
  process.exit(1);
}

// Run tests
runTest();

