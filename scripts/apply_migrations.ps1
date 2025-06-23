# Apply database migrations to the local PostgreSQL instance

param (
    [string]$MigrationFile = "../supabase/migrations/0001_initial_schema.sql",
    [string]$DbUser = "testuser",
    [string]$DbPassword = "testpass",
    [string]$DbName = "testdb",
    [string]$DbHost = "localhost",
    [int]$DbPort = 5433
)

# Check if migration file exists
if (-not (Test-Path $MigrationFile)) {
    Write-Error "Migration file not found: $MigrationFile"
    exit 1
}

# Read the migration SQL
$migrationSql = Get-Content -Path $MigrationFile -Raw

# Create a temporary file for the SQL commands
$tempFile = [System.IO.Path]::GetTempFileName()
$tempFile = [System.IO.Path]::ChangeExtension($tempFile, "sql")

# Add connection settings and migration SQL to the temp file
@"
\c $DbName

-- Set client encoding
SET client_encoding = 'UTF8';

-- Begin transaction
BEGIN;

$migrationSql

-- Commit transaction
COMMIT;
"@ | Out-File -FilePath $tempFile -Encoding utf8

try {
    # Execute the migration using psql
    $env:PGPASSWORD = $DbPassword
    & psql -h $DbHost -p $DbPort -U $DbUser -d postgres -f $tempFile -v ON_ERROR_STOP=1
    
    if ($LASTEXITCODE -ne 0) {
        throw "Migration failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "Migration applied successfully!" -ForegroundColor Green
}
catch {
    Write-Error "Error applying migration: $_"
    exit 1
}
finally {
    # Clean up
    if (Test-Path $tempFile) {
        Remove-Item $tempFile -Force
    }
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}
