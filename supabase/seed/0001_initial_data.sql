-- Seed data for the application

-- Clear existing data (be careful in production!)
TRUNCATE TABLE artifacts, task_dependencies, tasks, agents RESTART IDENTITY CASCADE;

-- Reset sequences to ensure consistent IDs
ALTER SEQUENCE agents_id_seq RESTART WITH 1;
ALTER SEQUENCE tasks_id_seq RESTART WITH 1;

-- Insert system agent first to satisfy foreign key constraints
INSERT INTO agents (id, name, role, is_active, created_at, updated_at)
VALUES (0, 'System', 'System', true, NOW(), NOW())
ON CONFLICT (id) DO UPDATE 
SET name = EXCLUDED.name,
    role = EXCLUDED.role, 
    is_active = EXCLUDED.is_active,
    updated_at = EXCLUDED.updated_at;

-- Reset the sequence to avoid conflicts with explicit IDs
SELECT setval('agents_id_seq', (SELECT MAX(id) FROM agents), true);

-- Insert sample agents
WITH inserted_agents AS (
    INSERT INTO agents (name, role, is_active, created_at, updated_at)
    VALUES 
        ('Frontend Developer', 'frontend', true, NOW(), NOW()),
        ('Backend Developer', 'backend', true, NOW(), NOW()),
        ('DevOps Engineer', 'deployment', true, NOW(), NOW()),
        ('QA Engineer', 'testing', true, NOW(), NOW()),
        ('Product Manager', 'planning', true, NOW(), NOW())
    RETURNING id, name, role
)
SELECT * FROM inserted_agents;

-- Insert sample tasks
DO $$
DECLARE
    v_system_agent_id INTEGER := 0; -- We know this is 0 from earlier
    v_frontend_agent_id INTEGER;
    v_backend_agent_id INTEGER;
    v_devops_agent_id INTEGER;
    
    v_setup_task_id INTEGER;
    v_auth_task_id INTEGER;
    v_landing_task_id INTEGER;
    v_cicd_task_id INTEGER;
BEGIN
    -- Get agent IDs
    SELECT id INTO v_frontend_agent_id FROM agents WHERE name = 'Frontend Developer' LIMIT 1;
    SELECT id INTO v_backend_agent_id FROM agents WHERE name = 'Backend Developer' LIMIT 1;
    SELECT id INTO v_devops_agent_id FROM agents WHERE name = 'DevOps Engineer' LIMIT 1;
    
    -- Insert tasks one by one to get their IDs
    INSERT INTO tasks (
        title, 
        description, 
        status, 
        task_type, 
        created_by, 
        assigned_to,
        created_at, 
        updated_at
    ) VALUES (
        'Setup project structure', 
        'Initialize the project with basic structure', 
        'completed', 
        'code_generation', 
        v_system_agent_id, 
        v_frontend_agent_id,
        NOW() - INTERVAL '5 days',
        NOW() - INTERVAL '4 days'
    ) RETURNING id INTO v_setup_task_id;
    
    INSERT INTO tasks (
        title, 
        description, 
        status, 
        task_type, 
        created_by, 
        assigned_to,
        created_at, 
        updated_at
    ) VALUES (
        'Implement authentication', 
        'Create user authentication endpoints', 
        'in_progress', 
        'code_generation',
        v_system_agent_id,
        v_backend_agent_id,
        NOW() - INTERVAL '3 days',
        NOW() - INTERVAL '2 days'
    ) RETURNING id INTO v_auth_task_id;
    
    INSERT INTO tasks (
        title, 
        description, 
        status, 
        task_type, 
        created_by, 
        assigned_to,
        created_at, 
        updated_at
    ) VALUES (
        'Create landing page', 
        'Design and implement the main landing page', 
        'pending', 
        'code_generation',
        v_system_agent_id,
        v_frontend_agent_id,
        NOW() - INTERVAL '2 days',
        NOW() - INTERVAL '1 day'
    ) RETURNING id INTO v_landing_task_id;
    
    INSERT INTO tasks (
        title, 
        description, 
        status, 
        task_type, 
        created_by, 
        assigned_to,
        created_at, 
        updated_at
    ) VALUES (
        'Set up CI/CD pipeline', 
        'Configure GitHub Actions for automated testing and deployment', 
        'pending', 
        'deployment',
        v_system_agent_id,
        v_devops_agent_id,
        NOW() - INTERVAL '1 day',
        NOW()
    ) RETURNING id INTO v_cicd_task_id;
    
    -- Insert task dependencies
    INSERT INTO task_dependencies (task_id, depends_on_task_id, created_at)
    VALUES 
        (v_auth_task_id, v_setup_task_id, NOW()),
        (v_landing_task_id, v_setup_task_id, NOW()),
        (v_cicd_task_id, v_auth_task_id, NOW()),
        (v_cicd_task_id, v_landing_task_id, NOW());
        
    -- Insert artifacts
    INSERT INTO artifacts (task_id, name, type, path, created_at, metadata)
    VALUES 
        (v_setup_task_id, 'Project Structure', 'documentation', '/docs/project-structure.md', NOW() - INTERVAL '4 days', '{"format": "markdown"}'),
        (v_auth_task_id, 'Auth API Spec', 'api_spec', '/docs/auth-api.yaml', NOW() - INTERVAL '2 days', '{"format": "openapi"}');
        
    -- Output results
    RAISE NOTICE 'Successfully inserted % tasks and their dependencies', 4;
END $$;

-- Verify the data
SELECT '=== Database Seeding Complete ===' as message;

-- Show summary
WITH agent_count AS (SELECT COUNT(*) as count FROM agents WHERE id != 0),
     task_count AS (SELECT COUNT(*) as count FROM tasks),
     dep_count AS (SELECT COUNT(*) as count FROM task_dependencies),
     artifact_count AS (SELECT COUNT(*) as count FROM artifacts)
SELECT 'Agents:' as entity, count FROM agent_count
UNION ALL
SELECT 'Tasks:', count FROM task_count
UNION ALL
SELECT 'Dependencies:', count FROM dep_count
UNION ALL
SELECT 'Artifacts:', count FROM artifact_count;

-- Show sample data
\echo '\nSample Agents:'
SELECT id, name, role, is_active FROM agents ORDER BY id;

\echo '\nSample Tasks:'
SELECT id, title, status, task_type, created_by, assigned_to FROM tasks ORDER BY id;

\echo '\nTask Dependencies:'
SELECT td.task_id, t1.title as depends_on, td.depends_on_task_id, t2.title as required_by 
FROM task_dependencies td
JOIN tasks t1 ON td.depends_on_task_id = t1.id
JOIN tasks t2 ON td.task_id = t2.id
ORDER BY td.task_id, td.depends_on_task_id;

\echo '\nArtifacts:'
SELECT a.id, t.title as task, a.name, a.type, a.path 
FROM artifacts a
JOIN tasks t ON a.task_id = t.id
ORDER BY a.task_id, a.id;
