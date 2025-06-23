<#
.SYNOPSIS
    Manage Supabase local development environment

.DESCRIPTION
    This script provides commands to manage the local Supabase development environment,
    including starting, stopping, and resetting services, as well as running migrations.

.PARAMETER Command
    The command to execute. Supported commands:
    - start: Start all Supabase services
    - stop: Stop all Supabase services
    - reset: Stop services, remove volumes, and start fresh
    - status: Show status of all services
    - logs: Show logs for all services
    - migrate: Run database migrations
    - seed: Seed the database with test data
    - help: Show this help message

.EXAMPLE
    .\supabase.ps1 start
    .\supabase.ps1 stop
    .\supabase.ps1 reset
    .\supabase.ps1 status
    .\supabase.ps1 logs
    .\supabase.ps1 migrate
    .\supabase.ps1 seed
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet('start', 'stop', 'reset', 'status', 'logs', 'migrate', 'seed', 'help')]
    [string]$Command = 'help'
)

$ErrorActionPreference = 'Stop'
$script:ProjectRoot = Split-Path -Parent $PSScriptRoot
$script:EnvFile = Join-Path $ProjectRoot ".env"

# Load environment variables
if (Test-Path $script:EnvFile) {
    Get-Content $script:EnvFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            # Remove surrounding quotes if present
            if ($value.StartsWith('"') -and $value.EndsWith('"')) {
                $value = $value.Substring(1, $value.Length - 2)
            }
            [Environment]::SetEnvironmentVariable($name, $value, 'Process')
        }
    }
}

function Show-Header {
    Write-Host "=== Supabase Local Development Manager ===" -ForegroundColor Cyan
    Write-Host "Project Root: $ProjectRoot"
    Write-Host ""
}

function Invoke-DockerCompose {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )
    
    $process = Start-Process -FilePath "docker-compose" -ArgumentList $Arguments -NoNewWindow -PassThru -WorkingDirectory $ProjectRoot
    $process.WaitForExit()
    return $process.ExitCode
}

function Start-Supabase {
    Write-Host "Starting Supabase services..." -ForegroundColor Green
    
    # Ensure Docker is running
    try {
        $null = docker info
    } catch {
        Write-Error "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    }
    
    # Create required directories
    $directories = @(
        "$ProjectRoot/supabase/migrations",
        "$ProjectRoot/supabase/seed",
        "$ProjectRoot/supabase/storage"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "Created directory: $dir" -ForegroundColor Yellow
        }
    }
    
    # Copy .env.example to .env if it doesn't exist
    $envExample = Join-Path $ProjectRoot ".env.example"
    if (-not (Test-Path $script:EnvFile) -and (Test-Path $envExample)) {
        Copy-Item $envExample $script:EnvFile
        Write-Host "Created .env file from .env.example" -ForegroundColor Yellow
    }
    
    # Start services
    $exitCode = Invoke-DockerCompose -Arguments @("up", "-d")
    
    if ($exitCode -eq 0) {
        Write-Host "`nSupabase services started successfully!" -ForegroundColor Green
        Write-Host "- Supabase Studio: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "- REST API: http://localhost:8000/rest/v1/" -ForegroundColor Cyan
        Write-Host "- Database: postgresql://postgres:your-super-secret@localhost:5432/postgres" -ForegroundColor Cyan
        Write-Host "`nRun '.\supabase.ps1 logs' to view logs" -ForegroundColor Yellow
    } else {
        Write-Error "Failed to start Supabase services. Exit code: $exitCode"
    }
}

function Stop-Supabase {
    Write-Host "Stopping Supabase services..." -ForegroundColor Yellow
    $exitCode = Invoke-DockerCompose -Arguments @("down")
    
    if ($exitCode -eq 0) {
        Write-Host "Supabase services stopped." -ForegroundColor Green
    } else {
        Write-Error "Failed to stop Supabase services. Exit code: $exitCode"
    }
}

function Reset-Supabase {
    Write-Host "Resetting Supabase services..." -ForegroundColor Yellow
    Write-Warning "This will remove all data in the database and storage!"
    
    $confirmation = Read-Host "Are you sure you want to continue? (y/N)"
    if ($confirmation -ne 'y') {
        Write-Host "Reset cancelled." -ForegroundColor Yellow
        return
    }
    
    $exitCode = Invoke-DockerCompose -Arguments @("down", "-v", "--remove-orphans")
    
    if ($exitCode -eq 0) {
        Write-Host "Supabase services and data have been reset." -ForegroundColor Green
    } else {
        Write-Error "Failed to reset Supabase services. Exit code: $exitCode"
    }
}

