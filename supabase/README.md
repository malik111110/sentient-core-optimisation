# Supabase Local Development

This directory contains the configuration and scripts for running Supabase locally using Docker Compose.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Docker Compose)
- [PowerShell 7+](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell) (for Windows users)
- [Git](https://git-scm.com/) (for version control)

## Quick Start

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd sentient-core
   ```

2. **Start Supabase services**:
   ```powershell
   .\scripts\supabase.ps1 start
   ```
   This will:
   - Create necessary directories
   - Copy `.env.example` to `.env` if it doesn't exist
   - Start all Supabase services in detached mode

3. **Access Supabase Studio**:
   Open your browser and navigate to http://localhost:3000

4. **Stop services when done**:
   ```powershell
   .\scripts\supabase.ps1 stop
   ```

## Available Commands

Use the `supabase.ps1` script to manage the local development environment:

| Command | Description |
|---------|-------------|
| `start` | Start all Supabase services |
| `stop` | Stop all Supabase services |
| `reset` | Stop services, remove volumes, and start fresh (⚠️ deletes all data) |
| `status` | Show status of all services |
| `logs` | Show logs for all services |
| `migrate` | Run database migrations from `supabase/migrations/` |
| `seed` | Seed the database with test data from `supabase/seed/` |
| `help` | Show help message |

## Directory Structure

```
supabase/
├── migrations/    # Database migration SQL files
├── seed/          # Seed data SQL files
└── storage/       # Local storage for file uploads
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and update the values as needed:

```bash
# Database
DATABASE_URL=postgresql://postgres:your-super-secret@localhost:5432/postgres

# Supabase
SUPABASE_URL=http://localhost:8000
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# JWT
JWT_SECRET=your-super-secret-jwt-token
```

### Ports

| Service | Port | Description |
|---------|------|-------------|
| Supabase Studio | 3000 | Web UI for database management |
| Kong API Gateway | 8000 | API endpoints (REST, Auth, Storage, etc.) |
| PostgreSQL | 5432 | Database server |
| Realtime | 4000 | Real-time subscriptions |
| Storage | 5000 | File storage service |

## Database Migrations

1. Create a new migration file in `supabase/migrations/`:
   ```bash
   # Example: 20230623_initial_schema.sql
   ```

2. Apply migrations:
   ```powershell
   .\scripts\supabase.ps1 migrate
   ```

## Seeding Test Data

1. Add seed SQL files to `supabase/seed/`
2. Run the seed command:
   ```powershell
   .\scripts\supabase.ps1 seed
   ```

## Troubleshooting

### Common Issues

1. **Port conflicts**
   - Check which process is using the port: `netstat -ano | findstr :<port>`
   - Update the port in `docker-compose.yml` if needed

2. **Database connection issues**
   - Verify the database is running: `docker ps | findstr db`
   - Check logs: `docker logs supabase_db`

3. **Permission issues**
   - Ensure Docker has the necessary permissions to access the project directory
   - On Windows, add the project directory to Docker's shared drives in Settings

### Viewing Logs

View logs for all services:
```powershell
.\scripts\supabase.ps1 logs
```

View logs for a specific service:
```powershell
docker logs supabase_db  # For database logs
docker logs supabase_studio  # For Supabase Studio logs
```

## Security Considerations

1. **Never commit sensitive data**
   - The `.env` file is in `.gitignore` for a reason

2. **Use strong passwords** in production
   - Update the default credentials in both `.env` and `docker-compose.yml`

3. **Limit access**
   - Only expose necessary ports to your local network

## Next Steps

1. Set up database schema and initial migrations
2. Configure authentication providers if needed
3. Set up storage buckets and access policies
4. Configure row-level security (RLS) for your tables

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
