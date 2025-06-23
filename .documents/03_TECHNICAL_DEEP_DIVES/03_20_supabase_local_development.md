# Supabase Local Development Setup

## Overview
This document outlines the local development setup for Supabase, which is used as the primary database for the Sentient Core project. The setup uses Docker Compose to run all necessary Supabase services locally.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git (for cloning the repository)
- Basic understanding of Docker and containerization

## Getting Started

### 1. Copy Environment File

First, copy the example environment file and update it with your local configuration:

```bash
cp .env.example .env
```

Edit the `.env` file to set appropriate values for your local development environment.

### 2. Start Supabase Services

To start all Supabase services, run:

```bash
docker-compose up -d
```

This will start the following services:
- PostgreSQL database
- Supabase Studio (web interface)
- Kong API Gateway
- Authentication service
- REST API
- Realtime service
- Storage service
- Image proxy

### 3. Access Services

- **Supabase Studio**: http://localhost:3000
  - Database management interface
  - Table editor, SQL editor, and more

- **API Endpoints**:
  - REST: http://localhost:8000/rest/v1/
  - Auth: http://localhost:8000/auth/v1/
  - Storage: http://localhost:8000/storage/v1/
  - Realtime: http://localhost:8000/realtime/v1/

### 4. Initial Setup

1. Open Supabase Studio at http://localhost:3000
2. Log in with the default credentials:
   - Email: `admin@example.com`
   - Password: `password`
3. Change the default password when prompted
4. Create a new project and note the API keys
5. Update your `.env` file with the new API keys

## Development Workflow

### Running Database Migrations

Database migrations are managed through SQL files in the `supabase/migrations` directory. To apply migrations:

```bash
docker-compose exec db psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/migrations/your_migration.sql
```

### Seeding Test Data

To seed test data, place your seed scripts in the `supabase/seed` directory and run:

```bash
docker-compose exec db psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/seed/your_seed_script.sql
```

### Stopping Services

To stop all services:

```bash
docker-compose down
```

To stop and remove all data (warning: this will delete all data in the database):

```bash
docker-compose down -v
```

## Configuration

### Environment Variables

Key environment variables used in the setup:

- `POSTGRES_PASSWORD`: Database superuser password
- `SUPABASE_URL`: Base URL for Supabase API
- `SUPABASE_ANON_KEY`: Public anonymous key for client-side usage
- `SUPABASE_SERVICE_ROLE_KEY`: Private key for admin operations
- `JWT_SECRET`: Secret used for JWT token signing
- `STORAGE_BUCKET`: Default storage bucket name

### Ports

- **3000**: Supabase Studio
- **8000**: Kong API Gateway
- **5432**: PostgreSQL database
- **4000**: Realtime service
- **5000**: Storage service

## Troubleshooting

### Common Issues

1. **Port conflicts**: If you get port conflicts, check which service is using the port and either stop it or change the port in `docker-compose.yml`

2. **Database connection issues**:
   - Verify the database is running: `docker ps | grep db`
   - Check logs: `docker logs supabase_db`
   - Verify credentials in `.env` match those in `docker-compose.yml`

3. **Migration issues**:
   - Ensure SQL syntax is valid
   - Check for duplicate migration versions
   - Verify table and column names match your schema

### Viewing Logs

To view logs for all services:

```bash
docker-compose logs -f
```

For a specific service:

```bash
docker-compose logs -f service_name
```

## Security Considerations

1. **Never commit sensitive data**: The `.env` file is in `.gitignore` for a reason
2. **Use strong passwords**: Always use strong, unique passwords in production
3. **Limit access**: Only expose necessary ports to your local network
4. **Regular updates**: Keep Docker images updated to the latest stable versions

## Next Steps

1. Set up database schema and initial migrations
2. Configure authentication providers if needed
3. Set up storage buckets and access policies
4. Configure row-level security (RLS) for your tables