function Show-Status {
    Write-Host "Checking service status..." -ForegroundColor Cyan
    Invoke-DockerCompose -Arguments @("ps") | Out-Null
}

function Show-Logs {
    Write-Host "Showing logs (press Ctrl+C to exit)..." -ForegroundColor Cyan
    Invoke-DockerCompose -Arguments @("logs", "-f")
}

function Invoke-Migrations {
    Write-Host "Running database migrations..." -ForegroundColor Cyan
    
    $migrationsDir = Join-Path $ProjectRoot "supabase\migrations"
    if (-not (Test-Path $migrationsDir)) {
        Write-Error "Migrations directory not found at: $migrationsDir"
        return
    }
    
    $migrationFiles = Get-ChildItem -Path $migrationsDir -Filter "*.sql" | Sort-Object Name
    if ($migrationFiles.Count -eq 0) {
        Write-Host "No migration files found in $migrationsDir" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Found $($migrationFiles.Count) migration file(s)" -ForegroundColor Cyan
    
    $env:PGPASSWORD = "your-super-secret"
    
    foreach ($file in $migrationFiles) {
        Write-Host "Applying migration: $($file.Name)" -ForegroundColor Cyan
        try {
            $command = "psql -h localhost -U postgres -d postgres -f `"$($file.FullName)`""
            $process = Start-Process -FilePath "docker" -ArgumentList @("exec", "-i", "supabase_db", "bash", "-c", $command) -NoNewWindow -PassThru -Wait
            if ($process.ExitCode -ne 0) {
                Write-Error "Failed to apply migration: $($file.Name)"
                return
            }
            Write-Host "Applied migration: $($file.Name)" -ForegroundColor Green
        } catch {
            Write-Error "Error applying migration $($file.Name): $_"
            return
        }
    }
    
    Write-Host "All migrations applied successfully!" -ForegroundColor Green
}

function Invoke-Seed {
    Write-Host "Seeding database with test data..." -ForegroundColor Cyan
    
    $seedDir = Join-Path $ProjectRoot "supabase\seed"
    if (-not (Test-Path $seedDir)) {
        Write-Error "Seed directory not found at: $seedDir"
        return
    }
    
    $seedFiles = Get-ChildItem -Path $seedDir -Filter "*.sql" | Sort-Object Name
    if ($seedFiles.Count -eq 0) {
        Write-Host "No seed files found in $seedDir" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Found $($seedFiles.Count) seed file(s)" -ForegroundColor Cyan
    
    $env:PGPASSWORD = "your-super-secret"
    
    foreach ($file in $seedFiles) {
        Write-Host "Applying seed: $($file.Name)" -ForegroundColor Cyan
        try {
            $command = "psql -h localhost -U postgres -d postgres -f `"$($file.FullName)`""
            $process = Start-Process -FilePath "docker" -ArgumentList @("exec", "-i", "supabase_db", "bash", "-c", $command) -NoNewWindow -PassThru -Wait
            if ($process.ExitCode -ne 0) {
                Write-Error "Failed to apply seed: $($file.Name)"
                return
            }
            Write-Host "Applied seed: $($file.Name)" -ForegroundColor Green
        } catch {
            Write-Error "Error applying seed $($file.Name): $_"
            return
        }
    }
    
    Write-Host "Database seeded successfully!" -ForegroundColor Green
}

function Show-Help {
    Write-Host @"
Supabase Local Development Manager

USAGE:
    .\supabase.ps1 [COMMAND]

COMMANDS:
    start     Start all Supabase services
    stop      Stop all Supabase services
    reset     Stop services, remove volumes, and start fresh
    status    Show status of all services
    logs      Show logs for all services
    migrate   Run database migrations
    seed      Seed the database with test data
    help      Show this help message

EXAMPLES:
    .\supabase.ps1 start
    .\supabase.ps1 stop
    .\supabase.ps1 reset
    .\supabase.ps1 status
    .\supabase.ps1 logs
    .\supabase.ps1 migrate
    .\supabase.ps1 seed
"@ -ForegroundColor Cyan
}

# Main script execution
Show-Header

switch ($Command) {
    'start' { Start-Supabase }
    'stop' { Stop-Supabase }
    'reset' { Reset-Supabase }
    'status' { Show-Status }
    'logs' { Show-Logs }
    'migrate' { Invoke-Migrations }
    'seed' { Invoke-Seed }
    'help' { Show-Help }
    default { Show-Help }
}
